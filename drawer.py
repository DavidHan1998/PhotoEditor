from tkinter import *
from tkinter import filedialog #if it is absent, filedialog will fail
import cv2
from PIL import Image, ImageTk
import numpy as np
def callback(e):
    """create rectangle and record the position of x_1 and y_1 which are right down of the rectangle"""
    global img
    global canvas
    global x_0, y_0, x_1, y_1
    global im
    img_ROI = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_ROI = Image.fromarray(img_ROI)
    img_ROI = ImageTk.PhotoImage(image = img_ROI) #必加，不然長方形會一直疊加
    im = canvas.create_image(0,0,image = img_ROI, anchor = NW) #anchor must be added. anchor=NW means north-west is the point of (0,0)
    x_1, y_1 = e.x, e.y
    canvas.create_rectangle(x_0,y_0,x_1,y_1) #左上右下
    canvas.place(x=0,y=0)
    window.mainloop()
def position(e):
    global x_0, y_0
    x_0 = e.x
    y_0 = e.y
def roi(e):
    global label
    global x_0, x_1, y_0, y_1
    global canvas
    global im
    global img
    img = img[y_0:y_1, x_0:x_1] #openCV and tkinter are reverse
    #cv2.imshow('test', img)
    img_roi = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_roi = Image.fromarray(img_roi)
    img_roi = ImageTk.PhotoImage(image = img_roi)
    canvas.delete("all")
    #label['image'] = img_roi
    canvas.create_image(0,0,image = img_roi, anchor=NW)
    window.mainloop()
def newfile():
    """"load new file and show picture"""
    global img
    global canvas
    file_path = filedialog.askopenfilename()
    img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8),-1) #chinese file path
    nr, nc = img.shape[:2]
    img_new = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #turn BGR into RGB
    img_new = Image.fromarray(img_new) #convert image to PIL form
    pic = ImageTk.PhotoImage(image = img_new)
    #label['image'] = pic
    #label.pack()
    canvas = Canvas(height = nr, width = nc)
    canvas.create_image(0,0,image=pic,anchor=NW)
    canvas.place(x=0,y=0)
    window.mainloop() #mainloop should show up here because the main part finish at F5 is pressed
def flip():
    """turn it upside down"""
    global img
    global canvas
    img = cv2.flip(img, 0) #because img should be use in other function, so I retain the name img
    img_flip = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_flip = Image.fromarray(img_flip)
    pic = ImageTk.PhotoImage(image = img_flip)
    #label['image'] = pic
    canvas.delete('all')
    canvas.create_image(0,0,image = pic, anchor = NW)
    canvas.place(0,0)
    window.mainloop()
def ROI():
    global img
    global x_0, y_0, x_1, y_1
    x_0, y_0, x_1, y_1 = 0,0,0,0
    window.bind("<Button-1>", position) #when press left key of mouse, record the first position
    window.bind('<B1-Motion>',callback) #long-press left key of mouse and
    window.bind("<ButtonRelease-1>", roi)
def rotate():
    def rot():
        global degree
        global img
        global canvas
        degree = e1.get()
        win.destroy()
        degree = int(degree)
        nr, nc = img.shape[:2]
        rotation_matrix = cv2.getRotationMatrix2D((nr//2, nc//2), degree, 1)
        img = cv2.warpAffine(img, rotation_matrix, (nc, nr))
        cv2.imshow('test', img_rotate)
        img_rotate = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_rotate = Image.fromarray(img_rotate)
        img_rotate = ImageTk.PhotoImage(image = img_rotate)
        #label['image'] = img_rotate
        canvas.delete('all')
        canvas.create_image(0,0,image = img_rotate, anchor = NW)
        window.mainloop()
    global img
    global canvas
    n1 = IntVar()
    win = Tk()
    win.geometry("300x300")
    e1 = Entry(win, textvariable = n1)
    lab = Label(win, text = "請輸入度數")
    lab.grid(row = 0, column = 0)
    e1.grid(row = 0, column = 1)
    btn1 = Button(win, text = "enter", command = rot)
    btn1.grid(row = 0, column = 2)
def rflip():
    global img
    global canvas
    img = cv2.flip(img, 1) #because img should be use in other function, so I retain the name img
    img_rflip = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_rflip = Image.fromarray(img_rflip)
    pic = ImageTk.PhotoImage(image = img_rflip)
    #label['image'] = pic
    canvas.delete('all')
    canvas.create_image(0,0,image = pic, anchor = NW)
    canvas.place(0,0)
    window.mainloop()
def scale():
    def sca():
        global s
        global img
        global canvas
        s = e1.get()
        win.destroy()
        nr, nc = img.shape[:2]
        s = float(s)
        nr2 = int(nr*s)
        nc2 = int(nc*s)
        img = cv2.resize(img, (nr2, nc2), interpolation = cv2.INTER_LINEAR)
        img_scale = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_scale = Image.fromarray(img_scale)
        img_scale = ImageTk.PhotoImage(image = img_scale)
        #label['image'] = img_rotate
        canvas.delete('all')
        canvas.create_image(0,0,image = img_scale, anchor = NW)
        window.mainloop()
    global img
    global canvas
    n1 = DoubleVar()
    win = Tk()
    win.geometry("300x300")
    e1 = Entry(win, textvariable = n1)
    lab = Label(win, text = "請輸入放大倍率")
    lab.grid(row = 0, column = 0)
    e1.grid(row = 0, column = 1)
    btn1 = Button(win, text = "enter", command = sca)
    btn1.grid(row = 0, column = 2)
"""
def ROI():
    global img
    canvas = Canvas(window, height = 600, width = 800)
    img_ROI = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_ROI = Image.fromarray(img_ROI)
    img_ROI = ImageTk.PhotoImage(image = img_ROI)
    canvas.create_image(0,0,image = img_ROI, anchor = NW)
    canvas.create_rectangle(30,30,180,120)
    canvas.place(x=0,y=0)
    window.mainloop()
"""
window = Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight() #讀取螢幕解析度
size = f'{screen_width}x{screen_height}'
window.geometry(size)
menu = Menu()
window.config(menu = menu)
filemenu = Menu(menu)
menu.add_cascade(label = "檔案", menu = filemenu)

filemenu.add_command(label = "開新檔案", command = newfile)
filemenu.add_separator()

helpmenu = Menu(menu)
menu.add_cascade(label = "功能", menu = helpmenu)
helpmenu.add_command(label = "上下翻轉", command = flip)
helpmenu.add_separator()
helpmenu.add_command(label = "切割", command = ROI)
helpmenu.add_separator()
helpmenu.add_command(label = "旋轉", command = rotate)
helpmenu.add_separator()
helpmenu.add_command(label = "左右翻轉", command = rflip)
helpmenu.add_separator()
helpmenu.add_command(label = "放大縮小", command = scale)
helpmenu.add_separator()
window.mainloop()