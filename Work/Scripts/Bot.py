from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery, BotCommand
import operator
from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from sqlalchemy import create_engine
from database import *
import sqlalchemy
from sqlalchemy.exc import OperationalError
import pymysql
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import request as req

storage = MemoryStorage()
bot = Bot(token='5655746725:AAEa9x8W9pwFKIRe13rg04zz5BZ3vwUGxig')
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)
scheduler = AsyncIOScheduler()
#engine = create_engine("mysql+pymysql://freedb_testadminuser:#q4UD$mVTfVrscM@sql.freedb.tech/freedb_Testbase")
engine = create_engine("mysql+pymysql://admin:testpassword!@194.67.206.233:3306/test_base")
Base.metadata.create_all(engine)
sqlalchemy.pool_recycle = 1
sqlalchemy.pool_timeout = 20
session = Session(engine)
db = DataBase(session)


class LoginFilter(BoundFilter):
    key = 'is_login'

    def __init__(self, is_login):
        self.is_login = is_login

    async def check(self, message: Message):
        if db.get_tg_user(message.from_user.id):
            return True
        else:
            return False


dp.filters_factory.bind(LoginFilter)


class MySG(StatesGroup):
    main = State()
    preview = State()
    purpose = State()
    confirm = State()


class LogSG(StatesGroup):
    mail = State()


async def on_input(msg: Message, dialog: Dialog, manager: DialogManager):
    manager.current_context().dialog_data["mail"] = msg.text
    usr = db.get_user_by_mail(msg.text)
    adm = db.get_admin_by_mail(msg.text)
    if usr or adm:
        await msg.answer("Успех!")
        db.add_tg_user(msg.from_user.id, usr[0].mail if usr else adm[0].mail, usr[1].power if usr else adm[1].power)
        await manager.done()
    else:
        await msg.answer("Нет пользователя с такой почтой! Пожалуйста, повторите ввод")


# async def hello(c: CallbackQuery, button: Button, manager: DialogManager):
#     await manager.dialog().switch_to(MySG.sec)
#     await c.message.delete()
#     await c.message.answer(button.widget_id)


