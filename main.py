from tkinter import *
from PIL import Image
import io
import numpy as np
import csv


def paint(event):
    python_green = "#476042"
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    w.create_oval(x1, y1, x2, y2, fill=python_green)


def clear_canvas():
    w.delete("all")


def convert_list_of_RGB_tuples_to_list_of_bits(param):
    new_list_of_bits = []
    for i in param:
        for j in i:
            if i[0] == 255:
                new_list_of_bits.append(0)
            elif i[0] == 0:
                new_list_of_bits.append(1)
            break

    return new_list_of_bits


def recognize():
    ps_from_canvas = w.postscript(colormode="mono")
    image = Image.open(io.BytesIO(ps_from_canvas.encode('utf-8')))

    list_of_RGB_tuples_from_image = list(image.getdata()) #each tuple represents one pixel
    convert_list_of_RGB_tuples_to_list_of_bits(list_of_RGB_tuples_from_image)


#learning mode view
def learning_mode():
    def canvas_to_list_of_RGB_tuples(canvas):
        ps_from_canvas = canvas.postscript(colormode="mono")
        image = Image.open(io.BytesIO(ps_from_canvas.encode('utf-8')))
        list_of_RGB_tuples_from_image = list(image.getdata())  # each tuple represents one pixel
        return list_of_RGB_tuples_from_image

    def paint(event):
        python_green = "#476042"
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        w.create_oval(x1, y1, x2, y2, fill=python_green)

    def clear_canvas():
        w.delete("all")

    def learn():
        list_of_RGB_tuples = canvas_to_list_of_RGB_tuples(w)
        list_of_bits = convert_list_of_RGB_tuples_to_list_of_bits(list_of_RGB_tuples)
        list_with_character = add_character_to_list_of_bits(list_of_bits, radio_variable)
        save_pattern(list_with_character)
        clear_canvas()

    def add_character_to_list_of_bits(list_of_bits, character):
        character = radio_variable.get()
        if character == 0:
            list_of_bits.append("A")
        elif character == 1:
            list_of_bits.append("B")
        elif character == 2:
            list_of_bits.append("C")

        return list_of_bits

    def save_pattern(list_of_bits):
        try:
            with open("dataset", "a+") as f:
                wr = csv.writer(f, quoting=csv.QUOTE_ALL)
                wr.writerow(list_of_bits)
        except FileNotFoundError:
            print("File not accessible")

    #test
    def read_from_csv():
        with open("dataset", "r", newline='\n') as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)

    master.destroy()

    learning_window = Tk()
    learning_window.title("Letter recognition - learning mode")
    learning_window.geometry("300x300")

    w = Canvas(learning_window,
               width=canvas_width,
               height=canvas_height,
               borderwidth=2,
               relief="groove",
               bg="white")
    w.pack(expand="True")
    w.bind("<B1-Motion>", paint)

    clear_button = Button(learning_window, text="Clear", command=clear_canvas)
    clear_button.pack(side=BOTTOM, pady=5, ipady=5, ipadx=22)

    #test
    read_button = Button(learning_window, text="Read", command=read_from_csv)
    read_button.pack(side=BOTTOM, pady=5, ipady=5, ipadx=22)

    learn_button = Button(learning_window, text="Learn", command=learn)
    learn_button.pack(side=BOTTOM, pady=5, ipady=5, ipadx=22)

    radio_variable = IntVar()
    radio_variable.set(0)
    Radiobutton(learning_window, text="A", variable=radio_variable, value=0).pack()
    Radiobutton(learning_window, text="B", variable=radio_variable, value=1).pack()
    Radiobutton(learning_window, text="C", variable=radio_variable, value=2).pack()

    message = Label(learning_window, text="Choose the character, draw and click Learn")
    message.pack(side=BOTTOM, pady=10)

    mainloop()


#recognition mode view
master = Tk()
master.title("Letter recognition")
master.geometry("300x300")

canvas_width = 28
canvas_height = 28

w = Canvas(master,
           width=canvas_width,
           height=canvas_height,
           borderwidth=2,
           relief="groove",
           bg="white")
w.pack(expand="True")
w.bind("<B1-Motion>", paint)

clear_button = Button(master, text="Clear", command=clear_canvas)
clear_button.pack(side=BOTTOM, pady=5, ipady=5, ipadx=22)

recognize_button = Button(master, text="Recognize", command=recognize)
recognize_button.pack(side=BOTTOM, pady=5, ipady=5, ipadx=10)

message = Label(master, text="Draw A, B or C in the canvas and click Recognize")
message.pack(side=BOTTOM, pady=10)

menu_bar = Menu(master)
menu_bar.add_command(label="Learning mode", command=learning_mode)

master.config(menu=menu_bar)

mainloop()
