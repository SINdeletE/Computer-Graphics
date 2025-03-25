from math import *
from typing import Type
from PIL import ImageDraw
import numpy

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

    x0, y0, x1, y1 = xy_swap_by_x(x0, y0, x1, y1)

    if resolution_check(x0, y0, resolution) and resolution_check(x1, y1, resolution): 
        return ERR_RESOLUTION

    L = max(abs(y1 - y0), abs(x1 - x0)) + 1
    x = x0
    y = y0
    dx = (x1 - x0) / L
    dy = (y1 - y0) / L

    flag = 1
    i = 0
    while (flag and i - float(L) < -EPS):
        # if resolution_check(x + dx, y + dy, resolution):
        #     color = RED
        #     flag = 0
        try:
            draw_point(DrawModule, (round(x), round(y)), color)
        except Exception:
            pass

        x += dx
        y += dy
        i += 1

    try:
        draw_point(DrawModule, (round(x), round(y)), color)
    except Exception:
        pass

    return 0

def DrawBRESENHAM_INT(DrawModule, x0, y0, x1, y1, color, resolution: list):
    if color is None: return ERR_COLOR

    x0, y0, x1, y1 = xy_swap_by_x(x0, y0, x1, y1)

    if resolution_check(x0, y0, resolution) and resolution_check(x1, y1, resolution): 
        return ERR_RESOLUTION
    
    x0 = round(x0)
    y0 = round(y0)
    x1 = round(x1)
    y1 = round(y1)

    dx = x1 - x0
    dy = y1 - y0

    sign_y = sign_num(dy)
    
    error = 2 * dy * sign_y - dx

    y = y0
    for x in range(x0, x1 + 1): # Тут +1 убрал
        try:
            draw_point(DrawModule, (x, y), color)
        except Exception:
            pass

        while y != y1 and error - 1.0 > EPS:
            try:
                draw_point(DrawModule, (x, y), color)
            except Exception:
                pass

            y += sign_y
            if dx < -EPS or dx > EPS:
                error -= 2 * dx
            else:
                error -= 1
            
            # if flag and resolution_raw(x, y, resolution):
            #     color = RED
        
        error += 2 * dy * sign_y

    try:
        draw_point(DrawModule, (x1, y1), color)
    except Exception:
        pass

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
    
    try:
        draw_point(DrawModule, (round(x0), round(y0)), color)
    except Exception:
        pass

    y = y0
    for x in range(x0, x1 + 1):
        error += abs_k

        if error - 1.0 <= EPS:
            try:
                draw_point(DrawModule, (round(x), round(y)), color)
            except Exception:
                pass
        else:
            while y != y1 and error - 1.0 > EPS:
                y += sign

                try:
                    draw_point(DrawModule, (round(x), round(y)), color)
                except Exception:
                    pass

                error -= 1.0

            try:
                draw_point(DrawModule, (round(x), round(y)), color)
            except Exception:
                pass
    
    try:
        draw_point(DrawModule, (x1, y1), color)
    except Exception:
        pass

    return 0

