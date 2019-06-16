import threading

class X:
    y = 10
    d = [3, 4]
    l = threading.Lock()

    def print_y(self):
        with self.l:
            print("y =", self.y, "d =", self.d, "l =", self.l)


x1 = X()
x2 = X()

x1.print_y()
x2.print_y()
print(id(x1.y), id(x2.y), id(x1.d), id(x2.d))

with x2.l:
    X.y += 1
    x1.d.append(5)


x1.print_y()
x2.print_y()
print(id(x1.y), id(x2.y), id(x1.d), id(x2.d))
