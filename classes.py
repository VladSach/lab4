class Pixel(object):
    def __init__(self, r, g, b):
        self.red = r
        self.green = g
        self.blue = b

    def __mul__(self, other):
        # Метод которые вызывается автоматически при умножении
        return Pixel(self.red * other, self.green * other, self.blue * other)

    def __add__(self, other):
        # Метод которые вызывается автоматически при суммировании
        return Pixel(self.red + other.red, self.green + other.green, self.blue + other.blue)


class Image(object):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.pixels = []

    def _interpolate(self, pX, pY):
        # Короче, что это и главное зачем он нахуй нужон этот ваш интерполятор
        """
        Суть такова: Это билинейная интерполяция, по факту, одна из самых простых.
        Работает по простому принципу: берем один пиксель, который мы не знаем,
        ебошим 4 пикселя, которые мы знаем как выглядят и которые находяться на по диагонали
        т.е. считай что у нас квадрат 2 на 2, в центре искомый, а на краях извесные.
        Мы и присваем неизвестному пикселю среднее значение между теми 4 что мы знаем
        """

        # Собсна сам неизвестный пикесь
        x1 = int(pX)
        y1 = int(pY)
        x2 = min(x1 + 1, self.width - 1)
        y2 = min(y1 + 1, self.height - 1)

        # 4 пикселя вокруг него
        bottom_left = self.pixels[y1][x1]
        bottom_right = self.pixels[y1][x2]
        top_left = self.pixels[y2][x1]
        top_right = self.pixels[y2][x2]

        lx = pX - x1
        ly = pY - y1

        # находим наше усредненное значение
        r1 = bottom_right * lx + bottom_left * (1. - lx)
        r2 = top_right * lx + top_left * (1. - lx)

        pixel = r2 * ly + r1 * (1. - ly)

        return Pixel(int(pixel.red), int(pixel.green), int(pixel.blue))
