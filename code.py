import tkinter as tk
import random
from tkinter import HORIZONTAL

colonne_size = 10
windowSize = 600
worker = None
is_verify = False

OPTIONS = [
    "Bubble Sort",
    "Selection Sort",
    "Insertion Sort",
    "Comb Sort",
    "Cocktail Shaker Sort",
]


def colorBar(col, color):
    canvas.itemconfig(col, fill=color)


# Function to swap two bars that will be animated
def swap(pos_0, pos_1):
    bar11, _, bar12, _ = canvas.coords(pos_0)
    bar21, x, bar22, _ = canvas.coords(pos_1)
    canvas.itemconfig(pos_0, fill='red')
    canvas.itemconfig(pos_1, fill='white')
    canvas.move(pos_0, bar21 - bar11, 0)
    canvas.move(pos_1, bar12 - bar22, 0)


# Insertion Sort
def _insertion_sort():
    global barList
    global lengthList

    for i in range(len(lengthList)):
        cursor = lengthList[i]
        cursorBar = barList[i]
        pos = i

        while pos > 0 and lengthList[pos - 1] > cursor:
            lengthList[pos] = lengthList[pos - 1]
            barList[pos], barList[pos - 1] = barList[pos - 1], barList[pos]
            swap(barList[pos], barList[pos - 1])
            yield
            pos -= 1

        lengthList[pos] = cursor
        barList[pos] = cursorBar
        swap(barList[pos], cursorBar)


# Bubble Sort
def _bubble_sort():
    global barList
    global lengthList

    for i in range(len(lengthList) - 1):
        for j in range(len(lengthList) - i - 1):
            if (lengthList[j] > lengthList[j + 1]):
                lengthList[j], lengthList[j + 1] = lengthList[j + 1], lengthList[j]
                barList[j], barList[j + 1] = barList[j + 1], barList[j]
                swap(barList[j + 1], barList[j])
                colorBar(barList[-i], 'white')
                yield
            else:
                colorBar(barList[j], 'white')


# Selection Sort
def _selection_sort():
    global barList
    global lengthList

    for i in range(len(lengthList)):
        min = i
        for j in range(i + 1, len(lengthList)):
            if (lengthList[j] < lengthList[min]):
                min = j
        lengthList[min], lengthList[i] = lengthList[i], lengthList[min]
        barList[min], barList[i] = barList[i], barList[min]
        swap(barList[min], barList[i])
        yield


def _comb_sort():
    """
    https://en.wikipedia.org/wiki/Comb_sort
    Worst-case performance: O(N^2)
    """
    global barList
    global lengthList

    n = len(lengthList)
    gap = n
    shrink = 1.3
    sorted = False
    while not sorted:
        gap = int(gap / shrink)
        if gap > 1:
            sorted = False
        else:
            gap = 1
            sorted = True

        i = 0
        while i + gap < n:
            if lengthList[i] > lengthList[i + gap]:
                lengthList[i], lengthList[i + gap] = lengthList[i + gap], lengthList[i]
                barList[i], barList[i + gap] = barList[i + gap], barList[i]
                swap(barList[i], barList[i + gap])
                sorted = False
                yield
            else:
                colorBar(barList[i], "white")
            i = i + 1


def _cocktail_shaker_sort():
    """
    Cocktail_shaker_sort
    Sorting a given array
    mutation of bubble sort
    reference: https://en.wikipedia.org/wiki/Cocktail_shaker_sort

    Worst-case performance: O(N^2)
    """
    global barList
    global lengthList

    n = len(lengthList)
    swapped = True
    while swapped:
        swapped = False
        for i in range(1, n):
            if lengthList[i - 1] > lengthList[i]:
                lengthList[i - 1], lengthList[i] = lengthList[i], lengthList[i - 1]
                barList[i - 1], barList[i] = barList[i], barList[i - 1]
                swap(barList[i], barList[i - 1])
                swapped = True
                yield
            else:
                colorBar(barList[i - 1], "white")
        if swapped == False:
            return
        swapped = False
        for i in range(n - 1, 0, -1):
            if lengthList[i - 1] > lengthList[i]:
                lengthList[i - 1], lengthList[i] = lengthList[i], lengthList[i - 1]
                barList[i - 1], barList[i] = barList[i], barList[i - 1]
                swap(barList[i - 1], barList[i])
                swapped = True
                yield
            else:
                colorBar(barList[i], "white")


def _verify():
    global barList
    global lengthList
    global is_verify

    for i in range(len(lengthList) - 1):
        if lengthList[i] < lengthList[i + 1]:
            colorBar(barList[i], 'green')
            yield
    colorBar(barList[-1], 'green')


def verify():
    global worker
    worker = _verify()
    animate()


def start():
    global worker
    algo = variable.get()
    if algo == OPTIONS[0]:
        worker = _bubble_sort()
    elif algo == OPTIONS[1]:
        worker = _selection_sort()
    elif algo == OPTIONS[2]:
        worker = _insertion_sort()
    elif algo == OPTIONS[3]:
        worker = _comb_sort()
    elif algo == OPTIONS[4]:
        worker = _cocktail_shaker_sort()
    animate()


# Animation Function
def animate():
    global worker
    global is_verify
    if worker is not None:
        try:
            next(worker)
            window.after(scale_speed.get(), animate)
        except StopIteration:
            if not is_verify:
                verify()
                is_verify = True
            else:
                is_verify = False
                worker = None


# Generator function for generating data
def generate():
    global barList
    global lengthList
    global colonne_size
    canvas.delete('all')
    barList = []
    lengthList = []

    colonne_size = scale.get()
    data = list(range(1, windowSize // colonne_size + 1))
    random.shuffle(data)

    for i, height in enumerate(data):
        bar = canvas.create_rectangle(i * colonne_size, windowSize - (height * colonne_size),
                                      i * colonne_size + colonne_size, windowSize,
                                      outline="black", fill="white")
        barList.append(bar)
        lengthList.append(height * colonne_size)


# Making a window using the Tk widget
window = tk.Tk()
window.title('Sorting Visualizer')
window.size = windowSize

# création canevas
canvas = tk.Canvas(window, bg="gray", height=windowSize, width=windowSize)
canvas.pack(side=tk.LEFT)

# boutons
window.start = tk.Button(window, text="Generate", command=generate, width=20)
window.start.pack(side=tk.TOP)

# List Dropdown
variable = tk.StringVar(window)
variable.set(OPTIONS[0])  # default value
w = tk.OptionMenu(window, variable, *OPTIONS)
w.config(width=20)
w.pack()

# Slider
scale = tk.Scale(window, from_=2, to=windowSize // 10, orient=HORIZONTAL, length=170, label="Size Bar")
scale.set(10)
scale.pack()
scale_speed = tk.Scale(window, from_=2, to=500, orient=HORIZONTAL, length=170, label="Speed")
scale_speed.set(10)
scale_speed.pack()

window.verify = tk.Button(window, text="Start", command=start)
window.verify.pack()

window.bouton_quitter = tk.Button(window, text="Exit", command=window.quit)
window.bouton_quitter.pack(side=tk.BOTTOM)

generate()
window.mainloop()