from math import *
from typing import Type
from PIL import ImageDraw

EPS = 1e-8

ERR_COLOR = 1
ERR_RESOLUTION = 2

RED = "#d90000"

def resolution_check(x0, y0, resolution: list):
    width = resolution[0]
    height = resolution[1]

    return abs(x0) - width > EPS or abs(y0) - height > EPS

def resolution_raw(x0, y0, resolution: list):
    width = resolution[0]
    height = resolution[1]

    return abs(abs(x0) - width) < EPS or abs(abs(y0) - height) < EPS

def draw_point(DrawModule, xy, color):
    red = int(color[1:3:], 16)
    green = int(color[3:5:], 16)
    blue = int(color[5:7:], 16)

    DrawModule.putpixel(xy, (red, green, blue, 255))

def draw_point_alpha(DrawModule, xy, color, alpha):
    red = int(color[1:3:], 16)
    green = int(color[3:5:], 16)
    blue = int(color[5:7:], 16)

    DrawModule.putpixel(xy, (red, green, blue, int(alpha * 255)))

def xy_swap_by_x(x0, y0, x1, y1):
    if x0 - x1 > EPS:
        return x1, y1, x0, y0
    
    return x0, y0, x1, y1
    
def xy_swap_by_y(x0, y0, x1, y1):
    if y0 - y1 > EPS:
        return x1, y1, x0, y0

    return x0, y0, x1, y1
    
def sign_num(k: float):
    if k >= EPS:
        return 1
    elif abs(k) < EPS:
        return 0

    return -1

def DrawDDA(DrawModule, x0, y0, x1, y1, color, resolution: list):
    if color is None: return ERR_COLOR

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
            color = RED
            flag = 0

        draw_point(DrawModule, (round(x), round(y)), color)

        x += dx
        y += dy
        i += 1

    draw_point(DrawModule, (round(x), round(y)), color)

    return 0

def DrawBRESENHAM(DrawModule, x0, y0, x1, y1, color, resolution: list):
    if color is None: return ERR_COLOR

    x0, y0, x1, y1 = xy_swap_by_x(x0, y0, x1, y1)

    if resolution_check(x0, y0, resolution) and resolution_check(x1, y1, resolution): 
        return ERR_RESOLUTION
    
    flag = resolution_check(x0, y0, resolution) or resolution_check(x1, y1, resolution)
    
    x0 = round(x0)
    y0 = round(y0)
    x1 = round(x1)
    y1 = round(y1)

    try:
        k = (y1 - y0) / (x1 - x0)
    except ZeroDivisionError:
        k = sign_num(y1 - y0) * inf
    
    abs_k = abs(k)
    sign = sign_num(k)
    error = 0.0
    
    draw_point(DrawModule, (round(x0), round(y0)), color)

    y = y0
    for x in range(x0, x1 + 1):
        error += abs_k

        if error - 1.0 <= EPS:
            draw_point(DrawModule, (round(x), round(y)), color)
        else:
            while y != y1 and not(resolution_raw(x, y, resolution)) and error - 1.0 > EPS:
                y += sign

                draw_point(DrawModule, (round(x), round(y)), color)

                error -= 1.0
            
            if flag and resolution_raw(x, y, resolution):
                color = RED

            draw_point(DrawModule, (round(x), round(y)), color)
    return 0

def DrawWU(DrawModule, x0, y0, x1, y1, color, resolution: list):
    if color is None: return ERR_COLOR

    if resolution_check(x0, y0, resolution) and resolution_check(x1, y1, resolution): 
        return ERR_RESOLUTION
    
    x0 = round(x0)
    y0 = round(y0)
    x1 = round(x1)
    y1 = round(y1)

    try:
        k = (y1 - y0) / (x1 - x0)
    except ZeroDivisionError:
        k = sign_num(y1 - y0) * inf

    x = x0
    y = y0
    if x1 - x0 >= y1 - y0:
        x0, y0, x1, y1 = xy_swap_by_x(x0, y0, x1, y1)

        x = x0
        y = y0
        while x <= x1:
            y_main = ceil(y)
            y_delta = floor(y)

            alpha_y_delta = abs(y - y_main)
            alpha_y = 1.0 - alpha_y_delta

            if y_main == y_delta:
                draw_point(DrawModule, (x, y_main), color)
            else:
                draw_point_alpha(DrawModule, (x, y_delta), color, alpha_y_delta)
                draw_point_alpha(DrawModule, (x, y_main), color, alpha_y)

            x += 1
            y += k
    else:
        x0, y0, x1, y1 = xy_swap_by_y(x0, y0, x1, y1)

        x = x0
        y = y0
        while y <= y1:
            x_main = ceil(x)
            x_delta = floor(x)

            alpha_x_delta = abs(x - x_main)
            alpha_x = 1 - alpha_x_delta

            if x_main == x_delta:
                draw_point(DrawModule, (x_main, y), color)
            else:
                draw_point_alpha(DrawModule, (x_delta, y), color, alpha_x_delta)
                draw_point_alpha(DrawModule, (x_main, y), color, alpha_x)

            y += 1
            x += 1 / k
    return 0
        
def DrawBRESENHAM_SMOOTH(DrawModule, x0, y0, x1, y1, color, resolution: list):
    if color is None: return ERR_COLOR

    if resolution_check(x0, y0, resolution) and resolution_check(x1, y1, resolution): 
        return ERR_RESOLUTION
    
    x0 = round(x0)
    y0 = round(y0)
    x1 = round(x1)
    y1 = round(y1)
    
    x0, y0, x1, y1 = xy_swap_by_x(x0, y0, x1, y1)

    dx = x1 - x0
    dy = y1 - y0
    SX = sign_num(dx)
    SY = sign_num(dy)

    k = abs(dx / dy)
    if k - 1 <= EPS:
        flag = False
    else:
        dx, dy = dy, dx

        k = 1 / k
        flag = True
    
    error = 0.5
    W = 255 - k

    x = x0
    y = y0
    draw_point(DrawModule, (x, y), color)

    for i in range(dx + 1):
        if error < W:
            if flag:
                x += SX
            else:
                y += SY
            
            error += k
        else:
            x += SX
            y += SY

            error -= W
        
        draw_point_alpha(DrawModule, (x, y), color, error)

def DrawLIB(DrawModule, x0, y0, x1, y1, color, resolution: list):
    if color is None: return ERR_COLOR

    if resolution_check(x0, y0, resolution) and resolution_check(x1, y1, resolution): 
        return ERR_RESOLUTION
    
    DrawModule.line((x0, y0, x1, y1), fill=color, width=1)

