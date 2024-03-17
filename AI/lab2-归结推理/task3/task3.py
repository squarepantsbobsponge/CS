import Resolution
import MGU
Kb = {("A(tony)",),("A(mike)",),("A(john)",),("L(tony,rain)",),("L(tony,snow)",),("~A(x)","S(x)","C(x)"),("~C(y)","~L(y,rain)"),("L(z,snow)","~S(z)"),("~L(tony,u)","~L(mike,u)"),("L(tony,v)","L(mike,v)"),("~A(w)","~C(w)","S(w)")}
#Kb = {("On(tony,mike)",),("On(mike,john)",),("Green(tony)",),("~Green(john)",),("~On(xx,yy)","~Green(xx)","Green(yy)")}
print(Resolution.ResolutionOL(Kb))
