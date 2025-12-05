import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
admin_id = [int(os.getenv('ADMIN_ID'))]