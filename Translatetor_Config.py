import os
#os.system("python -m pip install dl-translate pyyaml")
# https://www.browserling.com/tools/json-prettify
# https://onlineyamltools.com/prettify-yaml
import dl_translate as dlt
import yaml
import json

"""
print(mt.available_languages())
print(mt.translate("Hello", source="English", target="Bulgarian"))

data = {
    "hi": {
        "info": "hello"
    }
}
"""

src = "English"
targ  = "Bulgarian"
mt = dlt.TranslationModel()


def saveYAML(output_file_name, data) -> None:
    open(output_file_name+".yml", "a")
    with open(output_file_name+".yml", 'w') as yamlfile:
        yaml.dump(data, yamlfile, default_flow_style=False, sort_keys=False)
        print("YAML: Overwrite successful")

def readYAML(file_name):
    if not os.path.exists(file_name+".yml"):
        return None
    
    with open(file_name+".yml", "r") as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)
    
def saveJSON(output_file_name, data) -> None:
    open(output_file_name+".json", "a")
    with open(output_file_name+".json", "w") as jsonfile:
        json.dump(data, jsonfile)
        print("JSON: Overwrite successful")

def readJSON(file_name) -> dict:
    if not os.path.exists(file_name+".json"):
        return None

    with open(file_name+".json", "r") as jsonfile:
        return json.load(jsonfile)


def trans(text) -> str:
    return mt.translate(text, source=src, target=targ)



yaml_data_to_trans = readYAML("messages_4")
if yaml_data_to_trans is None:
    print("No YAML")
    exit()


#for k, v in json_data_to_trans.items():
#    json_data_to_trans[k] = trans(v)

def translateYML(d):
    if isinstance(d, dict):
        for key, value in d.items():
            if isinstance(value, dict):
                translateYML(value)
            else:
                d[key] = trans(value)
    else:
        return d
    
translateYML(yaml_data_to_trans)

saveYAML("translated-messages", yaml_data_to_trans)



