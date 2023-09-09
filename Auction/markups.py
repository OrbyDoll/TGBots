from aiogram import types
import config as cfg
from cryptography.fernet import Fernet

coder = Fernet(cfg.key)

def code_link(text):
    return coder.encrypt(text).decode()


action_choose = types.InlineKeyboardMarkup(row_width=2)
action_choose.add(
    types.InlineKeyboardButton(text='Список активных аукционов', callback_data='get_auctions'),
    types.InlineKeyboardButton(text='Создать аукцион', callback_data='create_auction'),
    types.InlineKeyboardButton(text='Перейти к своему аукциону', callback_data='my_auction')
)

owner_actions = types.InlineKeyboardMarkup(row_width=1)
owner_actions.add(
    types.InlineKeyboardButton(text='Удалить аукцион', callback_data='remove_auction'),
    types.InlineKeyboardButton(text='Изменить начальную ставку', callback_data='start_cost'),
    types.InlineKeyboardButton(text='Начать аукцион', callback_data='start_auction')
)

member_actions = types.InlineKeyboardMarkup(row_width=2)
member_actions.add(
    types.InlineKeyboardButton(text='Покинуть аукцион', callback_data='leave_auction'),
    types.InlineKeyboardButton(text='Предложить ставку', callback_data='offer_rate')
)
def accept_offer(offer_id):
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Приянть ставку', callback_data=f'accept_offer{offer_id}')
    )

del_auction = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(text='Вернуться в меню', callback_data='return'),
    types.InlineKeyboardButton(text='Перейти в гарант бота', url='https://t.me/pradagarantbot')

)

def get_auction_offer(author_id):
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Вступить в аукцион', callback_data=f'enter_auction{author_id}')
    )
   
# offer Продавец Покупатель Сумма