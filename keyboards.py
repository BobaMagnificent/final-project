from telebot import types

keyboard_first = types.InlineKeyboardMarkup(row_width=2)
btn1 = types.InlineKeyboardButton('Да', callback_data='yes')
btn2 = types.InlineKeyboardButton('Нет', callback_data='no')
keyboard_first.add(btn1, btn2)

keyboard_second = types.InlineKeyboardMarkup(row_width=2)
btn1_2 = types.InlineKeyboardButton('Об авторе', url='https://en.wikipedia.org/wiki/Boris_Ryzhy')
btn2_2 = types.InlineKeyboardButton('Стихи',
                                    url='https://www.culture.ru/literature/poems/author-boris-ryzhii'
                                    )
keyboard_second.add(btn1_2, btn2_2)