def DrawWU(DrawModule, x0, y0, x1, y1, color, resolution: list):
    if color is None: return ERR_COLOR

    if resolution_check(x0, y0, resolution) and resolution_check(x1, y1, resolution): 
        return ERR_RESOLUTION
    
    x0 = round(x0)
    y0 = round(y0)
    x1 = round(x1)
    y1 = round(y1)

    x = x0
    y = y0
    if abs(x1 - x0) >= abs(y1 - y0):
        x0, y0, x1, y1 = xy_swap_by_x(x0, y0, x1, y1)

        try:
            k = (y1 - y0) / (x1 - x0)
        except ZeroDivisionError:
            k = sign_num(y1 - y0) * inf

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
                if alpha_y_delta - alpha_y > -EPS:
                    draw_point_alpha(DrawModule, (x, y_main), color, alpha_y)
                    draw_point_alpha(DrawModule, (x, y_delta), color, alpha_y_delta)
                else:
                    draw_point_alpha(DrawModule, (x, y_delta), color, alpha_y_delta)
                    draw_point_alpha(DrawModule, (x, y_main), color, alpha_y)


            x += 1
            y += k
    else:
        x0, y0, x1, y1 = xy_swap_by_y(x0, y0, x1, y1)

        try:
            k = (y1 - y0) / (x1 - x0)
        except ZeroDivisionError:
            k = sign_num(y1 - y0) * inf

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
                if alpha_x_delta - alpha_x > -EPS:
                    draw_point_alpha(DrawModule, (x_main, y), color, alpha_x)
                    draw_point_alpha(DrawModule, (x_delta, y), color, alpha_x_delta)
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
    
    dx = x1 - x0
    dy = y1 - y0

    if abs(dx) - abs(dy) > -EPS:
        x0, y0, x1, y1 = xy_swap_by_x(x0, y0, x1, y1)

        x = round(x0)
        y = round(y0)
        dx = x1 - x0
        dy = y1 - y0

        sign_x = sign_num(dx)
        sign_y = sign_num(dy)

        I = 1
        m = abs(I * dy / dx)
        w = abs(I - m)
        error = abs(I / 2)

        try:
            draw_point_alpha(DrawModule, (x, y), color, m / 2)  
        except Exception:
            pass

        while x - x1 < EPS:
            if error < w:
                x += sign_x
                error += m
            else:
                x += sign_x
                y += sign_y
                error -= w
            try:
                draw_point_alpha(DrawModule, (x, y), color, error)
            except Exception:
                pass
    else:
        x0, y0, x1, y1 = xy_swap_by_y(x0, y0, x1, y1)

        x = round(x0)
        y = round(y0)
        dx = x1 - x0
        dy = y1 - y0

        sign_x = sign_num(dx)
        sign_y = sign_num(dy)

        I = 1
        m = abs(I * dx / dy)
        w = abs(I - m)
        error = abs(I / 2)

        try:
            draw_point_alpha(DrawModule, (x, y), color, m / 2)  
        except Exception:
            pass
        
        while y - y1 < EPS:
            if error < w:
                y += sign_y
                error += m
            else:
                x += sign_x
                y += sign_y
                error -= w
            try:
                draw_point_alpha(DrawModule, (x, y), color, error)
            except Exception:
                pass

    return 0

def DrawLIB(DrawModule, x0, y0, x1, y1, color, resolution: list):
    if color is None: return ERR_COLOR

    if resolution_check(x0, y0, resolution) and resolution_check(x1, y1, resolution): 
        return ERR_RESOLUTION
    
    DrawModule.line((x0, y0, x1, y1), fill=color, width=1)

def check_neg(x0, y0, x1, y1):
    # Обработка отрицательных x0
    if x0 < -EPS:
        if abs(x1 - x0) > EPS:
            k = (y1 - y0) / (x1 - x0)
            y0 = y1 - k * x1
        x0 = 0
    
    # Обработка отрицательных x1
    if x1 < -EPS:
        if abs(x0 - x1) > EPS:
            k = (y0 - y1) / (x0 - x1)
            y1 = y0 - k * x0
        x1 = 0
    
    # Обработка отрицательных y0
    if y0 < -EPS:
        if abs(y1 - y0) > EPS:
            k_inv = (x1 - x0) / (y1 - y0)
            x0 = x1 - k_inv * y1
        y0 = 0
    
    # Обработка отрицательных y1
    if y1 < -EPS:
        if abs(y0 - y1) > EPS:
            k_inv = (x0 - x1) / (y0 - y1)
            x1 = x0 - k_inv * y0
        y1 = 0
    
    return x0, y0, x1, y1

def SunDraw(DrawModule, Drawfunc, x, y, L, n, color, resolution: list):
    angles = list(numpy.linspace(0, 2 * pi, n + 1))
    
    for i in range(len(angles) - 1):
        x0 = x
        y0 = y
        x1 = x + L * cos(angles[i])
        y1 = y + L * sin(angles[i])

        x0, y0, x1, y1 = check_neg(x0, y0, x1, y1)

        try:
            Drawfunc(DrawModule, x0, y0, x1, y1, color, resolution)
        except Exception:
            pass
    
    return 0

























# _____________________________________________________________________________________________________________________-






















def CountDDA(x0, y0, x1, y1):
    count = 0
    count_d = 0
    count_coord = 0;

    x0, y0, x1, y1 = xy_swap_by_x(x0, y0, x1, y1)

    L = max(abs(y1 - y0), abs(x1 - x0)) + 1
    x = x0
    y = y0
    dx = (x1 - x0) / L
    dy = (y1 - y0) / L

    flag = 1
    i = 0

    if dx - dy > -EPS:
        count_d = dy
        count_coord = y
    else:
        count_d = dx
        count_coord = x
        
    while (flag and i < int(L)):
        x += dx
        y += dy
        i += 1

        last_coord = count_coord
        count_coord += count_d
        count += round(count_coord) - round(last_coord)

    return count

