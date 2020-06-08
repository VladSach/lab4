import struct


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

    def read_bmp(self, file_name):
        with open(file_name, 'rb') as file:
            file.seek(2)
            # Считываем размер нашего файла
            file_size = struct.unpack('<L', file.read(4))[0]
            file.seek(18)
            # Тут уже считываем высоту и ширину нашей картинки
            self.width, self.height = struct.unpack('<LL', file.read(8))
            # Готовим двумерный массив для пикселей
            self.pixels = [[Pixel(0, 0, 0) for i in range(self.width)] for j in range(self.height)]
            file.seek(54)
            position = file.tell()
            h = w = 0
            while position < file_size and h < self.height and w < self.width:
                # Ну и понеслась душа в рай, заполняем наш масив
                r, g, b = struct.unpack('<BBB', file.read(3))
                position = file.tell()
                self.pixels[h][w].red = r
                self.pixels[h][w].green = g
                self.pixels[h][w].blue = b
                w += 1
                if w >= self.width:
                    n = (4 - ((self.width * 3) % 4)) % 4
                    file.read(n)
                    position = file.tell()
                    h += 1
                    w = 0
            file.close()

    def just_zoom(self, scale):
        # Приближаем нашу картинку
        zoomed_width = int(self.width * scale)
        zoomed_height = int(self.height * scale)
        zoomed_image = Image()
        zoomed_image.width = zoomed_width
        zoomed_image.height = zoomed_height
        zoomed_image.pixels = [[None for i in range(zoomed_width)] for j in range(zoomed_height)]
        for i in range(zoomed_height):
            for j in range(zoomed_width):
                zoomed_image.pixels[i][j] = self._interpolate(j * self.width / zoomed_width,
                                                              i * self.height / zoomed_height)
        return zoomed_image

    def write_bmp(self, file_name):
        # Ну тут как бы из названия можно понять, что записываем картинку в новый файл
        with open(file_name, 'wb') as file:
            file.write(struct.pack("<BB", ord("B"), ord("M")))
            position = file.tell()
            # Распаковали? Молодцы! Пакуем обратно -_-
            file.write(struct.pack("<L", 0))
            file.write(struct.pack("<L", 0))
            file.write(struct.pack("<L", 54))
            file.write(struct.pack("<L", 40))
            file.write(struct.pack("<LL", self.width, self.height))
            file.write(struct.pack("<H", 1))
            file.write(struct.pack("<H", 24))
            file.write(struct.pack("<LLLLLL", 0, 0, 0, 0, 0, 0))
            for row in self.pixels:
                for pixel in row:
                    file.write(struct.pack("<BBB", pixel.red, pixel.green, pixel.blue))
                for _ in range((4 - ((self.width * 3) % 4)) % 4):
                    file.write(struct.pack("<B", 0))
            file_size = file.tell()
            file.seek(position)
            file.write(struct.pack("<L", file_size))
            file.close()
