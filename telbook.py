import telebot
import os.path
import requests

API_TOKEN = '5783465400:AAF6AcEbdTMLRweW05bkwCLip8DU3EQ_ohw'
TEL_BASE_PATH = './tel_base/'
MENU_TEXT = 'Выберите пункт меню:\n1. Показать все контакты\n2. Добавить контакт\n3. Импортировать из файла\n4. Экспортировать в файл\n5. Поиск по контактам'
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def bot_start(msg: telebot.types.Message):
    file_name = TEL_BASE_PATH + str(msg.from_user.id) + '.txt'
    if not os.path.exists(file_name):
        data = open(file_name, mode='w+')
        data.close()
    users_book = upload(file_name)
    bot.send_message(chat_id=msg.from_user.id, text=f'{msg.from_user.full_name}!\nЗаписей в книге: {len(users_book)}')
    bot.send_message(chat_id=msg.from_user.id, text=MENU_TEXT)
    bot.register_next_step_handler(msg, bot_menu)


def bot_menu(msg: telebot.types.Message):
    file_name = TEL_BASE_PATH + str(msg.from_user.id) + '.txt'
    if msg.text in {'1', '2', '3', '4'}:
        match msg.text:
            case '1':
                bot.send_message(chat_id=msg.from_user.id, text=f'{show_list(upload(file_name))}')
                bot.send_message(chat_id=msg.from_user.id, text=MENU_TEXT)
                bot.register_next_step_handler(msg, bot_menu)
            case '2':
                bot.send_message(chat_id=msg.from_user.id, text=f'Введите данные контакта через запятую\n<Фамилия,Имя,Телефон,Описание>')
                bot.register_next_step_handler(msg, add_contact)
            case '3':
                bot.send_message(chat_id=msg.from_user.id, text=f'Прикрепите файл к следующему сообщению')
                bot.register_next_step_handler(msg, add_box_contact)
            case '4':
                data = open(file_name, mode='r', encoding='utf-8')
                bot.send_document(chat_id=msg.from_user.id, document=data)
                bot.send_message(chat_id=msg.from_user.id, text=MENU_TEXT)
                bot.register_next_step_handler(msg, bot_menu)
            case '5':
                bot.send_message(chat_id=msg.from_user.id, text=f'Введите поисковый запрос')
                bot.register_next_step_handler(msg, find_request)
    else:
        bot.send_message(chat_id=msg.from_user.id, text=f'Ошибка, выберите пункт от 1 до 4')
        bot.register_next_step_handler(msg, bot_menu)


def add_box_contact(msg: telebot.types.Message):
    file_name = TEL_BASE_PATH + str(msg.from_user.id) + '.txt'
    file_info = bot.get_file(msg.document.file_id)
    data = requests.get(f'https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}')
    bot.send_message(chat_id=msg.from_user.id, text=data.text)
    zap_tmp = data.text.split('\r\n')
    zap_knig = []
    if '' in zap_tmp:
        empty_str = -1
        zap_tmp.append('')
        for index, i in enumerate(zap_tmp):
            if i == '':
                zap_knig.append(zap_tmp[empty_str+1:index])
                empty_str = index
    else:
        for zap in zap_tmp:
            zap_knig.append(zap.split(','))
    for zap in zap_tmp:
        zap_knig.append(zap.split(','))
    bot.send_message(chat_id=msg.from_user.id, text=f'Получены записи\n{show_list(zap_knig)}')
    zap_knig.extend(upload(file_name))
    tel_download(file_name, zap_knig)
    bot.send_message(chat_id=msg.from_user.id, text=MENU_TEXT)
    bot.register_next_step_handler(msg, bot_menu)


def add_contact(msg: telebot.types.Message):
    file_name = TEL_BASE_PATH + str(msg.from_user.id) + '.txt'
    tmp = upload(file_name)
    zapros = msg.text.split(',')
    tmp.append(zapros)
    tel_download(file_name, tmp)
    bot.send_message(chat_id=msg.from_user.id, text=f'Запись добавлена')
    bot.send_message(chat_id=msg.from_user.id, text=MENU_TEXT)
    bot.register_next_step_handler(msg, bot_menu)


def find_request(msg: telebot.types.Message):
    file_name = TEL_BASE_PATH + str(msg.from_user.id) + '.txt'
    zapros = msg.text
    tmp = [i for i in upload(file_name) if zapros in i[0] or zapros in i[1]]
    bot.send_message(chat_id=msg.from_user.id, text=f'Найдено {len(tmp)} записей')
    bot.send_message(chat_id=msg.from_user.id, text=f'{show_list(tmp)}')
    bot.send_message(chat_id=msg.from_user.id, text=MENU_TEXT)
    bot.register_next_step_handler(msg, bot_menu)


#чтение из файла
def upload(file_name):
    zap_tmp = []
    with open(file_name, mode='r', encoding='utf-8') as data:
        for line in data:
            zap_tmp.append(line.replace('\n', ''))
    zap_knig = []
    if '' in zap_tmp:
        empty_str = -1
        zap_tmp.append('')
        for index, i in enumerate(zap_tmp):
            if i == '':
                zap_knig.append(zap_tmp[empty_str+1:index])
                empty_str = index
    else:
        for zap in zap_tmp:
            zap_knig.append(zap.split(','))
    return zap_knig


#вывод списка
def show_list(list_data):
    exp_list_data = ''
    derevo = \
        {
            0: 'Фамилия',
            1: 'Имя',
            2: 'Телефон',
            3: 'Описание'
        }
    for index, i in enumerate(list_data):
        exp_list_data += '#' + str(index + 1) + '\n'
        for jindex, j in enumerate(i):
            exp_list_data += str(derevo[jindex]) + ': ' + str(j) + '\n'
    return exp_list_data


#сохранение в файл
def tel_download(file_name, telbook):
    with open(file_name, mode='w+', encoding='utf-8') as data:
        uploaded_list = [f'{",".join(key)}' for key in telbook]
        uploaded_str = '\n'.join(uploaded_list)
        data.write(uploaded_str)


print('Бот запущен')

bot.polling()