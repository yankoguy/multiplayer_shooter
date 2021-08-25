
number = 123457
part = "543210"
part2 = "1234"

min_num  = number*43999909900
num  = number*44000100000

table = "2121212121212121"

def merge(number):
    return int(str(number)[0]) + int(str(number)[1])

def luhn(number):
    sum=0
    for i in range(16):
        digit = int(number[i]) * int(table[i])
        if digit >= 10:
            sum+=merge(digit)
        else:
            sum+=digit

    return sum

for i in range(44000100000-43999909900):
    str_num = str(number*(43999909900+i))
    if part == str_num[0:6] and part2 == str_num[12:]:
        if luhn(str_num) % 10 ==0:
            print(str_num)

