import config
import json
import requests
from settings import register
from settings import delete_by_user
from settings import notify
from settings import undo_notify
from settings import add_metric
from settings import validate
from settings import not_ids
from settings import bot

from collections import defaultdict


@bot.message_handler(commands=['help'])
@validate
def command_help(message):
    cid = message.chat.id
    help_text = "The following commands are available: \n"
    for key in config.commands:
        help_text += "/" + key + ": "
        help_text += config.commands[key] + "\n"
    bot.send_message(cid, help_text)


@bot.message_handler(commands=['register'])
@validate
def command_register(message):
    msg = bot.reply_to(message, 'Please, provide your email and phone number (ex-le: "sofi@mail.ru +71112223344").')
    bot.register_next_step_handler(msg, register)


@bot.message_handler(commands=['delete'])
@validate
def command_delete(message):
    cid = message.chat.id
    delete_by_user(message)
    del_text = "You have been deleted from data base, please reenter again, if you want to continue!"
    bot.send_message(cid, del_text)


@bot.message_handler(commands=['show_templates'])
@validate
def command_show_temps(message):
    cid = message.chat.id
    text = "The following templates are available:"
    bot.send_message(cid, text)

    response = requests.get(config.SERVER + 'api/templates/')

    for template in response.json():
        text = "name: "
        text += template['name'] + "\n"
        text += "args: "
        text += str(template['args'])
        bot.send_message(cid, text)


@bot.message_handler(commands=['show_notifications'])
@validate
def command_show_notifications(message):
    cid = message.chat.id
    if len(not_ids[str(cid)]) == 0:
        bot.send_message(cid, 'You have no notifications yet!')
        return

    text = "The following notifications are currently overlooking:"
    bot.send_message(cid, text)

    response = requests.get(config.SERVER + 'api/notifications/')

    for n in response.json():
        if n['id'] in not_ids[str(cid)]:
            text = "id: "
            text += str(n['id']) + "\n"
            text += "template instance: "
            text += str(n['template_instance']) + "\n"
            text += "tags: "
            text += str(n['tags']) + "\n"

            bot.send_message(cid, text)


@bot.message_handler(commands=['subscribe'])
@validate
def command_notify(message):
    msg = bot.reply_to(message, 'Please provide template, tags, info, warn, crit in a row'
                                ' (ex-le "template: max 50 12 tags: Moscow info: 3 warn: 2 crit: 1").'
                                'You are able to leave some args as "none" if you want to make them default')
    bot.register_next_step_handler(msg, notify)


@bot.message_handler(commands=['undo_subscribe'])
@validate
def command_undo_notify(message):
    msg = bot.reply_to(message, 'Send the id of notification you want to stop receiving messages from.')
    bot.register_next_step_handler(msg, undo_notify)


@bot.message_handler(commands=['add_metric'])
@validate
def command_add_metric(message):
    name_and_unit = bot.reply_to(message, 'Write the name and the unit of the metric, '
                                          'separating them with space, please.')
    bot.register_next_step_handler(name_and_unit, add_metric)


@bot.message_handler(content_types=['text'])
@validate
def get_text_messages(message):
    pass


if __name__ == '__main__':
    with open('configs/validation.json') as f:
        validate_users = defaultdict(bool, json.load(f))
    with open('configs/users.json') as f:
        bot_users = json.load(f)
    bot.polling(none_stop=True, interval=0)
