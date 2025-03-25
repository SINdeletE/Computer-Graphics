import logic
import matplotlib.pyplot as plt
import numpy
from PIL import ImageTk, Image, ImageDraw
from math import *

import time

DEFAULT_FONT = 20

ITERS = 30

def stat_func_get(func, L):
    x0 = 0
    y0 = 0

    angles = list(numpy.linspace(0, pi / 2, 90 + 1))
    count_array = [0 for i in range(len(angles))]

    for i in range(len(angles)):
        count_array[i] = func(x0, y0, x0 + L * cos(angles[i]), y0 + L * sin(angles[i]))
    
    return angles, count_array

def stat_time_get(func, x, y, L, n, color, resolution: list):
    DrawModule = None

    # Создаем новое изображение с зеленым фоном
    pilImage = Image.new("RGBA", (resolution[0], resolution[1]), 'white')

    # Создаем объект ImageDraw для рисования на изображении
    draw = ImageDraw.Draw(pilImage)

    DrawModule = pilImage
    if func == logic.DrawLIB:
        DrawModule = draw
    
    total_time = 0.0
    for i in range(ITERS):
        start = time.time()
        logic.SunDraw(DrawModule, func, x, y, L, n, color, resolution)
        total_time += time.time() - start
    
    return total_time / ITERS / 360

class FloorsStatistics:
    def __init__(self, L):
        self.funcs = [
                        [logic.CountDDA, "ЦДА"],
                        [logic.CountBRESENHAM_INT, "Брезенхем для целых чисел"],
                        [logic.CountWU, "Алгоритм Ву"],
                        [logic.CountBRESENHAM, "Брезенхем для действит."],
                        [logic.CountBRESENHAM_SMOOTH, "Брезенхем с устранением ступенчатости"]
                    ]
        
        self.L = L

    def get(self):
        for i in range(len(self.funcs)):
            x, y = stat_func_get(self.funcs[i][0], self.L)
            
            plt.subplot(1, 5, i + 1)
            plt.plot(x, y, 'o')
            plt.title(self.funcs[i][1], fontsize=DEFAULT_FONT)
        
        plt.suptitle("Измерение ступенчатости", fontsize=DEFAULT_FONT)
        plt.show()

class TimeStatistics:
    def __init__(self, x, y, L, n, color, resolution: list):
        self.funcs = [
                        [logic.DrawDDA, "ЦДА"],
                        [logic.DrawBRESENHAM_INT, "Брезенхем для целых чисел"],
                        [logic.DrawWU, "Алгоритм Ву"],
                        [logic.DrawBRESENHAM, "Брезенхем для действительных чисел"],
                        [logic.DrawBRESENHAM_SMOOTH, "Брезенхем с устранением ступенчатости"],
                        [logic.DrawLIB, "Библиотечная реализация"]
                    ]
        self.x = x
        self.y = y
        self.L = L
        self.n = n
        self.color = color
        self.resolution = resolution

    def get(self):
        self.times = [0 for i in range(len(self.funcs))]

        for i in range(len(self.funcs)):
            self.times[i] = stat_time_get(self.funcs[i][0], self.x, self.y, self.L, self.n, self.color, self.resolution)
        
        plt.bar(list(map(lambda elem: elem[1], self.funcs)), self.times)
        plt.title("Измерение времени (в секундах)", fontsize=DEFAULT_FONT)
        plt.show()