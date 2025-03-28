import numpy
import math
import copy

EPS = 1e-5

DEFAULT_SCALE = 1
DEFAULT_SIZE_K = 40

# Информация для аппроксимации эллипса
STEPS = 360
DEFAULT_ELLIPSE_A = 6
DEFAULT_ELLIPSE_B = 1

DEFAULT_CENTER_X = 1400 / 2
DEFAULT_CENTER_Y = 1400 / 2

FST_Y = math.sqrt(3) / 2
LST_Y = math.sqrt(20) / 6

# Аппроксимация эллипса
def ellipse_y_from_x(x: float):
    res = 1 - x**2 / DEFAULT_ELLIPSE_A**2

    if (abs(res) < EPS):
        res = 0.0
    else:
        res = math.sqrt(res) * DEFAULT_ELLIPSE_B
    
    return res

def ellipse_approx(center, gen_a, gen_b):
    ax = list()

    for x in numpy.linspace(-gen_a, gen_a, STEPS):
        ax.append(numpy.array([center[0] + x * DEFAULT_SIZE_K, center[1] - ellipse_y_from_x(x) * DEFAULT_SIZE_K, DEFAULT_SCALE]))
    
    return ax

def semicircle_x_from_y(y: float, radius):
    res = radius**2 - y**2

    if (abs(res) < EPS):
        res = 0.0
    else:
        res = math.sqrt(res)
    
    return res

