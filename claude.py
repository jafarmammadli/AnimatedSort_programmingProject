from tkinter import *
import random

# GLOBAL VARIABLES - these store our data
bars = []  # stores the rectangle objects on canvas
values = []  # stores the actual height values
bar_width = 10  # how wide each bar is
canvas_size = 600  # size of the drawing area

def generate_bars():
    """Creates random bars on the canvas"""
    global bars, values
    
    # Clear everything first
    canvas.delete('all')
    bars = []
    values = []
    
    # Create list of heights: [10, 20, 30, 40...] then shuffle it
    heights = list(range(10, canvas_size, bar_width))
    random.shuffle(heights)
    
    # How many bars we actually have
    num_bars = len(heights)
    
    # Draw each bar
    for i in range(num_bars):
        height = heights[i]
        
        # Create rectangle: (x1, y1, x2, y2)
        # x1 = starting x position (i * bar_width)
        # y1 = top of bar (canvas_size - height, because canvas starts at top-left)
        # x2 = ending x position (x1 + bar_width)
        # y2 = bottom (canvas_size)
        bar = canvas.create_rectangle(
            i * bar_width,                    # x1
            canvas_size - height,             # y1
            (i * bar_width) + bar_width,      # x2
            canvas_size,                      # y2
            fill='white',
            outline='black'
        )
        
        bars.append(bar)
        values.append(height)

# ===== GUI SETUP =====
window = Tk()
window.title("Animated Sort 🔥")
window.config(background="#410ec4")

# Canvas - the drawing area
canvas = Canvas(window, width=canvas_size, height=canvas_size, bg='gray')
canvas.pack(side=LEFT, padx=10, pady=10)

# Control panel frame (right side)
control_frame = Frame(window, bg="#3600be")
control_frame.pack(side=RIGHT, padx=10, pady=10)

# Generate button
btn_generate = Button(
    control_frame, 
    text="Generate New Bars",
    command=generate_bars,
    font=('Sans Serif', 12, 'bold'),
    bg='white',
    fg='purple',
    width=20
)
btn_generate.pack(pady=5)

# Generate initial bars when program starts
generate_bars()

window.mainloop()