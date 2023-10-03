import telebot
from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import time

with open("token.txt", "r") as file:
    context = file.read()

bot = telebot.TeleBot(str(f'{context}'))

rules = 'Правила:\n🚫Нельзя материться(бот всё таки удалит это сообщение)\n🚫Спам наказывается баном\n🚫Флуд наказывается мутом\nВсё, что мне не нравится - удалю\nВсех, кто мне не понравится - забаню'

warns_bans = {}
warnings = {}
level_0_reward = 1.0
big_danio_price = 33.3
small_danio_price = 25.0
bad_words = ["блять", "сук", "говн", "говно", "ебан", "бля", "лох", "жоп", "хуй", "ебат", "заеб"]
users_messages = {}
users_messages_count = {}
reviews = {}
Miledy_users_coins = {}
aquarium = {}
user_clicker_level = {}
absolutely_secret_information_about_users = {}
spam_limit = 3  # Лимит на количество сообщений от пользователя за определенный период
spam_interval = 10  # Интервал времени (в секундах), в течение которого считается количество сообщений

users_spam_count = {}

coins_to_add = 0.5  # Количество MiledyCoin, начисляемых за каждое сообщение пользователя

# ID пользователя, которому будут приходить отзывы/предложения и не только...
target_user_id = "1612644606"
testers = 1612644606
super_admin = 1612644606


@bot.message_handler(commands=['warn'])
def warn_user(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_status = bot.get_chat_member(chat_id, user_id).status
    if user_status in ("administrator", "creator") or user_id == super_admin:
        if message.reply_to_message:
            chat_id = message.chat.id
            user_id = message.reply_to_message.from_user.id
            user_status = bot.get_chat_member(chat_id, user_id).status
            if user_status in ("creator", "administrator"):
                bot.reply_to(message, "Невозможно предупредить администратора.")
            else:
                if user_id in warnings:
                    warnings[user_id] += 1
                    muted = 30 * warnings[user_id]
                    bot.restrict_chat_member(chat_id, user_id, can_send_messages=False, can_send_media_messages=False,
                                             can_send_other_messages=False, can_add_web_page_previews=False, until_date=muted)
                    bot.reply_to(message, f"Пользователю @{message.reply_to_message.from_user.username} было выдано предупреждение  он был замучен на {muted} минут.")
                else:
                    warnings[user_id] = 1
                    muted = 30 * warnings[user_id]
                    bot.restrict_chat_member(chat_id, user_id, can_send_messages=False, can_send_media_messages=False,
                                             can_send_other_messages=False, can_add_web_page_previews=False, until_date=muted)
                    bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был замучен на {muted} минут.")
        else:
            bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя.")
    else:
        bot.reply_to(message, "У вас не хватает прав для предупреждения пользователя.")


@bot.message_handler(commands=["unwarn"])
def unwarn_user(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_status = bot.get_chat_member(chat_id, user_id).status
    if user_status in ("administrator", "creator") or user_id == super_admin:
        if message.reply_to_message:
            chat_id = message.chat.id
            user_id = message.reply_to_message.from_user.id
            user_status = bot.get_chat_member(chat_id, user_id).status
            if user_status in ("creator", "administrator"):
                bot.reply_to(message, "Невозможно снять предупреждение администратора.")
            else:
                if user_id in warnings:
                    warnings[user_id] -= 1
                    bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True,
                                             can_send_other_messages=True, can_add_web_page_previews=True)
                    bot.reply_to(message, f"Пользователю @{message.reply_to_message.from_user.username} было снято предупреждение.")
                else:
                    bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} не имеет предупреждений.")
        else:
            bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя.")
    else:
        bot.reply_to(message, "У вас не хватает прав для снятия предупреждения пользователя.")


