import telebot
from telebot import types
import time

# connect to the telegram bot
t_file = open(r'C:\Users\48885\Documents\Python Knowledge\ThiBaut_t.txt')
token_id = t_file.read()
t_file.close()
all_con_types = ['text','audio','document','photo','sticker','video','video_note','voice','location','contact','new_chat_members','left_chat_member','new_chat_title','new_chat_photo','delete_chat_photo','group_chat_created','supergroup_chat_created','channel_chat_created','migrate_to_chat_id','migrate_from_chat_id','pinned_message']

 
bot = telebot.TeleBot(token_id)

# button definition
button_yes = types.InlineKeyboardButton('Да', callback_data='yes')
button_no = types.InlineKeyboardButton('Нет', callback_data='no')

yn_keyboard = types.InlineKeyboardMarkup()
yn_keyboard.add(button_yes)
yn_keyboard.add(button_no)

# class ForwardFilter(SimpleCustomFilter):
#     # Check whether message was forwarded from channel or group.
#     key = 'is_forwarded'

#     def check(self, message):
#         return message.forward_date is not None

# Add start command /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи. Напиши мне что-нибудь )')

# @bot.message_handler(content_types=["text"])
# def handle_text(message):
#     resp = ''
#     if message.forward_from_chat is not None: 
#         resp = str(message.forward_from_chat.username)
#     else:
#         resp = str(message.from_user.username)
#     # bot.send_message(message.chat.id, 'Вы написали: ' + message.text)
#     # bot.send_message(message.chat.id, 'Это отправлено: ' + str(message.from_user.username))
#     bot.send_message(message.chat.id, 'Это отправлено: ' + resp)
# message.forward_from.id


@bot.message_handler(content_types=all_con_types)
def handle_message(message):
    if message.forward_from_chat is not None:
        if message.forward_from_chat.type == 'channel':
            bot.send_message(message.chat.id, str(message.forward_from_chat.username) + '\n' + str(message.content_type))
            # bot.send_message(message.chat.id, text='Политота небось?', reply_markup=keyboard)
            bot.reply_to(message, text='Политота небось?', reply_markup=yn_keyboard)
            # bot.reply_to(message, 'reply')
    else:
        i = 1

# keyboard callback
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "yes":
        bot.answer_callback_query(call.id, "Да")
        bot.send_message(call.from_user.id, 'Ну держись за стул, начинаю перевоспитание')
        until_date = int( time.time() ) + 60
        bot.restrictChatMember(call.message.chat.id, call.message.from_user.id, call.ChatMember(can_send_other_messages = False), until_date)
        bot.send_message(call.from_user.id, call.message.from_user.username + ' забанен')
    elif call.data == "no":
        bot.answer_callback_query(call.id, "Нет")
        bot.send_message(call.from_user.id, 'Да? Обманываешь бота небось? Ну ладно')


bot.polling(none_stop=True, interval=0)




# @bot.message_handler(content_types=['text'])
# #@bot.message_handler(content_types=['text', 'document', 'audio'])
# def get_text_messages(message):
#
#     if message.text == "Привет":
#         return bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#     elif message.text == "/help":
#         return bot.send_message(message.from_user.id, "Напиши привет")
#     else:
#         return bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")