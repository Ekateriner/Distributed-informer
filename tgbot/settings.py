import config
import json
import re
import requests
import telebot

from collections import defaultdict

bot = telebot.TeleBot(config.token)
validate_users = defaultdict(bool)
not_ids = defaultdict(list)
with open('configs/users.json', 'r') as fh:
    bot_users = json.load(fh)
with open('configs/notifications.json', 'r') as fh:
    nots = json.load(fh)

for key_elem in bot_users.keys():
    validate_users[key_elem] = True
    if key_elem in nots.keys():
        not_ids[key_elem] = nots[key_elem]


def build_user(message, email=None, phone=None, django_id=None, id_for_matrix=None):
    user = message.from_user
    return {
        'id': user.id,
        'chat': message.chat.id,
        'username': user.username,
        'email': email,
        'phone': phone,
        'django_id': django_id,
        'id_for_matrix': id_for_matrix,
    }


def register(message):
    global bot_users
    if " " not in message.text:
        bot.send_message(message.chat.id, 'Sorry, something went wrong, please try again!')
        return

    email, phone = message.text.split(" ")
    mail = re.compile(config.MAIL)
    p = re.compile(config.PHONE)
    if re.match(mail, email) and re.match(p, phone):
        data = {
            'name': message.from_user.first_name + " " + message.from_user.last_name,
            'telegram': message.from_user.username,
            'id_for_bot': message.chat.id,
            'email': email,
            'phone': phone,
        }
        response = requests.post(config.SERVER + 'api/recipients/', data)
        bot_users[str(message.chat.id)]['email'] = email
        bot_users[str(message.chat.id)]['phone'] = phone
        bot_users[str(message.chat.id)]['django_id'] = response.json()['id']
        with open('configs/users.json', 'w') as file:
            json.dump(bot_users, file)
        bot.send_message(message.chat.id, 'Done!')
    else:
        bot.send_message(message.chat.id, 'Sorry, something went wrong, please try again!')


def delete_by_user(message):
    global bot_users
    django_id = bot_users[str(message.chat.id)]['django_id']
    response = requests.delete(config.SERVER + f'api/recipients/{django_id}')
    for el in not_ids[str(message.chat.id)]:
        response = requests.delete(config.SERVER + f'api/notifications/{el}')
    del not_ids[str(message.chat.id)]
    with open('configs/notifications.json', 'w') as file:
        json.dump(not_ids, file)

    del bot_users[str(message.chat.id)]
    with open('configs/users.json', 'w') as file:
        json.dump(bot_users, file)

    del (validate_users[str(message.chat.id)])
    with open('configs/validation.json', 'w') as file:
        json.dump(dict(validate_users), file)

    bot.send_message(message.chat.id, 'Done!')


def notify(message):
    cid = message.chat.id
    notif = re.compile(config.NOTIFY)
    if re.match(notif, message.text):
        text = message.text.split(": ", 6)

        template = text[1].split()[0]
        tags = text[2].split()[:-1]
        info = text[3].split()[0]
        warn = text[4].split()[0]
        crit = text[5].split()[0]
        args = json.loads(text[6])

        template = requests.get(config.SERVER + f'api/templates/?template={template}')
        if not template.ok:
            bot.send_message(cid, template.json())
            return
        if len(template.json()) == 0:
            bot.send_message(cid, "No such template")
            return
        template = template.json()[0]

        temp_inst = {'template': template['id'],
                     'args': args,
                     'warn': warn,
                     'crit': crit,
                     'info': info,
                     }
        template_instance = requests.post(config.SERVER + 'api/template_instances/', json=temp_inst)
        if template_instance.ok:
            template_instance_id = template_instance.json()["id"]
        else:
            template_instance_json = template_instance.json()
            if len(template_instance_json) >= 1 and \
                    template_instance_json[0].split(": ")[0] == "Such template instance already exists":
                template_instance_id = template_instance_json[0].split(": ")[1]
            else:
                bot.send_message(cid, template_instance.json())
                return

        t = requests.get(config.SERVER + 'api/tags/')
        if not t.ok:
            bot.send_message(cid, t.json())
            return
        tag = []
        for i in range(len(tags)-1):
            if tags[i] == 'none':
                continue
            for k in t.json():
                if tags[i] == k['name']:
                    tag.append(k['id'])

        d_u = bot_users[str(cid)]['django_id']
        u = requests.get(config.SERVER + f'api/recipients/{d_u}/')
        if not u.ok:
            bot.send_message(cid, u.json())
            return
        data = {
            'user': u.json()['id'],
            'template_instance': template_instance_id,
            'tags': tag
        }
        response = requests.post(config.SERVER + 'api/notifications/', json=data)
        if not response.ok:
            bot.send_message(cid, response.json())
            return
        not_ids[str(cid)].append(response.json()['id'])
        with open('configs/notifications.json', 'w') as file:
            json.dump(not_ids, file)
        bot.send_message(cid, f'Your notification with id {response.json()["id"]} has been created!')
        if config.CAPACITOR:
            data['chat_id'] = cid
            response_capacitor = requests.post(config.CAPACITOR + 'api/notifications/', json=data)
    else:
        bot.send_message(cid, 'Wrong text! Please try again!')


def undo_notify(message):
    cid = message.chat.id
    try:
        id = int(message.text)
    except Exception:
        bot.send_message(cid, 'Incorrect id')
        return
    if id in not_ids[str(cid)]:
        to_delete = config.SERVER + 'api/notifications/' + str(id) + '/'
        data = requests.get(to_delete).json()
        if config.CAPACITOR:
            data['chat_id'] = cid
            data['delete'] = True
            response_capacitor = requests.post(config.CAPACITOR + 'api/notifications/', json=data)
        requests.delete(to_delete)
        not_ids[str(cid)].remove(id)
        with open('configs/notifications.json', 'w') as file:
            json.dump(not_ids, file)
        bot.send_message(cid, 'Done!')
    else:
        bot.send_message(cid, 'Incorrect id')


def add_metric(message):
    name, unit = str.split(message.text, ' ')
    metric = {
        'name': name,
        'unit': unit
    }
    response = requests.post(config.SERVER + 'api/metrics/', metric)
    bot.send_message(message.chat.id, 'Done!')


def validate(func):
    def wrapper(*args, **kwargs):
        global bot_users
        message = args[0]
        cid = str(message.chat.id)
        if validate_users[cid] or message.text == config.SECRET:
            if not validate_users[cid]:
                bot.send_message(message.chat.id, "Welcome")
                validate_users[cid] = True
                bot_users[cid] = build_user(message)
                with open('configs/users.json', 'w') as file:
                    json.dump(bot_users, file)
                with open('configs/validation.json', 'w') as file:
                    json.dump(dict(validate_users), file)
            else:
                django_id = bot_users[cid]['django_id']
                if django_id is not None:
                    r = requests.get(config.SERVER + f'api/recipients/{django_id}/')
                    if r.status_code == 200:
                        return func(*args, **kwargs)
                    elif r.status_code == 404:
                        bot.send_message(int(cid), 'You have been deleted from database.')
                        del (validate_users[cid])
                        del (bot_users[cid])
                        with open('configs/users.json', 'w') as file:
                            json.dump(bot_users, file)
                        with open('configs/validation.json', 'w') as file:
                            json.dump(dict(validate_users), file)
                else:
                    if message.text not in ['/register', '/help'] and message.text[0] == '/':
                        bot.send_message(int(cid), 'You have to register before.')
                    else:
                        return func(*args, **kwargs)
        else:
            bot.send_message(message.chat.id, 'Please enter password to proceed!')
        return None

    return wrapper
