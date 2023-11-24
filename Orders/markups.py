from aiogram import types

start_menu = (
    types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    .row(types.KeyboardButton("Заказать"))
    .row(types.KeyboardButton("Жалобы"), types.KeyboardButton("Условия"))
)

service_choose = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton("Дизайн", callback_data="service_design"),
    types.InlineKeyboardButton("Докс", callback_data="service_docs"),
    types.InlineKeyboardButton("СММ", callback_data="service_smm"),
    types.InlineKeyboardButton("Материалы", callback_data="service_materials"),
)


def get_service_description(service):
    descriptions = {
        "design": "Описание направления дизайна",
        "docs": "Описание направления докс",
        "smm": "Описание направления смм",
        "materials": "Описание направления материалов",
    }
    return descriptions[service]


def get_service_buttons(service):
    service_buttons = (
        types.InlineKeyboardMarkup()
        .row(types.InlineKeyboardButton("Заказать", callback_data=f"order_{service}"))
        .row(
            types.InlineKeyboardButton("Прайс", callback_data=f"price_{service}"),
            types.InlineKeyboardButton("Портфолио", callback_data=f"works_{service}"),
        )
        .row(
            types.InlineKeyboardButton(
                "Назад к выбору сервисов", callback_data="back_to_services"
            )
        )
    )
    return service_buttons
