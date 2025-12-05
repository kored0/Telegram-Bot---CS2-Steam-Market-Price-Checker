import requests
from urllib.parse import quote

class CS2SteamParser:
    def __init__(self):
        self.base_url = "https://steamcommunity.com/market/search/render/"
        self.appid = 730 
        self.wear_qualities = [
            "Factory New",
            "Minimal Wear", 
            "Field-Tested",
            "Well-Worn",
            "Battle-Scarred"
        ]
        
    def search_item(self, item_name):
        params = {
            'query': item_name,
            'start': 0,
            'count': 100,
            'search_descriptions': 0,
            'sort_column': 'popular',
            'sort_dir': 'desc',
            'appid': self.appid,
            'norender': 1
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('success'):
                return None
                
            return data.get('results', [])
        except Exception as e:
            print(f"Ошибка запроса: {e}")
            return None
    
    def parse_results(self, results):
        if not results:
            return {}
        
        grouped_items = {}
        
        for item in results:
            name = item.get('name') or item.get('hash_name', '')
            base_name = name
            wear = "Без качества"
            for quality in self.wear_qualities:
                if f"({quality})" in name:
                    base_name = name.replace(f"({quality})", "").strip()
                    wear = quality
                    break
            
            if base_name not in grouped_items:
                grouped_items[base_name] = {}
            
            if wear not in grouped_items[base_name]:
                price = item.get('sell_price_text', 'Нет данных')
                market_url = f"https://steamcommunity.com/market/listings/730/{quote(name)}"
                
                grouped_items[base_name][wear] = {
                    'name': name,
                    'price': price,
                    'url': market_url,
                    'listings': item.get('sell_listings', 0)
                }
        
        return grouped_items
    
    def format_for_telegram(self, grouped_items, parse_mode='HTML'):
        if not grouped_items:
            return ["❌ Ничего не найдено"]
        
        messages = []
        
        if parse_mode == 'HTML':
            for base_name, wears in grouped_items.items():
                msg = f"<b>📦 {base_name}</b>\n"
                msg += "─" * 30 + "\n\n"
                
                for wear, data in wears.items():
                    msg += f"<b>🔹 {wear}</b>\n"
                    msg += f"💰 Цена: <code>{data['price']}</code>\n"
                    msg += f"📊 Лотов: {data['listings']}\n"
                    msg += f"🔗 <a href='{data['url']}'>Открыть в Steam</a>\n\n"
                
                messages.append(msg)
        
        elif parse_mode == 'Markdown':
            for base_name, wears in grouped_items.items():
                msg = f"*📦 {base_name}*\n"
                msg += "─" * 30 + "\n\n"
                
                for wear, data in wears.items():
                    msg += f"*🔹 {wear}*\n"
                    msg += f"💰 Цена: `{data['price']}`\n"
                    msg += f"📊 Лотов: {data['listings']}\n"
                    msg += f"🔗 [Открыть в Steam]({data['url']})\n\n"
                
                messages.append(msg)
        
        return messages
    
    def get_item_data(self, item_name, parse_mode='HTML'):

        results = self.search_item(item_name)
        
        if not results:
            return ["❌ Не удалось получить данные. Попробуйте позже."]
        
        grouped = self.parse_results(results)
        
        if not grouped:
            return [f"❌ Ничего не найдено по запросу: {item_name}"]
        
        return self.format_for_telegram(grouped, parse_mode=parse_mode)