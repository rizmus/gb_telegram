import telebot
bot = telebot.TeleBot('')


@bot.message_handler(commands=['start'])
def take_start(msg: telebot.types.Message):
    global users_operations
    users_operations.setdefault(msg.from_user.id, ['', ''])
    bot.send_message(chat_id=msg.from_user.id, text=f'Привет!')
    bot.send_message(chat_id=msg.from_user.id, text=f'Выбери какие числа будем считать??\n1. Целые числа\n \
    2. Дробные числа')
    bot.register_next_step_handler(msg, take_type_number)


@bot.message_handler(commands=['help'])
def take_help(msg: telebot.types.Message):
    bot.send_message(chat_id=msg.from_user.id, text=f'Приложение позволяет получить результат \
    арифметических действий\n<+ - * />\nмежду двух чисел')
    bot.send_message(chat_id=msg.from_user.id, text=f'Для начала введите команду /start')


users_operations = {}


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
        bot.send_message(chat_id=msg.from_user.id, text=f'Введите два числа через пробел <Первое> <Второе>')
        bot.register_next_step_handler(msg, take_numbers)
    else:
        bot.send_message(chat_id=msg.from_user.id, text=f'Ошибка, введите арифметическое действие <+ - * />')
        bot.register_next_step_handler(msg, take_type_of_operations)


def take_numbers(msg: telebot.types.Message):
    tmp = msg.text.split()
    if len(tmp) == 2 and tmp[0].isdigit() and tmp[1].isdigit():
        itog = calcul(int(tmp[0]), int(tmp[1]), users_operations[msg.from_user.id][1])
        bot.send_message(chat_id=msg.from_user.id, text=f'Результат {itog}')
        bot.send_message(chat_id=msg.from_user.id, text=f'Для продолжения отправьте любое сообщение')
    else:
        bot.send_message(chat_id=msg.from_user.id, text=f'Введите два числа через пробел <Первое> <Второе>')
        bot.register_next_step_handler(msg, take_numbers)


def calcul(number_1, number_2, operation):
    if operation == 1:
        result = str(number_1 + number_2)
    elif operation == 2:
        result = str(number_1 - number_2)
    elif operation == 3:
        result = str(number_1 * number_2)
    elif operation == 4 and number_2 != 0:
        result = str(number_1 / number_2)
    else:
        result = 'Действие не поддерживается, вызывайте помощь'

    return result


@bot.message_handler()
def take_message(msg: telebot.types.Message):
    bot.send_message(chat_id=msg.from_user.id, text=f'Выберите, с какими числами будем работать?\n\
    1. Рациональные числа\n2. Комплексные числа')
    bot.register_next_step_handler(msg, take_type_number)


print('Бот запущен')

bot.polling()