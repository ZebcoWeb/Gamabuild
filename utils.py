import sys, motor, asyncio, inspect, importlib, discord, random, re, rom

from beanie import init_beanie, Document
from redis import exceptions

from config import Config, DB
from cache import VoiceTime



def success_embed(msg: str, color = None):
    return discord.Embed(
        description = msg,
        color = color if color else Config.DISCORD_COLOR
    )

def error_embed(msg: str, color = None):
    return discord.Embed(
        description = msg,
        color = color if color else Config.DISCORD_COLOR
    )   

def check_media(message):
        if message.content:
            if not re.match(r'(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png|mp4|jpeg|webm|mov|mp3)', message.content):
                return False
        if len(message.attachments) > 0:
            for attachment in message.attachments:
                if not attachment.content_type.startswith(('image/', 'video/', 'audio/')):
                    return False
        return True

def inspect_models(discord_client):
    models = []
    for name, obj in inspect.getmembers(importlib.import_module('models')):
        if inspect.isclass(obj):
            if issubclass(obj, Document):
                if name in Config.IGNORE_MODELS:
                    pass
                else:
                    setattr(obj, 'discord_client', discord_client)
                    models.append(obj)
    return models

def get_guide_number(secret_num: int, guess_num: int, max_number: int):
    if guess_num > secret_num:
        guide_num = random.randint(secret_num + 1, guess_num)
        guide_msg = f'The secret number is less than {guide_num}'
    elif guess_num < secret_num:
        guide_num = random.randint(guess_num, secret_num - 1)
        guide_msg = f'The secret number is larger than {guide_num}'

    return guide_num, guide_msg

async def init_database(loop: asyncio.AbstractEventLoop = None, discord_client: discord.Client = None):
    
    client = motor.motor_asyncio.AsyncIOMotorClient(
        f'mongodb+srv://{DB.USERNAME}:{DB.PASSWORD}@{DB.HOST}/?retryWrites=true&w=majority',
        io_loop=loop,
        connectTimeoutMS=10000 # 10 seconds
    )
    
    try:
        info = await client.server_info()

        if info['ok'] == 1.0:

            models = inspect_models(discord_client)

            await init_beanie(
                database= client[DB.DATABASE],
                document_models= models
            )
            print(' Database is alive. MongoDB version: ' + info['version'] + f'\n └ {len(models)} models were activated in the database!')
            
        else:
            print('└ Database is not alive!')
            sys.exit(1)

    except Exception as e:
        raise e
        print('> Could not connect to database!')
        print('> Exiting...')
        sys.exit(1)

def init_cache():

    rom.util.set_connection_settings(
        host='localhost',
        port=6379,
        db=0,
    )
    client = rom.util.get_connection()

    try:
        info = client.info()
        print(' └ Cache server is alive. Redis version: ' + info['redis_version'])
        for i in VoiceTime.query.all():
            i.delete()
    except exceptions.ConnectionError:
        print('> Cache server is not available.')
        print('> Exiting...')
        sys.exit(1)
    
    except exceptions.AuthenticationError:
        print('> Cache server authentication failed.')
        print('> Exiting...')
        sys.exit(1)
