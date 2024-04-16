import json
#purges the json files of all data

with open('data.json', 'w') as f:
    f.write(json.dumps({}))
with open('rooms.json', 'w') as f:
    f.write(json.dumps({}))
with open('maps.json', 'w') as f:
    f.write(json.dumps({}))
