import operator
import aiogram.utils.exceptions
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import *
from conf import *

storage = MemoryStorage()
bot = Bot(token='5655746725:AAEa9x8W9pwFKIRe13rg04zz5BZ3vwUGxig')
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)
scheduler = AsyncIOScheduler()
# engine = create_engine("mysql+pymysql://freedb_testadminuser:#q4UD$mVTfVrscM@sql.freedb.tech/freedb_Testbase")
# engine = create_engine("mysql+pymysql://developer:deVpass@194.67.206.233:3306/dev_base")
engine = create_engine(BASE_URL)
#engine = create_engine("mysql+pymysql://admin:Sapr_714@192.168.43.130:3306/test")
Base.metadata.create_all(engine)
db = DataBase(engine)


class LoginFilter(BoundFilter):
    key = 'is_login'

    def __init__(self, is_login):
        self.is_login = is_login

    async def check(self, message: Message):
        if db.get_tg_user_by_tg(message.from_user.id):
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
    setting_password = State()
    password = State()


async def on_input(msg: Message, curr_dialog: Dialog, manager: DialogManager):
    # manager.current_context().dialog_data["mail"] = msg.text
    usr = db.get_user_by_mail(msg.text)
    if usr:
        manager.data["login"] = msg.text
        db.add_last_login(msg.from_user.id, usr.mail)
        if db.get_user_login(usr.mail):
            await manager.dialog().switch_to(LogSG.password)
        else:
            await manager.dialog().switch_to(LogSG.setting_password)
    else:
        await msg.answer("Нет пользователя с такой почтой! Пожалуйста, повторите ввод")


async def setting_password(msg: Message, curr_dialog: Dialog, manager: DialogManager):
    password = msg.text
    usr = db.get_user_by_mail(db.get_last_login(msg.from_user.id).login)
    db.add_user_login(usr.id, usr.mail, password)
    db.add_tg_user(msg.from_user.id, usr.id)
    await msg.answer("Успех!")
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    inline_keyboard.add(*[
        InlineKeyboardButton(text="Войти как новый пользователь", callback_data="login"),
        InlineKeyboardButton(text="Запросить оборудование", callback_data="get_equipment"),
        InlineKeyboardButton(text="Посмотреть список ваших запросов", callback_data="my_requests")
    ])
    await msg.answer("Вот что вы можете сделать:", reply_markup=inline_keyboard)
    await manager.done()


async def input_password(msg: Message, curr_dialog: Dialog, manager: DialogManager):
    password = msg.text
    user_login = db.get_user_login(db.get_last_login(msg.from_user.id).login)
    if password == user_login.password:
        db.add_tg_user(msg.from_user.id, user_login.id)
        await msg.answer("Успех!")
        inline_keyboard = InlineKeyboardMarkup(row_width=1)
        inline_keyboard.add(*[
                InlineKeyboardButton(text="Войти как новый пользователь", callback_data="login"),
                InlineKeyboardButton(text="Запросить оборудование", callback_data="get_equipment"),
                InlineKeyboardButton(text="Посмотреть список ваших запросов", callback_data="my_requests")
             ])
        await msg.answer("Вот что вы можете сделать:", reply_markup=inline_keyboard)
        await manager.done()
    else:
        await msg.answer("Неверный пароль!")
        await manager.dialog().switch_to(LogSG.mail)