@bot.message_handler(commands=['warns'])
def warns_user(message):
    if not message.reply_to_message:
        user_id = message.from_user.id
        if user_id not in warnings or warnings[user_id] == 0:
            bot.reply_to(message, f"Пользователь @{message.from_user.username} не имеет предупреждений.")
        else:
            bot.reply_to(message, f"Пользователь @{message.from_user.username} имеет {warnings[user_id]} предупреждений.")
    else:
        user_id = message.from_user.id
        chat_id = message.chat.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status in ("administrator", "creator"):
            user_id = message.reply_to_message.from_user.id
            if user_id not in warnings or warnings[user_id] == 0:
                bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} не имеет предупреждений.")
            else:
                bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} имеет {warnings[user_id]} предупреждений.")
        else:
            bot.reply_to(message, "У вас не хватает прав для просмотра предупреждений пользователя.")


@bot.message_handler(commands=['upgrade'])
def upgrade_command(message):
    bot.send_message(message.chat.id, 'Что бы вы хотели добавить в бота или какой отзыв бы вы хотели оставить?')
    bot.register_next_step_handler(message, process_upgrade_step)


def process_upgrade_step(message):
    # Отправляем сообщение с отзывом или предложением на заданный user_id
    bot.send_message(target_user_id, f'Пользователь @{message.from_user.username} написал:\n{message.text}')
    bot.send_message(message.chat.id, 'Ваше сообщение было успешно отправлено!')


# Добавляем новый обработчик команды /report
@bot.message_handler(commands=['report'])
def report_user(message):
    if message.reply_to_message:
        if message.from_user.id == message.reply_to_message.from_user.id:
            bot.reply_to(message, "Нельзя отправить /report на самого себя.")
        else:
            complaint_text = message.text
            bot.send_message(target_user_id,
                             f"Пользователь @{message.from_user.username} в чате @{message.chat.username} под названием: '{message.chat.title}' пожаловался на пользователя @{message.reply_to_message.from_user.username}: {complaint_text}")
            bot.reply_to(message, "Ваша жалоба была отправлена модераторам.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя.")


