from aiogram import Bot, Dispatcher
import asyncio
import config as cfg
import time


class Start_the_bot:
    def __init__(self, dp: Dispatcher, bot: Bot, admins: list[int]):
        self.bot = bot
        self.admins = admins
        dp.startup.register(self.on_startup)
    
    async def on_startup(self, bot: Bot):
        for admin_id in self.admins:
            try:
                msg = await self.bot.send_message(admin_id, "🤖 Bot is active and running!")
                asyncio.create_task(self.delete_after(msg, 5))
            except Exception as e:
                print(f"❌ Can't send message to {admin_id}: {e}")

    async def delete_after(self, msg, delay: int):
        await asyncio.sleep(delay)
        try:
            await msg.delete()
        except Exception as e:
            print(f"⚠️ Can't delete message {msg.message_id}: {e}")