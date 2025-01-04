from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("TOKEN")
ADMIN = env.list("ADMIN")


GROUP_CHAT_ID = env.str("GROUP_CHAT_ID")
SPREADSHEET_ID = env.str("SPREADSHEET_ID")