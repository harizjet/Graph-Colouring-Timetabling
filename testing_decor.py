import time

def a_func(fx):
    def inner(*args):
        start = time.time()
        ans = fx(*args)
        end = time.time()
        print(end-start)
        return ans
    return inner

@a_func
def o_n_2(arr):
    ans, mint = 0, 0
    for i, a in enumerate(arr):
        t = 0
        for b in arr:
            t = min(t, a - b)
        if t < mint:
            ans, mint = i, t
    return arr[ans]

@a_func
def o_n(arr):
    ans = arr[0]
    for a in arr[1:]:
        ans = min(ans, a)
    return ans

if __name__ == '__main__':
    pass