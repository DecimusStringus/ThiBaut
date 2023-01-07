import csv

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