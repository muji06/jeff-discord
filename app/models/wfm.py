import requests
import aiohttp
from enum import Enum

class ItemSubtype(Enum):
    CRAFTED = "crafted"
    BLUEPRINT = "blueprint"


class WarframeMarket:
    def __init__(self, base_url="https://api.warframe.market/v2", headers=None):
        self.base_url = base_url
        self.session = requests.Session()
        self._items = None  
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Language": "en",
            "Platform": "pc",
            "Crossplay": "true"
        })
        if headers:
            self.session.headers.update(headers)

    def get_orders(self,       
            slug: str="",
            rank: int=0,
            charges: int=0,
            amber_stars: int=0,
            cyan_stars: int=0,
            subtype: ItemSubtype|None=None,
            top_5: bool=False,
        ) -> dict: 
        endpoint = f"/orders/item/{slug}"

        if top_5:
            endpoint += "/top"
        
        params = {
            "rank": rank,
            "charges": charges,
            "amberStars": amber_stars,
            "cyanStars": cyan_stars
        }

        if subtype:
            params["subtype"] = subtype.value

        data = self.session.get(f"{self.base_url}{endpoint}",params=params)
        data.raise_for_status()
        return data.json().get("data")
    
    async def get_orders_async(self,
            slug: str="",
            rank: int=0,
            charges: int=0,
            amber_stars: int=0,
            cyan_stars: int=0,
            subtype: ItemSubtype=ItemSubtype.BLUEPRINT,
            top_5: bool=False,
        ) -> dict: 
        endpoint = f"/orders/item/{slug}"

        if top_5:
            endpoint += "/top"
        
        params = {
            "rank": rank,
            "charges": charges,
            "amberStars": amber_stars,
            "cyanStars": cyan_stars,
            "subtype": subtype.value
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}{endpoint}",params=params) as response:
                data = await response.json()
                return data.get("data")


class PriceCheck:
    """
    Utility class to check prices of items on Warframe Market
    """
    platinum = "<:Platinum:992917150358589550>"

    def __init__(self, client: WarframeMarket=None, item: str=None):
        self.client = client if isinstance(client, WarframeMarket) else WarframeMarket()
        self.item = item

    @property
    def slug(self):
        name = self.item.lower()
        if name.endswith("collar blueprint"):
            name = name.lower().replace(" blueprint","")
        if "-" in name:
            name = " ".join(name.split("-"))
        if "&" in name:
            name = name.replace("&","and")
        if "\'" in name:
            name = name.replace("\'","")
        
        return "_".join(name.split(" "))
    
    def check(self,
        rank: int=0,
        charges: int=3,
        subtype: ItemSubtype|None=None,
        ):
        orders = [order["platinum"] for order in self.client.get_orders(slug=self.slug,rank=rank,charges=charges,top_5=True,subtype=subtype).get("sell")]
        # if less than 5 orders, fill the rest with N/A
        # orders += ["N/A"] * (5 - len(orders))
        if len(orders) == 0:
            return "(N/A)"
        
        text = f"({", ".join([str(x) for x in orders])}){self.platinum}"
        return text
    
    async def check_async(self,
        rank: int=0,
        charges: int=3,
        subtype: ItemSubtype|None=None,
        ):
        orders = [order["platinum"] for order in self.client.get_orders(slug=self.slug,rank=rank,charges=charges,top_5=True,subtype=subtype).get("sell")]
        # if less than 5 orders, fill the rest with N/A
        # orders += ["N/A"] * (5 - len(orders))
        if len(orders) == 0:
            return "(N/A)"

        text = f"({", ".join([str(x) for x in orders])}){self.platinum}"
        return text
    
    def check_with_quantity(self
        ,rank: int=0,
        charges: int=3,
        subtype: ItemSubtype|None=None,
        ):
        orders = [f"{order["platinum"]}{self.platinum} ({order["quantity"]})" for order in self.client.get_orders(slug=self.slug,rank=rank,charges=charges,top_5=True,subtype=subtype).get("sell")]
        # if less than 5 orders, fill the rest with N/A
        # orders += ["N/A"] * (5 - len(orders))
        if len(orders) == 0:
            return "N/A"
        
        text = f"{'| '.join([str(x) for x in orders])}"
        return text