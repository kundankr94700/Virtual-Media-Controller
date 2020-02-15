from tkinter import *
from PIL import ImageTk, Image
import numpy as np
import cv2
from pyautogui import *
import threading
import wmi
from tkinter.font import  Font
brightness=50
def image_filter(cropped_image):
    blur = cv2.GaussianBlur(cropped_image, (3, 3), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    mask2 = cv2.inRange(hsv, np.array([94, 80, 2]), np.array([126, 255, 255]))
    kernel = np.ones((5, 5))
    dilation = cv2.dilate(mask2, kernel, iterations=1)
    erosion = cv2.erode(dilation, kernel, iterations=1)
    filtered = cv2.GaussianBlur(erosion, (3, 3), 0)
    ret, thresh = cv2.threshold(filtered, 127, 255, 0)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours, hierarchy, thresh
def image_shape(contours, crop_image):
    contour = max(contours, key=lambda x: cv2.contourArea(x))
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(crop_image, (x, y), (x + w, y + h), (0, 0, 255), 0)

    hull = cv2.convexHull(contour)
    drawing = np.zeros(crop_image.shape, np.uint8)
    cv2.drawContours(drawing, [contour], -1, (0, 255, 0), 0)
    cv2.drawContours(drawing, [hull], -1, (0, 0, 255), 0)

    hull = cv2.convexHull(contour, returnPoints=False)

    defects = cv2.convexityDefects(contour, hull)

    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(contour[s][0])
        end = tuple(contour[e][0])

        cv2.line(crop_image, start, end, [0, 255, 0], 2)

    return x, y
def thread(x1, y1):

    global brightness

    c = wmi.WMI(namespace='wmi')
    m = c.WmiMonitorBrightnessMethods()[0]
    if x1 > 80 and x1 < 120 and y1 < 25:
        press('up')
        print("up")
        #  volume up
    elif x1 < 15 and y1 > 60 and y1 < 120:
        press('left')
        press("left")
        # left
    elif x1 > 140 and y1 > 60 and y1 < 120:
        press('right')
        print('right')
        # right
    elif x1 > 80 and x1 < 120 and y1 > 120:
        press('down')
        print("down")

    elif x1 <= 20 and y1 <= 30:
        if brightness < 100:
            brightness = brightness + 10
            m.WmiSetBrightness(brightness, 0)
            # left up
    elif x1 <=20 and y1 > 120:
        if brightness > 0:
            brightness = brightness - 10
            m.WmiSetBrightness(brightness, 0)
    elif x1 > 135 and y1 <= 10:
        press('space')
        press("Space")

        # right up


    else:
        pass
root_=Tk()
root_.geometry("1000x600+100+100")
f1 = Font(family="Time New Roman", size=12, weight="bold", underline=1)
f2 = Font(family="Time New Roman", size=12, weight="bold")
f3 = Font(family="Time New Roman", size=10, weight="bold")
img1 = ImageTk.PhotoImage(Image.open("Userlogin.jpg"))
panel = Label(root_, image=img1).place(x=400 ,y=1)
def abc():
    u = ss1.get()
    p = ss2.get()
    if u == 'Kundan' and p == 'Singh':
        root_.destroy()
        root = Tk()
        root.geometry("210x210+1200+830")
        app = Frame(root, bg="white")
        app.place(x=1, y=1)
        lmain = Label(app)
        lmain.grid()
        camera = cv2.VideoCapture(0)

        def video_stream():
            ret, image = camera.read()
            image = cv2.flip(image, 1)
            cv2.rectangle(image, (400, 120), (600, 300), (0, 255, 0), 1)
            img_frame_right = image[120:320, 420:620]

            contours_fing, hierarchy_fing, thresh_fing = image_filter(img_frame_right)

            try:

                p1, q1 = image_shape(contours_fing, img_frame_right)

                t = threading.Thread(name='child', target=thread, args=(p1, q1,))
                if not t.is_alive():
                    t.start()

            except:
                pass
            img = Image.fromarray(thresh_fing)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(1, video_stream)

        video_stream()

        root.attributes("-topmost", True)
        root.mainloop()


    elif u == '' and p == '':
        l4 = Label(root_, text="Please Enter the UserName and Passward         ", fg='brown', font=f3).place(x=1,
                                                                                                             y=470)
    else:
        l4 = Label(root_, text="Please Enter the Correct UserName and Passward", fg='brown', font=f3).place(x=1,
                                                                                                            y=470)


root_.title('Virtual Media Player')
l3 = Label(root_, text="Machine Learning ", fg='brown', font=f1).place(x=110, y=30)
l3 = Label(root_, text=" Virtual World Application: Virtual Media \n Control", fg='green', font=f1).place(x=1, y=80)
l3 = Label(root_, text="Enter Username and Password", fg='brown', font=f1).place(x=50, y=140)
l3 = Label(root_, text="Copyright @ Kundan Kumar ", fg='skyblue').place(x=750, y=550)
l1 = Label(root_, text='Username', fg='brown', font=f1).place(x=10, y=200)
l2 = Label(root_, text='Password', fg='brown', font=f1).place(x=10, y=260)
ss1 = StringVar()
ss2 = StringVar()
e1 = Entry(root_, textvariable=ss1,font=f2).place(x=135, y=200)
e2 = Entry(root_, textvariable=ss2, show='*',font=f2).place(x=135, y=260)
b=Button(root_,text='Login to Continue',command=abc,width=30,height=1,bg='green',font=f1,fg='white').place(x=10,y=330)
l4 = Label(root_, text="Message ", fg='brown', font=f1).place(x=150, y=390)
root_.mainloop()
