import telebot
from telebot import types
import time
import csv

# connect to the telegram bot
t_file = open(r'C:\Users\48885\Documents\Python Knowledge\ThiBaut_t.txt')
token_id = t_file.read()
t_file.close()
all_con_types = ['text','audio','document','photo','sticker','video','video_note','voice','location','contact','new_chat_members','left_chat_member','new_chat_title','new_chat_photo','delete_chat_photo','group_chat_created','supergroup_chat_created','channel_chat_created','migrate_to_chat_id','migrate_from_chat_id','pinned_message']

list_from_user_id = []
# dict_user_rep = {}
dict_channel_block = {}
set_channel_block = set()
list_channel_block = []

bot = telebot.TeleBot(token_id)

# button definition
button_yes = types.InlineKeyboardButton('Да', callback_data='yes')
button_no = types.InlineKeyboardButton('Нет', callback_data='no')

yn_keyboard = types.InlineKeyboardMarkup()
yn_keyboard.add(button_yes)
yn_keyboard.add(button_no)

# Function to add key:value
def dict_add(channel, user):
    if channel in dict_channel_block:
        if user not in dict_channel_block[channel]:
              dict_channel_block[channel].append(user)
    else:
        dict_channel_block[channel] = [user]

# update list of blocked channels
def block_list_update(list_channel_block):
    with open(r'C:\Users\48885\Documents\Python Knowledge\block_list.csv') as block_file:
        reader = block_file.read().strip("'")
        # reader = csv.reader(block_file)
        if reader:
            if len(reader.split()) >0:
                for row in reader.split():
                    if row.strip("'") not in list_channel_block:
                        list_channel_block.append(row)
    block_file.close()
    if len(list_channel_block) > 0:
        with open(r'C:\Users\48885\Documents\Python Knowledge\block_list.csv', 'w+', newline = '') as block_file:
            # writer = csv.DictWriter(block_file, fieldnames=['id', 'title'])
            # writer = csv.writer(block_file, dialect='excel')
            # writer.writeheader()
            # writer.writerow(set_channel_block)
            # for row in list_channel_block:
            #     writer.writerow(row)
            #     print(row)
            block_file.writelines(str(item) + '\n' for item in list_channel_block)
            # for item in list_channel_block:
            #     block_file.writelines(str(item))
    block_file.close()

# update list of blocked channels (dictionary)
def block_list_update_ext(dict_channel_block):
    # with open(r'C:\Users\48885\Documents\Python Knowledge\block_list_ext.csv') as block_file:
    with open("C:/Users/48885/Documents/Python Knowledge/block_list_ext.csv") as block_file:
        # reader = block_file.read()
        csvreader = csv.reader(block_file)
        next(csvreader)
        # if len(csvreader.split()) >0:
        for row in csvreader:
            dict_add(row[0], row[1])
    block_file.close()
    with open(r'C:\Users\48885\Documents\Python Knowledge\block_list_ext.csv', 'w', newline = '') as block_file:
        writer = csv.DictWriter(block_file, fieldnames=['id', 'vote'])
        writer.writeheader()
        for k, v in dict_channel_block.items():
            writer.writerow({'id': k, 'vote': v})
    block_file.close()

block_list_update_ext(dict_channel_block)




def remove_blocked_posts(list_channel_block):
    i = 1


# class ForwardFilter(SimpleCustomFilter):
#     # Check whether message was forwarded from channel or group.
#     key = 'is_forwarded'

#     def check(self, message):
#         return message.forward_date is not None

# Add start command /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я борюсь с политотой в отдельно взятом чате )')

@bot.message_handler(content_types=all_con_types)
def handle_message(message):
    if message.forward_from_chat is not None:
        if message.forward_from_chat.type == 'channel':
            # bot.send_message(message.chat.id, str(message.forward_from_chat.username) + '\n' + str(message.content_type))
            # bot.send_message(message.chat.id, text='Политота небось?', reply_markup=keyboard)
            if str(message.forward_from_chat.id) in dict_channel_block:
                # remove message
                bot.delete_message(message.chat.id, message_id=message.id)
            else:
                bot.reply_to(message, text='Политота небось?', reply_markup=yn_keyboard)

# keyboard callback
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "yes":
        bot.answer_callback_query(call.id, "Да")
        
        if str(call.message.reply_to_message.forward_from_chat.id) not in dict_channel_block:
            dict_add(call.message.reply_to_message.forward_from_chat.id, call.from_user.username)
            # dict_channel_block[call.message.reply_to_message.forward_from_chat.id] = call.message.reply_to_message.forward_from_chat.title
            block_list_update_ext(dict_channel_block)
            bot.send_message(call.message.chat.id, call.message.reply_to_message.forward_from_chat.title + ', давай до свидания!')
        else: 
            bot.send_message(call.message.chat.id, 'Канал уже в стоп-листе')

        

    elif call.data == "no":
        bot.answer_callback_query(call.id, "Нет")
        bot.send_message(call.message.chat.id, 'Как же нет? Обманываешь бота? Ну ладно')


# def mut(message):
#     bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=int(time())+86400)
        # bot.restrict_chat_member(call.message.chat.id, call.message.from_user.id, call.chatMember(can_send_other_messages = False), until_date)
        # bot.restrict_chat_member(call.message.chat.id, call.message.from_user.id, until_date=int(time.time())+120 , can_send_other_messages = False)
        # bot.restrict_chat_member(call.message.chat.id, user_id = list_from_user_id[-1], until_date=int(time.time())+120)
        # bot.send_message(call.from_user.id, list_from_user_id[-1] + ' забанен')


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