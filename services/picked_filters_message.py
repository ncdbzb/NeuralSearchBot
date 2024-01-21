from lexicon.lexicon import LEXICON

form_message_ru = {
    'app_scope': 'Сферы применения',
    'converting': 'Преобразование',
    'tasks': 'Задачи'
}


def form_message(p_dict) -> str:
    if not any(p_dict.values()):
        return LEXICON['picked_filters_message']

    message = '\n'

    for key, value in p_dict.items():
        if value:
            message += f"<b>{form_message_ru[key]}</b>: {', '.join(*[value])}\n"

    return message
