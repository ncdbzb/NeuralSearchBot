from random import sample
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_data.config import load_config, Config
from lexicon.lexicon import LEXICON
from keyboards.keyboards import (start_keyboard, filter_keyboard, convert_keyboards, app_scope_keyboards,
                                 tasks_keyboards, show_keyboard)
from dispatcher.dispatcher import dp, storage
from services.buttons_lists import *
from services.picked_filters_message import form_message
from services.form_sql_query import form_sql_query
from services.find_neurals import find_neurals
from database.database import Database


class FSMGame(StatesGroup):
    search_message = State()


config: Config = load_config('.env')
db = Database()
router = Router()
# picked_filters_dict = {'app_scope': [],
#                        'converting': [],
#                        'tasks': []}
matches_of_five = []
show_more_keyboards = []
show_less_keyboards = []
show_more_responses_list = []
show_less_responses_list = []


@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['start'].format(message.from_user.first_name), parse_mode='html',
                         reply_markup=start_keyboard.as_markup(resize_keyboard=True))
    key = StorageKey(bot_id=config.tg_bot.bot_id, chat_id=message.chat.id, user_id=message.from_user.id)
    data = await dp.storage.get_data(key)
    if 'picked_filters_dict' not in data.keys():
        await dp.storage.update_data(key=key, data={'picked_filters_dict': {'app_scope': [], 'converting': [], 'tasks': []}})
    await state.clear()


@router.message(StateFilter(FSMGame.search_message))
async def process_search_message(message: Message, state: FSMContext):
    answer = find_neurals(message.text, db.get_descriptions(), 3)
    await message.answer(text=answer[0])
    await state.clear()


@router.callback_query(F.data == 'filter_button_pressed')
async def process_filter_button(callback: CallbackQuery):
    key = StorageKey(bot_id=config.tg_bot.bot_id, chat_id=callback.message.chat.id, user_id=callback.from_user.id)
    data = await dp.storage.get_data(key)
    picked_filters_dict = data['picked_filters_dict']
    picked_filters_message = form_message(picked_filters_dict)
    await callback.message.answer(text=LEXICON['filter_process'].format(picked_filters_message), parse_mode='html',
                                  reply_markup=filter_keyboard.as_markup(resize_keyboard=True))
    await callback.answer()


@router.callback_query(F.data == 'search_button_pressed')
async def process_search_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['search_process'])
    await state.set_state(FSMGame.search_message)


@router.callback_query(F.data == 'about_button_pressed')
async def process_about_button(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON['about_process'])


@router.callback_query(F.data == 'app_scope_button_pressed')
async def process_app_scope_button(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['app_scope_process'],
                                     reply_markup=app_scope_keyboards[0].as_markup(resize_keyboard=True))


@router.callback_query(F.data == 'converting_button_pressed')
async def process_converting_button(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['converting_process'],
                                     reply_markup=convert_keyboards[0].as_markup(resize_keyboard=True))


@router.callback_query(F.data == 'tasks_button_pressed')
async def process_tasks_button(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['tasks_process'],
                                     reply_markup=tasks_keyboards[0].as_markup(resize_keyboard=True))


@router.callback_query(F.data.in_(['back_button_pressed', 'next_button_pressed']))
async def process_back_button(callback: CallbackQuery):
    mess = callback.message.text.split()[0]
    match mess:
        case 'Преобразование':
            keyd = convert_keyboards
            lex = 'converting_process'
        case 'Задачи':
            keyd = tasks_keyboards
            lex = 'tasks_process'
        case 'Сферы':
            keyd = app_scope_keyboards
            lex = 'app_scope_process'
        case _:
            keyd = []
            lex = ''
    page_pag = callback.message.reply_markup.inline_keyboard[-1][1].text
    page_id = int(page_pag[:page_pag.index('/')]) - 1
    if callback.data == 'back_button_pressed':
        if page_id > 0:
            await callback.message.edit_text(text=LEXICON[lex],
                                             reply_markup=keyd[page_id - 1].as_markup(resize_keyboard=True))
        else:
            await callback.answer(text='')
    elif callback.data == 'next_button_pressed':
        if page_id < len(keyd) - 1:
            await callback.message.edit_text(text=LEXICON[lex],
                                             reply_markup=keyd[page_id + 1].as_markup(resize_keyboard=True))
        else:
            await callback.answer(text='')


@router.callback_query(F.data == 'return_button_pressed')
async def process_return_button(callback: CallbackQuery):
    key = StorageKey(bot_id=config.tg_bot.bot_id, chat_id=callback.message.chat.id, user_id=callback.from_user.id)
    data = await dp.storage.get_data(key)
    picked_filters_dict = data['picked_filters_dict']
    picked_filters_message = form_message(picked_filters_dict)
    await callback.message.edit_text(text=LEXICON['filter_process'].format(picked_filters_message), parse_mode='html',
                                     reply_markup=filter_keyboard.as_markup(resize_keyboard=True))


@router.callback_query(F.data == 'clear_button_pressed')
async def process_clear_button(callback: CallbackQuery):
    key = StorageKey(bot_id=config.tg_bot.bot_id, chat_id=callback.message.chat.id, user_id=callback.from_user.id)
    await dp.storage.update_data(key=key, data={'picked_filters_dict': {'app_scope': [], 'converting': [], 'tasks': []}})
    data = await dp.storage.get_data(key)
    picked_filters_dict = data['picked_filters_dict']
    picked_filters_message = form_message(picked_filters_dict)
    await callback.message.edit_text(text=LEXICON['filter_process'].format(picked_filters_message), parse_mode='html',
                                     reply_markup=filter_keyboard.as_markup(resize_keyboard=True))


