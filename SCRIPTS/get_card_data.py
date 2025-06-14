import requests
import jmespath


#Script structure:
# - get list of cards from each set (BWBS, Rebels and Reinforcements, Factols and Factions, Powers and Proxies)
# - generate list of images urls from continued requests

# -- INITIATE VARIABLES --

setPageList = ["Blood Wars Basic Set", "Rebels and Reinforcements","Factols and Factions", "Powers and Proxies"]
card_list = {}

ENDPOINT = "https://cardguide.fandom.com/api.php"  #source of card info
HEADERS = {"User-Agent": "BloodWars-TCGArena (https://github.com/RaykWashington/TCG-Arena-BloodWars;hellorayk@gmail.com)"}
 
# -- FUNCTIONS --

def query(request_to_repeat): # -- make continued queries --
    #initiate default params
    request_to_repeat["action"] = "query",
    request_to_repeat["format"] = "json",
    last_continue = {}

    while True:
        
        iteration_req = request_to_repeat.copy() #clone original request using requests.copy method
        iteration_req.update(last_continue) # Modify it with the values returned in the 'continue' section of the last result.
        response = requests.get(ENDPOINT, params = iteration_req).json()         # make request to mediawiki api

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
        
for set in setPageList:
    for result in query({'prop':'linkshere', 'lhprop': 'pageid|title','lhlimit':'max','titles':set}):
        print(result)