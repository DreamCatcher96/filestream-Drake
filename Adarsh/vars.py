# (c) adarsh-goel
import os
from os import getenv, environ
from dotenv import load_dotenv



load_dotenv()

class Var(object):
    MULTI_CLIENT = True 
    API_ID = 1270600
    API_HASH = "20364627248fa3c42782c1fe16b65314"
    BOT_TOKEN = "5097487403:AAEJ1HCQjpS5SONX5f7JTUNVMai5nFA_Uog"
    name = str(getenv('name', 'filetobot'))
    SLEEP_THRESHOLD = int(getenv('SLEEP_THRESHOLD', '60'))
    WORKERS = 2000
    BIN_CHANNEL = -1002079967295
    PORT = int(getenv('PORT', 8080))
    BIND_ADRESS = str(getenv('WEB_SERVER_BIND_ADDRESS', '0.0.0.0'))
    PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
    OWNER_ID = 6366452257
    NO_PORT = bool(getenv('NO_PORT', False))
    MULTI_TOKEN1 = "6454293731:AAFJRf-rweRD2zxYVRZjM-MNztQ97zLU5wU"
    MULTI_TOKEN2 = "7142938916:AAHYnz5RKJLhr-0T-vXkmCiz7Gd1EutOqRM"
    MULTI_TOKEN3 = "6996144146:AAGxPMFKuiMw_T8x8hi7HEyo8gOqmzho2yc"
    MULTI_TOKEN4 = "7195519498:AAErJAHje-nGClq0iTBUa5TUPfmZfv1ae7w"
    MULTI_TOKEN5 = "6495625055:AAHGTprLeh1caHqVihi0m7HwpZp_Fu3Qo0c"
    APP_NAME = fsearch1bot
    OWNER_USERNAME = "WhitE_DeviL099"
    if 'DYNO' in environ:
        ON_HEROKU = True
        APP_NAME = str(getenv('APP_NAME'))
    
    else:
        ON_HEROKU = False
    FQDN = "https://fsearch1bot-1b7c04fe436d.herokuapp.com" str(getenv('FQDN', BIND_ADRESS)) if not ON_HEROKU or getenv('FQDN') else APP_NAME+'.herokuapp.com'
    HAS_SSL=bool(getenv('HAS_SSL',False))
    if HAS_SSL:
        URL = "https://{}/".format(FQDN)
    else:
        URL = "http://{}/".format(FQDN)
    DATABASE_URL = "mongodb+srv://filetolink0bot:filetolink0bot@cluster0.vnohdxn.mongodb.net/?retryWrites=true&w=majority"
    UPDATES_CHANNEL = str(getenv('UPDATES_CHANNEL', None))
    BANNED_CHANNELS = list(set(int(x) for x in str(getenv("BANNED_CHANNELS", "-10013779")).split())) 
