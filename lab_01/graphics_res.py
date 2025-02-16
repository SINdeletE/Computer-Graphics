import matplotlib.pyplot as plt
import matplotlib.lines as pltlines
import processing as pcs

TRIANGLE_COLOR = "blue"
CIRCLE_COLOR = "red"
POINTS_COLOR = "green"

RADIUS_SCALE = 1.1

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

        plt.show()