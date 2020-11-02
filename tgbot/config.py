token ='1011512469:AAF28pOATldHJhuZBGV14ehNhBFeZVVw86w'

SECRET = 'zombie'

commands = {
    'help'              : 'Gives user information about the available commands',
    'register'          : 'Registers user',
    'delete'            : 'Deletes user',
    'show_notifications': 'Shows all the notifications of the user',
    'subscribe'            : 'Provides settings for notifications',
    'undo_subscribe'       : 'Stops specified notification',
    'show_templates'        : 'Shows available templates to choose',
}

SERVER = 'http://admin:8000/'

CAPACITOR = None

MAIL = r'.+@.+'
PHONE = r"(^\+[0-9]{2}|^\+[0-9]{2}\(0\)|^\(\+[0-9]{2}\)\(0\)|^00[0-9]{2}|^0)([0-9]{9}$|[0-9\-\s]{10}$)"
NOTIFY = r'template: .+ tags: .+ info: .+ warn: .+ crit: .+ args: {.+}'
T_INST = r'template: .+'
