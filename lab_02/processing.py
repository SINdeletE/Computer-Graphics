import numpy
import math
import copy

DEFAULT_SCALE = 1
DEFAULT_SIZE_K = 40

FST_Y = math.sqrt(3) / 2
LST_Y = math.sqrt(20) / 6

# Список координат точек исходного рисунка
tank_figure_scheme = {
                        'rect':
                        {
                            'points':
                                [
                                    numpy.array([8 * DEFAULT_SIZE_K, 2 * DEFAULT_SIZE_K, DEFAULT_SCALE]),   # Нижняя правая точка
                                    numpy.array([8 * DEFAULT_SIZE_K, -2 * DEFAULT_SIZE_K, DEFAULT_SCALE]),  # Верхняя правая точка
                                    numpy.array([-8 * DEFAULT_SIZE_K, -2 * DEFAULT_SIZE_K, DEFAULT_SCALE]), # Верхняя левая точка
                                    numpy.array([-8 * DEFAULT_SIZE_K, 2 * DEFAULT_SIZE_K, DEFAULT_SCALE])   # Нижняя левая точка
                                ],
                            'arc_points':
                                [
                                    numpy.array([10 * DEFAULT_SIZE_K, -2 * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                    numpy.array([6 * DEFAULT_SIZE_K, 2 * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                    numpy.array([-10 * DEFAULT_SIZE_K, 2 * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                    numpy.array([-6 * DEFAULT_SIZE_K, -2 * DEFAULT_SIZE_K, DEFAULT_SCALE])
                                ]
                        },
                        'wheels':
                        {
                            'points':
                                [
                                    numpy.array([-7 * DEFAULT_SIZE_K, 1 * DEFAULT_SIZE_K, DEFAULT_SCALE]),   # 1-е колесо
                                    numpy.array([-5 * DEFAULT_SIZE_K, -1 * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                    numpy.array([-4 * DEFAULT_SIZE_K, 1 * DEFAULT_SIZE_K, DEFAULT_SCALE]),  # 2-е колесо
                                    numpy.array([-2 * DEFAULT_SIZE_K, -1 * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                    numpy.array([-1 * DEFAULT_SIZE_K, 1 * DEFAULT_SIZE_K, DEFAULT_SCALE]), # 3-е колесо
                                    numpy.array([1 * DEFAULT_SIZE_K, -1 * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                    numpy.array([2 * DEFAULT_SIZE_K, 1 * DEFAULT_SIZE_K, DEFAULT_SCALE]),  # 4-е колесо
                                    numpy.array([4 * DEFAULT_SIZE_K, -1 * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                    numpy.array([5 * DEFAULT_SIZE_K, 1 * DEFAULT_SIZE_K, DEFAULT_SCALE]),   # 5-е колесо
                                    numpy.array([7 * DEFAULT_SIZE_K, -1 * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                ]
                        },
                        'tower':
                            {
                                'points':
                                    [
                                        numpy.array([6 * DEFAULT_SIZE_K, -2 * DEFAULT_SIZE_K, DEFAULT_SCALE]),   # Нижняя правая точка
                                        numpy.array([6 * DEFAULT_SIZE_K, -5 * DEFAULT_SIZE_K, DEFAULT_SCALE]),  # Верхняя правая точка
                                        numpy.array([-6 * DEFAULT_SIZE_K, -5 * DEFAULT_SIZE_K, DEFAULT_SCALE]), # Верхняя левая точка
                                        numpy.array([-6 * DEFAULT_SIZE_K, -2 * DEFAULT_SIZE_K, DEFAULT_SCALE])   # Нижняя левая точка
                                    ],
                                'ellipse':
                                {
                                    "points":
                                    [
                                        numpy.array([-6 * DEFAULT_SIZE_K, -6 * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                        numpy.array([6 * DEFAULT_SIZE_K, -4 * DEFAULT_SIZE_K, DEFAULT_SCALE])
                                    ]

                                }
                            },
                        'tube':
                            {
                                'points':
                                    [
                                        numpy.array([-3 * DEFAULT_SIZE_K, -(FST_Y + 5) * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                        numpy.array([-3 * DEFAULT_SIZE_K, -8 * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                        numpy.array([-1 * DEFAULT_SIZE_K, -8 * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                        numpy.array([-1 * DEFAULT_SIZE_K, -9 * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                        numpy.array([-4 * DEFAULT_SIZE_K, -9 * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                        numpy.array([-4 * DEFAULT_SIZE_K, -(LST_Y + 5) * DEFAULT_SIZE_K, DEFAULT_SCALE])
                                    ]
                            },
                        'angle':
                            0,
                        'center': [0, 0, DEFAULT_SCALE]
                    }

# ___Перенос___
def figure_action(figure: dict, process_matrix_get, **kwargs):
    data = kwargs.items()

    try: # Изменение коэффициента масштабирования
        k = data['k']
    except Exception:
        k = 1

    try: # Измененение угла фигуры
        figure['angle'] = data['angle']
    except Exception:
        pass

    process_matrix = process_matrix_get(dict(data))
    new_figure = figure

    for i in range(len(new_figure['rect']['points'])):
        new_figure['rect']['points'][i][2] = k
        new_figure['rect']['points'][i] = numpy.dot(                \
                                        new_figure['rect']['points'][i],    \
                                        process_matrix
                                        )
    
    for i in range(len(new_figure['rect']['arc_points'])):
        new_figure['rect']['arc_points'][i][2] = k
        new_figure['rect']['arc_points'][i] = numpy.dot(                \
                                        new_figure['rect']['arc_points'][i],    \
                                        process_matrix
                                        )

    for i in range(len(new_figure['wheels']['points'])):
        new_figure['wheels']['points'][i][2] = k
        new_figure['wheels']['points'][i] = numpy.dot(                \
                                        new_figure['wheels']['points'][i],    \
                                        process_matrix
                                        )
        
    for i in range(len(new_figure['tower']['points'])):
        new_figure['tower']['points'][i][2] = k
        new_figure['tower']['points'][i] = numpy.dot(                \
                                        new_figure['tower']['points'][i],    \
                                        process_matrix
                                        )
    
    for i in range(len(new_figure['tower']['ellipse']['points'])):
        new_figure['tower']['ellipse']['points'][i][2] = k
        new_figure['tower']['ellipse']['points'][i] = numpy.dot(                \
                                        new_figure['tower']['ellipse']['points'][i],    \
                                        process_matrix
                                        )
    
    for i in range(len(new_figure['tube']['points'])):
        new_figure['tube']['points'][i][2] = k
        new_figure['tube']['points'][i] = numpy.dot(                \
                                        new_figure['tube']['points'][i],    \
                                        process_matrix
                                        )
    
    new_figure['center'] = numpy.dot(new_figure['center'], process_matrix)

    return new_figure

def move_matrix_get(data: dict):
    return numpy.array(
                        [
                            [1, 0, 0],
                            [0, 1, 0],
                            [data['x'], data['y'], 1]
                        ]
                    )

def scale_matrix_get(data: dict):
    return numpy.array(
                        [
                            [data['k'], 0, 0],
                            [0, data['k'], 0],
                            [0, 0, 1]
                        ]
                    )

def rotate_matrix_get(data: dict):
    return numpy.array(
                        [
                            [math.cos(data['rad']), -math.sin(data['rad']), 0],
                            [math.sin(data['rad']), math.cos(data['rad']), 0],
                            [0, 0, 1]
                        ]
                    )

def angle_to_rad(angle: float):
    return angle * math.pi / 180


# ___FIGURE___
class Figure:
    def __init__(self):
        self.figure = copy.deepcopy(tank_figure_scheme)

    def default(self):
        del self.figure
        self.figure = copy.deepcopy(tank_figure_scheme)

    def move(self, move_x: float, move_y: float):
        figure_action(self.figure, move_matrix_get, x=move_x, y=move_y)

    def scale(self, scale_k: float):
        figure_action(self.figure, scale_matrix_get, k=scale_k)

    def rotate(self, rotate_angle: float):
        center = self.figure['center']

        figure_action(self.figure, move_matrix_get, x=-center[0], y=-center[1])
        figure_action(self.figure, rotate_matrix_get, rad=angle_to_rad(rotate_angle))
        figure_action(self.figure, move_matrix_get, x=center[0], y=center[1])
    
    def get(self):
        return self.figure
