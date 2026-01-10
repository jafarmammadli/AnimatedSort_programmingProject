# animated sort - Jafar M.
##  I tried to use as much as comments for readablity
#####################################################

from tkinter import *
import random

bars = []
values = [] #it's for height values
bar_width = 10
can_size = 600 #canvas size
num_bars = 50

#region GUI WINDOW


window = Tk() 

window.title("Animated Sort🔥")

icon = PhotoImage(file="adidas.png") # the adidas logo looks like animated sort, thats why i put it :)
window.iconphoto(True, icon)
window.geometry("840x420")
window.config(background="#410ec4")

#endregion


# CANvVAS
canvas = Canvas(window, width=can_size, height=can_size, bg='white')
canvas.pack(side=LEFT)

settings_frame = Frame(window, background="#000000")
settings_frame.pack(side=RIGHT, padx= 10, pady=10)



#region RANDOM BARS
def generate_bars():  # - it's for clearing the space and creating random bars
    global bars, values
    canvas.delete('all')

    heights = list(range(10, num_bars, bar_width))
    print(heights)
    random.shuffle(heights)

    
    for i in range(num_bars):
        height = heights[i]
        bar = canvas.create_rectangle(
            
            #to create the recctangles
            i * bar_width,                     #x1     
            can_size - height,                 #y1
            (i* bar_width) + bar_width,        #x2
            can_size,                          #y2
            fill = 'black',     
            outline= 'gray'
        )
        print(bar)
        bars.append(bar)
        values.append(height)


#endregion


##region GENERATIOPN BUTTON 
generate = Button(settings_frame, text="GENERATE!", command=generate_bars,)
generate.pack(pady=1, padx=1)













window.mainloop()