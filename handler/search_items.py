from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
import asyncio
import logging
from parsing.data_get import CS2SteamParser

class SearchHandler(StatesGroup):
    waiting_for_item_name = State()

class SearchPrice:
    def __init__(self, router: Router, parser: CS2SteamParser):
        self.router = router
        self.parser = parser
        router.message.register(
            self.cancel_search,
            SearchHandler.waiting_for_item_name,
            F.text.in_(['❌Отмена', '◀️Назад', '/cancel'])
        )
        router.message.register(
            self.search_item, 
            SearchHandler.waiting_for_item_name
        )

        router.message.register(
            self.start_search, 
            F.text == '💵Найти цену.'
        )
    
    async def start_search(self, message: types.Message, state: FSMContext):
        await message.answer(
            "🔍 Напиши название предмета для поиска:\n\n"
            "Для выхода нажми ❌Отмена",
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(text="❌Отмена")]
                ],
                resize_keyboard=True
            )
        )
        await state.set_state(SearchHandler.waiting_for_item_name)
        await message.delete()
    
    async def search_item(self, message: types.Message, state: FSMContext):
        query = message.text.strip()
        
        if not query:
            await message.answer("❌ Напиши название предмета!")
            return
        
        wait_msg = await message.answer("🔍 Ищу на Steam торговой площадке...")
        
        try:
            results = self.parser.get_item_data(query, parse_mode='HTML')
            await wait_msg.delete()
            
            if not results:
                await message.answer("❌ Ничего не найдено")
            else:
                for msg in results:
                    await message.answer(
                        msg, 
                        parse_mode='HTML', 
                        disable_web_page_preview=True
                    )
                    await asyncio.sleep(0.3)
                    
        except Exception as e:
            await wait_msg.delete()
            await message.answer(
                f"❌ Ошибка:\n<code>{str(e)}</code>", 
                parse_mode='HTML'
            )
            logging.error(f"Ошибка при поиске '{query}': {e}")
        await message.answer(
            "✅ Поиск завершён!\n\n"
            "Можешь ввести новый запрос или нажми ❌Отмена для выхода.",
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(text="❌Отмена")]
                ],
                resize_keyboard=True
            )
        )
    
    async def cancel_search(self, message: types.Message, state: FSMContext):
        await state.clear()
        from key import button
        await message.answer(
            "❌ Поиск отменён",
            reply_markup=button.kb_menu
        )