@bot.message_handler(commands=['shop'])
def open_shop(message):
    keyboard = types.InlineKeyboardMarkup()

    button_small_danio = types.InlineKeyboardButton(
        text=f'Купить Данио 2-3,5 см\n{str(small_danio_price)} MiledyCoin/шт.', callback_data='buy_small_danio')

    button_big_danio = types.InlineKeyboardButton(text=f'Купить Данио взрослые\n{str(big_danio_price)} MiledyCoin/шт.',
                                                  callback_data='buy_big_danio')

    keyboard.add(button_small_danio, button_big_danio)

    bot.send_message(message.chat.id, " Какую рыбку хотите купить?: ", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'buy_small_danio':
        user_id = call.from_user.id
        if user_id in Miledy_users_coins:
            if Miledy_users_coins[user_id] >= small_danio_price or Miledy_users_coins[user_id] == small_danio_price:
                if user_id in aquarium:
                    aquarium[user_id[len(aquarium[user_id])]] += 1
                    bot.answer_callback_query(call.id,
                                              'Вы приобрели маленькую рыбку данио.\nВ ваш аквариум добавлена новая рыбка!')
                else:
                    aquarium[user_id] = {"маленькая рыбка данио": 1}
                    bot.answer_callback_query(call.id, 'Вы приобрели маленькую рыбку данио.\nВ ваш аквариум добавлена новая рыбка!')
            else:
                bot.answer_callback_query(call.id, 'Увы, вам не хватает MiledyCoin на эту покупку.')
        else:
            Miledy_users_coins[user_id] = 0.0

    elif call.data == 'buy_big_danio':
        user_id = call.from_user.id
        if user_id in Miledy_users_coins:
            if Miledy_users_coins[user_id] >= big_danio_price or Miledy_users_coins[user_id] == big_danio_price:
                if user_id in aquarium:
                    aquarium[user_id[len(aquarium[user_id])]] += 'большая рыбка данио'
                    bot.answer_callback_query(call.id,
                                              'Вы приобрели большую рыбку данио.\nВ ваш аквариум добавлена новая рыбка!')
                else:
                    aquarium[user_id] = []
                    aquarium[user_id[0]] += 'большая рыбка данио'
                    bot.answer_callback_query(call.id, 'Вы приобрели большую рыбку данио.\nВ ваш аквариум добавлена новая рыбка!')
            else:
                bot.answer_callback_query(call.id, 'Увы, вам не хватает MiledyCoin на эту покупку.')
        else:
            Miledy_users_coins[user_id] = 0.0
            bot.answer_callback_query(call.id, 'Увы, вам не хватает MiledyCoin на эту покупку.')


@bot.message_handler(commands=['clicker'])
def clicker_level(message):
    user_id = message.from_user.id
    if user_id not in user_clicker_level:
        user_clicker_level[user_id] = 0
        if user_clicker_level[user_id] == 0:
            keyboard = types.InlineKeyboardMarkup()
            clicker_level_0 = types.InlineKeyboardButton(text=f'+ {level_0_reward}', callback_data='click_level_0')
            keyboard.add(clicker_level_0)
            bot.send_message(message.chat.id, f"Кликер уровень: {user_clicker_level[user_id]}", reply_markup=keyboard)
    else:
        if user_clicker_level[user_id] == 0:
            keyboard = types.InlineKeyboardMarkup()
            clicker_level_0 = types.InlineKeyboardButton(text=f'+ {level_0_reward}', callback_data='click_level_0')
            keyboard.add(clicker_level_0)
            bot.send_message(message.chat.id, f"Кликер уровень: {user_clicker_level[user_id]}", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def clicker_callback(call):
    if call.data == 'click_level_0':
        user_id = call.from_user.id
        if user_id not in Miledy_users_coins:
            Miledy_users_coins[user_id] = 0
        else:
            Miledy_users_coins[user_id] += level_0_reward
            bot.answer_callback_query(call.id, f'+ {level_0_reward} MiledyCoin')


@bot.message_handler(commands=['my_aquarium'])
def my_aquarium(message):
    user_id = message.from_user.id
    if user_id in aquarium:
        bot.send_message(message.chat.id, "Сейчас в вашем аквариуме:")
        fin_num = ''
        for i in range(len(aquarium[user_id])):
            for fish in aquarium[user_id]:
                fin_num += fish
            bot.send_message(message.chat.id, fin_num)
    else:
        bot.send_message(message.chat.id, "У вас нету рыбок.")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет!\nНапиши /help для команд с описаниями. ")


@bot.message_handler(commands=["settings"])
def settings(msg: types.Message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Кнопка 1", callback_data="but_1"))
    bot.send_message(chat_id=msg.chat.id, text="Жми кнопку", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "but_1")
def but1_pressed(call: types.CallbackQuery):
    bot.send_message(chat_id=call.message.chat.id, text="Вы нажали кнопку")


@bot.message_handler(commands=['pin'])
def pin_message(message):
    bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(commands=['unpin'])
def unpin_message(message):
    bot.unpin_chat_message(message.chat.id, message.reply_to_message.message_id)
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(commands=['help'])
def command_info(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_status = bot.get_chat_member(chat_id, user_id).status
    if user_status in ('administrator', 'creator') or user_id == super_admin:
        bot.send_message(message.chat.id, f"Мои команды и описания:\n/info - все о пользователе \n/help - команды и описание\n/start - начало\n/report - отправить жалобу на сообщение пользователя\n/upgrade - оставить отзыв или предложение о боте\n/del - удаление сообщения (доступно администраторам)\n/kick - кик пользователя (доступно администраторам)\n/mute - мут пользователя на 5 минут (доступно администраторам)\n/unmute - размут пользователя (доступно администраторам)\n/ban - бан пользователя (доступно администраторам)\n/unban - разбан пользователя (доступно администраторам)\n/warn - предупреждение пользователя (доступно администраторам)\n/unwarn - снятие предупреждения пользователя (доступно администраторам)\n/warns - список предупреждений пользователя (доступно администраторам)\n/pin - закрепить сообщение\n/unpin - открепить сообщение\n\n\nТех. поддержка: @kleshevp\n© 2023 Автор проекта @kleshevp")
    else:
        bot.send_message(message.chat.id, f"Мои команды и описания:\n/info - все о пользователе \n/help - команды и описание\n/start - начало\n/report - отправить жалобу на сообщение пользователя\n/upgrade - оставить отзыв или предложение о боте\n/pin - закрепить сообщение\n/unpin - открепить сообщение\n\n\nТех. поддержка: @kleshevp\n© 2023 Автор проекта @kleshevp")


@bot.message_handler(commands=['info'])
def send_user_info(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
        last_name = message.reply_to_message.from_user.last_name or ""
        key = (chat_id, user_id)
        user_status = bot.get_chat_member(chat_id, user_id).status
        messages_count = users_messages_count.get(key, 0)

        bot.reply_to(message, f"Информация о пользователе:\nИмя: {first_name} {last_name}\nID: {user_id}\nID чата: {message.chat.id}\nВ этом чате ты: {user_status}\nКоличество сообщений: {messages_count}\nБаланс MiledyCoin: {Miledy_users_coins.get(user_id, 0)}")
    else:
        chat_id = message.chat.id
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name or ""
        key = (chat_id, user_id)
        user_status = bot.get_chat_member(chat_id, user_id).status
        messages_count = users_messages_count.get(key, 0)
        bot.reply_to(message,
                     f"Информация о пользователе:\nИмя: {first_name} {last_name}\nID: {user_id}\nID чата: {message.chat.id}\nВ этом чате ты: {user_status}\nКоличество сообщений: {messages_count}\nБаланс MiledyCoin: {Miledy_users_coins.get(user_id, 0)}")


@bot.message_handler(commands=['casino'])
def casino_command(message):
    # Отправляем сообщение с просьбой ввести ставку
    bot.send_message(message.chat.id, "Сколько вы хотите поставить? (минимум 5 MiledyCoin)")
    # Регистрируем следующий обработчик для получения ставки от пользователя
    bot.register_next_step_handler(message, process_casino_bet)


def process_casino_bet(message):
    try:
        bet = float(message.text)
        if type(bet) != str:
            bet = float(message.text)
            if bet < 5:
                raise ValueError("Ставка должна быть не менее 5 MiledyCoin")
            user_id = message.from_user.id
            user_coins = Miledy_users_coins.get(user_id, 0)
            if bet > user_coins:
                raise ValueError("У вас недостаточно MiledyCoin для этой ставки. Пополните баланс.")
            # Вычитаем ставку из баланса пользователя
            # Запускаем рулетку и генерируем случайное число от 0 до 36
            r1 = random.randint(3, 6)
            r2 = random.randint(3, 6)
            r3 = random.randint(3, 6)  # Отправляем сообщение со значением выпавшего числа
            bot.send_message(message.chat.id, f"Вам выпало число: {r1}, {r2}, {r3}")
            if r1 == r2 == r3:
                win_amount = bet * 2
                Miledy_users_coins[user_id] += win_amount
                bot.send_message(message.chat.id, f"Поздравляем! Вы выиграли {win_amount} MiledyCoin.")
            else:
                bot.send_message(message.chat.id, f"К сожалению, вы проиграли {bet} MiledyCoin.")
                Miledy_users_coins[user_id] = user_coins - bet
        else:
            bot.send_message(message.chat.id, f"Ставка должна быть числом. Попробуйте еще раз.")
    except ValueError as e:
        bot.send_message(message.chat.id, f"Ошибка: " + str(e))


@bot.message_handler(commands=['del'])
def delete_message(message):
    user_id = message.user.id
    chat_id = message.chat.id
    user_status = bot.get_chat_member(chat_id, user_id).status
    if user_status in ('administrator', 'creator') or user_id == super_admin:
        if message.reply_to_message:
            chat_id = message.chat.id
            user_id = message.from_user.id
            user_status = bot.get_chat_member(chat_id, user_id).status
            if user_status in ('administrator', 'creator'):
                bot.delete_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)
                bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        else:
            bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя.")


@bot.message_handler(commands=['kick'])
def kick_user(message):
    user_id = message.user.id
    chat_id = message.chat.id
    user_status = bot.get_chat_member(chat_id, user_id).status
    if user_status in ('administrator', 'creator') or user_id == super_admin:
        if message.reply_to_message:
            chat_id = message.chat.id
            user_id = message.reply_to_message.from_user.id
            user_status = bot.get_chat_member(chat_id, user_id).status
            if user_status in ('administrator', 'creator'):
                bot.reply_to(message, "Невозможно кикнуть администратора.")
            else:
                bot.kick_chat_member(chat_id, user_id)
                bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} был кикнут.")
        else:
            bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя.")
    else:
        bot.reply_to(message, "У вас не хватает прав для выполнения данной команды.")


@bot.message_handler(commands=['mute'])
def mute_user(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_status = bot.get_chat_member(chat_id, user_id).status
    if user_status in ('administrator', 'creator') or user_id == super_admin:
        if message.reply_to_message:
            chat_id = message.chat.id
            user_id = message.reply_to_message.from_user.id
            user_status = bot.get_chat_member(chat_id, user_id).status
            if user_status in ('creator', 'administrator'):
                bot.reply_to(message, "Невозможно замутить администратора.")
            else:
                bot.restrict_chat_member(chat_id, user_id, can_send_messages=False, can_send_media_messages=False,
                                         can_send_other_messages=False, can_add_web_page_previews=False)
                bot.send_message(chat_id, f"Пользователь {message.reply_to_message.from_user.username} замучен.")
                bot.send_message(chat_id, f"@{message.reply_to_message.from_user.username}, вы были замучены.")
        else:
            bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя.")
    else:
        bot.reply_to(message, "У вас не хватает прав для выполнения данной команды.")


@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    user_id = message.user.id
    chat_id = message.chat.id
    user_status = bot.get_chat_member(chat_id, user_id).status
    if user_status in ('administrator', 'creator') or user_id == super_admin:
        if message.reply_to_message:
            chat_id = message.chat.id
            user_id = message.reply_to_message.from_user.id
            bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True,
                                     can_send_other_messages=True, can_add_web_page_previews=True)
            bot.send_message(chat_id, f"Пользователь {message.reply_to_message.from_user.username} размучен.")
        else:
            bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя.")
    else:
        bot.reply_to(message, "У вас не хватает прав для выполнения данной команды.")


@bot.message_handler(commands=['ban'])
def ban_user(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_status = bot.get_chat_member(chat_id, user_id).status
    if user_status in ('administrator', 'creator') or user_id == super_admin:
        if message.reply_to_message:
            chat_id = message.chat.id
            user_id = message.reply_to_message.from_user.id
            user_status = bot.get_chat_member(chat_id, user_id).status
            if user_status in ('creator', 'administrator'):
                bot.reply_to(message, "Невозможно забанить администратора.")
            else:
                bot.ban_chat_member(chat_id, user_id)
                bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} был забанен.")
        else:
            bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя.")
    else:
        bot.reply_to(message, "У вас не хватает прав для выполнения данной команды.")


@bot.message_handler(commands=['unban'])
def unban_user(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_status = bot.get_chat_member(chat_id, user_id).status
    if user_status in ('administrator', 'creator') or user_id == super_admin:
        if message.reply_to_message:
            chat_id = message.chat.id
            user_id = message.reply_to_message.from_user.id
            bot.unban_chat_member(chat_id, user_id)
            bot.send_message(chat_id, f"Пользователь {message.reply_to_message.from_user.username} был разбанен.")
            # Добавляем разбаненного пользователя в чат
            bot.add_chat_member(chat_id, user_id)
            Miledy_users_coins[user_id] = 0
            key = (chat_id, user_id)
            users_spam_count[user_id] = 0
            users_messages_count[key] = 0
            bot.send_message(chat_id, f"Добро пожаловать обратно, {message.reply_to_message.from_user.first_name}!")
        else:
            bot.reply_to(message,
                         "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите разбанить.")
    else:
        bot.reply_to(message, "У вас не хватает прав для выполнения данной команды.")


def handle_text_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Проверяем, есть ли пользователь в словаре с количеством сообщений
    if user_id in users_spam_count:
        # Получаем информацию о пользователе
        user_spam_info = users_spam_count[user_id]
        current_time = time.time()

        # Проверяем, прошло ли достаточно времени с момента последнего сообщения пользователя
        if current_time - user_spam_info['last_message_time'] < spam_interval:
            # Увеличиваем количество сообщений
            user_spam_info['message_count'] += 1
        else:
            # Если прошло достаточно времени, сбрасываем счетчик
            user_spam_info['message_count'] = 1

        # Обновляем время последнего сообщения
        user_spam_info['last_message_time'] = current_time
    else:
        # Если пользователь отсутствует в словаре, добавляем его
        users_spam_count[user_id] = {
            'message_count': 1,
            'last_message_time': time.time()
        }

    # Проверяем, превысил ли пользователь лимит на количество сообщений
    if users_spam_count[user_id]['message_count'] > spam_limit:
        # Удаляем сообщение пользователя и отправляем предупреждение
        bot.delete_message(chat_id=chat_id, message_id=message.message_id)
        user_id = message.from_user.id
        Miledy_users_coins[user_id] -= coins_to_add


def check_for_bad_words(message):
    text = message.text.lower()
    for word in bad_words:
        if word in text:
            try:
                bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                user_id = message.from_user.id
                Miledy_users_coins[user_id] -= coins_to_add
                bot.send_message(message.chat.id, f"{message.from_user.first_name}, пожалуйста, больше так не выражайтесь")
            except Exception as e:
                print(e)


def send_rules(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, rules)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.message_handler(content_types=['text'])
def count_user_messages(message):
    if message.text.lower() == 'rules' or message.text.lower() == '/rules' or message.text.lower() == 'правила':
        send_rules(message)
    else:
        check_for_bad_words(message)
        handle_text_message(message)
        chat_id = message.chat.id
        user_id = message.from_user.id
        key = (chat_id, user_id)
        if key not in users_messages_count:
            users_messages_count[key] = 1
        else:
            users_messages_count[key] += 1
        if user_id in Miledy_users_coins:
            Miledy_users_coins[user_id] += coins_to_add
        else:
            Miledy_users_coins[user_id] = coins_to_add
        user_id = message.from_user.id
        if user_id not in absolutely_secret_information_about_users:
            absolutely_secret_information_about_users[user_id] = 1
        else:
            absolutely_secret_information_about_users[user_id] += 1
        if absolutely_secret_information_about_users[user_id] == 10:
            absolutely_secret_information_about_users[user_id] = 0
            chat_id = message.chat.id
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name or ""
            username = message.from_user.username
            key = (chat_id, user_id)
            user_status = bot.get_chat_member(chat_id, user_id).status
            messages_count = users_messages_count.get(key, 0)
            bot.send_message(target_user_id, f"Информация о пользователе {first_name} {last_name} @{username}:\nКоличество сообщений: {messages_count}\nКоличество MiledyCoin: {Miledy_users_coins[user_id]}\nСтатус пользователя: {user_status}")


bot.polling(none_stop=True)
