import telebot
from datetime import datetime


API_TOKEN = ''
LOG_PATH = 'log/'
users_operations = {}


bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def take_start(msg: telebot.types.Message):
    global users_operations
    users_operations.setdefault(msg.from_user.id, ['', '', '', ''])
    bot.send_message(chat_id=msg.from_user.id, text='Calculator Bot')
    bot.send_message(chat_id=msg.from_user.id, text=f'C какими числами будем работать?\n1. Действительные '
                                                    f'числа\n2. Комплексные числа')
    bot.register_next_step_handler(msg, take_type_number)


@bot.message_handler(commands=['help'])
def take_help(msg: telebot.types.Message):
    bot.send_message(chat_id=msg.from_user.id, text=f'Бот позволяет получить результат '
                                                    f'арифметических действий\n<+ - * />\nмежду двух чисел')
    bot.send_message(chat_id=msg.from_user.id, text=f'Для начала введите команду /start')


def take_type_number(msg: telebot.types.Message):
    if msg.text in {'1', '2'}:
        global users_operations
        users_operations[msg.from_user.id][0] = int(msg.text)
        bot.send_message(chat_id=msg.from_user.id, text=f'Выберите, арифметическое действие <+ - * />')
        bot.register_next_step_handler(msg, take_type_of_operations)
    else:
        bot.send_message(chat_id=msg.from_user.id, text=f'Ошибка, введите 1 или 2')
        bot.register_next_step_handler(msg, take_type_number)


def take_type_of_operations(msg: telebot.types.Message):
    if msg.text in {'+': 1, '-': 2, '*': 3, '/': 4}:
        global users_operations
        users_operations[msg.from_user.id][1] = {'+': 1, '-': 2, '*': 3, '/': 4}[msg.text]
        if users_operations[msg.from_user.id][0] == 1:
            bot.send_message(chat_id=msg.from_user.id, text=f'Введите первое действительное число')
        else:
            bot.send_message(chat_id=msg.from_user.id, text=f'Введите первое комплексное число в виде <действительная '
                                                            f'часть> <мнимая часть>')
        bot.register_next_step_handler(msg, take_first_number)
    else:
        bot.send_message(chat_id=msg.from_user.id, text=f'Ошибка, введите арифметическое действие <+ - * />')
        bot.register_next_step_handler(msg, take_type_of_operations)


def take_first_number(msg: telebot.types.Message):
    tmp = []
    if users_operations[msg.from_user.id][0] == 1:
        tmp.append(msg.text)
        tmp.append('0')
    else:
        tmp = msg.text.split()
    if check(tmp[0]) is not None and check(tmp[1]) is not None:
        users_operations[msg.from_user.id][2] = complex(check(tmp[0]), check(tmp[1]))
        if users_operations[msg.from_user.id][0] == 1:
            bot.send_message(chat_id=msg.from_user.id, text=f'Введите второе действительное число')
        else:
            bot.send_message(chat_id=msg.from_user.id, text=f'Введите второе комплексное число в виде <действительная '
                                                            f'часть> <мнимая часть>')
        bot.register_next_step_handler(msg, take_second_number)
    else:
        bot.send_message(chat_id=msg.from_user.id, text=f'Неверный формат числа')
        if users_operations[msg.from_user.id][0] == 1:
            bot.send_message(chat_id=msg.from_user.id, text=f'Введите первое действительное число')
        else:
            bot.send_message(chat_id=msg.from_user.id, text=f'Введите первое комплексное число в виде <действительная '
                                                            f'часть> <мнимая часть>')
        bot.register_next_step_handler(msg, take_first_number)


def take_second_number(msg: telebot.types.Message):
    tmp = []
    if users_operations[msg.from_user.id][0] == 1:
        tmp.append(msg.text)
        tmp.append('0')
    else:
        tmp = msg.text.split()
    if check(tmp[0]) is not None and check(tmp[1]) is not None:
        users_operations[msg.from_user.id][3] = complex(check(tmp[0]), check(tmp[1]))
        itog = calcul(users_operations[msg.from_user.id][2], users_operations[msg.from_user.id][3], users_operations[msg.from_user.id][1])
        if itog is not None:
            if itog.imag == 0:
                if itog.real.is_integer():
                    itog = int(itog.real)
                else:
                    itog = itog.real
        else:
            itog = 'Деление на 0'
        bot.send_message(chat_id=msg.from_user.id, text=f'Результат вычисления: {itog}')
        with open(LOG_PATH+'log'+str(datetime.date(datetime.today()))+'.csv', mode='a+', encoding='utf-8') as log:
            log.write(f'{msg.from_user.id},{",".join([str(x) for x in users_operations[msg.from_user.id]])},{itog}\n')
        bot.send_message(chat_id=msg.from_user.id, text=f'Для продолжения отправьте любое сообщение')
    else:
        bot.send_message(chat_id=msg.from_user.id, text=f'Неверный формат числа')
        if users_operations[msg.from_user.id][0] == 1:
            bot.send_message(chat_id=msg.from_user.id, text=f'Введите второе действительное число')
        else:
            bot.send_message(chat_id=msg.from_user.id, text=f'Введите второе комплексное число в виде <действительная '
                                                            f'часть> <мнимая часть>')
        bot.register_next_step_handler(msg, take_second_number)


@bot.message_handler()
def take_message(msg: telebot.types.Message):
    bot.send_message(chat_id=msg.from_user.id, text=f'Выберите, с какими числами будем работать?\n1. Действительные '
                                                    f'числа\n2. Комплексные числа')
    bot.register_next_step_handler(msg, take_type_number)


def check(vhod):
    new_chislo = []
    vhod = vhod.replace(',', '.').replace(' ', '')  # заменяем на точки и убиарем пробелы
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


def calcul(number_1, number_2, operation):
    if operation == 1:
        result = number_1 + number_2
    elif operation == 2:
        result = number_1 - number_2
    elif operation == 3:
        result = number_1 * number_2
    elif operation == 4 and number_2 != 0:
        try:
            result = number_1 / number_2
        except ZeroDivisionError:
            result = None
    else:
        result = None
    return result


print('Бот запущен')

bot.polling()