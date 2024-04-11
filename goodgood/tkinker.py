import tkinter as tk
import tkinter.ttk as ttk
import datetime
import tkinter.messagebox


from PIL import Image, ImageTk
def update_time(button):#复用
    now=datetime.datetime.now()
    formatted_time=now.strftime("%H:%H:%S") #格式化时间
    button.config(text=f"{button['text']} {formatted_time}")
def ins():
      if entry.get() != '':
          if todolist.curselection() == (): #返回索引有用于返回完成统计
              todolist.insert(todolist.size(),entry.get())
          else:
              todolist.insert(todolist.curselection(),entry.get())
def updt():
      if entry.get() != '' and todolist.curselection() != ():
           selected=todolist.curselection()[0]
           todolist.delete(selected)
           todolist.insert(selected,entry.get())
def delt():
      if todolist.curselection() != ():
           todolist.delete(todolist.curselection())
def finished():
    if(todolist.curselection()!=()):
        selected=todolist.curselection()[0]
        content=todolist.get(selected)
        content+=" ✔"
        todolist.delete(selected)
        todolist.insert(selected,content)        

    print(selected)

def start_countdown():  
    # 获取用户输入的倒计时时间（单位为秒）  
    countdown_time = int(time_entry.get())*60  
      
    # 定义倒计时函数  
    def countdown():  
        nonlocal countdown_time  
        if countdown_time > 0:  
            time_label.config(text=f"剩余时间：{countdown_time // 60}分{countdown_time % 60}秒") 
            countdown_time -= 1  
            root.after(1000, countdown)  # 每秒更新一次剩余时间  
        else:  
            tkinter.messagebox.showinfo("提醒", "摸鱼时间到，该study啦！")  
            sum_variable.set(sum_variable.get() + int(time_entry.get()))
    # 开始倒计时  
    countdown()
def start1_countdown():  
    # 获取用户输入的倒计时时间（单位为秒）  
    countdown1_time = int(study_time_entry.get())*60  
      
    # 定义倒计时函数  
    def countdown1():  
        nonlocal countdown1_time  
        if countdown1_time > 0:  
            time1_label.config(text=f"剩余时间：{countdown1_time // 60}分{countdown1_time % 60}秒") 
            countdown1_time -= 1  
            root.after(1000, countdown1)  # 每秒更新一次剩余时间  
        else:  
            tkinter.messagebox.showinfo("提醒", "专注结束，goodgood！")  
            sum1_variable.set(sum1_variable.get() + int(study_time_entry.get()))
    # 开始倒计时  
    countdown1()
root=tk.Tk() #初始化窗口
root.title("good good life")#主窗口名字
root.withdraw()  # 隐藏主窗口 知道点击开始按钮才显示
##创建开始窗口
start_window=tk.Toplevel()
start_window.configure(background="black")
start_window.title("开始")
lb0=tk.Label(start_window,text="愿你勇敢，愿你理智，愿你聪明\n愿你自律，愿你平和，愿你活泼...\n 但是更愿你快乐，更愿你自由！\n Good Good life\n from yiming",font=("Arial", 30, "bold"), background='black', foreground='yellow')
lb0.pack(side="top",expand=1,anchor="center")

button=tk.Button(start_window,text="开始",command=lambda:[start_window.destroy(),root.deiconify()],width=10, height=2, background='black', foreground='white')
button.pack(side="bottom",expand=1,anchor="center")
start_window.geometry("800x600")#窗口大小

# 注册一个回调函数，该函数将在窗口关闭时调用
def on_closing():
    root.destroy()

#划分窗口 
pw = ttk.PanedWindow(root,orient='vertical')
pw.pack(fill="both", expand=1)
top=ttk.LabelFrame(pw, text="top")
top.pack(side="top",fill="both",expand=1)
pw.add(top)
bottom=ttk.LabelFrame(pw, text="bottom")
bottom.pack(side="bottom",fill="both",expand=1)
pw.add(bottom)

pw2=ttk.PanedWindow(bottom,orient="horizontal")
pw2.pack(fill="both", expand=1)
task=ttk.LabelFrame(pw2, text="task")
task.pack(side="left",fill="both",expand=1)
pw2.add(task)
result=ttk.LabelFrame(pw2, text="result")
result.pack(side="right",fill="both",expand=1)
pw2.add(result)
#欢迎
lb1=tk.Label(top,text="welcome to good good life",font=("Arial", 20, "bold"))#文本居中对齐#font设置句体
# lb1.place(x=80,y=0,relwidth=0.8,relheight=0.05)
lb1.grid(row=0, column=0)
#lb1.grid(sticky="nsew")

