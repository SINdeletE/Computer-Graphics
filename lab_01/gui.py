import tkinter as tk
from tkinter import ttk
import graphics_res as gres
import processing as pcs

WIDGET_SHIFT = 3

MAIN_WIDTH = 1920
MAIN_HEIGHT = 1080

BUTTON_WIDTH = 15
BUTTON_HEIGHT = 1

ENTRY_WIDTH = 10
ENTRY_HEIGHT = 1

TASK_WIDTH = 700
TASK_HEIGHT = 300

TABLE_N_ID = "№"
TABLE_X_ID = "X"
TABLE_Y_ID = "Y"

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
    def task_label_create(self):
        task = "26. На плоскости дано множество точек. Найти такой треугольник с вершинами в этих точках, у которого разность площадей описанного круга и треугольника максимальны"

        self.task_label = ttk.Label(self.task_root, text=task, wraplength=TASK_WIDTH)
        self.task_label.pack(anchor="center", expand=1)

    def __init__(self) -> None:
        self.task_root = tk.Tk()
        self.task_root.title("Задание")
        self.task_root.geometry(f"{TASK_WIDTH}x{TASK_HEIGHT}")

        self.task_label_create()

class MainApplication:
    def task_window_create(self):
        self.task_window = TaskWindow()
    
    def widgets_task(self):
        self.task_button = tk.Button(text="Условие задачи", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command = self.task_window_create)
        self.task_button.place(relx = 300 * WIDGET_SHIFT / MAIN_WIDTH, rely = 20 * WIDGET_SHIFT / MAIN_HEIGHT)

    # TABLE TABLE TABLE TABLE TABLE TABLE TABLE TABLE TABLE

    def widgets_treeview(self):
        self.columns = (TABLE_N_ID, TABLE_X_ID, TABLE_Y_ID)
        self.IDs = list() # Совпадают с "№"
        self.IDs_current = 0

        # self.style = ttk.Style()
        # self.style.configure("Treeview", font=("Arial", 12))

        self.table = ttk.Treeview(columns = self.columns, show="headings", height = 22)
        self.table.place(relx = 20 * WIDGET_SHIFT / MAIN_WIDTH, rely = 100 * WIDGET_SHIFT / MAIN_HEIGHT)

        self.table.heading(TABLE_N_ID, text = "№")
        self.table.heading(TABLE_X_ID, text = "X")
        self.table.heading(TABLE_Y_ID, text = "Y")

    def is_treeview_element(self, x: float, y: float) -> bool:
        for stroke in self.table.get_children(""):
            item = self.table.item(stroke)

            if abs(float(item['values'][1]) - x) < pcs.EPS and abs(float(item['values'][2]) - y) < pcs.EPS :
                return True
        
        return False
    
    def treeview_all_elements(self):
        numbers = []
        points = []

        for stroke in self.table.get_children(""):
            item = self.table.item(stroke)

            data = item['values']
            data = [data[0]] + list(map(float, data[1::])) # Перевод координат точек во float

            points.append(data)
        
        return points

    def treeview_add(self, x: float, y: float) -> bool:
        self.table.insert("", tk.END, self.IDs_current, values = (self.IDs_current + 1, x, y))
        self.IDs.append(self.IDs_current)

        self.IDs_current += 1

    def treeview_delete(self, i: int) -> bool:
        if i not in self.IDs:
            return False
        
        self.table.delete(i)

        id_index = self.IDs.index(i)

        self.IDs = self.IDs[:id_index:] + self.IDs[id_index + 1:len(self.IDs):]

        return True
    
    def treeview_change(self, i: int, x: float, y: float):
        self.table.set(i, TABLE_X_ID, x)
        self.table.set(i, TABLE_Y_ID, y)

        return True
    
    def treeview_delete_all(self):
        for i in range(len(self.IDs) - 1, -1, -1):
            self.treeview_delete(self.IDs[i])
        
        return True

    # TABLE TABLE TABLE TABLE TABLE TABLE TABLE TABLE TABLE

    # MSG MSG MSG MSG MSG MSG MSG MSG MSG MSG MSG MSG MSG

    def widgets_result_msg(self):
        self.reslabel = tk.Label(text="Результаты действий")
        self.reslabel.place(relx = 20 * WIDGET_SHIFT / MAIN_WIDTH, rely = 290 * WIDGET_SHIFT / MAIN_HEIGHT)

        self.restxt = tk.Entry(width = 100)
        self.restxt.place(relx = 20 * WIDGET_SHIFT / MAIN_WIDTH, rely = 300 * WIDGET_SHIFT / MAIN_HEIGHT)

    def res_msg(self, txt: str):
        self.restxt.delete(0, tk.END)
        self.restxt.insert(0, txt)

    # MSG MSG MSG MSG MSG MSG MSG MSG MSG MSG MSG MSG MSG

    # DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE

    def point_delete(self) -> bool:
        i = 0

        entered = self.delete_entry_n.get()
        if not(is_int(entered)):
            self.res_msg("Неправильное значение №")

            return False

        i = int(entered) - 1

        if not(len(self.IDs)):
            self.res_msg("Число точек равно нулю")

            return False
        
        if not(self.treeview_delete(i)):
            self.res_msg("Нет точки с таким номером")

            return False
        
        self.res_msg("Точка успешно удалена")

        return True

    def points_delete_all(self) -> bool:
        self.treeview_delete_all()

        self.res_msg("Все точки в таблице были удалены")

        return False

    def widgets_points_delete(self):
        self.delete_button = tk.Button(text="Удалить точку", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command = self.point_delete)
        self.delete_button.place(relx = 180 * WIDGET_SHIFT / MAIN_WIDTH, rely = 40 * WIDGET_SHIFT / MAIN_HEIGHT)

        self.deletelabel_n = tk.Label(text="№")
        self.deletelabel_n.place(relx = 10 * WIDGET_SHIFT / MAIN_WIDTH, rely = 40 * WIDGET_SHIFT / MAIN_HEIGHT)

        self.delete_entry_n = tk.Entry(textvariable="№", width=ENTRY_WIDTH)
        self.delete_entry_n.place(relx = 20 * WIDGET_SHIFT / MAIN_WIDTH, rely = 40 * WIDGET_SHIFT / MAIN_HEIGHT)

    def widgets_points_delete_all(self):
        self.delete_all_button = tk.Button(text="Удалить все точки", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command = self.points_delete_all)
        self.delete_all_button.place(relx = 20 * WIDGET_SHIFT / MAIN_WIDTH, rely = 80 * WIDGET_SHIFT / MAIN_HEIGHT)

    # DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE

    # ADD ADD ADD ADD ADD ADD ADD ADD ADD ADD ADD ADD ADD ADD ADD

    def point_add(self) -> bool:
        x = 0
        y = 0

        entered = self.addentry_x.get()
        if not(is_float(entered)):
            self.res_msg("Неправильное значение X")

            return False

        x = float(entered)
        
        entered = self.addentry_y.get()
        if not(is_float(entered)):
            self.res_msg("Неправильное значение Y")

            return False
        
        y = float(entered)

        if self.is_treeview_element(x, y):
            self.res_msg("Такая точка уже есть")

            return False
        
        self.treeview_add(x, y)

        self.res_msg("Точка успешно добавлена")

        return True

    def widgets_points_add(self):
        self.addbutton = tk.Button(text="Добавить точку", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command = self.point_add)
        self.addbutton.place(relx = 180 * WIDGET_SHIFT / MAIN_WIDTH, rely = 20 * WIDGET_SHIFT / MAIN_HEIGHT)

        self.addlabel_x = tk.Label(text="X")
        self.addlabel_x.place(relx = 10 * WIDGET_SHIFT / MAIN_WIDTH, rely = 20 * WIDGET_SHIFT / MAIN_HEIGHT)

        self.addentry_x = tk.Entry(textvariable="X", width=ENTRY_WIDTH)
        self.addentry_x.place(relx = 20 * WIDGET_SHIFT / MAIN_WIDTH, rely = 20 * WIDGET_SHIFT / MAIN_HEIGHT)

        self.addlabel_y = tk.Label(text="Y")
        self.addlabel_y.place(relx = 90 * WIDGET_SHIFT / MAIN_WIDTH, rely = 20 * WIDGET_SHIFT / MAIN_HEIGHT)

        self.addentry_y = tk.Entry(textvariable="Y", width=ENTRY_WIDTH)
        self.addentry_y.place(relx = 100 * WIDGET_SHIFT / MAIN_WIDTH, rely = 20 * WIDGET_SHIFT / MAIN_HEIGHT)
    
    # ADD ADD ADD ADD ADD ADD ADD ADD ADD ADD ADD ADD ADD ADD ADD

    def point_change(self):
        x = 0
        y = 0

        i = 0

        entered = self.changeentry_n.get()
        if not(is_int(entered)):
            self.res_msg("Неправильное значение №")

            return False

        i = int(entered) - 1

        if not(len(self.IDs)):
            self.res_msg("Число точек равно нулю")

            return False

        if i not in self.IDs:
            self.res_msg("Нет точки с таким номером")

            return False

        entered = self.changeentry_x.get()
        if not(is_float(entered)):
            self.res_msg("Неправильное значение X")

            return False

        x = float(entered)
        
        entered = self.changeentry_y.get()
        if not(is_float(entered)):
            self.res_msg("Неправильное значение Y")

            return False
        
        y = float(entered)

        if self.is_treeview_element(x, y):
            self.res_msg("Такая точка уже есть")

            return False
        
        self.treeview_change(i, x, y)

        self.res_msg("Точка успешно изменена")

        return True

    def widgets_points_change(self):
        self.changebutton = tk.Button(text="Изменить точку", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command = self.point_change)
        self.changebutton.place(relx = 260 * WIDGET_SHIFT / MAIN_WIDTH, rely = 60 * WIDGET_SHIFT / MAIN_HEIGHT)

        self.changelabel_n = tk.Label(text="№")
        self.changelabel_n.place(relx = 10 * WIDGET_SHIFT / MAIN_WIDTH, rely = 60 * WIDGET_SHIFT / MAIN_HEIGHT)

        self.changeentry_n = tk.Entry(textvariable="№n", width=ENTRY_WIDTH)
        self.changeentry_n.place(relx = 20 * WIDGET_SHIFT / MAIN_WIDTH, rely = 60 * WIDGET_SHIFT / MAIN_HEIGHT)

        self.changelabel_x = tk.Label(text="X")
        self.changelabel_x.place(relx = 90 * WIDGET_SHIFT / MAIN_WIDTH, rely = 60 * WIDGET_SHIFT / MAIN_HEIGHT)

        self.changeentry_x = tk.Entry(textvariable="Xx", width=ENTRY_WIDTH)
        self.changeentry_x.place(relx = 100 * WIDGET_SHIFT / MAIN_WIDTH, rely = 60 * WIDGET_SHIFT / MAIN_HEIGHT)

        self.changelabel_y = tk.Label(text="Y")
        self.changelabel_y.place(relx = 170 * WIDGET_SHIFT / MAIN_WIDTH, rely = 60 * WIDGET_SHIFT / MAIN_HEIGHT)

        self.changeentry_y = tk.Entry(textvariable="Yy", width=ENTRY_WIDTH)
        self.changeentry_y.place(relx = 180 * WIDGET_SHIFT / MAIN_WIDTH, rely = 60 * WIDGET_SHIFT / MAIN_HEIGHT)

    def calculate(self):
        data = self.treeview_all_elements()
        points = list(map(lambda item: item[1::], data))
        numbers = list(map(lambda item: item[0], data))

        code, triangle_points, triangle_numbers = pcs.triangle_parse(points, numbers)
        match code:
            case pcs.PARSE_ERROR_POINTS_COUNT:
                self.res_msg("Недостаточно точек для создания треугольника")

                return False
            case pcs.PARSE_ERROR_NO_VALID_TRIANGLE:
                self.res_msg("Все точки лежат на одной прямой")

                return False

        result_window = gres.GraphicsSolution(triangle_points, triangle_numbers)

        self.res_msg("Найден подходящий треугольник")

        return True

    def widgets_calculate(self):
        self.addbutton = tk.Button(text="Получить результат", width=BUTTON_WIDTH + 10, height=BUTTON_HEIGHT, command = self.calculate)
        self.addbutton.place(relx = 20 * WIDGET_SHIFT / MAIN_WIDTH, rely = 320 * WIDGET_SHIFT / MAIN_HEIGHT)

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Лабораторная работа №1")
        self.root.geometry(f"{MAIN_WIDTH}x{MAIN_HEIGHT}")

        self.widgets_task()
        self.widgets_treeview()
        self.widgets_result_msg()
        self.widgets_points_add()
        self.widgets_points_delete()
        self.widgets_points_delete_all()
        self.widgets_points_change()
        self.widgets_calculate()

        self.root.mainloop()

