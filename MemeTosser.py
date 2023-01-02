import telebot
from telebot import types
import time
import csv


# connect to the telegram bot
t_file = open(r'C:\Users\48885\Documents\Python Knowledge\MoodKeepBot.txt')
token_id = t_file.read()
t_file.close()

# list connection types
all_con_types = ['text','audio','document','photo','sticker','video','video_note','voice','location','contact','new_chat_members','left_chat_member','new_chat_title','new_chat_photo','delete_chat_photo','group_chat_created','supergroup_chat_created','channel_chat_created','migrate_to_chat_id','migrate_from_chat_id','pinned_message']

dict_channel_block = {}

bot = telebot.TeleBot(token_id)

# keyboard and buttons definition
button_yes = types.InlineKeyboardButton('Да', callback_data='yes')
button_no = types.InlineKeyboardButton('Нет', callback_data='no')

yn_keyboard = types.InlineKeyboardMarkup()
yn_keyboard.add(button_yes)
yn_keyboard.add(button_no)


# is channel locked
def is_channed_blocked(channel_id: int):
    if channel_id in dict_channel_block:
        if len(dict_channel_block[channel_id]) > 1:
            return True
        else:
            return False

# has user voted
def has_voted(channel_id: int, username: str):
    if dict_channel_block:
        if channel_id in dict_channel_block and len(dict_channel_block) > 0:
            if dict_channel_block[channel_id]:
                if username in dict_channel_block[channel_id]:
                    return True
    return False

# Function to add key:value
def dict_add(key, value):
    if int(key) in dict_channel_block:
        if value not in dict_channel_block[int(key)]:
              dict_channel_block[int(key)].append(value)
    else:
        dict_channel_block[int(key)] = [value]

# parce user list from csv
def parce_user_list(str_value):
    chars_to_remove = ["'", "[", "]", '"']
    for char in chars_to_remove:
        str_value = str_value.replace(char, "")
    return str_value

# update block list dict & file
def block_list_update_ext(dict_channel_block):
    # read block list from file
    # with open(r'C:\Users\48885\Documents\Python Knowledge\block_list_ext.csv') as block_file:
    with open("C:/Users/48885/Documents/Python Knowledge/block_list_ext.csv") as block_file:
        csvreader = csv.reader(block_file)
        next(csvreader)
        for row in csvreader:
            if ',' in row[1]:
                for user in parce_user_list(row[1]).split(','):
                    dict_add(row[0], user.strip())
            else:
                dict_add(row[0], parce_user_list(row[1]))
    block_file.close()
    
    # update file from dictionary
    with open(r'C:\Users\48885\Documents\Python Knowledge\block_list_ext.csv', 'w+', newline = '') as block_file:
        writer = csv.DictWriter(block_file, fieldnames=['id', 'vote'])
        writer.writeheader()
        for k, v in dict_channel_block.items():
            writer.writerow({'id': k, 'vote': v})
    block_file.close()

# Add start command /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я борюсь с политотой в отдельно взятом чате )')

# handle messages
@bot.message_handler(content_types=all_con_types)
def handle_message(message):
    if message.forward_from_chat is not None:
        if message.forward_from_chat.type == 'channel':
            # bot.send_message(message.chat.id, str(message.forward_from_chat.username) + '\n' + str(message.content_type))
            if is_channed_blocked(message.forward_from_chat.id):
                # remove message
                bot.delete_message(message.chat.id, message_id=message.id)
            else:
                bot.reply_to(message, text='Политота небось?', reply_markup=yn_keyboard)

# keyboard callback handling
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "yes":
        print(call.from_user.username + ' hit YES at ' + str(time.time()) + ' ' + str(not has_voted(call.message.reply_to_message.forward_from_chat.id, call.from_user.username)))
        if is_channed_blocked(call.message.reply_to_message.forward_from_chat.id):
            bot.answer_callback_query(call.id, "Канал уже в стоп-листе")
            bot.delete_message(call.message.chat.id, message_id=call.message.id)
            # bot.send_message(call.message.chat.id, 'Канал уже в стоп-листе')
        else:
            if not has_voted(call.message.reply_to_message.forward_from_chat.id, call.from_user.username):
                bot.answer_callback_query(call.id, "Голос принят!")
                dict_add(call.message.reply_to_message.forward_from_chat.id, call.from_user.username)
                block_list_update_ext(dict_channel_block)
                if is_channed_blocked(call.message.reply_to_message.forward_from_chat.id):
                    bot.delete_message(call.message.chat.id, message_id=call.message.id)
                    bot.send_message(call.message.chat.id, call.message.reply_to_message.forward_from_chat.title + ', давай до свидания!')
                else:
                    bot.send_message(call.message.chat.id, 'Нужны еще голоса')
            else:
                bot.answer_callback_query(call.id, "Нельзя просто так взять и проголосовать два раза")

    elif call.data == "no":
        print(call.from_user.username + ' hit NO at ' + str(time.time()) + ' ' + str(not has_voted(call.message.reply_to_message.forward_from_chat.id, call.from_user.username)))
        if not is_channed_blocked(call.message.reply_to_message.forward_from_chat.id):
            bot.answer_callback_query(call.id, "Товарищи сообщали ранее, что канал политический")
        else:
            bot.delete_message(call.message.chat.id, message_id=call.message.id)
            bot.answer_callback_query(call.id, "Это замечательно")
        # bot.send_message(call.message.chat.id, 'Как же нет? Обманываешь бота? Ну ладно')
        
# def mut(message):
#     bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=int(time())+86400)
        # bot.restrict_chat_member(call.message.chat.id, call.message.from_user.id, call.chatMember(can_send_other_messages = False), until_date)
        # bot.restrict_chat_member(call.message.chat.id, call.message.from_user.id, until_date=int(time.time())+120 , can_send_other_messages = False)
        # bot.restrict_chat_member(call.message.chat.id, user_id = list_from_user_id[-1], until_date=int(time.time())+120)
        # bot.send_message(call.from_user.id, list_from_user_id[-1] + ' забанен')

block_list_update_ext(dict_channel_block)
bot.polling(none_stop=True, interval=0)
