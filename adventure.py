import random
import math


class ADVENTURE:
    # possibility to write custom adventures
    # possibly an intelligent AI adventure writer
    # use maps or something similar to move properly
    def __init__(self, name, locations, npcs, secrets, trigger, flags):
        self.name = name
        self.locations = locations
        self.npcs = npcs
        self.secrets = secrets
        self.trigger = trigger
        self.flags = flags
        # https://github.com/AdrianSI666/DnD_Bestiary-Spellbook-CT
        # https://github.com/opendnd/personae Can do relations between characters!
        # https://github.com/topics/npc-generator

    def rand_npcs(self):
        npcs = []
        for i in self.npcs:
            if i.activation_flag.value:
                npcs.append(i)

        # weighted random choice for how many npcs
        weights = [0.1, 0.15, 0.25]  # propper distribution shifted to the left and centered around 3 would be better
        for i in range(len(npcs) - 3):
            weights.append(1 / (2 ** (i + 2)))
        k = random.choices(range(len(npcs)), weights=weights)

        # weighted random choice which npc to choose
        weights = []
        for i in npcs:
            weights.append(i.chance_to_appear)
        npcs = random.choices(npcs, weights=weights, k=k)
        return npcs


class LOCATION:
    def __init__(self, name, activation_flag, description, start_items, secrets):
        self.name = name
        self.activation_flag = activation_flag
        self.description = description
        self.start_items = start_items
        self.secrets = secrets

    def call(self, message):
        # TODO call openai with your description and so on to generate an answer
        pass


class NPC:
    def __init__(self, name, activation_flag, description, start_items, skills, secrets, chance_to_appear=1):
        self.name = name
        self.activation_flag = activation_flag
        self.description = description
        self.start_items = start_items
        self.skills = skills
        self.secrets = secrets
        self.chance_to_appear = chance_to_appear

    def speak(self, message):
        # TODO call openai with your description and so on to generate an answer
        pass

    def fight(self, message):
        return f'You wrote: "{message}"\nBut fighting {self.name} doesn\'t work.\n(Violence is never a solution)'

    def call(self, message):
        # TODO call openai with your description and so on to generate an answer
        pass


class SECRET:
    def __init__(self, name, activation_flag, prompt):  # "where to find" system?
        self.name = name
        self.prompt = prompt  # TODO: Define a definite format for this prompt
        self.activation_flag = activation_flag
        self.found = False


class FLAG:  # like secrets without text. For example "won" is now a flag not a secret anymore.
    def __init__(self, name, value, conditions):  # "and" and "or" and "not" combinations work;
        self.name = name
        self.value = value  # boolean
        self.conditions = conditions
        # conditions consist of flags (true), secrets (found), npcs (in scene), locations (in scene)
        # conditions should be rather complex

    def check(self, stage):
        def check_item(item):  # this function checks for a "not" connection
            if isinstance(item, dict):
                if not len(dict.keys()) == 1:
                    raise ValueError
                if check_item2(item.keys()[0]) == item.values()[0]:
                    return True
                else:
                    return False
            else:
                return check_item2(item)

        def check_item2(item):
            if isinstance(item, FLAG):
                return item.value
            elif isinstance(item, SECRET):
                return item.found
            elif isinstance(item, NPC):
                if item in stage['npcs']:
                    return True
                else:
                    return False
            elif isinstance(item, LOCATION):
                if item == stage['location']:
                    return True
                else:
                    return False
            else:
                raise ValueError

        def check_list():
            # This function checks any amount of combinations of "and" and "or" connections
            new_list = [[]]  # list of lists of boolean values
            pos = [0]  # position (of item x) within the conditions
            while True:
                x = self.conditions
                maxs = []  # same length as pos
                for i in pos:
                    maxs.append(len(x))
                    x = x[i]
                if isinstance(x, list):
                    pos.append(0)
                    new_list.append([])
                else:
                    val = check_item(x)  # what to do now with this?
                    new_list[-1].append(val)
                    pos[-1] += 1
                    while maxs[-1] == pos[-1]:
                        vals = new_list.pop()
                        if pos[0] == maxs[0]:  # check if it's done
                            if False in vals:
                                return False
                            else:
                                return True
                        if (len(new_list) % 2) == 0:  # "and" connection
                            if False in vals:
                                new_list[-1].append(False)
                            else:
                                new_list[-1].append(True)
                        else:  # "or" connection
                            if True not in vals:
                                new_list[-1].append(False)
                            else:
                                new_list[-1].append(True)
                        pos.pop()
                        maxs.pop()
                        pos[-1] += 1

        if isinstance(self.conditions, list):
            self.value = check_list()
        elif isinstance(self.conditions, bool):
            self.value = self.conditions
        elif self.conditions is None:
            self.value = self.value
        else:
            self.value = check_item(self.conditions)


class TRIGGER:
    def __init__(self, name, activation_flag, func, call_flag):
        self.name = name
        self.activation_flag = activation_flag
        self.call_flag = call_flag  # to flags in case one is "static" and changed by the trigger or so.
        self.func = func

    def call(self, game):
        # count = game.trigger_count
        self.func(game)


if __name__ == "__main__":
    pass
