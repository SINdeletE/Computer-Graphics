from math import *

EPS = 1e-8

def triangle_side(p1: list, p2: list):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

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

# VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR

def vector_module(v: list):
    return v[0] ** 2 + v[1] ** 2

def vectors_cos(v1: list, v2: list):
    return (v1[0] * v2[0] + v1[1] * v2[1]) / vector_module(v1) / vector_module(v2)

# VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR VECTOR

def sin_from_cos(cosinus: float):
    return sqrt(1 - cosinus ** 2)

def triangle_circumcircle_center(points: list):
    R = triangle_circumcircle_radius(points, triangle_square(points))

    # Вычисления будут проходить относительно точек с индексами 0 и 1

    