import random
from prettytable import PrettyTable

def MillerTest(n, canon, t): #тест миллера на простоту
    a = []
    for i in range(t):
        a.append(random.randint(2, n-1))
    for ai in a:
        if pow(ai, n-1, n)!=1:
            return False
    for qi in canon:
        count = 0
        for aj in a:
            if pow(aj, int((n-1)/qi), n)!=1:
                break
            count+=1
            if count==len(a):
                return False
    return True

def GenerateBlumNumber(requiredLength): #генерация чисел для числа Блюма
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]
    done = False
    while not done:
        m = 1
        canon = []
        fl = True
        while fl:
            randomIndex = random.randint(0, len(primes)-1)
            m *= primes[randomIndex]
            if primes[randomIndex] not in canon:
                canon.append(primes[randomIndex])
            if m.bit_length()==requiredLength-2:
                fl = False
            elif m.bit_length()>requiredLength-2:
                m = 1
                canon.clear()
        n = 4*m+3
        done = MillerTest(n, canon, 50)
    return n

def Sign(p, q, x, r=0, rsize=0):
    if rsize==0:
        rsize=r.bit_length()
    n=p*q
    xs = 0
    if r!=0: #если r уже задано, использовать его
        xs = x << rsize
        xs ^= r
    else: #иначе выполнить поиск r
        while True:
            r = random.randint(0, n)
            xs = x << rsize
            xs ^= r
            if pow(xs, int((p-1)/2), p)==1 and pow(xs, int((q-1)/2), q)==1:
                break
    #китайская теорема об остатках, 1 решение
    z1 = pow(xs, int((p+1)/4), p)
    z2 = pow(xs, int((q+1)/4), q)

    y1 = 1
    y2 = 1

    while ((q*y1)%p)!=z1:
        y1+=1

    while ((p*y2)%q)!=z2:
        y2+=1

    s=(q*y1+p*y2)%n
    return r, s

def Verify(r, s, x, n, rsize=0):
    if rsize==0:
        rsize = rsize
    bs = pow(s, 2, n)
    xs = x << rsize
    xs ^= r
    return xs == bs

#p = GenerateBlumNumber(16)
#q = GenerateBlumNumber(16)

res_table = PrettyTable()

res_table.field_names = ['x', 'r', "x'", 'p', 'q', 'n', 's', 'verified']

test_data = [
    [14, int('1100', 2), 236, 5003, 4999],
    [17, int('0010', 2), 274, 5791, 3323],
    [15, int('0100', 2), 244, 8011, 9467],
    [22, int('0000', 2), 352, 2591, 5531],
    [30, int('0010', 2), 482, 8191, 4079]
    ]

for sample in test_data:
    x = sample[0]
    r = sample[1]
    xs = sample[2]
    p = sample[3]
    q = sample[4]
    n = p*q
    tmp = sample.copy()

    r, s = Sign(p, q, x, r, rsize=4) #подпись
    tmp.append(n)
    tmp.append(s)
    tmp.append(Verify(r, s, x, n, rsize = 4)) #проверка подписи
    res_table.add_row(tmp)

print(res_table)