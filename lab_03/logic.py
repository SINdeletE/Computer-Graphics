import numpy
from typing import Type
from PIL import ImageDraw

EPS = 1e-8

ERR_COLOR = 1
ERR_RESOLUTION = 2

def resolution_check(x0, y0, resolution: list):
    width = resolution[0]
    height = resolution[1]

    return abs(x0) - width > EPS or abs(y0) - height > EPS

def resolution_raw(x0, y0, resolution: list):
    width = resolution[0]
    height = resolution[1]

    return abs(abs(x0) - width) < EPS or abs(abs(y0) - height) < EPS

def DrawDDA(DrawModule: Type[ImageDraw.ImageDraw], x0, y0, x1, y1, color, resolution: list):
    if color is None: return ERR_COLOR

    width = resolution[0]
    height = resolution[1]
    if resolution_check(x0, y0, resolution) and resolution_check(x1, y1, resolution): 
        return ERR_RESOLUTION

    L = max(abs(y1 - y0), abs(x1 - x0)) + 1
    x = x0
    y = y0
    dx = (x1 - x0) / L
    dy = (y1 - y0) / L

    flag = 1
    i = 0
    while (flag and i < int(L)):
        if resolution_check(x + dx, y + dy, resolution):
            color = 'red'
            flag = 0

        DrawModule.point((round(x), round(y)), color)

        x += dx
        y += dy
        i += 1

    return 0

def DrawBRESENHAM(DrawModule: Type[ImageDraw.ImageDraw], x0, y0, x1, y1, color, resolution: list):
    if color is None: return ERR_COLOR

    width = resolution[0]
    height = resolution[1]
    if resolution_check(x0, y0, resolution) and resolution_check(x1, y1, resolution): 
        return ERR_RESOLUTION
    
    flag = resolution_check(x0, y0, resolution) or resolution_check(x1, y1, resolution)
    
    x0 = round(x0)
    y0 = round(y0)
    x1 = round(x1)
    y1 = round(y1)

    k = (y1 - y0) / (x1 - x0)
    abs_k = abs(k)
    sign = k / abs(k)
    error = 0.0
    
    y = y0
    for x in range(x0, x1 + 1):
        error += abs_k

        DrawModule.point((round(x), round(y)), color)
        while not(resolution_raw(x, y, resolution)) and error - 1.0 > EPS:
            y += sign

            DrawModule.point((round(x), round(y)), color)

            error -= 1.0
        
        if flag and resolution_raw(x, y, resolution):
            color = 'red'
            DrawModule.point((round(x), round(y)), color)

            break
    
    return 0


def DrawLIB(DrawModule: Type[ImageDraw.ImageDraw], x0, y0, x1, y1, color, resolution: list):
    if color is None: return ERR_COLOR

    width = resolution[0]
    height = resolution[1]
    if resolution_check(x0, y0, resolution) and resolution_check(x1, y1, resolution): 
        return ERR_RESOLUTION
    
    DrawModule.line((x0, y0, x1, y1), fill=color, width=1)

