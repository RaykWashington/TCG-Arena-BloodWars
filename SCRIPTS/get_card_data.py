import requests
import jmespath
import json


#-- SCRIPT STRUCTURE--
# - get list of cards and images from each set (BWBS, Rebels and Reinforcements, Factols and Factions, Powers and Proxies)
# - project list into TCG-Arena json format
# - wish me luck

# -- INITIATE VARIABLES --

setPageList = "Blood Wars Basic Set|Rebels and Reinforcements|Factols and Factions,Powers and Proxies"
card_data = json
card_data_file = "cardData2.json"

ENDPOINT = "https://cardguide.fandom.com/api.php"  #source of card info
HEADERS = {"User-Agent": "BloodWars-TCGArena (https://github.com/RaykWashington/TCG-Arena-BloodWars;hellorayk@gmail.com)"} #user-agent info
 
# -- FUNCTIONS --

def query(request_to_repeat): # -- make continued queries --
    #initiate default params
    request_to_repeat["action"] = "query",
    request_to_repeat["format"] = "json",
    last_continue = {}

    while True:
        
        iteration_req = request_to_repeat.copy() #clone original request using requests.copy method
        iteration_req.update(last_continue) # Modify it with the values returned in the 'continue' section of the last result.
        response = requests.get(ENDPOINT, params = iteration_req, headers=HEADERS).json()         # make request to mediawiki api

        #catch errors
        if 'error' in response:
            raise Exception(response['error'])
        if "warnings" in response:
            print(response['warnings'])
        
        #returning data
        if 'query' in response:
            yield response['query']
        
        #ending finished results
        if 'continue' not in response:
            break

        #continuing out of bounds response
        last_continue = response['continue']

#--RETRIEVING DATA--

search_string = "pages.*"
for result in query({'generator': 'linkshere', 'glhlimit': 'max', 'titles':'Blood Wars Basic Set|Rebels and Reinforcements|Factols and Factions|Powers and Proxies', 'prop':'pageimages', 'piprop':'original', 'pilimit':'max'}):

    try:
        with open(card_data_file, 'a+', encoding='utf-8') as file:
            json.dump(jmespath.search(search_string, result), file, ensure_ascii=False, indent=4)
    except(json.JSONDecodeError):
        data = []