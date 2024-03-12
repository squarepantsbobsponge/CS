#传入的原子公式为str类型，相同谓词（不用比较谓词了，也可能含~）
#变量在['xx','yy','zz','uu','vv','ww']中选取
#结果存在dict中
#首先要把参数从公式里面取出来，存在list里，将str去掉括号和谓词符号和~符号，然后按照str类的切割存在list里
#建立起dict空字典
#循环找出两个list中不匹配的项，没有就直接ret dict
    #判断项为变量，常数，还是函数
    #能够替换的场景:一个变量，一个常数或者不含该变量的函数（判断该函数中是否含有该变量，把所有变量在函数中都找一次，含有就直接把dict清空break）
    #对于函数还要提取子项归结的
    #先找找dict中有没有变量的key，没有的就加进去
def judge(a:str)->int:
    temp=['xx','yy','zz','uu','vv','ww']
    if a in temp:
        return 0 #是变量
    elif "(" in a and ")" in a:
        return 1 #是函数
    else:
        return 2 #是常量
def change(list1:list,f1:str,key:str,map:str):
    for i in range(0,len(list1)):
        list1[i] = list1[i].replace(key, map)
    f1=f1.replace(key,map)
    return f1
def MGU(f1:str, f2:str):
    """
    :param f1: str
    :param f2: str
    :return: dict
    """
    #先把f1和f2中的参数，按顺序提取出来，定位闭合括号的位置切片片
    index1=f1.find("(")
    index2=f1.rfind(")")
    f1_tm=f1[index1+1:index2]
    name1=f1[0:index1]
    index1=f2.find("(")
    index2=f2.rfind(")")
    f2_tm=f2[index1+1:index2]
    name2=f2[0:index1]
    list1=f1_tm.split(",")
    list2=f2_tm.split(",")
    ans={}
    if len(list2)!=len(list1) or name1!=name2: ##为了函数参数的判断和函数名的判断
        return ans
    #开始找两个list中不匹配的项
    for i in range(0,len(list1)):
        #如果一样就继续匹配
        if list1[i]==list2[i]:
            continue
        #判断参数类型
        type_flag1=judge(list1[i])
        type_flag2=judge(list2[i])
          ##两个参数都是常数
        if type_flag1==2 and type_flag2==2:
            ans.clear()
            break
          ##一个常数一个函数
        if (type_flag1+type_flag2)==3:
            ans.clear()
            break
            ##一个变量和一个函数
        if (type_flag1+type_flag2)==1:
            key_my=list2[i]
            map_my=list1[i]
            if(type_flag1==0):
                key_my=list1[i]
                map_my=list2[i]
            if key_my in map_my:#变量在函数中无法归一
                ans.clear()
                break
            ans[key_my]=map_my
            f1=change(list1,f1,key_my,map_my)
            f2=change(list2,f2,key_my,map_my)
            continue
            ##两个变量
        if type_flag1==0 and type_flag2==0:
            key_my=list2[i]
            map_my=list1[i]
            ans[key_my]=map_my
            f1=change(list1,f1,key_my,map_my)
            f2=change(list2,f2,key_my,map_my)
            continue
            ##两个函数:相当于谓词归一,只能递归了##还有点问题，递归的时候list的更新
        if type_flag1==1 and type_flag2==1:
            ##首先判断函数名是否相同
            ans_help=MGU(list1[i],list2[i]) #这里进去的是MGU的是list1[i]和list2[i]，原本MGU的设计就是在list上改动，而不是在str本身上改动
            list1[i]=ans_help[1]
            list2[i]=ans_help[2]
            if len(ans_help)==0:#能进这里本身就是两个函数存在不一样的地方，进去了出来的dict还是空的，就是无法归一
                ans.clear()
                break
            else:
                ans.update(ans_help[0])#合并字典
                f1=change(list1,f1,key_my,map_my)#在这里同步str的变动，则MGU出来的时候str是改变的#string是不可变量//形参影响不了实参//转成递归调用：递归函数返回元组，把f1，f2也改了
                f2=change(list2,f2,key_my,map_my)
                continue
            ##一个变量一个常量
        if (type_flag1+type_flag2)==2:
            key_my=list2[i]
            map_my=list1[i]
            if(type_flag1==0):
                key_my=list1[i]
                map_my=list2[i]
            ans[key_my]=map_my
            f1=change(list1,f1,key_my,map_my)
            f2=change(list2,f2,key_my,map_my)
            continue
    #print(list1)
    #print(list2)
    result=(ans,f1,f2)#将改变后的str和dict一起返回
    return result
#print(MGU('P(xx,a)', 'P(b,yy)'))
def MGU_real(f1:str,f2:str):
    return (MGU(f1,f2))[0]
print(MGU_real('P(a,xx,f(g(yy)))', 'P(zz,f(zz),f(uu))'))