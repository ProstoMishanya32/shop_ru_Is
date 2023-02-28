import json


def add_admin(user_id, nickname):
    with open('./data/main_config.json', 'r', encoding='utf-8') as f:
        id_users = []
        admins = json.load(f)
        for i in admins['bot']['admins']:
            id_users.append(i['user_id'])
    if user_id not in id_users:
        admins['bot']['admins'].append({"user_id":user_id, "nickname":nickname})
    with open('./data/main_config.json', 'w', encoding='utf-8') as f:
        json.dump(admins,  f,ensure_ascii=False, indent=4)
        return True


def see_admins():
    with open('./data/main_config.json', 'r', encoding='utf-8') as f:
        list_admins = []
        admins = json.load(f)
        current_position = 1
        for i in admins['bot']['admins']:
            character = dict()
            character['user_id'] = i['user_id']
            character['nickname'] = i['nickname']
            character['position'] = current_position
            list_admins.append(character)
            current_position += 1
        return list_admins

def remove_admin(user_id):
    with open('./data/main_config.json', 'r', encoding='utf-8') as f:
        admins = json.load(f)
    try:
        remove = []
        for i in admins['bot']['admins']:
            if int(user_id) == i['user_id']:
                id_user = i['user_id']
                nickname = i['nickname']
                admin = True
            else:
                admin = False
        admins['bot']['admins'].remove({"user_id":id_user, "nickname":nickname})
    except Exception as i:
        admin = False
    with open('./data/main_config.json', 'w', encoding='utf-8') as f:
        json.dump(admins,  f,ensure_ascii=False, indent=4)
    return admin

def get_admins():
    with open('./data/main_config.json', 'r', encoding='utf-8') as f:
        user_ids = []
        admins = json.load(f)
        for i in admins['bot']['admins']:
            user_ids.append( i['user_id'])
        return user_ids


def get_texts(text_category):
    with open('./data/main_config.json', 'r', encoding='utf-8') as f:
        texts = json.load(f)
        return texts['texts'][text_category]

def update_texts(text_category, text):
    with open('./data/main_config.json', 'r', encoding='utf-8') as f:
        print(text_category)
        texts = json.load(f)
        texts['texts'].pop(text_category)
        texts['texts'][text_category] = text
    with open('./data/main_config.json', 'w', encoding='utf-8') as f:
        json.dump(texts,  f,ensure_ascii=False, indent=4)

