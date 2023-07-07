import json
import re
import telebot
from telebot import types
import logging

# Создание бота и установка API-токена
bot = telebot.TeleBot('')

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Определение состояний
states = {}

CLOSED_CHAT_ID_RESPONSIBLE = ''
CLOSED_CHAT_ID_VAHTA = ''

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.send_message(message.chat.id, 'Привет! Это тестовый бот !')
        # Установка начального состояния для пользователя
        states[message.chat.id] = {
            'name': None,
            'destination': None,
            'contact_person': None,
            'number': None
        }

        # Очищаем клавиатуру
        keyboard = types.ReplyKeyboardRemove()

        # Отправляем сообщение с предложением отправить ФИО
        bot.send_message(message.chat.id, 'Напиши свое ФИО полностью', reply_markup=keyboard)
    except Exception as e:
        logger.error(f'Error in start handler: {e}')

# Обработчик получения ФИО
@bot.message_handler(func=lambda message: states[message.chat.id]['name'] is None)
def get_name(message):
    try:
       # Сохраняем ФИО в состоянии пользователя
       states[message.chat.id]['name'] = message.text

       # Создаем клавиатуру
       keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
       keyboard.row(types.KeyboardButton('до верхушки'))
       keyboard.row(types.KeyboardButton('на склад'))

       # Отправляем сообщение с предложением отправить направление
       bot.send_message(message.chat.id, f'Привет, {message.text}! Куда направляешься?', reply_markup=keyboard)
    except Exception as e:
        logger.error(f'Error in get_name handler: {e}')

# Обработчик получения направления
@bot.message_handler(func=lambda message: states[message.chat.id]['destination'] is None)
def get_destination(message):
    try:
       # Сохраняем направление в состоянии пользователя
       states[message.chat.id]['destination'] = message.text

       # Создаем клавиатуру
       keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
       keyboard.row(types.KeyboardButton('Иванов И.И.'))
       keyboard.row(types.KeyboardButton('Петров П.П.'))
       keyboard.row(types.KeyboardButton('Сидоров С.С.'))

       # Отправляем сообщение с предложением отправить адресата
       bot.send_message(message.chat.id, 'К кому направляешься?', reply_markup=keyboard)
    except Exception as e:
        logger.error(f'Error in get_destination handler: {e}')

# Обработчик получения адресата
@bot.message_handler(func=lambda message: states[message.chat.id]['contact_person'] is None)
def get_contact_person(message):
    try:
       # Сохраняем имя в состоянии пользователя
       states[message.chat.id]['contact_person'] = message.text
       # Удаляем клавиатуру
       keyboard = types.ReplyKeyboardRemove()
       # Отправляем сообщение с предложением отправить номер машины
       bot.send_message(message.chat.id, 'Напишите номер вашей машины без пробелов.\nПример: С357ВМ25', reply_markup=keyboard)
    except Exception as e:
        logger.error(f'Error in get_contact_person handler: {e}')


# Обработчик получения направления
@bot.message_handler(func=lambda message: states[message.chat.id]['number'] is None)
def get_car_number(message):
 try:
    # Получаем номер машины из ответа и приводим его к нижнему регистру
    number = message.text.lower()
    # Проверяем формат номера машины с помощью регулярного выражения
    # Есть вариант использовать готовую библиотеку для проверки российских номеров.
    patterns = [
        r'^[авекмнорстухabekmhopctyx]\d{3}[авекмнорстухabekmhopctyx]{2}\d{2}$',  # Х000ХХ00
        r'^[авекмнорстухabekmhopctyx]\d{3}[авекмнорстухabekmhopctyx]{2}\d{3}$',  # Х000ХХ000
        r'^[авекмнорстухabekmhopctyx]\d{3}[авекмнорстухabekmhopctyx]{2}$',  # Х000ХХ
        r'^[авекмнорстухabekmhopctyx]{2}\d{6}$',  # Х000000
        r'^[авекмнорстухabekmhopctyx]{2}\d{7}$',  # Х0000000
        r'^\d{4}[авекмнорстухabekmhopctyx]{2}\d{2}$',  # 0000ХХ00
        r'^\d{4}[авекмнорстухabekmhopctyx]{2}\d{3}$',  # 0000ХХ000
        r'^[авекмнорстухabekmhopctyx]{2}\d{5}$',  # ХХ00000
        r'^[авекмнорстухabekmhopctyx]{2}\d{9}$',  # ХХ0000000
        r'^[авекмнорстухabekmhopctyx]{3}\d{5}$',  # ХХХ00000
        r'^[авекмнорстухabekmhopctyx]{3}\d{6}$',  # ХХХ000000
        r'^[авекмнорстухabekmhopctyx]{2}\d{6}$',  # ХХ000000
        r'^[авекмнорстухabekmhopctyx]{2}\d{7}$',  # ХХ0000000
        r'^[авекмнорстухabekmhopctyx]{2}\d{8}$',  # ХХ00000000
    ]
    # Проверяем, соответствует ли введенный номер одному из указанных паттернов
    if not any(re.match(pattern, number) for pattern in patterns):
        bot.send_message(message.chat.id,
                         'Введенный вами номер машины некорректен. Попробуйте еще раз.')
        # Отправляем вопрос о номере машины и просим пользователя ввести его
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, 'Напишите номер вашей машины без пробелов.\nПример: С357ВМ25',
                         reply_markup=keyboard)
        return

    # Сохраняем номер авто пользователя
    states[message.chat.id]['number'] = message.text
    # Получаем данные пользователя из состояния
    name = states[message.chat.id]['name']
    destination = states[message.chat.id]['destination']
    contact_person = states[message.chat.id]['contact_person']
    number = states[message.chat.id]['number']

    bot.send_message(message.chat.id,
                     f'Ваш запрос:\n{name}\nНаправляетесь {destination}\nК {contact_person}\nНомер авто: {number}')
    # Создаем клавиатуру
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton('Начать заново'))
    keyboard.row(types.KeyboardButton('Отправить'))

    # Отправляем сообщение с выбором действия
    bot.send_message(message.chat.id, 'Выберете действие', reply_markup=keyboard)
 except Exception as e:
        logger.error(f'Error in get_car_number handler: {e}')

