
# Помехоустойчивое кодирование - Код Хемминга (усеченный)
# _______________________________________________________________________________________________________________________
# Преобразование произвольной последовательности, введенной пользователем текстовой строки в последовательность
# 8-битных блоков

# Шифрование исходной последовательности кодом Хемминга

# Внесение единичной ошибки в один из битов кадждого блока "при передаче" или "передача" блока без внесения ошибки (50%)

# Проверка на "принимающей" стороне наличия ошибок в информационных разрядах и их исправление

# Дешифрование "принятой" последовательности

# Преобразование битовой последовательности в текстовую строку

# Вывод на экран данных, относящихся к произвольному выбранному пользователем, элементу строки
# на каждом этапе преобразования (двоичного представления символа, избыточного кода, кода после "передачи",
# кода после исправления ошибок)
# ______________________________________________________________________________________________________________________

import random

s = input()

print(s)

word_ascii = s.encode('ascii')
print(ord(word_ascii))

if __name__ == '__main__':
    print('Введите исходное слово:', s)

