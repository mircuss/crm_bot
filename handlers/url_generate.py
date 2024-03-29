import aiohttp
from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from states.channel import ChannelStates

url_router = Router()


@url_router.callback_query(F.data.startswith("channel"))
async def get_names(call: CallbackQuery, state: FSMContext):
    channel = int(call.data.split("_")[-1])
    await call.message.answer(
        text="Введите названия для ссылок с начала строки")
    await state.set_state(ChannelStates.get_names)
    await state.update_data({"channel": channel})


@url_router.message(StateFilter(ChannelStates.get_names))
async def add_data(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    links = []
    names = message.text.split("\n")
    for i in range(len(names)):
        link = await bot.create_chat_invite_link(chat_id=data["channel"],
                                                 name=f"{names[i]}",
                                                 creates_join_request=True)
        links.append(link.invite_link)
    params = {'links': ','.join(links), 'names': ','.join(names)}
    async with aiohttp.ClientSession() as session:
        await session.get(url="http://127.0.0.1:8000/add_links", params=params)
    await message.answer(text="\n".join(links))
    await state.clear()
