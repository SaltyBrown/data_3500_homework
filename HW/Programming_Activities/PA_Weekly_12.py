import requests
import json
# Activity 1
# set up url
url = "https://api.datamuse.com/words?rel_trg=cow"

# send request
req = requests.get(url)

# load data as python dictionary
dct1 = json.loads(req.text)

for word in dct1:
    if word["word"] == "cheese":
        print(word["word"], word["score"])