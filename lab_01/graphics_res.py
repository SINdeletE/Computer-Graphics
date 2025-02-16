import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import matplotlib.lines as pltlines
import processing as pcs

TRIANGLE_COLOR = "blue"
CIRCLE_COLOR = "red"
POINTS_COLOR = "green"

RADIUS_SCALE = 1.1

RESULT_WIDTH = 200
RESULT_HEIGHT = 200
RESULT_DELTA = 5

class ResultWindow:
    def labels_create(self, points: list):
        self.label_1 = ttk.Label(self.res_root, text="Треугольник был найден!")
        self.label_1.pack(anchor="center", expand=1)

        self.label_2 = ttk.Label(self.res_root, text="Точки:")
        self.label_2.pack(anchor="center", expand=1)

        self.label_p1 = ttk.Label(self.res_root, text=f"{points[0]}")
        self.label_p1.pack(anchor="center", expand=1)

        self.label_p2 = ttk.Label(self.res_root, text=f"{points[1]}")
        self.label_p2.pack(anchor="center", expand=1)

        self.label_p3 = ttk.Label(self.res_root, text=f"{points[2]}")
        self.label_p3.pack(anchor="center", expand=1)

    def __init__(self, points: list) -> None:
        self.res_root = tk.Tk()
        self.res_root.title("Результаты вычислений")
        self.res_root.geometry(f"{RESULT_WIDTH}x{RESULT_HEIGHT}")

        self.labels_create(points)

class GraphicsSolution:
    def graphics_triangle_draw(self, points: list):
        ax = plt.gca()

        for i in range(len(points) - 1):
            for j in range(i + 1, len(points)):
                line = pltlines.Line2D([points[i][0], points[j][0]], [points[i][1], points[j][1]], color=TRIANGLE_COLOR)

                ax.add_line(line)
    
    def graphics_points_draw(self, points: list):
        for p in points:
            plt.scatter(p[0], p[1], label=f"{p}", color=POINTS_COLOR)
            plt.text(p[0], p[1], f'({p[0]:.2g}, {p[1]:.2g})', fontsize=10, ha='right')
    
    def graphics_circle_draw(self, center: list, radius: float):
        ax = plt.gca()

        circle = plt.Circle(center, radius, color=CIRCLE_COLOR, fill=False)
        ax.add_patch(circle)
    
    def graphics_scale(self, points: list, center: list, radius: float):
        ax = plt.gca()

        # min_x = min(p[0] for p in points)
        # max_x = max(p[0] for p in points)

        # min_y = min(p[1] for p in points)
        # max_y = max(p[1] for p in points)

        # delta = max(max_x - min_x, max_y - min_y)

        # ax.set_xlim(min_x, min_x + delta)
        # ax.set_ylim(min_y, min_y + delta)

        ax.set_xlim(center[0] - radius * RADIUS_SCALE, center[0] + radius * RADIUS_SCALE)
        ax.set_ylim(center[1] - radius * RADIUS_SCALE, center[1] + radius * RADIUS_SCALE)


    def __init__(self, points: list):

        fig = plt.gcf()
        fig.set_size_inches(18, 18)

        plt.title("Результат работы программы")
        plt.xlabel("x") 
        plt.ylabel("y") 
        plt.grid(which='major') # включение отображение сетки

        circumcircle_center, R = pcs.triangle_circumcircle(points)

        self.graphics_triangle_draw(points)
        self.graphics_points_draw(points)
        self.graphics_circle_draw(circumcircle_center, R)
        self.graphics_scale(points, circumcircle_center, R)

        res = ResultWindow(points)

        plt.show()
