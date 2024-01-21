from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon import LEXICON
from services.buttons_lists import *
from services.split_list import split_list


start_buttons = [InlineKeyboardButton(text=LEXICON['filter_button'], callback_data='filter_button_pressed'),
                 InlineKeyboardButton(text=LEXICON['search_button'], callback_data='search_button_pressed'),
                 InlineKeyboardButton(text=LEXICON['about_button'], callback_data='about_button_pressed')]

start_keyboard = InlineKeyboardBuilder()
start_keyboard.row(*start_buttons, width=2)


filter_buttons = [InlineKeyboardButton(text=LEXICON['app_scope_button'], callback_data='app_scope_button_pressed'),
                  InlineKeyboardButton(text=LEXICON['converting_button'], callback_data='converting_button_pressed'),
                  InlineKeyboardButton(text=LEXICON['tasks_button'], callback_data='tasks_button_pressed')]

filter_buttons2 = [InlineKeyboardButton(text=LEXICON['clear_button'], callback_data='clear_button_pressed'),
                   InlineKeyboardButton(text=LEXICON['find_button'], callback_data='find_button_pressed')]

filter_keyboard = InlineKeyboardBuilder()
filter_keyboard.row(*filter_buttons, width=1)
filter_keyboard.row(*filter_buttons2, width=2)

return_button = InlineKeyboardButton(text='🔙Вернуться назад', callback_data='return_button_pressed')

back_button = InlineKeyboardButton(text='◀️', callback_data='back_button_pressed')
next_button = InlineKeyboardButton(text='▶️', callback_data='next_button_pressed')

show_button = InlineKeyboardButton(text='Показать', callback_data='show_button_pressed')

show_keyboard = InlineKeyboardBuilder()
show_keyboard.row(show_button, width=1)


def make_sev_keyboards(list_for_splitting: list[InlineKeyboardButton], max_elements) -> list[InlineKeyboardBuilder]:
    result_list = []
    splitted_list = split_list(list_for_splitting, max_elements)

    for arr_id in range(len(splitted_list)):
        some_keyboard = InlineKeyboardBuilder()

        some_keyboard.row(return_button, width=1)
        some_keyboard.row(*splitted_list[arr_id], width=2)

        id_button = InlineKeyboardButton(text=f'{arr_id + 1}/{len(splitted_list)}', callback_data=f'id_button{arr_id}_pressed')

        some_keyboard.row(back_button, id_button, next_button, width=3)

        result_list.append(some_keyboard)

    return result_list


convert_buttons = []

for i in range(len(convert_list)):
    convert_buttons.append(InlineKeyboardButton(text=convert_list[i],
                                                callback_data=convert_callback_list[i]))

convert_keyboards = make_sev_keyboards(convert_buttons, 12)

app_scope_buttons = []

for i in range(len(app_scope_list)):
    app_scope_buttons.append(InlineKeyboardButton(text=app_scope_list[i],
                                                  callback_data=app_scope_callback_list[i]))

app_scope_keyboards = make_sev_keyboards(app_scope_buttons, 10)


tasks_buttons = []

for i in range(len(tasks_list)):
    tasks_buttons.append(InlineKeyboardButton(text=tasks_list[i],
                                              callback_data=tasks_callback_list[i]))

tasks_keyboards = make_sev_keyboards(tasks_buttons, 12)

