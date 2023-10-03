# демонстрация работы с словарём, 
# передачи одних функций в качестве аргументов другой функции
a = 7
def hi():
    print("Hello, friend!")

def by():
    print("By-by, friend!")

def out_f(a, b, c):
    if a == 0:
        b()
    elif a == 1:
        c()



my_dict = {a : 1,
            "position two" : "any word",
            "next_position" : True,
            "my func" : hi}

class Tryexp(object):
    SOSA = 1
    BOBA = 2
    mor = SOSA + BOBA
    
    def show(self):
        print(Tryexp.mor)
        print(Tryexp.SOSA + self.BOBA)
        print("end show!\n")

tr = Tryexp()
tr.show()


print(a)
print(my_dict[a])
print(my_dict["position two"])
print(my_dict["next_position"])
print(a)
print(my_dict["my func"])
my_dict["my func"]()

print()
out_f(1, hi, by)
out_f(0, hi, by)

