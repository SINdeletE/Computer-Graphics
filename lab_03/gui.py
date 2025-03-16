import tkinter as tk
from tkinter import ttk

from functools import partial
from tkinter.colorchooser import askcolor

import PIL
from PIL import ImageTk, Image, ImageDraw

MAIN_HEIGHT = 1920
MAIN_WIDTH = 3000

CANVAS_HEIGHT = MAIN_HEIGHT
CANVAS_WIDTH = MAIN_HEIGHT

MAIN_SHIFT = 100

VERTICAL_LEVEL_1 = (CANVAS_WIDTH + (MAIN_WIDTH - CANVAS_WIDTH - MAIN_SHIFT) / 4 * 0) / MAIN_WIDTH
VERTICAL_LEVEL_2 = (CANVAS_WIDTH + (MAIN_WIDTH - CANVAS_WIDTH - MAIN_SHIFT) / 4 * 1) / MAIN_WIDTH
VERTICAL_LEVEL_3 = (CANVAS_WIDTH + (MAIN_WIDTH - CANVAS_WIDTH - MAIN_SHIFT) / 4 * 2) / MAIN_WIDTH
VERTICAL_LEVEL_4 = (CANVAS_WIDTH + (MAIN_WIDTH - CANVAS_WIDTH - MAIN_SHIFT) / 4 * 3) / MAIN_WIDTH

CDA = 1
CDA_SMOOTH = 2
WU = 3
BRESENHAM = 4
BRESENHAM_SMOOTH = 5
LIB = 6

DEFAULT_FONT = 27
DEFAULT_BUTTON_SIZE = 25

class MainWindow:

    # __WIDGET__

    def algorithm_label_set(self):
        algo_str = ""

        match self.algorithm.get():
            case 1:
                algo_str = "ЦДА"
            case 2:
                algo_str = "ЦДА (со сглаж.)"
            case 3:
                algo_str = "Алгоритм Ву"
            case 4:
                algo_str = "Брезенхем"
            case 5:
                algo_str = "Брезенхем (со сглаж.)"
            case 6:
                algo_str = "Библиотечный"
            case _:
                algo_str = "?"

        self.algorithm_label.config(text=f"Выбрано: {algo_str}")

    def widget_radiobuttons(self):
        self.algorithm = tk.IntVar()

        self.algorithm_label = ttk.Label(text="Выбрано: ЦДА", font=DEFAULT_FONT)
        self.algorithm_label.place(relx=VERTICAL_LEVEL_1, rely=0.05)

        self.CDA_radiobutton = tk.Radiobutton(self.root, font=DEFAULT_FONT, text="ЦДА", variable=self.algorithm, value=CDA, command=self.algorithm_label_set)
        self.CDA_radiobutton.place(relx=VERTICAL_LEVEL_1, rely=0.10)

        self.CDA_SMOOTH_radiobutton = tk.Radiobutton(self.root, font=DEFAULT_FONT, text="ЦДА (со сглаж.)", variable=self.algorithm, value=CDA_SMOOTH, command=self.algorithm_label_set)
        self.CDA_SMOOTH_radiobutton.place(relx=VERTICAL_LEVEL_1, rely=0.15)

        self.WU_radiobutton = tk.Radiobutton(self.root, font=DEFAULT_FONT, text="Алгоритм Ву", variable=self.algorithm, value=WU, command=self.algorithm_label_set)
        self.WU_radiobutton.place(relx=VERTICAL_LEVEL_1, rely=0.20)

        self.BRESENHAM_radiobutton = tk.Radiobutton(self.root, font=DEFAULT_FONT, text="Брезенхем", variable=self.algorithm, value=BRESENHAM, command=self.algorithm_label_set)
        self.BRESENHAM_radiobutton.place(relx=VERTICAL_LEVEL_3, rely=0.10)

        self.BRESENHAM_SMOOTH_radiobutton = tk.Radiobutton(self.root, font=DEFAULT_FONT, text="Брезенхем (со сглаж.)", variable=self.algorithm, value=BRESENHAM_SMOOTH, command=self.algorithm_label_set)
        self.BRESENHAM_SMOOTH_radiobutton.place(relx=VERTICAL_LEVEL_3, rely=0.15)

        self.LIB_radiobutton = tk.Radiobutton(self.root, font=DEFAULT_FONT, text="Библиотечный", variable=self.algorithm, value=LIB, command=self.algorithm_label_set)
        self.LIB_radiobutton.place(relx=VERTICAL_LEVEL_3, rely=0.20)

        self.CDA_radiobutton.select()

    def color_set(self):
        self.color = askcolor()[1]
        self.color_label.config(text=f"Выбрано: {self.color}")

    def widget_color_button(self):
        self.color = "#000000"

        self.color_label = tk.Label(self.root, font=DEFAULT_FONT, text="Цвет: Чёрный")
        self.color_label.place(relx=VERTICAL_LEVEL_3, rely=0.05)

        self.color_button = tk.Button(self.root, text="Выбрать цвет", width=DEFAULT_BUTTON_SIZE, command=self.color_set)
        self.color_button.place(relx=VERTICAL_LEVEL_1, rely=0.25)

    def widget_level_1(self):
        self.level_1_label = tk.Label(self.root, font=DEFAULT_FONT, text="I часть")
        self.level_1_label.place(relx=VERTICAL_LEVEL_3, rely=0.0)

        self.widget_radiobuttons()

    def widget_canvas(self):
        self.canvas = tk.Canvas(self.root, bg='white', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
        self.canvas.pack(anchor='w')

    # ___CANVAS___

    def canvas_image(self):
        # Создаем новое изображение с зеленым фоном
        self.pilImage = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), "white")

        # Создаем объект ImageDraw для рисования на изображении
        self.draw = ImageDraw.Draw(self.pilImage)

    def canvas_clear(self):
        self.canvas_image()
        self.canvas_image_submit()

    def canvas_image_submit(self):
        # Преобразуем изображение в формат, который может быть использован в Tkinter
        self.image = ImageTk.PhotoImage(master=self.canvas, image=self.pilImage)  # Сохраняем ссылку на изображение

        # Отображаем изображение на Canvas
        self.canvas.create_image(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, image=self.image)

    # ___DRAW___

    def draw_line_pillow_lib(self, coords):
        # Рисуем линию на изображении
        self.draw.line(coords, fill=(128, 128, 128, 255), width=1)

        self.canvas_image_submit()

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Лабораторная работа №3")
        self.root.geometry(f"{MAIN_WIDTH}x{MAIN_HEIGHT}")

        self.widget_level_1()
        self.widget_color_button()
        self.widget_canvas()


