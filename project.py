# animated sort - Jafar M. v2
## PEAK CODE
#####################################################

from tkinter import *
import random


OPTIONS = [
    "Bubble Sort",
    "Insertion Sort",
    "Merge Sort",
    "Quick Sort"
]


class SortVisualizer:
    """Main class for the sorting visualizer application."""


    def __init__(self):
        #(previously global variables)
        """
        bars (list): list of canvas rectangle objects representing values
        values (list): list of integer heights corresponding to each bar
        bar_width (int): width of each bar in pixels
        can_size (int): canvas size (width and height)
        num_bars (int): number of bars to generate
        worker (generator): currently running sorting algorithm generator
        is_verify (bool): flag indicating if verification animation is running
        window (Tk): main tkinter window
        canvas (Canvas): canvas widget for drawing bars
        settings_frame (Frame): frame containing control buttons and settings
        
        """

        self.bars = []
        self.values = []
        self.bar_width = 10
        self.can_size = 600
        self.num_bars = 50
        self.worker = None
        self.is_verify = False
        
        # GUI setup
        self.window = Tk()
        self.window.title("Animated Sort 🔥")
        
        icon = PhotoImage(file="adidas.png")  # the adidas logo looks like animated sort, thats why i put it :)
        self.window.iconphoto(True, icon)
        
        self.window.geometry("840x650")
        self.window.config(background="#410ec4")
        
        # Canvas
        self.canvas = Canvas(self.window, width=self.can_size, height=self.can_size, bg='#1a1a1a')
        self.canvas.pack(side=LEFT, padx=10, pady=10)
        
        self.settings_frame = Frame(self.window, background="#8000FF")
        self.settings_frame.pack(side=RIGHT, padx=10, pady=10)
        
        # Create GUI controls
        self._create_controls()
        
        # Generate initial bars
        self.generate_bars()
    
    def _create_controls(self):
        """creates all GUI control elements (buttons, dropdown, speed slider, exit button)"""
        self.generate_btn = Button(
            self.settings_frame,
            text="GENERATE!",
            command=self.generate_bars,
            bg='red',
            font=('Arial', 10, 'bold'),
            width=20
        )
        self.generate_btn.pack(pady=10)
        
        # Selection MENU
        self.variable = StringVar(self.window)
        self.variable.set(OPTIONS[0])
        self.dropdown = OptionMenu(self.settings_frame, self.variable, *OPTIONS)
        self.dropdown.config(width=18, bg='white')
        self.dropdown.pack(pady=5)
        
        # SPEED SLIDER
        self.speed_label = Label(self.settings_frame, text="SPEED", bg='#8000FF', fg='white', font=('Arial', 9, 'bold'))
        self.speed_label.pack(pady=(10, 0))
        
        self.speed_slider = Scale(
            self.settings_frame,
            from_=1,
            to=67, #it was probably unnecessary :)
            orient=HORIZONTAL,
            length=200,
            bg='#8000FF',
            fg='white',
            troughcolor='#410ec4'
        )
        self.speed_slider.set(1)
        self.speed_slider.pack(pady=5)
        
        # START BUTTON
        self.start_btn = Button(
            self.settings_frame,
            text="START SORT!",
            command=self.start_sort,
            bg='#00ff00',
            font=('Arial', 11, 'bold'),
            width=20
        )
        self.start_btn.pack(pady=10)
        
        # EXIT BUTTON
        self.exit_btn = Button(
            self.settings_frame,
            text="EXIT",
            command=self.window.quit,
            bg='red',
            fg='white',
            font=('Arial', 10),
            width=20
        )
        self.exit_btn.pack(side=BOTTOM, pady=10)
    
    #region HELPER FUNCTIONS
    
    def colorBar(self, bar, color):
        self.canvas.itemconfig(bar, fill=color)
    
    def swap(self, pos0, pos1):
        x0, _, x0b, _ = self.canvas.coords(pos0)
        x1, _, x1b, _ = self.canvas.coords(pos1)
        
        self.canvas.itemconfig(pos0, fill='red')
        self.canvas.itemconfig(pos1, fill='#00ff00')
        
        self.canvas.move(pos0, x1 - x0, 0)
        self.canvas.move(pos1, x0 - x1, 0)
    
    #endregion
    
    #region GENERATE BARS FUNCTION
    
    def generate_bars(self):
        self.canvas.delete('all')
        self.bars = []
        self.values = []
        
        heights = [random.randint(10, self.can_size - 10) for _ in range(self.num_bars)]
        
        for i in range(self.num_bars):
            height = heights[i]
            
            bar = self.canvas.create_rectangle(
                i * self.bar_width,
                self.can_size - height,
                (i * self.bar_width) + self.bar_width,
                self.can_size,
                fill='white',
                outline='#444444'
            )
            
            self.bars.append(bar)
            self.values.append(height)
        
        self.worker = None
        self.is_verify = False
    
    #endregion
    
    #region BUBBLE SORT
    
    def bubble_sort(self):
        n = len(self.values)
        
        for i in range(n - 1):
            for j in range(n - i - 1):
                
                if self.values[j] > self.values[j + 1]:
                    self.values[j], self.values[j + 1] = self.values[j + 1], self.values[j]
                    self.bars[j], self.bars[j + 1] = self.bars[j + 1], self.bars[j]
                    self.swap(self.bars[j], self.bars[j + 1])
                    yield
                
                else:
                    self.colorBar(self.bars[j], 'white')
    
    #endregion
    
    #region INSERTION SORT
    
    def insertion_sort(self):
        for i in range(1, len(self.values)):
            key = self.values[i]
            key_bar = self.bars[i]
            j = i - 1
            
            while j >= 0 and self.values[j] > key:
                self.values[j + 1] = self.values[j]
                self.bars[j + 1], self.bars[j] = self.bars[j], self.bars[j + 1]
                self.swap(self.bars[j + 1], self.bars[j])
                
                yield
                j -= 1
            
            self.values[j + 1] = key
            self.bars[j + 1] = key_bar
    
    #endregion
    
    #region MERGE SORT
    
    def merge_sort_helper(self, l, r):
        if l < r:
            m = (l + r) // 2
            
            yield from self.merge_sort_helper(l, m)
            yield from self.merge_sort_helper(m + 1, r)
            

            # MERGE STEP - rebuild the array section
            left_vals = self.values[l:m + 1][:]
            right_vals = self.values[m + 1:r + 1][:]
            
            i = j = 0
            k = l
            
            while i < len(left_vals) and j < len(right_vals):
                
                if left_vals[i] <= right_vals[j]:
                    self.values[k] = left_vals[i]
                    i += 1
                
                else:
                    self.values[k] = right_vals[j]
                    j += 1
                
                k += 1
            
            while i < len(left_vals):
                self.values[k] = left_vals[i]
                i += 1
                k += 1
            
            while j < len(right_vals):
                self.values[k] = right_vals[j]
                j += 1
                k += 1
            
            # UPDATING THE VISUAL BARS to match the sorted values
            for idx in range(l, r + 1):
                current_height = self.values[idx]
                
                # updating bar height
                self.canvas.coords(
                    self.bars[idx],
                    idx * self.bar_width,
                    self.can_size - current_height,
                    idx * self.bar_width + self.bar_width,
                    self.can_size
                )
            
                self.colorBar(self.bars[idx], 'green') 
                yield
    
    def merge_sort(self):
        yield from self.merge_sort_helper(0, len(self.values) - 1)
    
    #endregion
    
    #region QUICK SORT
    
    def quick_sort_helper(self, low, high):
        if low < high:
            pivot = self.values[high]
            i = low - 1
            
            for j in range(low, high):
                
                if self.values[j] <= pivot:
                    i += 1
                    self.values[i], self.values[j] = self.values[j], self.values[i]
                    self.bars[i], self.bars[j] = self.bars[j], self.bars[i]
                    self.swap(self.bars[i], self.bars[j])
                    yield
                
                else:
                    self.colorBar(self.bars[j], 'white')
            
            self.values[i + 1], self.values[high] = self.values[high], self.values[i + 1]
            self.bars[i + 1], self.bars[high] = self.bars[high], self.bars[i + 1]
            self.swap(self.bars[i + 1], self.bars[high])
            
            
            
            yield
            


            yield from self.quick_sort_helper(low, i)
            yield from self.quick_sort_helper(i + 2, high)
    
    def quick_sort(self):
        yield from self.quick_sort_helper(0, len(self.values) - 1)
    
    #endregion
    
    #region VERIFICATION
    
    def verify(self):
        """verify that the array is sorted by coloring bars green"""
        for i in range(len(self.values) - 1):
            if self.values[i] <= self.values[i + 1]:
                self.colorBar(self.bars[i], 'green')
                yield
        
        self.colorBar(self.bars[-1], 'green')
    
    #endregion
    
    #region ANIMATION
    
    def animate(self):
        """control the animation loop using the generator pattern.
        repetedly calls next() on the worker generator to advance the sorting
        algorithm one step at a time. the delay between steps is controlled by
        the speed slider. when sorting completes, automatically starts the
        verification animation.
        """


        if self.worker is not None:
            try:
                next(self.worker)
                # speed controller
                speed = 68 - self.speed_slider.get()
                self.window.after(speed, self.animate)
            
            except StopIteration:
                if not self.is_verify:
                    self.worker = self.verify()
                    self.is_verify = True
                    self.animate()
                else:
                    self.is_verify = False
                    self.worker = None
    
    def start_sort(self):
        algo = self.variable.get()
        
        if algo == "Bubble Sort":
            self.worker = self.bubble_sort()
        
        elif algo == "Insertion Sort":
            self.worker = self.insertion_sort()
        
        elif algo == "Merge Sort":
            self.worker = self.merge_sort()
        
        elif algo == "Quick Sort":
            self.worker = self.quick_sort()
        
        self.animate()
    
    #endregion
    
    def run(self):
        self.window.mainloop()


# Run the application
if __name__ == "__main__":
    app = SortVisualizer()
    app.run()