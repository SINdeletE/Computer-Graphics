from math import *

#ERRORS
PARSE_OK = 0
PARSE_ERROR_POINTS_COUNT = 1
PARSE_ERROR_NO_VALID_TRIANGLE = 2

EPS = 1e-8

def triangle_side(p1: list, p2: list):
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def triangle_square(points: list):
    a = triangle_side(points[0], points[1])
    b = triangle_side(points[0], points[2])
    c = triangle_side(points[1], points[2])
    p = (a + b + c) / 2

    return sqrt(p * (p - a) * (p - b) * (p - c))

def triangle_circumcircle_radius(points: list, s: float):
    a = triangle_side(points[0], points[1])
    b = triangle_side(points[0], points[2])
    c = triangle_side(points[1], points[2])

    return a * b * c / 4 / s

# Показывает положение 3-й точки относительно основание: -1, если ниже, 1 в остальных случаях
def triangle_point_polar(p_last: list, p_max_x: list, k_base: float):
    shifted_p_last = [p_max_x[0], k_base * (p_max_x[0] - p_last[0]) + p_last[1]] # Смещённая точка p_last (Смещение к p_max_x по Ox) 

    if shifted_p_last[1] - p_max_x[1] < -EPS:
        return -1
    else:
        return 1

# VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR

def vector_not(v: list):
    return list(map(lambda a: -a, v))

def vector_module(v: list):
    return sqrt(v[0] ** 2 + v[1] ** 2)

def vectors_cos(v1: list, v2: list):
    return (v1[0] * v2[0] + v1[1] * v2[1]) / vector_module(v1) / vector_module(v2)

def vector_from_points(p1: list, p2: list):
    return [p2[0] - p1[0], p2[1] - p1[1]]

def vector_k(v: list, k: float):
    return list(map(lambda param: k * param, v))

# VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR

# POINT POINT POINT POINT POINT POINT POINT POINT POINT POINT POINT POINT

def point_vector_sum(point: list, vector: list):
    return [point[0] + vector[0], point[1] + vector[1]]

# POINT POINT POINT POINT POINT POINT POINT POINT POINT POINT POINT POINT

def sin_from_cos(cosinus: float):
    return sqrt(1 - cosinus ** 2)

# Функция, вычисляющая информация об описанной окружности по 3-м точкам
def triangle_circumcircle(points: list):
    R = triangle_circumcircle_radius(points, triangle_square(points))
    M = [[], []]

    p_min_x = min(points, key=lambda p: p[0])
    p_max_x = max(points, key=lambda p: p[0])
    p_last = []
    for p in points:
        if p != p_min_x and p != p_max_x:
            p_last = p

            break
    
    # Векторы от 3-й точки до p_max_x и p_min_x
    vector_last_to_max = vector_from_points(p_last, p_max_x)
    vector_last_to_min = vector_from_points(p_last, p_min_x)

    # Вычисления будут проходить относительно точек с min_x и min_y

    vector_base = vector_from_points(p_min_x, p_max_x) # Вектор p_min_x -> p_max_x
    k_base = (p_max_x[1] - p_min_x[1]) / (p_max_x[0] - p_min_x[0]) # Угол наклона вектора p_min_x -> p_max_x

    # Вектор до основания серединного перпендикуляра
    vector_to_perp_base = vector_k(vector_base, 0.5)

    if abs(k_base) > EPS:
        k_perp = -1 / k_base # Коэффициент k = dy/dx - угол наклона серединного перпендикуляра
    perp = [] # Серединный перпендикуляр

    perp_length = R ** 2 - vector_module(vector_base) ** 2 / 4
    if abs(perp_length) > EPS:
        perp_length = sqrt(perp_length) # Длина серединного перпендикуляра
    else:
        perp_length = 0

    if abs(p_min_x[1] - p_max_x[1]) < EPS: # Если k_perp -> inf
        perp = [0, perp_length]
    else:
        perp = [1, k_perp * 1] # Перпендикуляр произвольной длины
        perp = list(map(lambda n: n / vector_module(perp) * perp_length, perp)) # Серединный перпендикуляр, где направление y неизвестно
        if perp[1] < -EPS:
            perp = vector_not(perp)

    # ------ДОП. УСЛОВИЯ

    if triangle_point_polar(p_last, p_max_x, k_base) == -1: # Смотрим расположение 3-й другой точки и основания
        perp = vector_not(perp)

    p_last_cos = vectors_cos(vector_last_to_max, vector_last_to_min)
    if p_last_cos < -EPS:
        perp = vector_not(perp)

    # ------

    result = point_vector_sum(p_min_x, vector_to_perp_base)
    result = point_vector_sum(result, perp)

    return result, R

def circle_square(radius: float):
    return pi * radius * radius

# ----------------------------------------------------------

# Перебор точек на наличие 

def triangle_parse_compare_func(circle_square: float, triangle_square: float):
    return circle_square - triangle_square

def triangle_parse(points: list):
    delta = None # Разница между площадью описанной окружности и площади треугольника
    delta_points = None

    if len(points) < 3:
        return PARSE_ERROR_POINTS_COUNT, delta_points

    for i in range(len(points) - 2):
        for j in range(i + 1, len(points) - 1):
            for k in range(j + 1, len(points)):
                triangle_points = [points[i], points[j], points[k]]

                if triangle_square(triangle_points) > EPS: # Можно ли вообще составить треугольник из данных точек
                    t_square = triangle_square(triangle_points)
                    c_square = circle_square(triangle_circumcircle_radius(triangle_points, t_square))
                    
                    current_delta = triangle_parse_compare_func(c_square, t_square)

                    if delta is None or (current_delta - delta) > EPS:
                        delta = current_delta
                        delta_points = triangle_points
    
    if delta is None:
        return PARSE_ERROR_NO_VALID_TRIANGLE, delta_points

    return PARSE_OK, delta_points
