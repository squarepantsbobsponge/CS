import Resolution
import MGU
Kb = {("A(tony)",),("A(mike)",),("A(john)",),("L(tony,rain)",),("L(tony,snow)",),("~A(x)","S(x)","C(x)"),("~C(y)","~L(y,rain)"),("L(z,snow)","~S(z)"),("~L(tony,u)","~L(mike,u)"),("L(tony,v)","L(mike,v)"),("~A(w)","~C(w)","S(w)")}
#Kb = {("On(tony,mike)",),("On(mike,john)",),("Green(tony)",),("~Green(john)",),("~On(xx,yy)","~Green(xx)","Green(yy)")}
#Kb = {("GradStudent(sue)",),("~GradStudent(x)","Student(x)"),("~Student(x)","HardWorker(x)"),("~HardWorker(sue)",)}
ans=Resolution.ResolutionOL(Kb)
for i in range(0,len(ans)):
    print(ans[i])
