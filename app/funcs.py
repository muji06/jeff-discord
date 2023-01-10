from requests import get
import json

def dispo(num:int):
    """
    
    """
    if num >= 0.5 and num <=0.69:
        return '●○○○○'
    elif num >= 0.7 and num <=0.89:
        return '●●○○○'
    elif num >= 0.9 and num <=1.1:
        return '●●●○○'
    elif num >= 1.11 and num <=1.3:
        return '●●●●○'
    elif num >= 1.31 and num <=1.55:
        return '●●●●●'


# async def pc_arcane(name:str, rank:int):
    
#     arcane = '_'.join(name.lower().split(' '))
#     res = get(f'https://api.warframe.market/v1/items/{arcane}/orders')
#     data = json.loads(res.text)
#     trades = data['payload']['orders']
#     lowest = [10000, 10000, 10000]
#     for trade in trades:
#         if trade['user']['status'] == 'ingame' and trade['order_type'] == 'sell' and trade['mod_rank'] == rank and trade['platform'] == 'pc':
#             if trade['platinum'] < lowest[0] :
#                 lowest[0] = trade['platinum']
#                 lowest.sort()
    
#     return lowest

# same function for both 
async def pricecheck(name:str, rank:int):
    if not (name.lower().endswith('prime blueprint') or name.lower().endswith('collar blueprint')):
        name = name.lower().replace(' blueprint','')
    if '-' in name:
        name = ' '.join(name.split('-'))
    if '&' in name:
        name = name.replace('&','and')
    prime = '_'.join(name.lower().split(' '))
    res = get(f'https://api.warframe.market/v1/items/{prime}/orders')
    data = json.loads(res.text)
    if "error" in data:
        prime+="_blueprint"
        res = get(f'https://api.warframe.market/v1/items/{prime}/orders')
        data = json.loads(res.text)
    trades = data['payload']['orders']

    lowest = [10000, 10000, 10000]
    for trade in trades:
        if 'mod_rank' in trade:
            if trade['user']['status'] == 'ingame' and trade['order_type'] == 'sell' and trade['mod_rank'] == rank and trade['platform'] == 'pc':
                if trade['platinum'] < lowest[0] :
                    lowest[0] = trade['platinum']
                    lowest.sort(reverse=True)
        else:
            if trade['user']['status'] == 'ingame' and trade['order_type'] == 'sell' and trade['platform'] == 'pc':
                if trade['platinum'] < lowest[0] :
                    lowest[0] = trade['platinum']
                    lowest.sort(reverse=True)
    
    return lowest

# call function above to create the final string
async def find(string: str, rank: int = None):
    if('forma' in string.lower()):
        return ''
    if int is None:
        arr = await pricecheck(string)
    else:
        arr = await pricecheck(string,rank)

    for i,x in enumerate(arr):
        if x == 10000:
            arr[i] = "N/A"
    return f"({arr[2]} , {arr[1]} , {arr[0]})<:Platinum:992917150358589550>"



async def relic_pricecheck(string: str):
    
    relic = '_'.join(string.lower().split(' '))+'_relic'
    res = get(f'https://api.warframe.market/v1/items/{relic}/orders')
    data = json.loads(res.text)
    trades = data['payload']['orders']
    lowest = [[10000,0],[10000,0],[10000,0]]
    for trade in trades:
        if trade['user']['status'] == 'ingame' and trade['order_type'] == 'sell' and trade['platform'] == 'pc':
            if trade['platinum'] <lowest[0][0]:
                lowest[0] = [trade['platinum'],trade['quantity']]
                lowest.sort(key=lambda x: x[0])

    return lowest

# special call for relics
async def relic_finder(string: str):

    arr = await relic_pricecheck(string)
    text = 'Price (Quantity): '
    for x in arr:
        if x[0] == 10000:
            text +='N/A '
        else:
            text +=f"{x[0]}<:Platinum:992917150358589550> ({x[1]}) "
    
    return text






# func for mod polarity emotes
def polarity(name:str):
    text = name.lower()
    if text == "vazarin":
        return "<:vazarin:1006594423620124812>"
    
    elif text == "madurai":
        return "<:madurai:1006594433422204989>"
    
    elif text == "naramon":
        return "<:naramon:1006594431782223932>"
    
    elif text == "zenurik":
        return "<:zenurik:1006594421262909590>"
    
    elif text == "unariu":
        return "<:unariu:1006594425595642016>"
    
    elif text == "penjaga":
        return "<:penjaga:1006594429651517551>"
    
    elif text == "umbra":
        return "<:umbra:1006594427772469248>"
    
    elif text == "aura":
        return "<:aura:1006594434718253148>"
    
    else: 
        return ""

def get_shard(archon: str):
    archon = archon.lower()
    if 'amar' in archon:
        return "<:CrimsonArchonShard:1052215232090620034>"

    elif 'nira' in archon:
        return "<:AmberArchonShard:1052215210657714327>"

    elif 'boreal' in archon:
        return "<:AzureArchonShard:1052215162704253030>"

    else:
        return ""