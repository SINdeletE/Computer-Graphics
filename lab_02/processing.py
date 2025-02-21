import numpy
import math
import copy

DEFAULT_SCALE = 1
DEFAULT_SIZE_K = 40

FST_Y = math.sqrt(11025 / 144) - 99 / 12
LST_Y = math.sqrt(10017 / 144) - 99 / 12

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
                                    numpy.array([-10 * DEFAULT_SIZE_K, 2 * DEFAULT_SIZE_K, DEFAULT_SCALE])
                                ],
                            'radius': 
                                2 * DEFAULT_SIZE_K
                        },
                        'wheels':
                        {
                            'points':
                                [
                                    numpy.array([-6 * DEFAULT_SIZE_K, 0 * DEFAULT_SIZE_K, DEFAULT_SCALE]),   # 1-е колесо
                                    numpy.array([-3 * DEFAULT_SIZE_K, 0 * DEFAULT_SIZE_K, DEFAULT_SCALE]),  # 2-е колесо
                                    numpy.array([0 * DEFAULT_SIZE_K, 0 * DEFAULT_SIZE_K, DEFAULT_SCALE]), # 3-е колесо
                                    numpy.array([3 * DEFAULT_SIZE_K, 0 * DEFAULT_SIZE_K, DEFAULT_SCALE]),  # 4-е колесо
                                    numpy.array([6 * DEFAULT_SIZE_K, 0 * DEFAULT_SIZE_K, DEFAULT_SCALE])   # 5-е колесо
                                ],
                            'radius':
                                DEFAULT_SIZE_K # Радиус колеса
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
                                    # "forming":
                                    #     [6 * DEFAULT_SIZE_K, 1 * DEFAULT_SIZE_K], # Образующие дуги эллипса
                                    "points":
                                    [
                                        numpy.array([-6 * DEFAULT_SIZE_K, -6 * DEFAULT_SIZE_K]),
                                        numpy.array([6 * DEFAULT_SIZE_K, -5 * DEFAULT_SIZE_K])
                                    ]

                                }
                            },
                        'tube':
                            {
                                'points':
                                    [
                                        numpy.array([-3 * DEFAULT_SIZE_K, (FST_Y + 5) * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                        numpy.array([-3 * DEFAULT_SIZE_K, -8 * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                        numpy.array([-1 * DEFAULT_SIZE_K, -8 * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                        numpy.array([-1 * DEFAULT_SIZE_K, -9 * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                        numpy.array([-4 * DEFAULT_SIZE_K, -9 * DEFAULT_SIZE_K, DEFAULT_SCALE]),
                                        numpy.array([-4 * DEFAULT_SIZE_K, (LST_Y + 5) * DEFAULT_SIZE_K, DEFAULT_SCALE])
                                    ]
                            }
                    }

# ___Перенос___
def figure_action(figure: dict, process_matrix_get, **kwargs):
    data = kwargs.items()

    try: # Изменение коэффициента масштабирования
        k = data['k']
    except Exception:
        k = 1

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
    
    for i in range(len(new_figure['tower']['points'])):
        new_figure['tube']['points'][i][2] = k
        new_figure['tube']['points'][i] = numpy.dot(                \
                                        new_figure['tube']['points'][i],    \
                                        process_matrix
                                        )
    
    for i in range(len(new_figure['tube']['points'])):
        new_figure['tube']['points'][i][2] = k
        new_figure['tube']['points'][i] = numpy.dot(                \
                                        new_figure['tube']['points'][i],    \
                                        process_matrix
                                        )

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
                            [data['kx'], 0, 0],
                            [0, data['ky'], 0],
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
        figure_action(self.figure, scale_matrix_get, rad=angle_to_rad(rotate_angle))
    
    def get(self):
        return self.figure
