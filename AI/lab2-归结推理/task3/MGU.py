#判断字符类型（变量，函数，常量）
def judge(a:str)->int:
    temp=['xx','yy','zz','uu','vv','ww']
    if a in temp:
        return 0                                                                       #是变量
    elif len(a)==1:                                                                    #一个字符的就是变量
        return 0                                                                       #是变量
    elif "(" in a and ")" in a:
        return 1 #是函数
    else:
        return 2 #是常量
#根据得到的置换规则，将list（原子公式list版）和f1（原子公式str版）里面置换合一
def change(list1:list,f1:str,key:str,map:str):
    for i in range(0,len(list1)):
        list1[i] = list1[i].replace(key, map)
    f1=f1.replace(key,map)
    return f1
#MGU_real的递归函数，可以对函数和谓词公式MGU
def MGU(f1:str, f2:str):
    """
    :param f1: str
    :param f2: str
    :return: dict
    """
    #先把f1和f2中的参数，按顺序提取出来：定位闭合括号的位置切片片
    index1=f1.find("(")
    index2=f1.rfind(")")                                                             # 注意这里要用rfind 从后往前的第一个闭合括号
    f1_tm=f1[index1+1:index2]                                                        # f1_tm:str,存储f1的参数
    name1=f1[0:index1]                                                               # name1：提取出f1的谓词或者是函数名称 
    index1=f2.find("(")
    index2=f2.rfind(")")
    f2_tm=f2[index1+1:index2]
    name2=f2[0:index1]
    list1=f1_tm.split(",")                                                           # list1:list(str),存储f1的参数
    list2=f2_tm.split(",")
    ans={}                                                                           # ans：dict 存储置换对应关系
    ##为了谓词/函数参数数量的判断和谓词/函数名的判断：不一样肯定不能合一，直接ret
    if len(list2)!=len(list1) or (name1!=name2 and name1!="~"+name2 and name2!="~"+name1 ): 
        return (ans,f1,f2)
    #开始找两个list中不匹配的项
    for i in range(0,len(list1)):
        #如果一样就继续匹配
        if list1[i]==list2[i]:
            continue
        #判断参数类型
        type_flag1=judge(list1[i])
        type_flag2=judge(list2[i])

          ##两个参数都是常数：不能合一
        if type_flag1==2 and type_flag2==2:
            ans.clear()
            break

          ##一个常数一个函数：不能合一
        if (type_flag1+type_flag2)==3:
            ans.clear()
            break

          ##一个变量和一个函数：
        if (type_flag1+type_flag2)==1:
            key_my=list2[i]                                                     
            map_my=list1[i]
             #变量才能是key
            if(type_flag1==0):
                key_my=list1[i]
                map_my=list2[i]
             #变量在函数中无法归一   
            if key_my in map_my:
                ans.clear()
                break
             #归一的时候：把置换规则添加进ans，还要更新list和f
            ans[key_my]=map_my
            f1=change(list1,f1,key_my,map_my)
            f2=change(list2,f2,key_my,map_my)
            continue

            ##两个变量：随便合一，不影响后面操作
        if type_flag1==0 and type_flag2==0:
            key_my=list2[i]
            map_my=list1[i]
            ans[key_my]=map_my
            f1=change(list1,f1,key_my,map_my)
            f2=change(list2,f2,key_my,map_my)
            continue

            ##两个函数:相当于谓词归一,只能递归了
        if type_flag1==1 and type_flag2==1:
            #递归
            ans_help=MGU(list1[i],list2[i]) 
            list1[i]=ans_help[1]
            list2[i]=ans_help[2]
            if len(ans_help)==0:                                                        #能到这一步本身就是两个函数存在不一样的地方，出来的dict还是空的，就是无法归一
                ans.clear()
                break
            else:
                #合一操作：合并字典，更新f，list                                          #为什么要同步f的变化：如果谓词中的参数没有函数，不调用递归是不需要同步f
                ans.update(ans_help[0])                                                 #                   但是调用递归了，返回的是f，list上的变化并不能直接返回
                f1=change(list1,f1,key_my,map_my)
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
    #将改变后的str和dict一起返回
    result=(ans,f1,f2)
    return result
#MGU调用入口
def MGU_real(f1:str,f2:str):
    return (MGU(f1,f2))[0]
