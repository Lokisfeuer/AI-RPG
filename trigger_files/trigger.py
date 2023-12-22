# TODO: consider making this a package with an __init_ file and co
import inspect

# import all trigger files:
import trigger_files.test_trigger
import trigger_files.jonny_trigger


def get_func(adventure, func):  # both are strings
    modules = {
        'webadventure_ip:"127.0.0.1"_id:"2023-08-29_13:53:32.507045+00:00"': trigger_files.test_trigger,
        'webadventure_ip:"127.0.0.1"_id:"2023-08-29_18:36:28.072562+00:00"': trigger_files.jonny_trigger,
    }  # keys are the name of adventures, values are the modules for these adventures
    funcs = get_funcs(modules[adventure])
    if func in funcs.keys():
        return funcs[func]

    def something_went_wrong(*args, **kwargs):
        return 'trigger not found'
    return something_went_wrong

def get_funcs(module):
    names = dir(module)
    funcs = {}
    # Iterate over the names and check if each is a function
    for name in names:
        # Get the object for the name
        obj = getattr(module, name)
        # Check if the object is a function
        if inspect.isfunction(obj):
            funcs.update({name: obj})
    return funcs