async def end(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.edit_text("Выбор отменён")
    await manager.done()


# def test_buttons_creator(database: DataBase):
#     buttons = []
#     mas = database.get_all_equipment()
#     for i in mas:
#         if (i.count - i.reserve_count) > 0:
#             buttons.append(Button(Const(i.title), id=str(i.id), on_click=hello))
#     return buttons


async def get_data(**kwargs):
    try:
        mas = db.get_all_equipment()
    except OperationalError:
        session.rollback()
        mas = db.get_all_equipment()
    print(len(mas))
    out_list = []
    for i in mas:
        if i.count - i.reserve_count > 0:
            out_list.append((i.title, i.id))
    return {"eq": out_list}


async def ans(c: CallbackQuery, button: Button, manager: DialogManager, button_id):
    user = db.get_tg_user(c.from_user.id)
    eq = db.get_equipment_by_id(button_id)
    manager.data["title"] = eq.title
    manager.data["description"] = eq.description
    if eq.access > user.power:
        manager.data["possible"] = "Вы не можете запросить это оборудование."
        manager.data["extend"] = False
    else:
        manager.data["possible"] = "Вы можете запросить это оборудование"
        manager.data["extend"] = True
        db.add_last_request(c.from_user.id, eq.title, eq.description)
    await manager.dialog().switch_to(MySG.preview)


async def get_equipment_user_data(dialog_manager: DialogManager, **kwargs):
    return {
        "title": dialog_manager.data.get("title"),
        "purpose": dialog_manager.data.get("purpose"),
        "description": dialog_manager.data.get("description"),
        "possible": dialog_manager.data.get("possible"),
        "extend": dialog_manager.data.get("extend"),
        "input": dialog_manager.data.get("input")
    }


async def switch_to_choice(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(MySG.main)


async def switch_to_confirm(msg: Message, dialog: Dialog, manager: DialogManager):
    manager.data["input"] = msg.text
    await manager.dialog().switch_to(MySG.confirm)


async def send_request(c: CallbackQuery, button: Button, manager: DialogManager):
    r = db.get_last_request(c.from_user.id)
    mail = db.get_tg_user(c.from_user.id).mail
    request = req.Request(c.from_user.id, mail, r.title,
                          1, c.message.text[c.message.text.find(":")+2: c.message.text.find("Продолжить?")])
    db.add_request(request)
    await c.message.edit_text(f"Оборудование {r.title} заказано!\nКак только администратор ответит на ваш запрос "
                              f"- вы получите уведомление")
    await manager.done()


async def switch_to_input(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(MySG.purpose)


scrolling_group = ScrollingGroup(
    Select(
        Format("{item[0]}"),
        item_id_getter=operator.itemgetter(1),
        items="eq",
        id="test",
        on_click=ans
    ),
    id="numbers",
    width=1,
    height=6,
)

main_window = Window(
    Const("Список оборудования, которое есть в наличии: (Я работаю)!!!"),
    scrolling_group,
    Button(Const("Отмена"), id="34", on_click=end),
    state=MySG.main,
    getter=get_data
)

preview_window = Window(
    Format("Оборудование: {title}\nОписание: {description}\n{possible}"),
    Button(Const("Продолжить"), id="next", when="extend", on_click=switch_to_input),
    Button(Const("Назад"), id="prev", on_click=switch_to_choice),
    getter=get_equipment_user_data,
    state=MySG.preview
)

purpose_window = Window(
    Const("Последний шаг: введите для какой цели вы запрашиваете оборудование"),
    MessageInput(switch_to_confirm),
    Button(Const("Отмена"), id="cancel", on_click=switch_to_choice),
    getter=get_equipment_user_data,
    state=MySG.purpose
)

confirm_input = Window(
    Format("Вы ввели:\n{input}\nПродолжить?"),
    Button(Const("Отправить"), id="yes", on_click=send_request),
    Button(Const("Повторить ввод"), id="retry", on_click=switch_to_input),
    Button(Const("Отмена"), id="cancel", on_click=switch_to_choice),
    getter=get_equipment_user_data,
    state=MySG.confirm
)

greetings_window = Window(
    Const("Введите почту"),
    MessageInput(on_input),
    state=LogSG.mail,
)

dialog = Dialog(main_window, preview_window, purpose_window, confirm_input)
log_menu = Dialog(greetings_window)


@dp.message_handler(commands=["start"])
async def start(msg: Message, dialog_manager: DialogManager):
    if not db.get_tg_user(msg.from_user.id):
        await msg.answer("Добро пожаловть! Для запроса оборудования необходимо войти в систему!")
        await dialog_manager.start(LogSG.mail, mode=StartMode.NORMAL)
    else:
        await msg.answer("Вы уже вошли! Для смена аккаунта используйте комманду /login")


@dp.message_handler(commands=["login"])
async def login(msg: Message, dialog_manager: DialogManager):
    await dialog_manager.start(LogSG.mail, mode=StartMode.RESET_STACK)


@dp.message_handler(is_login=True, commands=["get_equipment"])
async def get_equipment(msg: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK)


async def send_notification(dp: Dispatcher):
    mas = db.get_solved_requests()
    for i in mas:
        if i.approved is False:
            db.del_request(i.user_id, i.title)
            await dp.bot.send_message(i.user_id, f"Ваш запрос на выдачу {i.tittle} отклонён!")
        else:
            await dp.bot.send_message(i.user_id, f"Ваш запрос на выдачу {i.tittle} принят! Вы можете забрать "
                                                 f"своё оборудование уже сейчас!")

scheduler.add_job(send_notification, "interval", seconds=600, args=(dp,))
if __name__ == '__main__':
    registry.register(dialog)
    registry.register(log_menu)
    scheduler.start()
    executor.start_polling(dp, skip_updates=True)
