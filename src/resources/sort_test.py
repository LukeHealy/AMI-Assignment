import random


class thing:

    def __init__(self, F, G):
        self.f = F
        self.g = G

    def __str__(self):
        return "thing: " + str(self.f) + ", " + str(self.g)

if __name__ == '__main__':
    l = []

    for i in range(10):
        l.append(thing(random.randint(1,5), random.randint(1,10)))

    for li in l:
        print li

    l.sort(key=lambda x: (x.f, -x.g))

    print "Sorted:"

    for li in l:
        print li