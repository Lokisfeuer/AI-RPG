import json
import jsonpickle
import game


class MENU:
    def __init__(self, options=None):
        # options is a dict with {option1_name: option1_func_to_call, option2_name: option2_func_to_call, ...}
        self.func = None
        if options is None:
            options = {}
        self.options = list(options.values())
        self.option_strings = list(options.keys())
        # !play adventure
        # generate character
        # write adventure
        # invent skill

    def __call__(self, message):
        if '/exit' in message:
            self.func = None
        if self.func is None:
            answer = self.main_menu(message)
        else:
            answer = self.func(message)
        return answer

    def check_for_new_adventures(self):
        with open('adventures.json', 'r') as f:
            data = json.load(f)
        for i in list(data.keys())[1:]:
            if i not in self.option_strings:
                adv = jsonpickle.decode(data[i], keys=True)
                new = game.GAME(adventure=adv, use_roberta=False)
                self.option_strings.append(i)
                self.options.append(new)

    def main_menu(self, message):
        self.check_for_new_adventures()
        if message.isnumeric():
            message = self.option_strings[int(message)-1]
        if message in self.option_strings:
            self.func = self.options[self.option_strings.index(message)]
            return f'You chose option {self.option_strings.index(message)+1}: {message}'
        answer = 'You are in the main menu. You have different options:\n\n'
        for i in self.option_strings:
            answer += f'\t({self.option_strings.index(i)+1}) {i}\n\n'
        answer += '\n\nPlease choose one of these options by entering its digit or name.'
        return answer
