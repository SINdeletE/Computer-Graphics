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

class MainApplication:
    # TABLE TABLE TABLE TABLE TABLE TABLE TABLE TABLE TABLE

    def widgets_treeview(self):
        self.columns = (TABLE_N_ID, TABLE_X_ID, TABLE_Y_ID)
        self.IDs = list() # Совпадают с "№"
        self.IDs_current = 0

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
        points = []

        for stroke in self.table.get_children(""):
            item = self.table.item(stroke)
            data = list(map(float, item["values"][1::]))

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

    # TABLE TABLE TABLE TABLE TABLE TABLE TABLE TABLE TABLE

    # MSG MSG MSG MSG MSG MSG MSG MSG MSG MSG MSG MSG MSG

    def widgets_result_msg(self):
        self.restxt = tk.Entry(width = 100)
        self.restxt.insert(0, "Результаты действий")
        self.restxt.place(relx = 20 * WIDGET_SHIFT / MAIN_WIDTH, rely = 300 * WIDGET_SHIFT / MAIN_HEIGHT)

    def res_msg(self, txt: str):
        self.restxt.delete(0, tk.END)
        self.restxt.insert(0, txt)

    # MSG MSG MSG MSG MSG MSG MSG MSG MSG MSG MSG MSG MSG

    # DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE

    def point_delete(self) -> bool:
        i = 0

        entered = self.deleteentry_n.get()
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

    def widgets_points_delete(self):
        self.addbutton = tk.Button(text="Удалить точку", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command = self.point_delete)
        self.addbutton.place(relx = 180 * WIDGET_SHIFT / MAIN_WIDTH, rely = 40 * WIDGET_SHIFT / MAIN_HEIGHT)

        self.deleteentry_n = tk.Entry(textvariable="№", width=ENTRY_WIDTH)
        self.deleteentry_n.insert(0, "№")
        self.deleteentry_n.place(relx = 20 * WIDGET_SHIFT / MAIN_WIDTH, rely = 40 * WIDGET_SHIFT / MAIN_HEIGHT)

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

        self.addentry_x = tk.Entry(textvariable="X", width=ENTRY_WIDTH)
        self.addentry_x.insert(0, "X")
        self.addentry_x.place(relx = 20 * WIDGET_SHIFT / MAIN_WIDTH, rely = 20 * WIDGET_SHIFT / MAIN_HEIGHT)

        self.addentry_y = tk.Entry(textvariable="Y", width=ENTRY_WIDTH)
        self.addentry_y.insert(0, "Y")
        self.addentry_y.place(relx = 100 * WIDGET_SHIFT / MAIN_WIDTH, rely = 20 * WIDGET_SHIFT / MAIN_HEIGHT)
    
    # ADD ADD ADD ADD ADD ADD ADD ADD ADD ADD ADD ADD ADD ADD ADD

    def calculate(self):
        points = self.treeview_all_elements()

        code, triangle_points = pcs.triangle_parse(points)
        match code:
            case pcs.PARSE_ERROR_POINTS_COUNT:
                self.res_msg("Недостаточно точек для создания треугольника")

                return False
            case pcs.PARSE_ERROR_NO_VALID_TRIANGLE:
                self.res_msg("Нет точек для создания треугольника")

                return False

        result_window = gres.GraphicsSolution(triangle_points)

        self.res_msg("Найден подходящий треугольник")

        return True

    def widgets_calculate(self):
        self.addbutton = tk.Button(text="Получить результат", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command = self.calculate)
        self.addbutton.place(relx = 20 * WIDGET_SHIFT / MAIN_WIDTH, rely = 320 * WIDGET_SHIFT / MAIN_HEIGHT)

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Лабораторная работа №1")
        self.root.geometry(f"{MAIN_WIDTH}x{MAIN_HEIGHT}")

        self.widgets_treeview()
        self.widgets_result_msg()
        self.widgets_points_add()
        self.widgets_points_delete()
        self.widgets_calculate()

        self.root.mainloop()

