import requests

class WarframeMarketAPI:
    def __init__(self, base_url="https://api.warframe.market/v2", headers=None):
        self.base_url = base_url
        self.session = requests.Session()
        self._items = None  
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        if headers:
            self.session.headers.update(headers)

    def get_item(self, item_name):
        """
        Retrieve item details by name, including its URL name for API requests
        
        Args:
            item_name (str): The display name of the item to search for
            
        Returns:
            dict: Item information including id, url_name, and other details
            
        Raises:
            ValueError: If item is not found
            HTTPError: For API request failures
        """
        if self._items is None:
            self._fetch_all_items()
            
        lower_name = item_name.lower()
        for item in self._items:
            if item['item_name'].lower() == lower_name:
                return item
            
        raise ValueError(f"Item '{item_name}' not found")

    def _fetch_all_items(self):
        """Internal method to fetch and cache all items from the API"""
        response = self.session.get(f"{self.base_url}/items")
        response.raise_for_status()
        self._items = response.json()['payload']['items']

    def get_orders(self, item_name=None, url_name=None, order_type=None, platform='pc', include_profile=False):
        """
        Retrieve market orders for a specific item
        
        Args:
            item_name (str): Display name of the item (either this or url_name required)
            url_name (str): URL-friendly name of the item (either this or item_name required)
            order_type (str): 'buy' or 'sell' to filter order type
            platform (str): Platform to check (pc, ps4, xbox, switch)
            include_profile (bool): Whether to include profile information
            
        Returns:
            list: A list of order dictionaries
            
        Raises:
            ValueError: For invalid parameters or missing item
            HTTPError: For API request failures
        """
        if not (item_name or url_name):
            raise ValueError("Either item_name or url_name must be provided")
        if item_name and url_name:
            raise ValueError("Provide either item_name or url_name, not both")

        if item_name:
            item = self.get_item(item_name)
            url_name = item['url_name']

        params = {
            'platform': platform.lower()
        }
        
        if order_type:
            order_type = order_type.lower()
            if order_type not in ('buy', 'sell'):
                raise ValueError("order_type must be 'buy' or 'sell'")
            params['type'] = order_type
            
        if include_profile:
            params['include'] = 'profile'

        response = self.session.get(
            f"{self.base_url}/items/{url_name}/orders",
            params=params
        )
        response.raise_for_status()
        
        return response.json()['payload']['orders']