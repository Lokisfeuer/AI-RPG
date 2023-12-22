import os

import json
import jsonpickle
from flask import Flask, request, render_template

import menu as menu
import writer as writer

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route('/play', methods=['POST'])
def play():
    user_input = request.form.get('user_input')
    if 'user_data.json' not in os.listdir():
        data = {}
    else:
        with open('user_data.json', 'r') as f:
            data = json.load(f)
    if request.remote_addr not in data.keys():
        user_menu = menu.MENU()
    else:
        user_menu = jsonpickle.decode(data[request.remote_addr], keys=True)
    output = user_menu(user_input)
    data[request.remote_addr] = jsonpickle.encode(user_menu, keys=True)
    with open('user_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    return render_template("index.html", text_output=output)


@app.route('/write_adventure')
def write_adventure():
    return render_template("adventures.html")


@app.route('/finished_adventure', methods=['POST'])
def finished_adventure():
    objects, raw = get_objects()
    loca = request.form.get('sta_loca')
    npcs = request.form.getlist('sta_npcs')
    starting_stage = {'location': loca, 'npcs': npcs}
    all_obj_str = request.form.get('myvariables')
    all_obj = []
    for i in all_obj_str[:-1].split(' '):
        all_obj.append(i[1:-1])
    name = writer.from_webform(all_obj, raw, starting_stage, request.remote_addr)
    back = f"Your adventure was saved to {name}\n\nThis is your adventure:\n{objects}\n{starting_stage}\n\nTo return " \
           f"to the main page enter \"/exit\""
    return render_template("index.html", text_output=back)


def get_objects():
    raw_everything = {}
    objects = {'npc': [], 'loc': [], 'sec': [], 'fla': [], 'tri': []}
    print('getting objects')
    for i in ['npc', 'loc', 'sec', 'fla', 'tri']:
        done = False
        t = 0
        while True:
            ob = {}
            for j in ['name', 'flag', 'desc', 'secr', 'appe', 'item', 'skil', 'prom', 'cond', 'ccon', 'call', 'func']:
                object_id = f'{i}_{t}_{j}'
                if object_id.endswith('secr') or object_id.endswith('cond'):
                    asp = request.form.getlist(object_id)
                elif object_id.endswith('item') or object_id.endswith('skill'):
                    asp = request.form.get(object_id)
                    if asp is not None:
                        asp = asp.split(', ')
                else:
                    asp = request.form.get(object_id)
                if asp is not None:
                    ob.update({j: asp})
                elif j == 'name':
                    done = True
                    break
            if done:
                break
            else:
                objects[i].append(ob)
                raw_everything.update({f'{i}_{t}': ob})
            t += 1
    return objects, raw_everything


def run_webapp():
    # app.run(host="0.0.0.0", port=80)
    app.run(debug=True)


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=80)
    app.run(debug=True)
