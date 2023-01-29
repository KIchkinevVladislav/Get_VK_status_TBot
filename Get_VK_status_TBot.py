import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

"""
We assign the values specified in the .env file to the variables
"""
VK_TOKEN = os.getenv('VK_TOKEN') 
USER_ID = os.getenv('USER_ID') # user id information about which we want to get
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN') 
CHAT_ID = os.getenv('CHAT_ID') # your user id in Telegram


def get_user_statuses(user_id):
    """
    Request about the online status of a Vkontakte user.
    We get 1 or 0.
    """
    params = {'user_id': str(user_id), 
            'fields': 'online',
            'access_token': VK_TOKEN,
            'v': 5.131}
    status_user = requests.post('https://api.vk.com/method/users.get', data = params).json()
    result = status_user.get('response')

    return (result[0]['online'])

def parse_user_status(status):
    """
    Checking the received data with the “get_user_statuses” function
    Returns the text for the message being sent
    """
    if status == 1:
        return f'Пользователь зашел в сеть'
    else:
        return f'Пользователь оф-лайн'


def send_message(message):
    """
    We transfer the TOKEN of your bot to Telegram
    The function sends the message passed in the parameter through the bot
    """
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_TOKEN)
    params = {
            'text': message,
            'chat_id': CHAT_ID}
    send_message =requests.post(url, params=params)
    return send_message.text


def main():
    """
    Interaction of previously defined functions. 
    Implementation of the function of obtaining the status and sending information about it once every 20 minutes.
    """

    while True:
        try:
            get_status = get_user_statuses(USER_ID)
            send_message(parse_user_status(get_status))
            time.sleep(1200)  # ask every 20 minutes

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(5)
            continue


if __name__ == '__main__':
   main()
