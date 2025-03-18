import tkinter as tk
from tkinter import ttk

from functools import partial
from tkinter.colorchooser import askcolor

import PIL
from PIL import ImageTk, Image, ImageDraw

import logic

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

DEFAULT_FONT = 24
DEFAULT_WIDGET_SIZE = 25
DEFAULT_ENTRY_SIZE = 10
DEFAULT_LABEL_SHIFT = 40 / MAIN_WIDTH

def is_int(text: str) -> bool:
    try:
        int(text)
    except Exception:
        return False

    return True

def is_float(text: str) -> bool:
    try:
        float(text)
    except Exception:
        return False

    return True

class MainWindow:

    # __WIDGET__

    def algorithm_set(self):
        algo_str = ""

        match self.algorithm.get():
            case 1:
                algo_str = "ЦДА"
                self.algorithm_func = logic.DrawDDA
            case 2:
                algo_str = "ЦДА (со сглаж.)"
                self.algorithm_func = logic.DrawDDA
            case 3:
                algo_str = "Алгоритм Ву"
                self.algorithm_func = logic.DrawWU
            case 4:
                algo_str = "Брезенхем"
                self.algorithm_func = logic.DrawBRESENHAM
            case 5:
                algo_str = "Брезенхем (со сглаж.)"
                self.algorithm_func = logic.DrawBRESENHAM_SMOOTH
            case 6:
                algo_str = "Библиотечный"
                self.algorithm_func = logic.DrawLIB
            case _:
                algo_str = "?"
                self.algorithm_func = None

        self.algorithm_label.config(text=f"Выбрано: {algo_str}")

    def widget_radiobuttons(self):
        self.algorithm = tk.IntVar()
        self.algorithm_func = None

        self.algorithm_label = ttk.Label(text="Выбрано: ЦДА", font=DEFAULT_FONT)
        self.algorithm_label.place(relx=VERTICAL_LEVEL_1, rely=0.05)

        self.CDA_radiobutton = tk.Radiobutton(self.root, font=DEFAULT_FONT, text="ЦДА", variable=self.algorithm, value=CDA, command=self.algorithm_set)
        self.CDA_radiobutton.place(relx=VERTICAL_LEVEL_1, rely=0.10)

        self.CDA_SMOOTH_radiobutton = tk.Radiobutton(self.root, font=DEFAULT_FONT, text="ЦДА (со сглаж.)", variable=self.algorithm, value=CDA_SMOOTH, command=self.algorithm_set)
        self.CDA_SMOOTH_radiobutton.place(relx=VERTICAL_LEVEL_1, rely=0.15)

        self.WU_radiobutton = tk.Radiobutton(self.root, font=DEFAULT_FONT, text="Алгоритм Ву", variable=self.algorithm, value=WU, command=self.algorithm_set)
        self.WU_radiobutton.place(relx=VERTICAL_LEVEL_1, rely=0.20)

        self.BRESENHAM_radiobutton = tk.Radiobutton(self.root, font=DEFAULT_FONT, text="Брезенхем", variable=self.algorithm, value=BRESENHAM, command=self.algorithm_set)
        self.BRESENHAM_radiobutton.place(relx=VERTICAL_LEVEL_3, rely=0.10)

        self.BRESENHAM_SMOOTH_radiobutton = tk.Radiobutton(self.root, font=DEFAULT_FONT, text="Брезенхем (со сглаж.)", variable=self.algorithm, value=BRESENHAM_SMOOTH, command=self.algorithm_set)
        self.BRESENHAM_SMOOTH_radiobutton.place(relx=VERTICAL_LEVEL_3, rely=0.15)

        self.LIB_radiobutton = tk.Radiobutton(self.root, font=DEFAULT_FONT, text="Библиотечный", variable=self.algorithm, value=LIB, command=self.algorithm_set)
        self.LIB_radiobutton.place(relx=VERTICAL_LEVEL_3, rely=0.20)

        self.CDA_radiobutton.select()
        self.algorithm_func = logic.DrawDDA

    def color_set(self):
        self.color = askcolor()[1]
        self.color_label.config(text=f"Выбрано: {self.color}")

    def widget_color_button(self):
        self.color = "#000000"

        self.color_label = tk.Label(self.root, font=DEFAULT_FONT, text="Цвет: Чёрный")
        self.color_label.place(relx=VERTICAL_LEVEL_3, rely=0.05)

        self.color_button = tk.Button(self.root, text="Выбрать цвет", width=DEFAULT_WIDGET_SIZE, command=self.color_set)
        self.color_button.place(relx=VERTICAL_LEVEL_1, rely=0.30)

    # ___LEVEL_1___

    def draw_line(self):
        if self.algorithm_func is None:
            self.result_msg("Нет функции для отрисовки")

            return
        
        # ------------------------------------
        
        x0 = 0
        y0 = 0
        x1 = 0
        y1 = 0

        entered = self.x0_entry.get()
        if not(is_float(entered)):
            self.result_msg("Неправильное значение x0")

            return False

        x0 = float(entered)
        
        entered = self.y0_entry.get()
        if not(is_float(entered)):
            self.result_msg("Неправильное значение y0")

            return False
        
        y0 = float(entered)
        
        entered = self.x1_entry.get()
        if not(is_float(entered)):
            self.result_msg("Неправильное значение x1")

            return False

        x1 = float(entered)
        
        entered = self.y1_entry.get()
        if not(is_float(entered)):
            self.result_msg("Неправильное значение y1")

            return False
        
        y1 = float(entered)
    # ------------------------------------
        
        if self.algorithm.get() == LIB:
            code = self.algorithm_func(self.draw, x0, y0, x1, y1, self.color, [CANVAS_WIDTH, CANVAS_HEIGHT])
        else:
            code = self.algorithm_func(self.pilImage, x0, y0, x1, y1, self.color, [CANVAS_WIDTH, CANVAS_HEIGHT])

        if code == logic.ERR_COLOR:
            self.result_msg("Нет цвета для отрисовки")
        elif code == logic.ERR_RESOLUTION:
            self.result_msg("Отрезок не лежит в видимой области")
        else:
            self.canvas_image_submit()
            self.result_msg("Отрезок отрисована успешно")

    def widget_draw_coords(self):
        self.x0_label = tk.Label(self.root, font=DEFAULT_FONT, text="x0")
        self.x0_label.place(relx=VERTICAL_LEVEL_1 - DEFAULT_LABEL_SHIFT, rely=0.25)
        self.x0_entry = tk.Entry(self.root, width=DEFAULT_ENTRY_SIZE)
        self.x0_entry.place(relx=VERTICAL_LEVEL_1, rely=0.25)

        self.y0_label = tk.Label(self.root, font=DEFAULT_FONT, text="y0")
        self.y0_label.place(relx=VERTICAL_LEVEL_2 - DEFAULT_LABEL_SHIFT, rely=0.25)
        self.y0_entry = tk.Entry(self.root, width=DEFAULT_ENTRY_SIZE)
        self.y0_entry.place(relx=VERTICAL_LEVEL_2, rely=0.25)

        self.x1_label = tk.Label(self.root, font=DEFAULT_FONT, text="x1")
        self.x1_label.place(relx=VERTICAL_LEVEL_3 - DEFAULT_LABEL_SHIFT, rely=0.25)
        self.x1_entry = tk.Entry(self.root, width=DEFAULT_ENTRY_SIZE)
        self.x1_entry.place(relx=VERTICAL_LEVEL_3, rely=0.25)

        self.y1_label = tk.Label(self.root, font=DEFAULT_FONT, text="y1")
        self.y1_label.place(relx=VERTICAL_LEVEL_4 - DEFAULT_LABEL_SHIFT, rely=0.25)
        self.y1_entry = tk.Entry(self.root, width=DEFAULT_ENTRY_SIZE)
        self.y1_entry.place(relx=VERTICAL_LEVEL_4, rely=0.25)

    def widget_draw_button(self):
        self.color_button = tk.Button(self.root, text="Рисовать", width=DEFAULT_WIDGET_SIZE, command=self.draw_line)
        self.color_button.place(relx=VERTICAL_LEVEL_3, rely=0.30)

    def widget_clean_button(self):
        self.color_button = tk.Button(self.root, text="Очистить", width=DEFAULT_WIDGET_SIZE, command=self.canvas_clear)
        self.color_button.place(relx=VERTICAL_LEVEL_3, rely=0.35)

    def widget_level_1(self):
        self.level_1_label = tk.Label(self.root, font=DEFAULT_FONT, text="I часть")
        self.level_1_label.place(relx=VERTICAL_LEVEL_3, rely=0.0)

        self.widget_radiobuttons()
        self.widget_draw_coords()
        self.widget_draw_button()
        self.widget_clean_button()



    # ___CANVAS___



    def widget_canvas(self):
        self.canvas = tk.Canvas(self.root, bg='white', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
        self.canvas.pack(anchor='w')

        self.canvas_image()

    def result_msg(self, stroke: str):
        self.result_label.config(text=f"Результат: {stroke}")

    def widget_result(self):
        self.result_label = tk.Label(self.root, font=DEFAULT_FONT, text="")
        self.result_label.place(relx=VERTICAL_LEVEL_1, rely=0.95)

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

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Лабораторная работа №3")
        self.root.geometry(f"{MAIN_WIDTH}x{MAIN_HEIGHT}")

        self.widget_canvas()
        self.widget_level_1()
        self.widget_color_button()
        self.widget_result()