async def end(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.edit_text("Выбор отменён")
    await manager.done()


async def get_data(**kwargs):
    mas = db.get_all_equipment()
    out_list = []
    for i in mas:
        if i.count - i.reserve_count > 0:
            out_list.append((i.title, i.id))
    return {"eq": out_list}


async def ans(c: CallbackQuery, button: Button, manager: DialogManager, button_id):
    eq = db.get_equipment_by_id(button_id)
    manager.data["title"] = eq.title
    manager.data["description"] = eq.description
    """if not any(x in [j.group_id for j in eq.equipment_groups] for x in mas):
        manager.data["possible"] = "Вы не можете запросить это оборудование."
        manager.data["extend"] = False
    else:"""
    manager.data["possible"] = "Вы можете запросить это оборудование"
    manager.data["extend"] = True
    db.add_last_request(c.from_user.id, eq.title)
    await manager.dialog().switch_to(MySG.purpose)


async def get_equipment_user_data(dialog_manager: DialogManager, **kwargs):
    return {
        "title": dialog_manager.data.get("title"),
        "description": dialog_manager.data.get("description"),
        "possible": dialog_manager.data.get("possible"),
        "extend": dialog_manager.data.get("extend"),
        "input": dialog_manager.data.get("input")
    }


async def get_login_user_data(dialog_manager: DialogManager, **kwargs):
    return {"login": dialog_manager.data.get("login")}


async def switch_to_choice(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(MySG.main)


async def switch_to_confirm(msg: Message, curr_dialog: Dialog, manager: DialogManager):
    manager.data["input"] = msg.text
    await manager.dialog().switch_to(MySG.confirm)


async def send_request(c: CallbackQuery, button: Button, manager: DialogManager):
    r = db.get_last_request(c.from_user.id)
    usr = db.get_tg_user_by_tg(c.from_user.id)
    adm = db.get_admin_by_id(usr.id)
    eq = db.get_equipment_by_title(r.title)
    mas = [j.group_id for j in usr.user.user_groups]
    if adm:
        db.add_admin_request(req.Request(adm.user.id, db.get_equipment_by_title(r.title).id, 1,
                                         c.message.text[
                                         c.message.text.find(":") + 2: c.message.text.find("Продолжить?")]))
        await c.message.edit_text(
            f"Оборудование *{r.title}* заказано!\nНа правах администратора система вам автоматически"
            f"одобрила запрос! Вы можете забрать оборудование уже сейчас!", parse_mode='Markdown')
        await manager.done()
    elif any(x in [j.group_id for j in eq.equipment_groups] for x in mas):
        db.add_admin_request(req.Request(usr.user.id, db.get_equipment_by_title(r.title).id, 1,
                                         c.message.text[
                                         c.message.text.find(":") + 2: c.message.text.find("Продолжить?")]))
        await c.message.edit_text(f"Оборудование *{r.title}* заказано!\nТак как вы принадлежите к одной из групп с "
                                  f"доступом - система вам автоматически одобрила запрос! "
                                  f"Вы можете забрать оборудование уже сейчас!", parse_mode='Markdown')
        await manager.done()
    else:
        request = req.Request(usr.user.id, db.get_equipment_by_title(r.title).id,
                              1, c.message.text[c.message.text.find(":") + 2: c.message.text.find("Продолжить?")])
        db.add_user_request(request)
        await c.message.edit_text(f"Оборудование *{r.title}* заказано!\nКак только администратор ответит на ваш запрос "
                                  f"- вы получите уведомление", parse_mode='Markdown')
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
    Const("Список оборудования, которое есть в наличии:"),
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
    Format("Оборудование: {title}\nОписание: {description}\n{possible}"),
    Const("Последний шаг: введите для какой цели вы запрашиваете оборудование"),
    MessageInput(switch_to_confirm),
    Button(Const("Отмена"), id="cancel", on_click=switch_to_choice),
    getter=get_equipment_user_data,
    state=MySG.purpose
)

confirm_input_window = Window(
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

setting_password_window = Window(
    Format("Вы впервые вошли под {login}, пожалуйста, установите пароль"),
    MessageInput(setting_password),
    getter=get_login_user_data,
    state=LogSG.setting_password
)

input_password_window = Window(
    Format("Введите пароль для {login}"),
    MessageInput(input_password),
    getter=get_login_user_data,
    state=LogSG.password
)

dialog = Dialog(main_window, preview_window, purpose_window, confirm_input_window)
log_menu = Dialog(greetings_window, setting_password_window, input_password_window)


@dp.message_handler(commands=["start"])
async def start(msg: Message, dialog_manager: DialogManager):
    if not db.get_tg_user_by_tg(msg.from_user.id):
        await msg.answer("Добро пожаловть! Для запроса оборудования необходимо войти в систему!")
        await dialog_manager.start(LogSG.mail, mode=StartMode.NORMAL)
    else:
        await msg.answer("Вы уже вошли! Для смена аккаунта используйте комманду /login")


@dp.message_handler(commands=["login"])
@dp.callback_query_handler(text="login")
async def login(msg: Message, dialog_manager: DialogManager):
    if isinstance(msg, CallbackQuery):
        await msg.answer()
    await dialog_manager.start(LogSG.mail, mode=StartMode.RESET_STACK)


@dp.message_handler(commands=['my_requests'])
@dp.callback_query_handler(text="my_requests")
async def my_equip(msg: Union[Message, CallbackQuery]):
    user_id = db.get_tg_user_by_tg(msg.from_user.id).id
    mas = db.get_user_requests(user_id)
    answer = "*Ваши запросы*\n*Полученные:*\n"
    for i in mas:
        if i.taken:
            answer += f"__{i.equipment.title}__\n"
    answer += "*Ожидающие получения:*\n"
    for i in mas:
        if i.approved is True and not i.taken:
            answer += f"__{i.equipment.title}__\n"
    answer += "*Ожидающие решения администратора:*\n"
    for i in mas:
        if not i.solved:
            answer += f"__{i.equipment.title}__"
    if isinstance(msg, CallbackQuery):
        await msg.answer()
        await bot.send_message(msg.message.chat.id, answer, parse_mode='Markdown')
    else:
        await msg.answer(answer, parse_mode='Markdown')


@dp.message_handler(is_login=True, commands=["get_equipment"])
@dp.callback_query_handler(text="get_equipment")
async def get_equipment(msg: Message, dialog_manager: DialogManager):
    if isinstance(msg, CallbackQuery):
        await msg.answer()
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK)


async def send_request_notification(user_tg_id: int, title: str, user_login: str, request: Type[UserRequests]):
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    inline_keyboard.add(*[
        InlineKeyboardButton(text="Одобрить", callback_data="approve"),
        InlineKeyboardButton(text="Отклонить", callback_data="reject")
    ])
    msg = await bot.send_message(user_tg_id, f"Поступил запрос на *{title}*\n"
                                       f"От: *{user_login}*\n"
                                       f"Для: *{request.purpose}*\n"
                                       f"Одобрить?", reply_markup=inline_keyboard, parse_mode='Markdown')

    db.add_tg_message(msg.chat.id, request.id, msg.message_id)


@dp.callback_query_handler(text="approve")
async def approve_request(c: CallbackQuery):
    request = db.get_message_by_chat_and_message_id(c.message.chat.id, c.message.message_id).request
    if not request or request.solved is True:
        await c.answer("Решение по запросу уже приняли, простите за беспокойство")
        await bot.delete_message(c.message.chat.id, c.message.message_id)
    else:
        request.solved = True
        request.approved = True
        db.update_user_request(request)
        await c.answer("Запрос одобрен!")
    await del_useless_messages()


@dp.callback_query_handler(text="reject")
async def reject_request(c: CallbackQuery):
    request = db.get_message_by_chat_and_message_id(c.message.chat.id, c.message.message_id)
    if not request or request.request.solved is True:
        await c.answer("Решение по запросу уже приняли, простите за беспокойство")
        await bot.delete_message(c.message.chat.id, c.message.message_id)
    else:
        request.solved = True
        request.approved = False
        db.update_user_request(request.request)
        await c.answer("Запрос отклонён!")
    await del_useless_messages()


async def send_notification(dp: Dispatcher):
    mas = db.get_solved_unannounced_users_request()
    for i in mas:
        try:
            if i.approved is False:
                for j in db.get_tg_user_by_id(i.sender_id):
                    await dp.bot.send_message(j.tg_id,
                                            f"Ваш запрос на выдачу *{db.get_equipment_by_id(i.equipment_id).title}* отклонён!",
                                            parse_mode='Markdown')
                eq = db.get_equipment_by_id(i.equipment_id)
                eq.reserve_count -= i.count
                db.update_equipment(eq)
                db.del_user_request(i.id)
            else:
                for j in db.get_tg_user_by_id(i.sender_id):
                    await dp.bot.send_message(j.tg_id,
                                            f"Ваш запрос на выдачу *{db.get_equipment_by_id(i.equipment_id).title}* принят! Вы можете забрать "
                                            f"своё оборудование уже сейчас!", parse_mode='Markdown')
                i.notified = True
                db.update_user_request(i)
        except aiogram.utils.exceptions.ChatNotFound:
            pass
    mas = db.get_unsolved_users_requests()
    notified = db.get_all_adm_notified_requests()
    notified = [i[0] for i in notified]
    mas = [i for i in mas if i.id not in notified]
    admins = db.get_all_tg_admins()
    for i in mas:
        equipment = db.get_equipment_by_id(i.equipment_id)
        user = db.get_user_by_id(i.sender_id)
        for j in admins:
            try:
                await send_request_notification(j.tg_id, equipment.title, user.mail, i)
            except aiogram.utils.exceptions.ChatNotFound:
                pass
    await del_useless_messages()


async def del_useless_messages():
    mas = db.get_useless_tg_messages()
    reqs = set([i.request_id for i in mas])
    for i in mas:
        await bot.delete_message(i.tg_chat_id, i.message_id)
    for i in reqs:
        db.del_tg_message_by_request(i)


scheduler.add_job(send_notification, "interval", seconds=10, args=(dp,))
if __name__ == '__main__':
    registry.register(dialog)
    registry.register(log_menu)
    scheduler.start()
    executor.start_polling(dp, skip_updates=True)

