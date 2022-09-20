'''
def calcul(number_1, number_2, operation):
    if operation == 1:
        result = str(number_1 + number_2)
    elif operation == 2:
        result = str(number_1 - number_2)
    elif operation == 3:
        result = str(number_1 * number_2)
    elif operation == 4:
        result = str(number_1 / number_2)
    else:
        result = None
        print('Действие не поддерживается, вызывайте помощь')

    return result


def calc(number_type):
    if number_type == 1:  # работа с целыми числами
        strnum = 'целое число'
        strnum1 = 'первое'
        strnum2 = 'второе'
    elif number_type == 2:  # работа с дробными числами
        strnum = 'дробь'
        strnum1 = 'первую'
        strnum2 = 'вторую'

    num1 = None
    while num1 is None:
        num1 = input(f'Введите {strnum1} {strnum} : ')
        num1 = check(num1)

    num2 = None
    while num2 is None:
        num2 = input(f'Введите {strnum2} {strnum} : ')
        num2 = check(num2)

    return num1, num2


def check(vhod):
    new_chislo = []
    vhod = vhod.replace(',','.').replace(' ','')
    koef = ''
    tochka = 0
    tire = 0
    for i in vhod:
        if i == '-':
            if tire:
                return None
            koef = '-'
            tire += 1
        elif i.isdigit():
            new_chislo.append(koef + i)
            if koef == '-':
                koef = ''
        elif i == '.':
            tochka += 1
            if tochka < 2:
                new_chislo.append(i)
            else:
                break
        else:
            return None
    chislo = ''.join(new_chislo)
    if chislo != '':
        return float(chislo)
    else:
        return None


def menu():
    print("Дорогой пользователь! Приложение Калькулятор приветсвует тебя!")
    print("1. Рациональные числа")
    print("2. Комплексные числа\n")
    p1 = p2 = None
    ok = False
    while not ok:
        p1 = input("Выберите, с какими числами будем работать? Введите 1 или 2:")
        if p1.isdigit() and 1 <= int(p1) <= 2:
            ok = True
            p1 = int(p1)
        else:
            print("Ошибка, введите 1 или 2")

    print("Выберите арифметическое действие")
    print("1. Сложение")
    print("2. Вычитание")
    print("3. Умножение")
    print("4. Деление")

    ok = False
    while not ok:
        p2 = input("Выберите арифметическое действие. Введите число от 1 до 4:")
        if p2.isdigit() and 1 <= int(p2) <= 4:
            p2 = int(p2)
            ok = True
        else:
            print("Ошибка, введите число от 1 до 4")

    number_1, number_2 = calc(p1)
    result = calcul(number_1, number_2, p2)
    print(result)


menu()
'''


from distutils.cmd import Command
from fileinput import filename
from imaplib import Commands
from os import path

'''
код от Сергея
@bot.message_handler(commands=['start'])
def take_start(msg: telebot.types.Message):
    bot.send_message(chat_id=msg.from_user.id, text=f'Здравствуйте, {msg.from_user.full_name}, {msg.from_user.id}')


@bot.message_handler(commands=['help'])
def take_help(msg: telebot.types.Message):
    bot.send_message(chat_id=msg.from_user.id, text=f'Справка: qweqwd \nqwqw  \nqwrq \nwr \nqwr \nr')


def take_second_message1(msg: telebot.types.Message):
    bot.send_message(chat_id=msg.from_user.id, text=f'Ранее вы прислали только буквы.\nВаше второе сообщение {msg.text}')


def take_second_message2(msg: telebot.types.Message):
    bot.send_message(chat_id=msg.from_user.id, text=f'Ранее вы прислали только цифры.\nВаше второе сообщение {msg.text}')


@bot.message_handler()
def take_message(msg: telebot.types.Message):
    bot.send_message(chat_id=msg.from_user.id, text=f'Вы прислали сообщение {msg.text}')
    if msg.text.isalpha():
        bot.register_next_step_handler(msg, take_second_message1)
    elif msg.text.isdigit():
        bot.register_next_step_handler(msg, take_second_message2)


bot.polling()'''

# filename = 'seminary\\konstatin.txt'

# if path.exists(filename):
#     with open(filename) as f:
#         print(f.read())
# else:
#     print('Файла нет')

# filename = 'seminary\\konstatin.txt'

# if path.isfile(filename):
#     with open(filename) as f:
#         print(f.read())
# else:
#     print('Файла нет')


# @bot.message_handler(commands = ['start'])
# def take_start(msg: telebot.types.Message):
#     bot.send_message(chat_id=msg.from_user.id, text=f'Здравствуйте, {msg.from_user.full_name}')


# def take_second_message1(msg: telebot.types.Message):
#     bot.send_message(chat_id=msg.from_user.id, text=f'ранее вы прислали буквы {msg.text}')

# def take_second_message2(msg: telebot.types.Message):
#     bot.send_message(chat_id=msg.from_user.id, text=f'ранее вы прислали цыфрв {msg.text}')


# @bot.message_handler()
# def take_message(msg: telebot.types.Message):
#     bot.send_message(chat_id=msg.from_user.id, text=f'Вы прислали сообщение {msg.text}')
#     if msg.text.isalpha():
#         bot.register_next_step_handler(msg, take_second_message1)
#     elif msg.text.isdigit():
#         bot.register_next_step_handler(msg, take_second_message2)