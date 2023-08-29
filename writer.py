# write adventures
import datetime
import adventure as adv
import json
import jsonpickle


def write(message):
    if message.startswith('/reset'):
        data = {'aco': {}, 'all': {}}
        with open('trashfile.json', 'w') as f:
            json.dump(data, f)
        return 'resetted'
    id = str(datetime.datetime.now(datetime.timezone.utc)).lower().replace(' ', '_')
    with open('trashfile.json', 'r') as f:
        data = json.load(f)
    if message.startswith('/create'):
        create_adventure(data['all'])
    ob, type = None  # TODO: get ob and type from message
    ob = add(data['aco'], ob, type)
    data['aco'].update({ob['name']: ob})
    data['all'][type].append(ob)
    with open('trashfile.json', 'w') as f:
        json.dump(data, f)
    return 'Added to adventure'


def add(aco, ob, type):
    # {'name' 'flag', 'desc', 'secr', 'appe', 'prom', 'cond', 'ccon'}
    secrets = []
    if 'secr' in ob.keys():
        for i in ob['secr']:
            secrets.append(aco[i])
    if type == 'npc':
        try:
            appe = float(ob['appe'])
        except ValueError:
            appe = 1
        # no skills or items
        new = adv.NPC(
            name=ob['name'],
            activation_flag=aco[ob['flag']],
            description=ob['desc'],
            secrets=secrets,
            chance_to_appear=appe
        )
    elif type == 'loc':
        # name, activation_flag, description, start_items, secrets
        new = adv.LOCATION(
            name=ob['name'],
            activation_flag=aco[ob['flag']],
            description=ob['desc'],
            secrets=secrets
        )
    elif type == 'sec':
        new = adv.SECRET(  # no start items
            name=ob['name'],
            activation_flag=aco[ob['flag']],
            prompt=ob['prom']
        )
    elif type == 'fla':
        # TODO: include complex conditions CCON here as well!
        conditions = []
        for i in ob['cond']:
            conditions.append(aco[i])
        if conditions == []:
            conditions = True
        new = adv.FLAG(
            name=ob['name'],
            value=True,
            conditions=conditions
        )
    elif type == 'tri':
        new = adv.TRIGGER(
            name=ob['name'],
            activation_flag=aco[ob['flag']],
            call_flag=aco[ob['call']],
            func=getfunc(ob['func'])
        )
    else:
        raise ValueError
    return new


def getfunc(name):
    def func():
        print(f'This text is simulating the following function: {name}')
    return func


def from_webform(order, objects, starting_stage, userip):
    aco = {}
    all = {'npc': [], 'loc': [], 'sec': [], 'fla': [], 'tri': [], 'starting_stage': {'location': None, 'npcs': []}}
    ob = add(aco, {'name': '', 'cond': []}, 'fla')
    aco.update({ob.name: ob})
    all['fla'].append(ob)
    for i in order:
        ob = add(aco, objects[i], i[0:3])
        aco.update({ob.name: ob})
        all[i[0:3]].append(ob)
    all['starting_stage']['location'] = aco[starting_stage['location']]
    for i in starting_stage['npcs']:
        all['starting_stage']['npcs'].append(aco[i])
    return create_adventure(all, userip)


def create_adventure(all, userip):
    id = str(datetime.datetime.now(datetime.timezone.utc)).lower().replace(' ', '_')
    name = f'webadventure_ip:"{userip}"_id:"{id}"'
    adventure = adv.ADVENTURE(
        name=name,
        locations=all['loc'],
        npcs=all['npc'],
        secrets=all['sec'],
        trigger=all['tri'],
        flags=all['fla'],
        starting_stage=all['starting_stage']
    )
    with open('adventures.json', 'r') as f:
        data = json.load(f)
    data.update({f'{name}': jsonpickle.encode(adventure, keys=True)})
    with open('adventures.json', 'w') as f:
        json.dump(data, f, indent=4)
    print(f'adventure is saved to <<{name}>>')
    return name