# Обработчик нажатия кнопки куда от пользователя
@bot.message_handler(func=lambda message: message.text == 'Отправить')
def send_greeting(message):
 try:
    # Сохраняем идентификатор пользователя
    user_id = message.from_user.id
    # Получаем данные пользователя из состояния
    name = states[message.chat.id]['name']
    destination = states[message.chat.id]['destination']
    contact_person = states[message.chat.id]['contact_person']
    number = states[message.chat.id]['number']

    # Создаем клавиатуру с кнопками "Принять" и "Отказать"
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton('Принять', callback_data=json.dumps({'message': 'accept', 'user': user_id})),
        types.InlineKeyboardButton('Отказать', callback_data=json.dumps({'message': 'reject', 'user': user_id}))
    )

    # Формируем сообщение с информацией о направлении и имени пользователя
    text = f'{name} направляется {destination} к {contact_person}\nНомер автомобиля:{number}'

    # Отправляем сообщение в закрытую группу с кнопками
    bot.send_message(chat_id=CLOSED_CHAT_ID_RESPONSIBLE, text=text, reply_markup=keyboard)

    # Удаляем клавиатуру
    keyboard = types.ReplyKeyboardRemove()
    # Отправляем пользователю сообщение с информацией ожидания ответа
    bot.send_message(user_id, 'Ожидайте ответа...', reply_markup=keyboard)
 except Exception as e:
        logger.error(f'Error in send_request handler: {e}')

# Обработчик нажатия кнопок "Принять" и "Отказать" в закрытой группе
@bot.callback_query_handler(func=lambda call: str(call.message.chat.id) == CLOSED_CHAT_ID_RESPONSIBLE)
def handle_group_button_click(call):
 try:
    data = json.loads(call.data)

    # Создаем клавиатуру
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton('Начать заново'))

    if 'accept' == data['message']:
        accept_message = f'{call.message.text}\n\nОдобрено пользователем {call.from_user.first_name}'
        # Отправляем ответ пользователю
        bot.send_message(data['user'], accept_message, reply_markup=keyboard)
        # Отправляем ответ на вахту
        bot.send_message(chat_id=CLOSED_CHAT_ID_VAHTA, text=accept_message)
        # Отправляем ответ отвественным
        bot.send_message(chat_id=CLOSED_CHAT_ID_RESPONSIBLE, text=accept_message)


    elif 'reject' == data['message']:
        reject_message = f'{call.message.text}\n\nОтказано пользователем {call.from_user.first_name}'
        # Отправляем ответ пользователю
        bot.send_message(data['user'], reject_message, reply_markup=keyboard)
        # Отправляем ответ отвественным
        bot.send_message(chat_id=CLOSED_CHAT_ID_RESPONSIBLE, text=reject_message)


    # Удаляем кнопки из сообщения в группе
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
 except Exception as e:
    logger.error(f'Error in handle_group_button_click handler: {e}')

# Обработчик нажатия кнопки "Начать заново"
@bot.message_handler(func=lambda message: message.text == 'Начать заново')
def restart(message):
    try:
        # Сброс всех состояний и данных
        states.clear()

        # Вызываем команду /start
        start(message)
    except Exception as e:
        logger.error(f'Error in restart handler: {e}')

# Запуск бота
bot.infinity_polling()
