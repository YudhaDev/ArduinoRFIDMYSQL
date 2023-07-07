#Import the required Libraries
from tkinter import *
from tkinter import ttk

#Define a Function to enable the frame
def enable(children):
   for child in children:
      child.configure(state='enable')

#Create an instance of tkinter frame
win = Tk()

#Set the geometry of tkinter frame
win.geometry("750x250")

#Creates top frame
frame1 = LabelFrame(win, width= 400, height= 180, bd=5)
frame1.pack()

#Create an Entry widget in Frame2
entry1 = ttk.Entry(frame1, width= 40)
entry1.insert(INSERT,"Enter Your Name")
entry1.pack()
entry2= ttk.Entry(frame1, width= 40)
entry2.insert(INSERT, "Enter Your Email")
entry2.pack()

#Creates bottom frame
frame2 = LabelFrame(win, width= 150, height=100)
frame2.pack()

#Create a Button to enable frame
button1 = ttk.Button(frame2, text="Enable", command=lambda: enable(frame1.winfo_children()))
button1.pack()
for child in frame1.winfo_children():
   child.configure(state='disable')

win.mainloop()