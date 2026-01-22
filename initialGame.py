class Fraction:
    def __init__(self, n, d):
        self.__numo = n
        self.__demo = d

    def __repr__(self):
        return str(self.__numo) + "/" + str(self.__demo)        

    def __add__(self,other):
        a = self.__n * other.__d
        b = self.__d * other.__n
        c = a+b
        return c, self.__d * other.__d