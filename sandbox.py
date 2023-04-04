import threading
import time


# x = 'hello'

# a = 'yada yada'

# def printer(x, y, z):
#     print(x, y, z)


# def wrapper(d):
#     printer(a, 1, 2)
#     print('wrapper executed')



# wrapper(a)



lst = ['a', 'b', 'c', 'd', 'e']



def run(var):
    l = []
    for i in range(10**7):
        if i%2 == 0:
            l.append(i)
    print(f'running on {var}')
    return f'running on {var}'

# print(run(lst[0]))




def inf_runner(var):
    while True:
        print(var, '\n')
        time.sleep(1)






d = []

def run_threads(lst):
    threads = []
    for item in lst:
        threads.append(threading.Thread(target=inf_runner, args=[item], daemon=True))
    for thread in threads:
        thread.start()
        time.sleep(2)
        print('runing on ', thread.getName(), '\n')
    for thread in threads:
        thread.join()


run_threads(lst)
# inf_runner(lst[0])