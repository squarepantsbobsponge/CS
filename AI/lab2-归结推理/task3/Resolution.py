import MGU
#步骤中先把子句集里面的子句表达出来
def stored_my(ans:list,clause_set:list):
    for i in range(0,len(clause_set)):
        index_str=str(i+1)
        index_str+=" "
        index_str+=str(clause_set[i])#元组要转回str
        ans.append(index_str)
#归结步骤放置
def stored_plus(ans:list,count:int,fromwhich:int,towhich:int,clause:tuple,ans_dict:dict):
    if len(ans_dict)!=0:
        index=str(count)+" "+"R["+str(fromwhich+1)+","+str(towhich+1)+"]"+str(ans_dict)+": "+str(clause)
    else:
        index=str(count)+" "+"R["+str(fromwhich+1)+","+str(towhich+1)+"]"+": "+str(clause)
    ans.append(index)
#完成归一，并且更改新的arr和clause（list(tuple)）
def cluase_MGU(clause:tuple,arr:tuple)->list:
    arr_dict={}                                                                # arr_dict:用于存储合一后的映射置换关系
    #由于MGU_real算法的实现传入的是原子公式：
    #clause是单子句（直接提取出原子公式），arr子句可能有多个原子公式（遍历提取）
    for i in range(0,len(clause)):
        flag=0
        for j in range(0,len(arr)):         
            tm_dict=MGU.MGU_real(clause[i],arr[j])                                        
            arr_dict.update(tm_dict)                    # arr_dict每循环一次update一次，因为一次单步归结和单步的最一般合一化都是针对子句，则映射置换应该普及共享到每个子句
            if(len(tm_dict)!=0):
                flag=1
                break
        if flag==1:
            break
    ans=[]                                                                     # ans：list，装载一次单步合一后的置换和置换后的子句
    clause_ans=list(clause)                                                    # 转换为list便于修改
    arr_ans=list(arr)
    #根据置换法则，修改子句
    for key, value in arr_dict.items():
        for i in range(0,len(clause_ans)):
           clause_ans[i]= clause_ans[i].replace(key,value)
    for key, value in arr_dict.items():
        for i in range(0,len(arr_ans)):
            arr_ans[i]=arr_ans[i].replace(key,value)           
    ans.append(tuple(clause_ans))
    ans.append(tuple(arr_ans))
    ans.append(arr_dict)
    return ans
#一阶逻辑归结
def ResolutionOL(clause_set1:set):
    i=0
    flag=0                                                                   # flag：标记到时候单子句和后面的子句匹配结果（1：有有匹配成功的 2：匹配成功并且获得空子句）
    clause_set=[x for x in clause_set1]                                      # clause_set:将传入子句集的格式改造成list，利于后面操作,存在问题？？不是每次转换的顺序都一样一一对应
    ans=[]                                                                   # ans：用于存储步骤的list
    #先把子句集按序号存起来
    stored_my(ans,clause_set)                                                  
    count=len(clause_set)+1                                                  # count:步骤计数器
    ans_dict={}                                                              # ans_dict:存储每一步的置换对应关系
    while i<len(clause_set):
        clause=clause_set[i]                                                 # clause：元组，小心修改，用于遍历子句集中的子句
    #单子句优先策略：选择单子句,一开始肯定有单元子句，因为加入某个命题的否定
        if len(clause)>1:
            i+=1
            continue
        flag=0
        for j in range(0,len(clause)):                                       # 遍历选定子句中的每个公式
            #这里其实由于上面选的单元子句，则只循环一次
            
            # 遍历clause子句后面的子句用于匹配
            for w in range(i+1,len(clause_set)):                             
                arr=clause_set[w]                                            # arr:选定用来和clause匹配的子句（元组）
            #调用最一般合一算法：单步合一
                change_list=cluase_MGU(clause,arr)                           
                clause=change_list[0]
                arr=change_list[1]
                ans_dict=change_list[2]
                ato_formula=clause[j]
            #获得单元子句的否定，方便下面匹配    
                if ato_formula[0]=='~':
                    ne_ato_formula=ato_formula[1:]
                else:
                    ne_ato_formula="~"+ato_formula
            #挑选所有含有否定的子句归结,单步归结
                if ne_ato_formula in arr:
                    index=arr.index(ne_ato_formula)
                    new_clause=clause[0:j]                                # new_clause：存储两个子句归结后的结果
                    new_clause+=clause[j+1:len(clause)]
                    new_clause+=arr[0:index]
                    new_clause+=arr[(index+1):len(arr)]
                    if len(new_clause)==0:                                # 归结出空子句
                        flag=2
                        stored_plus(ans,count,i,w,new_clause,ans_dict)
                        count+=1
                        break
                    else:
                        flag=1
                        stored_plus(ans,count,i,w,new_clause,ans_dict)
                        count+=1
                    clause_set.append(new_clause)
                    
                    
            if  flag==2 :
                break
            # 遍历clause子句前面的子句用于匹配
            for w in range(0,i):
                arr=clause_set[w]
            #调用最一般合一算法：单步合一    
                change_list=cluase_MGU(clause,arr)
                clause=change_list[0]
                arr=change_list[1]
                ans_dict=change_list[2]
                ato_formula=clause[j]
            #获得单元子句的否定，方便下面匹配     
                if ato_formula[0]=='~':
                    ne_ato_formula=ato_formula[1:]
                else:
                    ne_ato_formula="~"+ato_formula #
            #挑选所有含有否定的子句归结,单步归结
                if ne_ato_formula in arr:
                    index=arr.index(ne_ato_formula)
                    new_clause=clause[0:j]
                    new_clause+=clause[j+1:len(clause)]
                    new_clause+=arr[0:index]
                    new_clause+=arr[(index+1):len(arr)]
                    if len(new_clause)==0:
                        flag=2
                        stored_plus(ans,count,i,w,new_clause,ans_dict)
                        count+=1
                        break
                    else:
                        flag=1
                        stored_plus(ans,count,i,w,new_clause,ans_dict)
                        count+=1
                    clause_set.append(new_clause)
                     
                    
            if  flag==2 :
                break

        if flag==2:
            print('Yes')                                                  #能够归结出空子句：打印出yes            
            break
        else:
            i+=1
    return ans
#Kb= {("GradStudent(sue)",),("~GradStudent(x)","Student(x)"),("~Student(x)","HardWorker(x)"),("~HardWorker(sue)",)}

        
                    


            
      