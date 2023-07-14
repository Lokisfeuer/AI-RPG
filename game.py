class GAME:  # a running game containing its adventure, its PC, the current status (stage), etc.
    def __init__(self, adventure, player):
        self.object = None
        self.answer = None
        self.player = player
        self.adventure = adventure
        self.message = ''
        self.response = None
        self.stage = None
        self.triggering = None
        self.trigger_count = 0
        # At some point: consider take-back option; ideally a full history which isn't too long to save including a log

    def play(self, message):
        self.message = message
        self.check_for_trigger()
        if self.response is not None:
            return self.response
        self.generate_response()
        self.check_for_secret()
        self.response = f'You are here: {self.stage["location"]}\n\n{self.response}'
        if self.get_by_name('won').value:
            self.response = f'{self.response}\n\nYou have successfully finished this adventure. You can return to the ' \
                            f'main menu with "/exit".'
        return self.response

    def check_for_secret(self):
        self.response = self.response
        # use AI modul. Binary modul for whether a secret is in or not. TODO: Build AI Modul
        # TODO: add secret to the bottom of the response
        for i in self.adventure.flags:
            i.check(self.stage)

    def check_for_trigger(self):
        if self.triggering is not None:
            self.trigger_count += 1
            self.response = self.triggering.call(self)
            if self.response is not None:
                return
            self.triggering = None
            self.trigger_count = 0
        for i in self.adventure.trigger:
            i.call_flag.check(self.stage)  # just in case there are dependencies on other flags
            if i.activation_flag.value and i.call_flag.value:
                self.triggering = i
                self.response = self.triggering.call(self)
                if self.response is not None:
                    return
                self.triggering = None
                self.trigger_count = 0
        self.response = None
        return

    def generate_response(self):
        # possible objects are necessary; possible objects are in self.stage
        self.object = None  # get object from AI model TODO: Build AI Modul
        input_type = None  # get input_type from AI model. Multiple choice modul TODO: Build AI Modul
        types = {'info': self.info,
                 'talk': self.talk,
                 'speech': self.speech,
                 'action': self.action,
                 'room change': self.location_change}
        types[input_type]()
        # TODO: Make sure input type and self.object fit to each other. (Don't talk to a room)

    def info(self):
        self.response = self.object.call(self.message)

    def talk(self):
        self.response = self.object.call(self.message)

    def speech(self):
        self.response = self.object.call(self.message)

    def verbatim(self):
        self.response = self.object.speak(self.message)

    def fight(self):
        self.response = self.object.fight(self.message)
        # At some point: when fighting you could lose objects instead of health. And gain objects or even secrets.

    def action(self):
        self.response = self.object.call(self.message)
        # At some point: Let actions have effect. Like picking up objects

    def location_change(self):
        # generate new stage.
        where = None  # get where from AI modul. TODO: Build AI Modul
        self.stage['location'] = where
        self.stage['npcs'] = self.adventure.rand_npcs()
        self.response = f'You are going to {where}.'

    def get_by_name(self, name):
        lst = self.adventure.secrets + self.adventure.locations + self.adventure.npcs + self.adventure.flags
        for i in lst:
            if i.has_attribute(name):
                if i.name == name:
                    return i
        return None
