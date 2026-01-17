# animated sort - Jafar M. v2
## PEAK CODE
#####################################################

from tkinter import *
import random

bars = []
values = [] 
bar_width = 10
can_size = 600 
num_bars = 50
worker = None
is_verify = False



OPTIONS = [
    "Bubble Sort",
    "Insertion Sort",
    "Merge Sort",
    "Quick Sort"
]

#region GUI WINDOW SETUP

window = Tk() 

window.title("Animated Sort 🔥")

window.geometry("840x650")
window.config(background="#410ec4")

#endregion


# CANvVAS
canvas = Canvas(window, width=can_size, height=can_size, bg='#1a1a1a')  
canvas.pack(side=LEFT, padx=10, pady=10)

settings_frame = Frame(window, background="#8000FF") 
settings_frame.pack(side=RIGHT, padx= 10, pady=10)



#region HELPER FUNCTIONS

def colorBar(bar, color):
    canvas.itemconfig(bar, fill=color)


def swap(pos0, pos1):
    
    x0, _, x0b, _ = canvas.coords(pos0)
    x1, _, x1b, _ = canvas.coords(pos1)
    
    canvas.itemconfig(pos0, fill='red')
    canvas.itemconfig(pos1, fill='#00ff00')
    
    canvas.move(pos0, x1 - x0, 0)
    canvas.move(pos1, x0 - x1, 0)

#endregion


#region GENERATE BARS FUNCTION

def generate_bars():  
    global bars, values, worker, is_verify
    
    canvas.delete('all')
    bars = []
    values = []

    heights = [random.randint(10, can_size - 10) for _ in range(num_bars)]
    
    for i in range(num_bars):
        
        height = heights[i]
        
        bar = canvas.create_rectangle(
            i * bar_width,                     
            can_size - height,                 
            (i* bar_width) + bar_width,        
            can_size,                          
            fill = 'white',     
            outline= '#444444'
        )
        
        bars.append(bar)
        values.append(height)

    worker = None
    is_verify = False

#endregion


#region BUBBLE SORT

def bubble_sort():
    
    global bars, values
    n = len(values)
    
    for i in range(n-1):
        for j in range(n-i-1):
            
            if values[j] > values[j+1]:
                values[j], values[j+1] = values[j+1], values[j]
                bars[j], bars[j+1] = bars[j+1], bars[j]
                swap(bars[j], bars[j+1])
                yield
            
            else:
                colorBar(bars[j], 'white')

#endregion



#region INSERTION SORT

def insertion_sort():
    
    global bars, values
    
    for i in range(1, len(values)):
        key = values[i]
        key_bar = bars[i]
        j = i - 1
    
        while j >= 0 and values[j] > key:
            values[j+1] = values[j]
            bars[j+1], bars[j] = bars[j], bars[j+1]
            swap(bars[j+1], bars[j])
            
            yield
            j -= 1
    
        values[j+1] = key
        bars[j+1] = key_bar

#endregion


#region MERGE SORT

def merge_sort_helper(l, r):
    
    global bars, values
    
    if l < r:
        m = (l + r) // 2
        
        yield from merge_sort_helper(l, m)
        yield from merge_sort_helper(m+1, r)

        # MERGE STEP - rebuild the array section
        left_vals = values[l:m+1][:]
        right_vals = values[m+1:r+1][:]
        

        i = j = 0
        k = l

        while i < len(left_vals) and j < len(right_vals):
            
            if left_vals[i] <= right_vals[j]:
                values[k] = left_vals[i]
                i += 1


            else:
                values[k] = right_vals[j]
                j += 1
            
            k += 1


        while i < len(left_vals):
            values[k] = left_vals[i]
            i += 1
            k += 1


        while j < len(right_vals):

            values[k] = right_vals[j]
            j += 1
            k += 1

        
        # UPDATING THE VISUAL BARS to match the sorted values
        for idx in range(l, r+1):
            current_height = values[idx]
            
            # updating bar height
            canvas.coords(

                bars[idx],
                idx * bar_width,
                can_size - current_height,
                idx * bar_width + bar_width,
                can_size
            )
                        
        colorBar(bars[idx], 'cyan')
        yield


