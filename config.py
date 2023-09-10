import os

class Config:
    API_ID = int(os.getenv("API_ID", '25374144'))
    API_HASH = os.getenv("API_HASH", '4f1efaef6551e30c5fa3a7b9dac7cf8e')
    BOT_TOKEN = os.getenv("BOT_TOKEN", '6116413872:AAHwJ-3a2oefzMhTHsVE6ppbrirUY2K5488')
