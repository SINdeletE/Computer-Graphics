import matplotlib.pyplot as plt
import matplotlib.lines as pltlines
import processing as pcs

EPS = 1e-8

TRIANGLE_COLOR = "blue"

class GraphicsSolution:
    


    def graphics_triangle_draw(self, points: list):
        ax = plt.gca()

        for i in range(len(points) - 1):
            for j in range(i + 1, len(points)):
                line = pltlines.Line2D([points[i][0], points[j][0]], [points[i][1], points[j][1]], color=TRIANGLE_COLOR)

                ax.add_line(line)
        
        min_x = min(p[0] for p in points)
        max_x = max(p[0] for p in points)

        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)

        ax.set_xlim(min_x - 1, max_x + 1)
        ax.set_ylim(min_y - 1, max_y + 1)
    
    def graphics_points_draw(self, points: list):
        for p in points:
            plt.scatter(p[0], p[1], label=f"{p}")
            plt.text(p[0], p[1], f'({p[0]:.2g}, {p[1]:.2g})', fontsize=10, ha='right')

    def __init__(self, points: list):
        plt.title("Результат работы программы")
        plt.xlabel("x") 
        plt.ylabel("y") 
        plt.grid() # включение отображение сетки

        self.graphics_triangle_draw(points)
        self.graphics_points_draw(points)

        plt.show()