def merge_sort():
    global bars, values
    yield from merge_sort_helper(0, len(values)-1)

#endregion


#region QUICK SORT

def quick_sort_helper(low, high):
    
    
    global bars, values


    if low < high:
        pivot = values[high]
        i = low - 1
       
        for j in range(low, high):
        
            if values[j] <= pivot:
                
                i += 1
                values[i], values[j] = values[j], values[i]
                bars[i], bars[j] = bars[j], bars[i]
                swap(bars[i], bars[j])
                yield


            else:
                colorBar(bars[j], 'white')
        
        
        values[i+1], values[high] = values[high], values[i+1]
        bars[i+1], bars[high] = bars[high], bars[i+1]
        swap(bars[i+1], bars[high])
        
        yield
        

        yield from quick_sort_helper(low, i)
        yield from quick_sort_helper(i+2, high)


def quick_sort():
    
    global bars, values
    yield from quick_sort_helper(0, len(values)-1)

#endregion


#region VERIFICATION

def verify():
    global bars, values
    
    for i in range(len(values) - 1):
        if values[i] <= values[i + 1]:
            colorBar(bars[i], 'green')
            yield
    

    colorBar(bars[-1], 'green')

#endregion


#region ANIMATION 

def animate():
    
    global worker, is_verify
    
    if worker is not None:
    
        try:
            next(worker)
            #speed controller
            speed = 68 - speed_slider.get()  
            window.after(speed, animate)
        
        except StopIteration:
            if not is_verify:
                worker = verify()
                is_verify = True
                animate()
            else:
                is_verify = False
                worker = None


def start_sort():
    
    global worker
    algo = variable.get()
    
    if algo == "Bubble Sort":
        worker = bubble_sort()
    
    elif algo == "Insertion Sort":
        worker = insertion_sort()
    
    elif algo == "Mergr Sort":
        worker = merge_sort()
    
    elif algo == "Quick Sort":
        worker = quick_sort()
    
    animate()

#endregion


#region GUI CONTROLS

# GENERATE BUTTON 
generate_btn = Button(
    settings_frame, 
    text="GENERATE!", 
    command=generate_bars, 
    bg='red',
    font=('Arial', 10, 'bold'),
    width=20
)
generate_btn.pack(pady=10)


# Selection MENU

variable = StringVar(window)
variable.set(OPTIONS[0])
dropdown = OptionMenu(settings_frame, variable, *OPTIONS)
dropdown.config(width=18, bg='white')
dropdown.pack(pady=5)


# SPEED SLIDER 
speed_label = Label(settings_frame, text="SPEED", bg='#8000FF', fg='white', font=('Arial', 9, 'bold'))
speed_label.pack(pady=(10,0))

speed_slider = Scale(
    settings_frame, 
    from_=1, 
    to=67, #https://en.wikipedia.org/wiki/6-7_meme | i hope i won't fail :pray:
    orient=HORIZONTAL, 
    length=200,
    bg='#8000FF',
    fg='white',
    troughcolor='#410ec4'
)


speed_slider.set(1)
speed_slider.pack(pady=5)


# START BUTTON
start_btn = Button(
    settings_frame, 
    text="START SORT!", 
    command=start_sort, 
    bg='#00ff00',
    font=('Arial', 11, 'bold'),
    width=20
)
start_btn.pack(pady=10)


# EXIT BUTTON
exit_btn = Button(
    settings_frame, 
    text="EXIT", 
    command=window.quit, 
    bg='red',
    fg='white',
    font=('Arial', 10),
    width=20
)
exit_btn.pack(side=BOTTOM, pady=10)

#endregion


# GENERATE INITIAL BARS
generate_bars()

window.mainloop()