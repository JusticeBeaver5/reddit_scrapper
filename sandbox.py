
x = 'hello'

a = 'yada yada'

def printer(x, y, z):
    print(x, y, z)


def wrapper(d):
    printer(a, 1, 2)
    print('wrapper executed')



wrapper(a)