#输入每日一句
lb2=tk.Label(top,text="每日一句",font=("Arial", 15, "bold"),fg='blue')#文本居中对齐#font设置句体
lb2.grid(row=1, column=0,sticky="W")
inpl=tk.Entry(top)
inpl.grid(row=1,column=1,sticky="W")#放在单元格左侧动态划分单元格，一次加一个
#打卡标签的设置静态和动态选项
lb3=tk.Label(task,text="好好吃饭",font=("Arial", 12, "bold"),fg='red')#文本居中对齐#font设置句体
lb3.grid(row=0, column=0)
lb3.grid(rowspan=2)
#     # 创建一个选项变量来存储选定的选项
# judge_var =tk.IntVar(root)
# #     # 创建单选项按钮
# # ja0 = tk.Radiobutton(task, text="三顿按时饭", variable=judge_var, value=0)
# # ja0.grid(row=0, column=1)
#创建个按钮
breabutton=tk.Button(root,text="早餐")
breabutton.config(bg="#ADD8E6")
breabutton.config(width=10,height=1,fg="white")
breabutton.config(command=lambda: update_time(breabutton))
breabutton.grid(row=0, column=1,in_=task)
lunchbutton=tk.Button(root,text="午餐")
lunchbutton.config(bg="#87CEEB")
lunchbutton.config(width=10,height=1,fg="white")
lunchbutton.config(command=lambda: update_time(lunchbutton))
lunchbutton.grid(row=0, column=2,in_=task)
subutton=tk.Button(root,text="晚餐")
subutton.config(bg="#6495ED")
subutton.config(width=10,height=1,fg="white")
subutton.config(command=lambda: update_time(subutton))
subutton.grid(row=0, column=3,in_=task)

lb4=tk.Label(task,text="好好喝水",font=("Arial", 12, "bold"),fg='red')#文本居中对齐#font设置句体
lb4.grid(row=2, column=0)
lb4.grid(rowspan=2)
    # 创建一个选项变量来存储选定的选项
judge_var =tk.IntVar(root)
#     # 创建单选项按钮
ja0 = tk.Radiobutton(task, text="0滴水", variable=judge_var, value=0,bg="#E6E6FA" )
ja0.grid(row=2, column=1,in_=task)
ja1 = tk.Radiobutton(task, text="饮料", variable=judge_var, value=1,bg="#FFC0CB" )
ja1.grid(row=2, column=2,in_=task)
ja2 = tk.Radiobutton(task, text="两瓶水", variable=judge_var, value=2,bg="#B482D9")
ja2.grid(row=2, column=3,in_=task)

lb5=tk.Label(task,text="好好睡觉",font=("Arial", 12, "bold"),fg='red')#文本居中对齐#font设置句体
lb5.grid(row=4, column=0)
lb5.grid(rowspan=2)
    #创建待办checkbutton
c_var=tk.IntVar(root)
b_var=tk.IntVar(root)
a_var=tk.IntVar(root)
c=tk.Checkbutton(root,text="午睡",variable=c_var,bg="#7CFC00")#var=1时被选
c.grid(row=4,column=1,in_=task)
b=tk.Checkbutton(root,text="早睡",variable=b_var,bg="#90EE90")#var=1时被选
b.grid(row=4,column=2,in_=task)
a=tk.Checkbutton(root,text="早起",variable=a_var,bg="#B2F2BB")#var=1时被选
a.grid(row=4,column=3,in_=task)

lb6=tk.Label(task,text="好好运动",font=("Arial", 12, "bold"),fg='red')#文本居中对齐#font设置句体
lb6.grid(row=6, column=0)
lb6.grid(rowspan=2)
    #运动选项
sport_var=tk.IntVar(root)
sport=tk.Checkbutton(root,text="运动",variable=sport_var)#var=1时被选
sport.grid(row=6,column=1,in_=task)
sportbutton=tk.Button(root,text="时间")
    #sportbutton.config(bg="#ADD8E6")
sportbutton.config(width=10,height=1,fg="black")
sportbutton.config(command=lambda: update_time(sportbutton))
sportbutton.grid(row=6, column=2,in_=task)

lb7=tk.Label(task,text="好好学习",font=("Arial", 12, "bold"),fg='red')#文本居中对齐#font设置句体
lb7.grid(row=8, column=0)
lb7.grid(rowspan=2)
    #滑块代表程度
study_var=tk.DoubleVar(root)
scale=tk.Scale(root,from_=0,to=5, orient=tk.HORIZONTAL,label="专注程度",resolution=0.1,tickinterval=1,variable=study_var,length=200)
scale.grid(row=8,column=1,in_=task,columnspan=2)

