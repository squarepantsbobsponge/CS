def stored_my(ans:list,clause_set:list):#把子句集里面的元组先表达出来
    for i in range(0,len(clause_set)):
        index_str=str(i+1)
        index_str+=" "
        index_str+=str(clause_set[i])#元组要转回str
        ans.append(index_str)
def stored_plus(ans:list,count:int,fromwhich:int,towhich:int,clause:tuple):#归结步骤放置
    index=str(count)+" "+"R["+str(fromwhich)+","+str(towhich)+"]"+": "+str(clause)
    ans.append(index)

def ResolutionProp(clause_set1:set):
  #子句集用set，子句用tuple元组
  #归结算法：首先子句中查找相同的原子和原子否定，然后归结合并重新放入，直到找到假，或者没有相互否定的
  #对一个元组中的元素遍历，元素变成否定的，看后面元组是否出现它的否定，出现归结
  #注意遍历的指针是动态的 
  #问题：归结推理不能只是简单的遍历，而是要考虑最大地靠近删除
  #对于原子公式Q，除了要找到~Q,在找到~Q前还要将Q提前考虑，加入计数器
  #问题：在子句集中选择两个子句归结，这两个子句的选取的优先性，以及一个子句生成多个副本和多个子句归结吗
  #子句集用set，子句用tuple元组
  #归结算法：首先子句中查找相同的原子和原子否定，然后归结合并重新放入，直到找到假，或者没有相互否定的
  #对一个元组中的元素遍历，元素变成否定的，看后面元组是否出现它的否定，出现归结
  #注意遍历的指针是动态的 
    i=0
    flag=0
    clause_set=[x for x in clause_set1] #set转为list且顺序不变
    ans=[]#存储步骤
    #先把子句集按序号存起来
    stored_my(ans,clause_set)
    count=len(clause_set)+1#步骤计数器
    while i<len(clause_set):
        clause=clause_set[i]#小心修改，
        if len(clause)>1:#选择单元子句
            i+=1
            continue
        flag=0
        for j in range(0,len(clause)):#单元优先策略，一开始肯定有单元子句，因为加入某个命题的否定，需要询问？？
            ato_formula=clause[j]#小心修改ato_formula只是引用
            if ato_formula[0]=='~':#获得单元子句的否定，方便下面匹配
                ne_ato_formula=ato_formula[1:]
            else:
              ne_ato_formula="~"+ato_formula #
              #挑选所有含有否定的子句归结
            for w in range(i+1,len(clause_set)):#遍历后面
                arr=clause_set[w]
                if ne_ato_formula in arr:#在就要和clause归结
                    index=arr.index(ne_ato_formula)
                    new_clause=clause[0:j]
                    new_clause+=clause[j+1:len(clause)]
                    new_clause+=arr[0:index]
                    new_clause+=arr[(index+1):len(arr)]
                    if len(new_clause)==0:
                        flag=2
                        stored_plus(ans,count,i,w,new_clause)
                        count+=1
                        break
                    else:
                        flag=1
                        stored_plus(ans,count,i,w,new_clause)
                        count+=1
                    clause_set.append(new_clause)
                    #clause_set.remove(arr),单元归结策略中不需要删除两个归结的句子  
                    
            if  flag==2 :
                break
            for w in range(0,i):#遍历前面
                arr=clause_set[w]
                if ne_ato_formula in arr:#在就要和clause归结
                    index=arr.index(ne_ato_formula)
                    new_clause=clause[0:j]
                    new_clause+=clause[j+1:len(clause)]
                    new_clause+=arr[0:index]
                    new_clause+=arr[(index+1):len(arr)]#为什么这里会归结错误
                    if len(new_clause)==0:
                        flag=2
                        stored_plus(ans,count,i,w,new_clause)
                        count+=1
                        break
                    else:
                        flag=1
                        stored_plus(ans,count,i,w,new_clause)
                        count+=1
                    clause_set.append(new_clause)
                    #clause_set.remove(arr),单元归结策略中不需要删除两个归结的句子  
                    
            if  flag==2 :
                break

        if flag==2:
            print('Yes')
            break
        else:
            i+=1
    return ans
Kb={("FirstGrade",),("~FirstGrade","Child"),("~Child",)}
print(ResolutionProp(Kb))
Kb={('P',),('~P','~Q','R'),('~S','Q'),('~T','Q'),('T',),('~R',)}
print(ResolutionProp(Kb))
Kb={('P',),('~P','Q',),('~Q','R')}
print(ResolutionProp(Kb))
        
        
                    


            
      