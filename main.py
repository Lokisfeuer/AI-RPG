import json
import jsonpickle
import menu

from bot import run_bot
from webapp import run_webapp


def main():
    user_name = None
    while user_name is None:
        user_name = input("Please enter your username: ")
        resp = input(f'You entered "{user_name}". Do you want to use this username? ')
        if resp.lower() not in ['true', '1', 't', 'y', 'yes']:
            print("Username deleted.")
            user_name = None
    running = True
    output = 'Please enter anything.'
    while running:
        user_input = input(output)
        if '/exit/exit' in user_input:
            running = False
        with open('user_data.json', 'r') as f:
            data = json.load(f)
        if user_name not in data.keys():
            user_menu = menu.MENU()
        else:
            user_menu = jsonpickle.decode(data[user_name], keys=True)
        output = user_menu(user_input)
        data[user_name] = jsonpickle.encode(user_menu, keys=True)
        with open('user_data.json', 'w') as f:
            json.dump(data, f, indent=4)
    print('You exited the program, it will now run out.')


if __name__ == '__main__':
    # run_webapp()
    # run_bot()
    main()
