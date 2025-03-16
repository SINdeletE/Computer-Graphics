import tkinter as tk

import PIL
from PIL import ImageTk, Image, ImageDraw

MAIN_HEIGHT = 1920
MAIN_WIDTH = 3000

CANVAS_HEIGHT = MAIN_HEIGHT
CANVAS_WIDTH = MAIN_HEIGHT

class MainWindow:
    def widget_canvas(self):
        self.canvas = tk.Canvas(self.root, bg='white', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
        self.canvas.pack(anchor='w')

    def canvas_image(self):
        # Создаем новое изображение с зеленым фоном
        self.pilImage = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), "white")

        # Создаем объект ImageDraw для рисования на изображении
        self.draw = ImageDraw.Draw(self.pilImage)

    def canvas_clear(self):
        self.canvas_image()
        self.canvas_image_submit()

    def canvas_image_submit(self):
        # Преобразуем изображение в формат, который может быть использован в Tkinter
        self.image = ImageTk.PhotoImage(master=self.canvas, image=self.pilImage)  # Сохраняем ссылку на изображение

        # Отображаем изображение на Canvas
        self.canvas.create_image(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, image=self.image)

    def draw_line_pillow_lib(self, coords):
        # Рисуем линию на изображении
        self.draw.line(coords, fill=(128, 128, 128, 255), width=3)

        self.canvas_image_submit()

    def __init__(self, root):
        self.root = root
        self.root = tk.Tk()
        self.root.title("Лабораторная работа №3")
        self.root.geometry(f"{MAIN_WIDTH}x{MAIN_HEIGHT}")

        self.widget_canvas()
        self.canvas_image()

        self.draw_line_pillow_lib((1920, 200, 0, 20))
        self.draw_line_pillow_lib((800, 200, 0, 200))

        # self.canvas_clear()


