def test(game):
    if game.trigger_count > 3:
        return None
    else:
        return f'Triggering test (triggercount={game.trigger_count})'
