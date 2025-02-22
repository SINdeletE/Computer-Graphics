import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

import processing as pcs

MAIN_HEIGHT = 1400
MAIN_WIDTH = MAIN_HEIGHT * 2

# ___CANVAS___
CANVAS_HEIGHT = MAIN_HEIGHT
CANVAS_WIDTH = CANVAS_HEIGHT

# ___TASK___
TASK_HEIGHT = 700
TASK_WIDTH = 700

BUTTON_WIDTH = 300

# Разница по делениям
VERTICAL_SPACE = 40

# Деление окна по вертикали
VERTICAL_LEVEL_1 = (VERTICAL_SPACE * (0 + 1) + BUTTON_WIDTH * 0) / MAIN_WIDTH
VERTICAL_LEVEL_2 = (VERTICAL_SPACE * (1 + 1) + BUTTON_WIDTH * 1) / MAIN_WIDTH
VERTICAL_LEVEL_3 = (VERTICAL_SPACE * (2 + 1) + BUTTON_WIDTH * 2) / MAIN_WIDTH
VERTICAL_LEVEL_4 = (VERTICAL_SPACE * (3 + 1) + BUTTON_WIDTH * 3) / MAIN_WIDTH

#___DRAW___
FIGURE_COLOR = 'blue'
FIGURE_BORDER_WIDTH = 4

DEFAULT_CENTER_X = CANVAS_WIDTH / 2
DEFAULT_CENTER_Y = CANVAS_HEIGHT / 2

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

class TaskWindow:
    def __init__(self) -> None:
        self.task_root = tk.Tk()
        self.task_root.title("Задание")
        self.task_root.geometry(f"{TASK_WIDTH}x{TASK_HEIGHT}")

        self.task_label_create()
        
    def task_label_create(self):
        task = "16. Нарисовать исходный рисунок, осуществить его перенос, масштабирование и поворот"

        self.task_label = ttk.Label(self.task_root, text=task, wraplength=TASK_WIDTH)
        self.task_label.pack(anchor="n", expand=1)

        # Изображение с заданием
        # img = Image.open('image.JPG')
        # task_image = ImageTk.PhotoImage(img)

        # self.task_image_label = ttk.Label(self.task_root, text=task, wraplength=TASK_WIDTH, image=task_image)
        # self.task_image_label.pack(anchor="center", expand=1)

class MainApplication:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Лабораторная работа №2")
        self.root.geometry(f"{MAIN_WIDTH}x{MAIN_HEIGHT}")

        self.widget_canvas()
        self.widget_error_entry()
        self.widget_task_button()

        # ID объектов
        self.IDs = []

        # Класс фигуры
        self.figure = pcs.Figure()
        self.figure.move(DEFAULT_CENTER_X, DEFAULT_CENTER_Y) # Смещаем к центру холста canvas
        
        self.figure_draw()

        self.root.mainloop()

    # ___TASK___

    def task_window_open(self):
        self.task = TaskWindow()
    
    def widget_task_button(self):
        self.task_button = tk.Button(self.root, text="Условие задания", command=self.task_window_open)
        self.task_button.place(relx=VERTICAL_LEVEL_1, rely=0.95, width=BUTTON_WIDTH)

    # ___CANVAS___

    def widget_canvas(self):
        self.canvas = tk.Canvas(self.root, bg='white', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
        self.canvas.pack(anchor='e')

    # ___ERROR___
    def widget_error_entry(self):
        self.error_label = tk.Label(self.root, text='Результаты действий над рисунком', width=30)
        self.error_label.place(relx=VERTICAL_LEVEL_2, rely=0.92)

        self.error_entry = tk.Entry(self.root, width=50)
        self.error_entry.config(state='readonly')
        self.error_entry.place(relx=VERTICAL_LEVEL_2, rely=0.95)

    # ___DRAW___
    def figure_draw(self):
        figure_link = self.figure.get()
        
        # ___rect___
        rect_lines = [
                        [figure_link['rect']['points'][0][:2:], figure_link['rect']['points'][3][:2:]],
                        [figure_link['rect']['points'][1][:2:], figure_link['rect']['points'][2][:2:]]
                    ]

        for line in rect_lines:
            self.figure_line_create(line[0], line[1])

        arc_lines = [
                        [figure_link['rect']['arc_points'][0][:2:], figure_link['rect']['arc_points'][1][:2:]],
                        [figure_link['rect']['arc_points'][2][:2:], figure_link['rect']['arc_points'][3][:2:]]
                    ]

        self.figure_arc_create(arc_lines[0][0], arc_lines[0][1], -90)
        self.figure_arc_create(arc_lines[1][0], arc_lines[1][1], 90)

        # ___wheels___
        for i in range(0, len(figure_link['wheels']['points']), 2):
            self.figure_circle_create(figure_link['wheels']['points'][i][:2:], figure_link['wheels']['points'][i + 1][:2:])
        
        # ___tower___
        for i in range(len(figure_link['tower']['points']) - 1):
            self.figure_line_create(figure_link['tower']['points'][i][:2:], figure_link['tower']['points'][i + 1][:2:])

        # ___tower_ellipse___
        self.figure_arc_create(figure_link['tower']['ellipse']['points'][0][:2:], figure_link['tower']['ellipse']['points'][1][:2:], 0)

        # ___tube___
        for i in range(len(figure_link['tube']['points']) - 1):
            self.figure_line_create(figure_link['tube']['points'][i][:2:], figure_link['tube']['points'][i + 1][:2:])
        

    def figure_line_create(self, p1: list, p2: list):
        object_id = self.canvas.create_line(*p1, *p2, fill=FIGURE_COLOR, width=FIGURE_BORDER_WIDTH)
        self.IDs.append(object_id)

    def figure_arc_create(self, p_left_up: list, p_right_down: list, angle: float):
        object_id = self.canvas.create_arc(*p_left_up, *p_right_down, start=angle, extent=180, style='arc', outline=FIGURE_COLOR, width=FIGURE_BORDER_WIDTH)
        self.IDs.append(object_id)

    def figure_circle_create(self, p_left_up: list, p_right_down: list):
        object_id = self.canvas.create_oval(*p_left_up, *p_right_down, outline=FIGURE_COLOR, width=FIGURE_BORDER_WIDTH)
        self.IDs.append(object_id)