@router.callback_query(F.data == 'find_button_pressed')
async def process_find_button(callback: CallbackQuery):
    key = StorageKey(bot_id=config.tg_bot.bot_id, chat_id=callback.message.chat.id, user_id=callback.from_user.id)
    matches_of_five.clear()
    data = await dp.storage.get_data(key)
    picked_filters_dict = data['picked_filters_dict']
    sql_query = form_sql_query(picked_filters_dict)
    if sql_query.startswith('SELECT'):
        matches = db.get_data(sql_query)
        if not matches:
            await callback.message.answer(text=LEXICON['nothing_found'])
            return
        matches_length = len(matches)
        response = LEXICON['before_find_button'].format(matches_length)
        if matches_length > 5:
            matches = sample(matches, 5)
        for i in matches:
            matches_of_five.append(i)
        await callback.message.answer(text=response,
                                      reply_markup=show_keyboard.as_markup(resize_keyboard=True))
    else:
        await callback.message.answer(text=sql_query)


@router.callback_query(F.data == 'show_button_pressed')
async def process_show_button(callback: CallbackQuery):
    show_more_responses_list.clear()
    show_less_responses_list.clear()
    show_more_keyboards.clear()
    show_less_keyboards.clear()
    for matches_id in range(len(matches_of_five)):
        show_more_responses = LEXICON['show_more_responses'].format(matches_of_five[matches_id][0],
                                                                    matches_of_five[matches_id][4],
                                                                    matches_of_five[matches_id][5])
        show_more_responses_list.append(show_more_responses)

        show_more_button = InlineKeyboardButton(text='Показать больше',
                                                callback_data=f'learn_more_button_pressed{matches_id}')
        show_less_button = InlineKeyboardButton(text='Показать меньше',
                                                callback_data=f'learn_less_button_pressed{matches_id}')
        next_neural_button = InlineKeyboardButton(text='Далее', callback_data=f'next_neural_button_pressed{matches_id}')

        show_more_keyboard = InlineKeyboardBuilder()
        show_less_keyboard = InlineKeyboardBuilder()
        show_more_keyboard.row(show_more_button, next_neural_button, width=2)
        show_less_keyboard.row(show_less_button, width=1)
        show_more_keyboards.append(show_more_keyboard)
        show_less_keyboards.append(show_less_keyboard)

        response = LEXICON['find_button_pressed'].format(matches_of_five[matches_id][0],
                                                         matches_of_five[matches_id][1],
                                                         matches_of_five[matches_id][2],
                                                         matches_of_five[matches_id][3])
        show_less_responses_list.append(response)
    await callback.message.answer(text=show_less_responses_list[0],
                                  reply_markup=show_more_keyboards[0].as_markup(resize_keyboard=True))


@router.callback_query(F.data.startswith('learn_less_button_pressed'))
async def process_learn_less_button(callback: CallbackQuery):
    neural_id = int(str(callback.data)[-1])
    await callback.message.edit_text(text=show_less_responses_list[neural_id],
                                     reply_markup=show_more_keyboards[neural_id].as_markup(resize_keyboard=True))


@router.callback_query(F.data.startswith('learn_more_button_pressed'))
async def process_learn_more_button(callback: CallbackQuery):
    neural_id = int(str(callback.data)[-1])
    await callback.message.edit_text(text=show_more_responses_list[neural_id],
                                     reply_markup=show_less_keyboards[neural_id].as_markup(resize_keyboard=True))


@router.callback_query(F.data.startswith('next_neural_button_pressed'))
async def process_next_neural_button(callback: CallbackQuery):
    neural_id = int(str(callback.data)[-1])
    if neural_id == len(matches_of_five) - 1:
        await callback.message.answer(LEXICON['pay_money'])
    else:
        await callback.message.answer(text=show_less_responses_list[neural_id + 1],
                                      reply_markup=show_more_keyboards[neural_id + 1]
                                      .as_markup(resize_keyboard=True))
    await callback.answer()


@router.callback_query(F.data.in_(app_scope_callback_list + convert_callback_list[:-1] + tasks_callback_list))
async def process_click_button(callback: CallbackQuery):
    key = StorageKey(bot_id=config.tg_bot.bot_id, chat_id=callback.message.chat.id, user_id=callback.from_user.id)
    data = await dp.storage.get_data(key)
    picked_filters_dict = data['picked_filters_dict']
    cb_data = callback.data
    if cb_data in app_scope_callback_list:
        index = app_scope_callback_list.index(cb_data)
        mess = app_scope_list[index]
        if mess not in picked_filters_dict['app_scope']:
            picked_filters_dict['app_scope'].append(mess)
            await callback.answer(text='Фильтр добавлен!')
        else:
            picked_filters_dict['app_scope'].remove(mess)
            await callback.answer(text='Выбор отменен')
    elif cb_data in convert_callback_list:
        index = convert_callback_list.index(cb_data)
        mess = convert_list[index]
        if mess not in picked_filters_dict['converting']:
            picked_filters_dict['converting'].append(mess)
            await callback.answer(text='Фильтр добавлен!')
        else:
            picked_filters_dict['converting'].remove(mess)
            await callback.answer(text='Выбор отменен')
    else:
        index = tasks_callback_list.index(cb_data)
        mess = tasks_list[index]
        if mess not in picked_filters_dict['tasks']:
            picked_filters_dict['tasks'].append(mess)
            await callback.answer(text='Фильтр добавлен!')
        else:
            picked_filters_dict['tasks'].remove(mess)
            await callback.answer(text='Выбор отменен')

    await dp.storage.update_data(key=key, data={'picked_filters_dict': picked_filters_dict})
