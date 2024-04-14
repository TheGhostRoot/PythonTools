import os
#os.system("python -m pip install dl-translate pyyaml")
# https://www.browserling.com/tools/json-prettify
# https://onlineyamltools.com/prettify-yaml
import dl_translate as dlt
import yaml
import json
import requests


src = "English"
targ  = "Bulgarian"

print("From lang: " + src)
print("To lang: " + targ)

mt = dlt.TranslationModel()

blacklist = []


def saveYAML(output_file_name, data) -> None:
    open(output_file_name+".yml", "a")
    with open(output_file_name+".yml", 'w') as yamlfile:
        yaml.dump(data, yamlfile, indent=6)
        print("YAML: Overwrite successful")

def readYAML(file_name):
    if not os.path.exists(file_name+".yml"):
        return None
    
    with open(file_name+".yml", "r") as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)

    
def saveJSON(output_file_name, data) -> None:
    open(output_file_name+".json", "a")
    with open(output_file_name+".json", "w") as jsonfile:
        json.dump(data, jsonfile, indent=6)
        print("JSON: Overwrite successful")

def readJSON(file_name) -> dict:
    if not os.path.exists(file_name+".json"):
        return None

    with open(file_name+".json", "r") as jsonfile:
        return json.load(jsonfile)


def trans(text) -> str:
    if type(text) != str or text in blacklist:
        return text
    return mt.translate(text, source=src, target=targ)


def getInputFilePath():
  while True:
    file_path = input("File you want to translate: ");
    if len(file_path.replace(" ", "")) > 0:
       return file_path

def getOutputFilePath():
  while True:
    file_path = input("File you want to save the translation: ");
    if len(file_path.replace(" ", "")) > 0:
       return file_path


def getBlacklistFilePath():
  while True:
    file_path = input("Blacklist file path: ");
    if len(file_path.replace(" ", "")) > 0:
       return file_path


def translateYML(d):
    if isinstance(d, dict):
        for key, value in d.items():
            if isinstance(value, dict):
                d[key] = translateYML(value)
            elif isinstance(value, list):
                d[key] = [translateYML(item) if isinstance(item, dict) else trans(item) for item in value]
            else:
                d[key] = trans(value)
    return d


def translateJSON(d):
    for k, v in d.items():
        d[k] = trans(v)

input_file = getInputFilePath()
output_file = getOutputFilePath()
blacklist_file = getBlacklistFilePath()
b_file = open(blacklist_file, "rt")
for line in b_file:
    blacklist.append(line.replace("\n", ""))

if input_file.split(".")[-1] == "yml":
    yaml_file_name = input_file.split(".")[0]
    yaml_data_to_trans = readYAML(yaml_file_name)
    if yaml_data_to_trans is None:
        print("No YAML")
        exit()
   
    a = translateYML(yaml_data_to_trans)
    saveYAML(output_file.split(".")[0], a)

elif input_file.split(".")[-1] == "json":
    json_file_name = input_file.split(".")[0]
    json_data_to_trans = readJSON(json_file_name)
    if json_data_to_trans is None:
        print("No JSON")
        exit()
   
    translateJSON(json_data_to_trans)
    saveJSON(output_file.split(".")[0], json_data_to_trans)

else:
    print("unsupported format")




