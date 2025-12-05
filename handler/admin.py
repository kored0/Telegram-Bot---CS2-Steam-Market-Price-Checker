from aiogram.filters import BaseFilter
from aiogram.types import Message
import config as cfg

class Check_admin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if isinstance(cfg.admin_id, list):
            return message.from_user.id in cfg.admin_id
        else:
            return message.from_user.id == cfg.admin_id