def CountBRESENHAM_INT(x0, y0, x1, y1):
    count = 0

    x0, y0, x1, y1 = xy_swap_by_x(x0, y0, x1, y1)
    
    x0 = round(x0)
    y0 = round(y0)
    x1 = round(x1)
    y1 = round(y1)

    dx = x1 - x0
    dy = y1 - y0

    if dx - dy > -EPS:
        is_x = False
    else:
        is_x = True

    sign_y = sign_num(dy)
    sign_x = sign_num(dx)
    
    try:
        sign = sign_num(dy / dx)
    except Exception:
        sign = sign_num(dy * inf)
    error = 2 * dy * sign_y - dx

    y = y0
    for x in range(x0, x1 + 1):
        if is_x:
            count += 1

        while y != y1 and error - 1.0 > EPS:
            y += sign_y

            if not(is_x):
                count += 1

            if dx < -EPS or dx > EPS:
                error -= 2 * dx
            else:
                error -= 1
        
        error += 2 * dy * sign_y

    return count

def CountBRESENHAM(x0, y0, x1, y1):
    count = 0

    x0, y0, x1, y1 = xy_swap_by_x(x0, y0, x1, y1)
    
    x0 = round(x0)
    y0 = round(y0)
    x1 = round(x1)
    y1 = round(y1)

    try:
        k = (y1 - y0) / (x1 - x0)
    except ZeroDivisionError:
        k = sign_num(y1 - y0) * inf

    if abs(k) - 1 > EPS:
        is_x = True
    else:
        is_x = False
    
    abs_k = abs(k)
    sign = sign_num(k)
    error = 0.0

    y = y0
    for x in range(x0, x1 + 1):
        error += abs_k

        if is_x:
            count += 1

        if error - 1.0 <= EPS:
            pass
        else:
            while y != y1 and error - 1.0 > EPS:
                y += sign

                if not(is_x):
                    count += 1

                error -= 1.0
    
    return count

def CountWU(x0, y0, x1, y1):
    count = 0
    
    x0 = round(x0)
    y0 = round(y0)
    x1 = round(x1)
    y1 = round(y1)

    x = x0
    y = y0
    if abs(x1 - x0) >= abs(y1 - y0):
        x0, y0, x1, y1 = xy_swap_by_x(x0, y0, x1, y1)

        try:
            k = (y1 - y0) / (x1 - x0)
        except ZeroDivisionError:
            k = sign_num(y1 - y0) * inf

        x = x0
        y = y0
        while x <= x1:
            x += 1
            y += k
            count += k
    else:
        x0, y0, x1, y1 = xy_swap_by_y(x0, y0, x1, y1)

        try:
            k = (y1 - y0) / (x1 - x0)
        except ZeroDivisionError:
            k = sign_num(y1 - y0) * inf

        x = x0
        y = y0
        while y <= y1:
            y += 1
            x += 1 / k
            count += 1 / k
    
    return round(count)
        
def CountBRESENHAM_SMOOTH(x0, y0, x1, y1):
    count = 0
    
    dx = x1 - x0
    dy = y1 - y0

    if abs(dx) - abs(dy) > -EPS:
        x0, y0, x1, y1 = xy_swap_by_x(x0, y0, x1, y1)

        x = round(x0)
        y = round(y0)
        dx = x1 - x0
        dy = y1 - y0

        sign_x = sign_num(dx)
        sign_y = sign_num(dy)

        I = 1
        m = abs(I * dy / dx)
        w = abs(I - m)
        error = abs(I / 2)

        while x - x1 < EPS:
            if error < w:
                x += sign_x
                error += m
            else:
                x += sign_x
                y += sign_y
                count += 1
                error -= w
    else:
        x0, y0, x1, y1 = xy_swap_by_y(x0, y0, x1, y1)

        x = round(x0)
        y = round(y0)
        dx = x1 - x0
        dy = y1 - y0

        sign_x = sign_num(dx)
        sign_y = sign_num(dy)

        I = 1
        m = abs(I * dx / dy)
        w = abs(I - m)
        error = abs(I / 2)

        while y - y1 < EPS:
            if error < w:
                y += sign_y
                error += m
            else:
                x += sign_x
                y += sign_y
                count += 1
                error -= w

    return count

