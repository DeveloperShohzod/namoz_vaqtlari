import requests
from telegram.ext import Updater, CallbackQueryHandler, ConversationHandler, MessageHandler, CallbackContext, \
    CommandHandler, Filters
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

updater = Updater(token="5422254647:AAHVqXt1KDMmm_TY90esfElQ_JSaKmFvXGU", use_context=True)
SHAHARLAR, NAMOZ_VAQTLARI = range(2)

buttons = [
    [InlineKeyboardButton("Toshkent", callback_data='Toshkent'),
     InlineKeyboardButton("Buxoro", callback_data='Buxoro')],
    [InlineKeyboardButton("Samarqand", callback_data='Samarqand'),]
]

keyboards = ReplyKeyboardMarkup([["Bomdod", "Quyosh"], ["Peshin", "Asr"], ["Shom", "Hufton"], ['back']],
                                resize_keyboard=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Namoz vaqtlari botga xush kelibsiz!!\nKerakli viloyatni tanlang",
                              reply_markup=InlineKeyboardMarkup(buttons))
    return SHAHARLAR


def shaharlar(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    global shahar
    shahar = query.data
    query.message.reply_text(f"{shahar}ning namoz vaqtlarini korish uchun")
    query.message.reply_text("kerakli tugmani tanlang", reply_markup=keyboards)
    return NAMOZ_VAQTLARI


def namoz_vaqtlari(update: Update, context: CallbackContext):
    soz = update.message.text
    data = requests.request('GET', url=f"https://islomapi.uz/api/present/day?region={shahar}").json()
    if soz == "Bomdod":
        update.message.reply_text(f'Bomdod vaqti: {data["times"]["tong_saharlik"]}')
    elif soz == "Quyosh":
        update.message.reply_text(f'Quyosh vaqti: {data["times"]["quyosh"]}')
    elif soz == "Peshin":
        update.message.reply_text(f'Peshin vaqti: {data["times"]["peshin"]}')
    elif soz == "Asr":
        update.message.reply_text(f'Asr vaqti: {data["times"]["asr"]}')
    elif soz == "Shom":
        update.message.reply_text(f'Shom vaqti: {data["times"]["shom_iftor"]}')
    elif soz == "Hufton":
        update.message.reply_text(f'Hufton vaqti: {data["times"]["hufton"]}')


dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={SHAHARLAR: [CallbackQueryHandler(shaharlar)],
            NAMOZ_VAQTLARI: [MessageHandler(Filters.regex("^(Bomdod)$"), namoz_vaqtlari),
                             MessageHandler(Filters.regex("^(Quyosh)$"), namoz_vaqtlari),
                             MessageHandler(Filters.regex("^(Peshin)$"), namoz_vaqtlari),
                             MessageHandler(Filters.regex("^(Asr)$"), namoz_vaqtlari),
                             MessageHandler(Filters.regex("^(Shom)$"), namoz_vaqtlari),
                             MessageHandler(Filters.regex("^(Hufton)$"), namoz_vaqtlari),
                             MessageHandler(Filters.regex("^(back)$"), start),
                             ]},
    fallbacks=[],
)
dispatcher.add_handler(conv_handler)
updater.start_polling()
updater.idle()
