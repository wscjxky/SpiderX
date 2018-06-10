try:
    while True:
        num = input().split(' ')
        x = int(num[0])
        y = int(num[1])
        res = []
        mod = []
        res.append(str(x / y))
        if not x % y:
            print(res[0])
            break
        res.append('.')

        while x % y not in mod and len(mod) < 100:
            mod.append(x % y)
            x = mod[-1] * 10
            res.append(str(x / y))
            loop = -1
            try:
                loop = mod.index(x % y)
                if loop != -1:
                    res[loop + 2] = "(" + res[loop + 2]
                res[-1] = res[-1] + ")"
                print("".join(res))

            except:
                pass
except:
    pass

