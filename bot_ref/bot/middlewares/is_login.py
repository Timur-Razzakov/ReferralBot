from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot_ref.bot.keyboards import sign_inup_kb
from bot_ref.bot.texts import login_required_text
from bot_ref.bot.utils import check_login


class IsLoginMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            user_id = event.chat.id
        else:
            user_id = event.message.chat.id

        if not await check_login(user_id):
            await event.answer(
                login_required_text,
                reply_markup=sign_inup_kb.markup
            )
            return

        return await handler(event, data)
