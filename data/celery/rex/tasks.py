from __future__ import absolute_import
from rex.celery import app
import importlib

KEYS = ["properties", "provider", "lifecycle", "type"]

@app.task
def broadcast(message):
    print message
    return message


@app.task
def run(resource_dict):
    '''
    Run the module on target
    '''
    print resource_dict

    if type(resource_dict) is dict\
            and all(key in resource_dict.keys() for key in KEYS)\
            and type(resource_dict["provider"]) is dict\
            and type(resource_dict["properties"]) is dict:

        provider = resource_dict["provider"]

        module = "wrappers.wrapper_%s_%s" % (provider["name"], provider["version"])
        func = "%s_%s" % (resource_dict["lifecycle"], resource_dict["type"])

        m = importlib.import_module(module)
        module_func = getattr(m, func)

        return module_func(resource=resource_dict["properties"],\
                           provider=provider["properties"])
    else:
        message = "Check resource format, must contains {0}."\
                  "provider and properties must be dict."\
                  "Getting {1}".format(KEYS, resource_dict)
        print message
        return {"status":False, "response": {}, "message": message}
