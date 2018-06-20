import math

a = 1120
b = 1210
zb, za = b // 100, a // 100
xb, xa = b % 100, a % 100

xb = xb - xa
zb = zb - za
if xb < 0:
    zb -= 1
    xb = xb + 60
    print(xb)

print(zb, xb, )
print(zb * 8 + math.ceil(xb / 15) * 2)
