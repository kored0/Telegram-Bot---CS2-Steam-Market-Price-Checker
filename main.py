import asyncio
import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
import config as cfg
from handler import admin, start_note, commands
from handler.search_items import SearchPrice
from parsing.data_get import CS2SteamParser
from key import button
from aiogram.filters import Command
from aiogram.types import Message

dp = Dispatcher(storage=MemoryStorage())
router = Router()
parser = CS2SteamParser()

router.message.filter(admin.Check_admin())

@router.message(Command("start"))
async def start_cmd(message: Message, state: FSMContext) -> None:
    await state.clear()
    msg = await message.answer("Чем могу помочь?", reply_markup=button.kb_menu)
    await message.delete()
    await asyncio.sleep(60)
    await msg.delete()

async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    bot = Bot(
        token=cfg.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    
    start_note.Start_the_bot(dp, bot, cfg.admin_id)
    SearchPrice(router, parser)
    
    dp.include_router(router)
    
    await commands.set_commands(bot)
    
    logging.info("Бот запущен!")
    
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()
        logging.info("Бот остановлен!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен пользователем")