import logic
import matplotlib.pyplot as plt
import numpy

from math import *

def stat_func_get(func, L):
    x0 = 0
    y0 = 0

    angles = list(numpy.linspace(0, pi / 2, 90 + 1))
    count_array = [0 for i in range(len(angles))]

    for i in range(len(angles)):
        count_array[i] = func(x0, y0, x0 + L * cos(angles[i]), y0 + L * sin(angles[i]))
    
    return angles, count_array

class FloorsStatistics:
    def __init__(self, L):
        self.funcs = [
                        [logic.CountDDA, "ЦДА"],
                        [logic.CountBRESENHAM_INT, "Брезенхем для целых чисел"],
                        [logic.CountWU, "Алгоритм Ву"],
                        [logic.CountBRESENHAM, "Брезенхем для действительных чисел"],
                        [logic.CountBRESENHAM_SMOOTH, "Брезенхем с устранением ступенчатости"]
                    ]
        
        self.L = L

    def get(self):
        for i in range(len(self.funcs)):
            x, y = stat_func_get(self.funcs[i][0], self.L)
            
            plt.subplot(1, 5, i + 1)
            plt.plot(x, y, 'o')
            plt.title(self.funcs[i][1])
        
        plt.suptitle("Измерение ступенчатости")
        plt.show()