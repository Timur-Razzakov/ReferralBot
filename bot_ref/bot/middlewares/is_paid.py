from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot_ref.bot.keyboards.default_kb import paid_kb
from bot_ref.bot.utils import paid_check


class IsPaidMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.chat.id

        if not await paid_check(user_id):
            await event.answer(
                'С начало оплатите взнос 💵',
                reply_markup=paid_kb
            )
            return

        return await handler(event, data)
