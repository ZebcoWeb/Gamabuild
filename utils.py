import sys, motor, asyncio, inspect, importlib, discord, random

from beanie import init_beanie, Document

from config import Config, DB

def success_embed(msg: str, color = None):
    return discord.Embed(
        description = ':white_check_mark: ' + msg,
        color = color if color else Config.DISCORD_COLOR
    )


def error_embed(msg: str, color = None):
    return discord.Embed(
        description = ':exclamation: ' + msg,
        color = color if color else Config.DISCORD_COLOR
    )   

def inspect_models():
    models = []
    for name, obj in inspect.getmembers(importlib.import_module('models')):
        if inspect.isclass(obj):
            if issubclass(obj, Document):

                if name in Config.IGNORE_MODELS:
                    pass
                else:
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

async def init_database(loop: asyncio.AbstractEventLoop = None):
    
    client = motor.motor_asyncio.AsyncIOMotorClient(
        host=DB.HOST,
        port=27017,
        username=DB.USERNAME,
        password=DB.PASSWORD,
        io_loop=loop,
        connectTimeoutMS=10000 # 10 seconds
    )
    
    try:
        info = await client.server_info()

        if info['ok'] == 1.0:

            models = inspect_models()

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

