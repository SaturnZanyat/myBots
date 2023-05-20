import asyncio

from telebot import asyncio_filters

import commands
from DB import close_connection_DB

while True:
    if __name__ == "__main__":
        try:
            commands.bot.add_custom_filter(asyncio_filters.StateFilter(commands.bot))
            commands.bot.add_custom_filter(asyncio_filters.IsDigitFilter())

            asyncio.run(commands.bot.polling(non_stop=True, interval=0))
            close_connection_DB(commands.connection)
        except Exception as err:
            print("!!!!!!! Ошибка: ", err)