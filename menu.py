class MENU:
    def __init__(self, options):
        self.func = self.main_menu
        self.options = list(options.values())
        self.option_strings = list(options.keys())
        # !play adventure
        # generate character
        # write adventure
        # invent skill
        pass

    def call(self, message):
        if '/exit' in message:
            self.func = self.main_menu
        answer = self.func(message)
        return answer

    def main_menu(self, message):
        if message.isdigit():
            message = self.option_strings[int(message)-1]
        if message in self.option_strings:
            self.func = self.options[self.option_strings.index(message)]
            return f'You chose option {self.option_strings.index(message)+1}: {message}'
        answer = 'You are in the main menu. You have different options:\n'
        for i in self.option_strings:
            answer += f'\t({self.option_strings.index(i)+1}) {i}\n'
        answer += '\nPlease choose one of these options by entering its digit or name.'
        return answer
