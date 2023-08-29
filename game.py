import adventure as adv


class GAME:  # a running game containing its adventure, its PC, the current status (stage), etc.
    def __init__(self, adventure):
        self.object = None
        self.answer = None
        self.adventure = adventure
        self.message = ''
        self.response = None
        self.stage = adventure.starting_stage
        self.triggering = None
        self.trigger_count = 0
        # At some point: consider take-back option; ideally a full history which isn't too long to save including a log

    def __call__(self, message):  # TODO: Check that this is nowhere called with .play anymore
        self.message = message
        self.check_for_trigger()
        if self.response is not None:
            return self.response
        self.generate_response()
        self.check_for_secret()
        self.response = f'You are here: {self.stage["location"].name}\n\n{self.response}'
        if self.get_by_name('won').value:
            self.response = f'{self.response}\n\nYou have successfully finished this adventure. ' \
                            f'You can return to the main menu with "/exit".'
        return self.response

    def check_for_secret(self):
        self.response = self.response
        secs = self.stage['location'].secrets
        for i in self.stage['npcs']:
            secs = secs + i.secrets
        secrets = []
        for i in secs:
            if i.activation_flag.value and not i.found:
                secrets.append(i)
        for i in secrets:
            # use AI modul. Binary modul for whether a secret is in or not. TODO: Build AI Modul
            resp = input(f'Was this secret found: {i.name}?\n{i.prompt}\nPlease enter a boolean answer: ')
            i.found = resp.lower() in ['true', '1', 't', 'y', 'yes']
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
        self.response = None  # this line is necessary to overwrite the prior response
        for i in self.adventure.flags:
            i.check(self.stage)
        return

    def generate_response(self):
        # possible objects are necessary; possible objects are in self.stage
        self.object = None  # get object from AI model TODO: Build AI Modul
        poss_objects = [self.stage['location']] + self.stage['npcs']
        self.object = poss_objects[int(input(f'Please enter the index of the currently relevant '
                                             f'object:\n{poss_objects}\n'))]
        input_type = None  # get input_type from AI model. Multiple choice modul TODO: Build AI Modul
        poss_input_type = ['info', 'talk', 'verbatim', 'action', 'room change']
        input_type = poss_input_type[int(input(f'Please enter the index of the current input type:'
                                               f'\n{poss_input_type}\n'))]
        types = {'info': self.info,
                 'verbatim': self.verbatim,  # only with npcs
                 'action': self.action,
                 'fight': self.fight,  # only with npcs
                 'room change': self.location_change}
        types[input_type]()
        # TODO: Make sure input type and self.object fit to each other. (Don't talk to a room)

    # the following functions may seem a little repetitive, but I believe it is easier to implement new concepts like
    # abilities if they are written like this.
    def info(self):
        if isinstance(self.object, adv.LOCATION):
            self.response = self.object.call(self.message, self.stage['npcs'])
        else:
            self.response = self.object.call(self.message)

    def verbatim(self):
        self.response = self.object.speak(self.message)  # this one is really innovative, isn't it?

    def fight(self):
        self.response = self.object.fight(self.message)
        # At some point: when fighting you could lose objects instead of health. And gain objects or even secrets.

    def action(self):
        self.response = self.object.call(self.message)
        # At some point: Let actions have effect. Like picking up objects

    def location_change(self):
        # generate new stage.
        where = None  # get where from AI modul. TODO: Build AI Modul
        poss_where = []
        for i in self.adventure.locations:
            if i.activation_flag.value:
                poss_where.append(i)
        where = poss_where[int(input(f'Please enter the index of where you go:\n{poss_where}\n'))]
        self.stage['location'] = where
        self.stage['npcs'] = self.adventure.rand_npcs()
        self.response = f'You are going to {where}.'

    def get_by_name(self, name):
        lst = self.adventure.secrets + self.adventure.locations + self.adventure.npcs + self.adventure.flags
        for i in lst:
            if i.name == name:
                return i
        return None
