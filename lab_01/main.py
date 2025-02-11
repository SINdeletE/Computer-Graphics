import tkinter as tk

MAIN_WIDTH = 700
MAIN_HEIGHT = 500

BUTTON_WIDTH = 15
BUTTON_HEIGHT = 1

ENTRY_WIDTH = 10
ENTRY_HEIGHT = 1

class MainApplication:
    def widgets_result_msg(self):
        self.restxt = tk.Entry(width = 30)
        self.restxt.insert(0, "Результаты действий")
        self.restxt.place(relx = 20 / MAIN_WIDTH, rely = 450 / MAIN_HEIGHT)

    def widgets_points_add(self):
        self.addbutton = tk.Button(text="Добавить точку", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        self.addbutton.place(relx = 180 / MAIN_WIDTH, rely = 20 / MAIN_HEIGHT)

        self.addentry_x = tk.Entry(textvariable="X", width=ENTRY_WIDTH)
        self.addentry_x.insert(0, "X")
        self.addentry_x.place(relx = 20 / MAIN_WIDTH, rely = 20 / MAIN_HEIGHT)

        self.addentry_y = tk.Entry(textvariable="Y", width=ENTRY_WIDTH)
        self.addentry_y.insert(0, "Y")
        self.addentry_y.place(relx = 100 / MAIN_WIDTH, rely = 20 / MAIN_HEIGHT)

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Лабораторная работа №1")
        self.root.geometry(f"{MAIN_WIDTH}x{MAIN_HEIGHT}")

        self.widgets_result_msg()
        self.widgets_points_add()

        self.root.mainloop()

if __name__ == '__main__':
    app = MainApplication()
