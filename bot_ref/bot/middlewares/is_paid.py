from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot_ref.bot.dataclasses import admins_id
from bot_ref.bot.handlers.user_login import payment_text
from bot_ref.bot.keyboards.default_kb import paid_kb
from bot_ref.bot.texts import paid_text
from bot_ref.bot.utils import paid_check


class IsPaidMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.chat.id

        if not await paid_check(user_id) and user_id not in admins_id:
            await event.answer(
                paid_text,
                reply_markup=paid_kb
            )
            await event.answer(payment_text)

            return

        return await handler(event, data)
