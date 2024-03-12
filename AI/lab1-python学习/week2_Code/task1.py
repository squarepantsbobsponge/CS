class StuData():
    def __init__(self,filename):
        self.data=[]
        with open(filename) as file_object:
            for line in file_object.readlines():
                s1=line.split()
                s1[3]=int(s1[3])#将age改为int
                self.data.append(s1)#先将line以空格为界分开，然后塞到data中
    def AddData(self,name,stu_num,gender,age):
        s1=[]
        s1.append(name)
        s1.append(stu_num)
        s1.append(gender)
        s1.append(age)
        self.data.append(s1)
    def SortData(self,req):
        if req=='name':
           self.data.sort(key=lambda x:x[0])
        elif req=='stu_num':
            self.data.sort(key=lambda x:x[1])
        elif req=='gender':
            self.data.sort(key=lambda x:x[2])
        elif req=='age':
            self.data.sort(key=lambda x:x[3])   
    def ExportFile(self,filename):
        with open(filename,'a') as file_object:
            for line in range(0,len(self.data)):
                for word in range(0,len(self.data[line])):
                    file_object.write(str(self.data[line][word]))
                    file_object.write(" ")
                file_object.write("\n")

stu1=StuData("student_data.txt")
stu1.AddData(name="Bob", stu_num="003", gender="M", age=20)
stu1.SortData('age')
stu1.ExportFile('new.txt')
print(stu1.data)