def semicircle_approx(center, radius, is_left):
    ax = list()
    sign = 1

    if is_left is True:
        sign = -1
    
    for y in numpy.linspace(-radius, radius, STEPS):
        ax.append(numpy.array([center[0] + sign * semicircle_x_from_y(y, radius) * DEFAULT_SIZE_K, center[1] + y * DEFAULT_SIZE_K, DEFAULT_SCALE]))
    
    return ax

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
                            'ax':
                                [
                                    semicircle_approx(numpy.array([-8 * DEFAULT_SIZE_K, 0 * DEFAULT_SIZE_K, DEFAULT_SCALE]), 2, True),
                                    semicircle_approx(numpy.array([8 * DEFAULT_SIZE_K, 0 * DEFAULT_SIZE_K, DEFAULT_SCALE]), 2, False)
                                ]
                        },
                        'wheels':
                        {
                            'ax':
                                [
                                    semicircle_approx(numpy.array([-6 * DEFAULT_SIZE_K, 0 * DEFAULT_SIZE_K, DEFAULT_SCALE]), 1, True),
                                    semicircle_approx(numpy.array([-6 * DEFAULT_SIZE_K, 0 * DEFAULT_SIZE_K, DEFAULT_SCALE]), 1, False),
                                    semicircle_approx(numpy.array([-3 * DEFAULT_SIZE_K, 0 * DEFAULT_SIZE_K, DEFAULT_SCALE]), 1, True),
                                    semicircle_approx(numpy.array([-3 * DEFAULT_SIZE_K, 0 * DEFAULT_SIZE_K, DEFAULT_SCALE]), 1, False),
                                    semicircle_approx(numpy.array([0 * DEFAULT_SIZE_K, 0 * DEFAULT_SIZE_K, DEFAULT_SCALE]), 1, True),
                                    semicircle_approx(numpy.array([0 * DEFAULT_SIZE_K, 0 * DEFAULT_SIZE_K, DEFAULT_SCALE]), 1, False),
                                    semicircle_approx(numpy.array([3 * DEFAULT_SIZE_K, 0 * DEFAULT_SIZE_K, DEFAULT_SCALE]), 1, True),
                                    semicircle_approx(numpy.array([3 * DEFAULT_SIZE_K, 0 * DEFAULT_SIZE_K, DEFAULT_SCALE]), 1, False),
                                    semicircle_approx(numpy.array([6 * DEFAULT_SIZE_K, 0 * DEFAULT_SIZE_K, DEFAULT_SCALE]), 1, True),
                                    semicircle_approx(numpy.array([6 * DEFAULT_SIZE_K, 0 * DEFAULT_SIZE_K, DEFAULT_SCALE]), 1, False)
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
                                    'ax':
                                        ellipse_approx(numpy.array([0 * DEFAULT_SIZE_K, -5 * DEFAULT_SIZE_K, DEFAULT_SCALE]), \
                                                                                        DEFAULT_ELLIPSE_A, DEFAULT_ELLIPSE_B)
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
                        'kx':
                            DEFAULT_SCALE,
                        'ky':
                            DEFAULT_SCALE,
                        'center': [0, 0, DEFAULT_SCALE]
                    }

# ___Перенос___
def figure_action(figure: dict, process_matrix_get, **kwargs):
    data = dict(kwargs.items())

    process_matrix = process_matrix_get(data)
    new_figure = figure

    try: # Изменение коэффициента масштабирования
        new_figure['kx'] *= data['kx']
        new_figure['ky'] *= data['ky']
    except Exception:
        pass

    try:
        center = kwargs['center']
    except Exception:
        center = [0, 0]

    for i in range(len(new_figure['rect']['points'])):
        new_figure['rect']['points'][i] = numpy.dot(                \
                                        new_figure['rect']['points'][i],    \
                                        process_matrix
                                        )
    
    for z in range(len(new_figure['rect']['ax'])):
        for i in range(len(new_figure['rect']['ax'][z])):
            new_figure['rect']['ax'][z][i] = numpy.dot(                \
                                            new_figure['rect']['ax'][z][i],    \
                                            process_matrix
                                            )

    for z in range(len(new_figure['wheels']['ax'])):
        for i in range(len(new_figure['wheels']['ax'][z])):
            new_figure['wheels']['ax'][z][i] = numpy.dot(                \
                                            new_figure['wheels']['ax'][z][i],    \
                                            process_matrix
                                            )

    for i in range(len(new_figure['tower']['points'])):
        new_figure['tower']['points'][i] = numpy.dot(                \
                                        new_figure['tower']['points'][i],    \
                                        process_matrix
                                        )
    
    for i in range(len(new_figure['tower']['ellipse']['ax'])):
        new_figure['tower']['ellipse']['ax'][i] = numpy.dot(                \
                                        new_figure['tower']['ellipse']['ax'][i],    \
                                        process_matrix
                                        )
    
    for i in range(len(new_figure['tube']['points'])):
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
        self.__init__()

    def move(self, move_x: float, move_y: float):
        self.figure = figure_action(self.figure, move_matrix_get, x=move_x, y=move_y)

    def scale(self, scale_kx: float, scale_ky: float, x, y):
        center = self.figure['center']

        self.figure = figure_action(self.figure, move_matrix_get, x=-x, y=-y)
        self.figure = figure_action(self.figure, scale_matrix_get, kx=scale_kx, ky=scale_ky)
        self.figure = figure_action(self.figure, move_matrix_get, x=x, y=y)

    def rotate(self, rotate_angle: float):
        self.figure['angle'] += rotate_angle # Добавляем угол к нынешнему
        self.figure['angle'] %= 360

        center = self.figure['center']

        self.figure = figure_action(self.figure, move_matrix_get, x=-center[0], y=-center[1])
        self.figure = figure_action(self.figure, rotate_matrix_get, rad=angle_to_rad(rotate_angle), center=[0, 0])
        self.figure = figure_action(self.figure, move_matrix_get, x=center[0], y=center[1])
    def rotate_center(self, rotate_angle: float, x, y):
        self.figure['angle'] += rotate_angle # Добавляем угол к нынешнему
        self.figure['angle'] %= 360

        rotate_center = [x, y]

        self.figure = figure_action(self.figure, move_matrix_get, x=-rotate_center[0], y=-rotate_center[1])
        self.figure = figure_action(self.figure, rotate_matrix_get, rad=angle_to_rad(rotate_angle))
        self.figure = figure_action(self.figure, move_matrix_get, x=rotate_center[0], y=rotate_center[1])
    
    def get(self):
        return self.figure
