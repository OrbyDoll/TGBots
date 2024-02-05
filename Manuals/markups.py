from aiogram import types
import config as cfg

categor_choose_forward = types.InlineKeyboardMarkup(row_width=1).add(
    types.InlineKeyboardButton(
        text="🏺АУКЦИОН BY PRADA🏺", callback_data="АУКЦИОН BY PRADA"
    ),
    types.InlineKeyboardButton(
        text="🏠НЕДВИГА 1.0 BY PRADA🏠", callback_data="НЕДВИГА 1.0 BY PRADA"
    ),
    types.InlineKeyboardButton(
        text="🏠НЕДВИГА 2.0 BY PRADA🏠", callback_data="НЕДВИГА 2.0 BY PRADA"
    ),
    types.InlineKeyboardButton(text="💊N@RKO BY PRADA💊", callback_data="N@RKO BY PRADA"),
    types.InlineKeyboardButton(text="📑МФО BY PRADA📑", callback_data="МФО BY PRADA"),
    types.InlineKeyboardButton(text="👥ТРАФИК BY PRADA👥", callback_data="трафик by prada"),
).row(
    types.InlineKeyboardButton(text="⬅️Назад", callback_data="forward_1"),
    types.InlineKeyboardButton(text="Вперед➡️", callback_data="forward"),
)
categor_choose_back_1 = types.InlineKeyboardMarkup(row_width=1).add(
    types.InlineKeyboardButton(
        text="💱EXCHANGE BY PRADA💱", callback_data="EXCHANGE BY PRADA"
    ),
    types.InlineKeyboardButton(text="⚙️ADMINISTRATOR⚙️", callback_data="ADMINISTRATOR"),
    types.InlineKeyboardButton(
        text="📜ПОСОБИЯ BY PRADA📜", callback_data="ПОСОБИЯ BY PRADA"
    ),
    types.InlineKeyboardButton(
        text="🕵️‍♂️SAFETY 1.0 BY PRADA💻 (техника)",
        callback_data="SAFETY 1.0 BY PRADA (техника)",
    ),
    types.InlineKeyboardButton(
        text="🕵️‍♂️SAFETY 2.0 BY PRADA🧠 (поведение)",
        callback_data="SAFETY 2.0 BY PRADA (поведение)",
    ),
    types.InlineKeyboardButton(
        text="🕵️‍♂️SAFETY 3.0 BY PRADA💰 (отмыв)",
        callback_data="SAFETY 3.0 BY PRADA (отмыв)",
    ),
).row(
    types.InlineKeyboardButton(text="⬅️Назад", callback_data="back_1"),
    types.InlineKeyboardButton(text="Вперед➡️", callback_data="forward_1"),
)

categor_choose_back = types.InlineKeyboardMarkup(row_width=1).add(
    types.InlineKeyboardButton(
        text="💳ПРЯМИКИ BY PRADA💳", callback_data="прямик by prada"
    ),
    types.InlineKeyboardButton(
        text="🤝ЗНАКОМСТВА BY PRADA🤝", callback_data="трафик by prada (знакомства)"
    ),
    types.InlineKeyboardButton(
        text="💋ЭСКОРТ BY PRADA💋",
        callback_data="эскорт by prada",
    ),
    types.InlineKeyboardButton(
        text="🔪ЖЕРТВЫ BY PRADA🔪",
        callback_data="жертвы by prada",
    ),
    types.InlineKeyboardButton(
        text="📉NFT/TRADE BY PRADA📈",
        callback_data="nft - trade by prada",
    ),
    types.InlineKeyboardButton(
        text="💉N@RKO 2.0 BY PRADA💉",
        callback_data="n@rko 2.0 by prada",
    )
).row(
    types.InlineKeyboardButton(text="⬅️Назад", callback_data="back"),
    types.InlineKeyboardButton(text="Вперед➡️", callback_data="back_1"),
)
channel_url = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Перейти в канал", url=cfg.channel_url),
    types.InlineKeyboardButton("Я подписался", callback_data="check_member"),
)