lb8=tk.Label(task,text="好好快乐",font=("Arial", 12, "bold"),fg='red')#文本居中对齐#font设置句体
lb8.grid(row=10, column=0)
#创建打勾选项
h1_var=tk.IntVar(root)
h2_var=tk.IntVar(root)
h3_var=tk.IntVar(root)
h1=tk.Checkbutton(root,text="不内耗",variable=h1_var,bg="#7CFC00")#var=1时被选
h1.grid(row=10,column=1,in_=task)
h2=tk.Checkbutton(root,text="自信鸭",variable=h2_var,bg="#90EE90")#var=1时被选
h2.grid(row=10,column=2,in_=task)
h3=tk.Checkbutton(root,text="别难过",variable=h3_var,bg="#B2F2BB")#var=1时被选
h3.grid(row=10,column=3,in_=task)
#插入列表项
count_row=11
count_col=0
frame1=tk.Frame(task) #设置列表框
frame1.grid(row=12,column=0,rowspan=6,columnspan=4,in_=task)
frame2=tk.Frame(task) #设置按钮框
frame2.grid(row=18,column=0,rowspan=5,columnspan=4)

# todolist=tk.Listbox(frame1)
# todolist.grid(rowspan=5, columnspan=4)
todolist = tk.Listbox(frame1, height=16, width=50)
todolist.pack(fill=tk.BOTH, expand=1)
entry = tk.Entry(frame2)
entry.grid(row=0, column=1,in_=frame2)
lb01=tk.Label(frame2,text="Todo",font=("Arial", 12, "bold"),fg='green')#文本居中对齐#font设置句体
lb01.grid(row=0, column=0,in_=frame2)
lb01.grid(rowspan=2)
btn1 = tk.Button(frame2,text='添加',command=ins,width=10,height=1)
btn1.grid(row=2,column=0)
btn2 = tk.Button(frame2,text='修改',command=updt,width=10,height=1)
btn2.grid(row=2,column=1)
btn3 = tk.Button(frame2,text='删除',command=delt,width=10,height=1)
btn3.grid(row=3,column=0)
btn4 = tk.Button(frame2,text='完成',command=finished,width=10,height=1)
btn4.grid(row=3,column=1)
##摸鱼倒计时
rest_label=tk.Label(result, text="摸鱼时刻：", font=("Arial", 14,"bold"))  
rest_label.grid(row=0,column=0)

rest_label2=tk.Label(result, text="摸鱼计时（min）：", font=("Arial", 9))  
rest_label2.grid(row=1,column=0,pady=10)

time_entry=tk.Entry(result,width=20)
time_entry.grid(row=1,column=2,pady=10)

sum_label2=tk.Label(result, text="今日总共摸鱼（min）：", font=("Arial", 9))  
sum_label2.grid(row=1,column=4,pady=10)

sum_variable = tk.IntVar()
sum_label3=tk.Label(result, textvariable=sum_variable, font=("Arial", 9))  
sum_label3.grid(row=1,column=5,pady=10)
sum_variable.set(0)

time_label = tk.Label(result, text="剩余时间：", font=("Arial", 12,"bold"),fg="blue")   #剩余时间
time_label.grid(row=2,column=1)
start_button = tk.Button(result, text="开始摸鱼", command=start_countdown)  
start_button.grid(row=1,column=3,columnspan=1)
##专注倒计时
study_label=tk.Label(result, text="学习时刻：", font=("Arial", 14,"bold"))  
study_label.grid(row=3,column=0)

study_label2=tk.Label(result, text="专注计时（min）：", font=("Arial", 9))  
study_label2.grid(row=4,column=0,pady=10)

study_time_entry=tk.Entry(result,width=20)
study_time_entry.grid(row=4,column=2,pady=10)

sum_label1=tk.Label(result, text="今日总共专注（min）：", font=("Arial", 9))  
sum_label1.grid(row=4,column=4,pady=10)

sum1_variable = tk.IntVar()
sum1_label3=tk.Label(result, textvariable=sum1_variable, font=("Arial", 9))  
sum1_label3.grid(row=4,column=5,pady=10)
sum1_variable.set(0)

time1_label = tk.Label(result, text="剩余时间：", font=("Arial", 12,"bold"),fg="red")   #剩余时间
time1_label.grid(row=5,column=1)
start1_button = tk.Button(result, text="开始专注", command=start1_countdown)  
start1_button.grid(row=4,column=3,columnspan=1)


#设置背景图
# image=Image.open("./image/background.png")
# photo=ImageTk.PhotoImage(image,name="back")

# label=tk.Label(root,image="back")
# label.place(x=0, y=0, relwidth=1, relheight=1)
# label.lower()
# canvas = tk.Canvas(root, width=800, height=600)
# canvas.pack()
# image=tk.PhotoImage(file="./image/background.png")
# canvas.create_image(0, 0, anchor=tk.NW, image=image)


#result变量
root.geometry("950x750")#窗口大小
# 将回调函数绑定到窗口关闭事件
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()#主循环根窗口

