import tkinter as tk
import tkinter.ttk as ttk
##创建开始窗口
start_window=tk.Tk()
start_window.configure(background="black")
start_window.title("开始")
lb0=tk.Label(start_window,text="愿你勇敢，愿你理智，愿你聪明，愿你自律，愿你平和，愿你活泼...\n 但是更愿你快乐，更愿你自由！",font=("Arial", 30, "bold"), background='black', foreground='yellow')
lb0.pack(side="top",expand=1,anchor="center")

button=tk.Button(start_window,text="开始",command=lambda:[start_window.destroy(),root.deiconify()],width=10, height=2, background='black', foreground='white')
button.pack(side="bottom",expand=1,anchor="center")
start_window.geometry("800x600")#窗口大小

root=tk.Tk() #初始化窗口
root.title("good good life")#主窗口名字
root.withdraw()  # 隐藏主窗口 知道点击开始按钮才显示
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
#打卡标签的设置静态
lb3=tk.Label(task,text="好好吃饭",font=("Arial", 12, "bold"),fg='red')#文本居中对齐#font设置句体
lb3.grid(row=0, column=0)
lb3.grid(rowspan=2)

lb4=tk.Label(task,text="好好喝水",font=("Arial", 12, "bold"),fg='red')#文本居中对齐#font设置句体
lb4.grid(row=2, column=0)
lb4.grid(rowspan=2)

lb5=tk.Label(task,text="好好睡觉",font=("Arial", 12, "bold"),fg='red')#文本居中对齐#font设置句体
lb5.grid(row=4, column=0)
lb5.grid(rowspan=2)

lb6=tk.Label(task,text="好好运动",font=("Arial", 12, "bold"),fg='red')#文本居中对齐#font设置句体
lb6.grid(row=6, column=0)
lb6.grid(rowspan=2)

lb7=tk.Label(task,text="好好学习",font=("Arial", 12, "bold"),fg='red')#文本居中对齐#font设置句体
lb7.grid(row=8, column=0)
lb7.grid(rowspan=2)

lb8=tk.Label(task,text="好好快乐",font=("Arial", 12, "bold"),fg='red')#文本居中对齐#font设置句体
lb8.grid(row=10, column=0)

#result变量

root.geometry("800x600")#窗口大小
# 将回调函数绑定到窗口关闭事件
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()#主循环根窗口

