def eric(game):
    if game.trigger_count == 0:
        return 'I know where Jonny went but I wont tell you unless you solve this riddle:\nWhat can run but never ' \
               'walks, has a mouth but never talks, has a head but never weeps, has a bed but never sleeps?'
    else:
        game.get_by_name('eric_flag').conditions = False
        game.get_by_name('eric_flag').value = False
        if 'river' in game.message.lower():
            return 'Thats the correct response. I saw Jonny going up to the attic.'
        else:
            return 'No! Wrong! I am really sorry but I wont help you. Maybe you\'ll find something in the garden.'


def jonny(game):
    game.stage['npcs'] = [game.get_by_name('Jonny')]
    return None
