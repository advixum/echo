x, y = 3, 4
sum_even = 0
while x <= 7_000_000:
    if x % 2 == 0:
        sum_even += x
    x, y = y, x + y
print("Сумма четных чисел Фибоначчи до 7 миллионов:", sum_even)