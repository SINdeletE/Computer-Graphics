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

ENTRY_WIDTH = 15
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
FIGURE_POINT_COLOR = 'red'
FIGURE_BORDER_WIDTH = 4

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

class Stack:
    def __init__(self):
        self.stack = []
    
    def stack_push(self, element):
        self.stack.append(element)
    
    def stack_pop(self):
        try:
            return self.stack.pop()
        except Exception:
            return None
    
    def stack_clear(self):
        while (self.stack_pop() is not None):
            pass
    
    def stack_is_empty(self):
        if self.stack == []:
            return True
        
        return False

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
        self.widgets_error_entry()
        self.widgets_task_button()
        self.widgets_move()
        self.widgets_scale()
        # self.widgets_rotate()
        self.widgets_default()
        self.widgets_action_cancel()
        self.widgets_rotate_center()

        # Класс фигуры
        self.figure = pcs.Figure()
        self.figure.move(pcs.DEFAULT_CENTER_X, pcs.DEFAULT_CENTER_Y) # Смещаем к центру холста canvas

        # Стек из действий
        self.action_stack = Stack()
        
        self.figure_draw()

        self.root.mainloop()

    # ___TASK___

    def task_window_open(self):
        self.task = TaskWindow()
    
    def widgets_task_button(self):
        self.task_button = tk.Button(self.root, text="Условие задания", command=self.task_window_open)
        self.task_button.place(relx=VERTICAL_LEVEL_1, rely=0.95, width=BUTTON_WIDTH)

    # ___ERROR___

    def widgets_error_entry(self):
        self.error_label = tk.Label(self.root, text='Результаты действий над рисунком', width=30)
        self.error_label.place(relx=VERTICAL_LEVEL_2, rely=0.92)

        self.error_entry = tk.Entry(self.root, width=50)
        self.error_entry.config(state='readonly')
        self.error_entry.place(relx=VERTICAL_LEVEL_2, rely=0.95)
    
    def error_msg(self, msg: str):
        self.error_entry.config(state='normal')
        self.error_entry.delete(0, tk.END)
        self.error_entry.insert(0, msg)
        self.error_entry.config(state='readonly')

    # ___MOVE___
    
    def widget_move(self):
        move_x = 0
        move_y = 0

        entered = self.move_x_entry.get()
        if not(is_float(entered)):
            self.error_msg("Неправильное значение dX")

            return False

        move_x = float(entered)
        
        entered = self.move_y_entry.get()
        if not(is_float(entered)):
            self.error_msg("Неправильное значение dY")

            return False
        
        move_y = float(entered)
        
        self.figure_event('move', x=move_x, y=move_y)
        self.action_stack.stack_push(['move', [move_x, move_y]])

        self.error_msg("*Перемещение*")

        return True

    def widgets_move(self):
        self.move_x_label = tk.Label(self.root, text='dX:', width=2)
        self.move_x_label.place(relx=0.000, rely=0.00)

        self.move_x_entry = tk.Entry(self.root, width=ENTRY_WIDTH)
        self.move_x_entry.place(relx=VERTICAL_LEVEL_1, rely=0.00)

        self.move_y_label = tk.Label(self.root, text='dY:', width=2)
        self.move_y_label.place(relx=0.121, rely=0.00)

        self.move_y_entry = tk.Entry(self.root, width=ENTRY_WIDTH)
        self.move_y_entry.place(relx=VERTICAL_LEVEL_2, rely=0.00)

        self.move_button = tk.Button(self.root, text="Перенос", command=self.widget_move)
        self.move_button.place(relx=VERTICAL_LEVEL_3, rely=0.00, width=BUTTON_WIDTH)

    # ___SCALE___
    
    def widget_scale(self):
        scale_kx = 0
        scale_ky = 0

        entered = self.scale_kx_entry.get()
        if not(is_float(entered)):
            self.error_msg("Неправильное значение kx")

            return False

        scale_kx = float(entered)

        if (abs(scale_kx) < pcs.EPS):
            self.error_msg("Масштаб kx не может быть равен нулю")

            return False
        
        entered = self.scale_ky_entry.get()
        if not(is_float(entered)):
            self.error_msg("Неправильное значение ky")

            return False

        scale_ky = float(entered)

        if (abs(scale_ky) < pcs.EPS):
            self.error_msg("Масштаб ky не может быть равен нулю")

            return False
        
        move_x = 0
        move_y = 0

        entered = self.center_scale_kx_entry.get()
        if not(is_float(entered)):
            self.error_msg("Неправильное значение X")

            return False

        move_x = float(entered)
        
        entered = self.center_scale_ky_entry.get()
        if not(is_float(entered)):
            self.error_msg("Неправильное значение Y")

            return False
        
        move_y = float(entered)
        
        self.figure_event('scale', kx=scale_kx, ky=scale_ky, x=move_x, y=move_y)
        self.action_stack.stack_push(['scale', [scale_kx, scale_ky, move_x, move_y]])

        self.error_msg("*Масштабирование*")

        return True

    def widgets_scale(self):
        self.center_scale_x_label = tk.Label(self.root, text='X:', width=2)
        self.center_scale_x_label.place(relx=0.000, rely=0.05)

        self.center_scale_kx_entry = tk.Entry(self.root, width=ENTRY_WIDTH)
        self.center_scale_kx_entry.place(relx=VERTICAL_LEVEL_1, rely=0.05)

        self.center_scale_y_label = tk.Label(self.root, text='Y:', width=2)
        self.center_scale_y_label.place(relx=0.121, rely=0.05)

        self.center_scale_ky_entry = tk.Entry(self.root, width=ENTRY_WIDTH)
        self.center_scale_ky_entry.place(relx=VERTICAL_LEVEL_2, rely=0.05)

        self.msg_scale_label = tk.Label(self.root, text='<- Центр масштабирования', width=25)
        self.msg_scale_label.place(relx=VERTICAL_LEVEL_3, rely=0.05)

        self.scale_x_label = tk.Label(self.root, text='kx:', width=2)
        self.scale_x_label.place(relx=0.000, rely=0.10)

        self.scale_kx_entry = tk.Entry(self.root, width=ENTRY_WIDTH)
        self.scale_kx_entry.place(relx=VERTICAL_LEVEL_1, rely=0.10)

        self.scale_y_label = tk.Label(self.root, text='ky:', width=2)
        self.scale_y_label.place(relx=0.121, rely=0.10)

        self.scale_ky_entry = tk.Entry(self.root, width=ENTRY_WIDTH)
        self.scale_ky_entry.place(relx=VERTICAL_LEVEL_2, rely=0.10)

        self.scale_button = tk.Button(self.root, text="Масштабирование", command=self.widget_scale)
        self.scale_button.place(relx=VERTICAL_LEVEL_3, rely=0.10, width=BUTTON_WIDTH)

    # ___ROTATE___
    
    def widget_rotate(self):
        rotate_angle = 0

        entered = self.rotate_angle_entry.get()
        if not(is_float(entered)):
            self.error_msg("Неправильное значение k")

            return False

        rotate_angle = float(entered)
        
        self.figure_event('rotate', angle=rotate_angle)
        self.action_stack.stack_push(['rotate', [rotate_angle]])

        self.error_msg("*Поворот*")

        return True

    def widgets_rotate(self):
        self.rotate_angle_label = tk.Label(self.root, text='°:', width=2)
        self.rotate_angle_label.place(relx=0.003, rely=0.15)

        self.rotate_angle_entry = tk.Entry(self.root, width=ENTRY_WIDTH)
        self.rotate_angle_entry.place(relx=VERTICAL_LEVEL_1, rely=0.15)

        self.rotate_button = tk.Button(self.root, text="Повернуть", command=self.widget_rotate)
        self.rotate_button.place(relx=VERTICAL_LEVEL_3, rely=0.15, width=BUTTON_WIDTH)
    
    # ___DEFAULT___

    def widget_default(self):
        self.figure_event('default')

        self.error_msg("*Восстановление*")

    def widgets_default(self):
        self.default_button = tk.Button(self.root, text="Восстановить", command=self.widget_default)
        self.default_button.place(relx=VERTICAL_LEVEL_1, rely=0.25, width=BUTTON_WIDTH * 2)

    # ___CANCEL_LAST_ACTION___

    def widget_action_cancel(self):
        last_action = self.action_stack.stack_pop()
        if last_action is None:
            self.error_msg("*Нет предыдущих действий*")
            
            return False
        
        action = last_action[0]
        kwargs = list(map(float, last_action[1]))
    
        match action:
            case 'move':
                self.figure_event('move', x=-kwargs[0], y=-kwargs[1])

            case 'scale':
                self.figure_event('scale', kx=1 / kwargs[0], ky=1 / kwargs[1], x=kwargs[2], y=kwargs[3])

            case 'rotate':
                self.figure_event('rotate', angle=-kwargs[0])

            case 'rotate center':
                self.figure_event('rotate center', angle=-kwargs[0], x=kwargs[1], y=kwargs[2])

        self.error_msg("*Отмена*")

        return True

    def widgets_action_cancel(self):
        self.default_button = tk.Button(self.root, text="Отменить предыдущее действие", command=self.widget_action_cancel)
        self.default_button.place(relx=VERTICAL_LEVEL_1, rely=0.30, width=BUTTON_WIDTH * 2)
    
    # ___ROTATE_CENTER___

    def widget_rotate_center(self):
        rotate_angle = 0
        center_x = 0
        center_y = 0

        entered = self.rotate_center_angle_entry.get()
        if not(is_float(entered)):
            self.error_msg("Неправильное значение k")

            return False

        rotate_angle = float(entered)

        entered = self.rotate_center_x_entry.get()
        if not(is_float(entered)):
            self.error_msg("Неправильное значение X")

            return False

        center_x = float(entered)
        
        entered = self.rotate_center_y_entry.get()
        if not(is_float(entered)):
            self.error_msg("Неправильное значение Y")

            return False
        
        center_y = float(entered)
        
        self.figure_event('rotate center', angle=rotate_angle, x=center_x, y=center_y)
        self.action_stack.stack_push(['rotate center', [rotate_angle, center_x, center_y]])

        self.error_msg("*Поворот*")

        return True
    
    def widgets_rotate_center(self):
        self.rotate_center_angle_label = tk.Label(self.root, text='°:', width=2)
        self.rotate_center_angle_label.place(relx=0.003, rely=0.20)

        self.rotate_center_angle_entry = tk.Entry(self.root, width=ENTRY_WIDTH)
        self.rotate_center_angle_entry.place(relx=VERTICAL_LEVEL_1, rely=0.20)

        self.rotate_center_x_label = tk.Label(self.root, text='X:', width=2)
        self.rotate_center_x_label.place(relx=0.121, rely=0.20)

        self.rotate_center_x_entry = tk.Entry(self.root, width=ENTRY_WIDTH)
        self.rotate_center_x_entry.place(relx=VERTICAL_LEVEL_2, rely=0.20)

        self.rotate_center_y_label = tk.Label(self.root, text='Y:', width=2)
        self.rotate_center_y_label.place(relx=0.242, rely=0.20)

        self.rotate_center_y_entry = tk.Entry(self.root, width=ENTRY_WIDTH)
        self.rotate_center_y_entry.place(relx=VERTICAL_LEVEL_3, rely=0.20)

        self.rotate_center_button = tk.Button(self.root, text="Повернуть", command=self.widget_rotate_center)
        self.rotate_center_button.place(relx=VERTICAL_LEVEL_4, rely=0.20, width=BUTTON_WIDTH)

    # ___CANVAS___

    def widget_canvas(self):
        self.canvas = tk.Canvas(self.root, bg='white', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
        self.canvas.pack(anchor='e')

    def canvas_clear(self):
        self.canvas.delete('all')

    # ___DRAW___

    def figure_draw(self):
        figure_link = self.figure.get()

        sign = 1
        if figure_link['kx'] < -pcs.EPS:
            sign = -1
        
        # ___rect___
        rect_lines = [
                        [figure_link['rect']['points'][0][:2:], figure_link['rect']['points'][3][:2:]],
                        [figure_link['rect']['points'][1][:2:], figure_link['rect']['points'][2][:2:]]
                    ]

        for line in rect_lines:
            object_id = self.figure_line_create(line[0], line[1])
            # self.IDs['rect']['points'].append(object_id)

        # __arc___
        for z in range(len(figure_link['rect']['ax'])):
            for i in range(len(figure_link['rect']['ax'][z]) - 1):
                object_id = self.figure_line_create(figure_link['rect']['ax'][z][i][:2:], figure_link['rect']['ax'][z][i + 1][:2:])
                # self.IDs['tower']['ellipse']['ax'].append(object_id)

        # ___wheels___
        for z in range(len(figure_link['wheels']['ax'])):
            for i in range(len(figure_link['wheels']['ax'][z]) - 1):
                object_id = self.figure_line_create(figure_link['wheels']['ax'][z][i][:2:], figure_link['wheels']['ax'][z][i + 1][:2:])
                # self.IDs['tower']['ellipse']['ax'].append(object_id)
        
        # ___tower___
        for i in range(len(figure_link['tower']['points']) - 1):
            object_id = self.figure_line_create(figure_link['tower']['points'][i][:2:], figure_link['tower']['points'][i + 1][:2:])
            # self.IDs['tower']['points'].append(object_id)

        # ___tower_ellipse___
        for i in range(len(figure_link['tower']['ellipse']['ax']) - 1):
            object_id = self.figure_line_create(figure_link['tower']['ellipse']['ax'][i][:2:], figure_link['tower']['ellipse']['ax'][i + 1][:2:])
            # self.IDs['tower']['ellipse']['ax'].append(object_id)

        # ___tube___
        for i in range(len(figure_link['tube']['points']) - 1):
            object_id = self.figure_line_create(figure_link['tube']['points'][i][:2:], figure_link['tube']['points'][i + 1][:2:])
            # self.IDs['tube']['points'].append(object_id)

        pts = [[figure_link['center'][0] - 5, figure_link['center'][1] + 5],
                [figure_link['center'][0] + 5, figure_link['center'][1] - 5]]
        object_id = self.figure_circle_create(*pts)
        
        object_id = self.canvas.create_text(*figure_link['center'][:2:], text=f"({figure_link['center'][0]:.3f}, {figure_link['center'][1]:.3f})")

    def figure_line_create(self, p1: list, p2: list):
        object_id = self.canvas.create_line(*p1, *p2, fill=FIGURE_COLOR, width=FIGURE_BORDER_WIDTH)
        
        return object_id

    def figure_arc_create(self, p_left_up: list, p_right_down: list, angle: float):
        object_id = self.canvas.create_arc(*p_left_up, *p_right_down, start=angle, extent=180, style='arc', outline=FIGURE_COLOR, width=FIGURE_BORDER_WIDTH)
        
        return object_id

    def figure_circle_create(self, p_left_up: list, p_right_down: list):
        object_id = self.canvas.create_oval(*p_left_up, *p_right_down, outline=FIGURE_POINT_COLOR, width=FIGURE_BORDER_WIDTH)
        
        return object_id

    # ___EVENT___

    def figure_event(self, event: str, **kwargs):
        match event:
            case 'move':
                self.figure.move(kwargs['x'], kwargs['y'])

                self.canvas_clear()
                self.figure_draw()
            
            case 'scale':
                self.figure.scale(kwargs['kx'], kwargs['ky'], kwargs['x'], kwargs['y'])

                self.canvas_clear()
                self.figure_draw()
            
            case 'rotate':
                self.figure.rotate(kwargs['angle'])

                self.canvas_clear()
                self.figure_draw()
            case 'default':
                self.action_stack.stack_clear()
                self.figure.default()
                self.figure.move(pcs.DEFAULT_CENTER_X, pcs.DEFAULT_CENTER_Y) # Смещаем к центру холста canvas

                self.canvas_clear()
                self.figure_draw()
            case 'rotate center':
                self.figure.rotate_center(kwargs['angle'], kwargs['x'], kwargs['y'])

                self.canvas_clear()
                self.figure_draw()


