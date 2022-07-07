import os


class Config:
    SERVER_ID = 769855661223313413
    TOKEN = os.getenv('TOKEN')
    PREFIX = '-'

    IGNORE_EXTENTIONS = []
    IGNORE_MODELS = []

    TICKET_SECTIONS = [
        ('Build Comissions', '🧱'),
        ('SponsorShip/Advertising', '📢'),
    ]

    DISCORD_COLOR = 0x2F3136

    INC_XP_CHITCHAT = 5
    INC_XP_MEME = 20
    INC_XP_BOOST = 3000

    MIN_XP_DAILY = 10
    MAX_XP_DAILY = 50

    MIN_XP_WEEKLY = 100
    MAX_XP_WEEKLY = 200

    GTN_BETS = {
        # bet - guess
        5: {'guess': 3, 'max_number': 25},
        10: {'guess': 6, 'max_number': 50},
        15: {'guess': 9, 'max_number': 50},
        20: {'guess': 12, 'max_number': 50},
        25: {'guess': 13, 'max_number': 100},
        30: {'guess': 14, 'max_number': 100},
        35: {'guess': 15, 'max_number': 150},
        40: {'guess': 16, 'max_number': 150},
        45: {'guess': 17, 'max_number': 200},
        50: {'guess': 18, 'max_number': 200}
    }

    WHEEL_BETS = (
        # coefficient - weight
        (5, 0.1),
        (3, 2.9),
        (2, 10),
        (1.5, 18),
        (1, 20),
        (0.5, 30),
        (0, 20),
    )


class Roles:
    NEW = 842843180608127038
    TRAVELER = 781407403211620393
    NOTICE = 866976860625043456
    OPTIONAL_ROLES = [
    (981943526789107742, '🏃'),
    (981943879920128000, '👷‍♂️'), 
    (981943988695220334, '⚡'), 
    (981944083872358440, '🧑‍💻'), 
    (981944176004452473, '🛠️'), 
    (981944263854153789, '👽'),
    (981944460961280060, '😳'), 
    (981944311056846890, '🏕️'), 
    (981944408742166538, '☠️'), 
    (981943694221525092, '⚔️')
    ]

    ROLES_MARKER = 982656124639649872


class Channel:
    ANNOUNCEMENT = 781409442545008640
    CHITCHAT = 769858253190070303
    JOIN_LOG = 847806714840875069
    TICKET = 789777105201397811
    ROLES = 981941598025818234
    VERIFY = 842431646648369224
    TICKET_CATEGORY = 789787201981382656
    TERM = 769856028425977876
    PREVIOUS_PROJECTS = 769857325422608384
    INSTA = 841982534502187008
    MEME = 980880694354014319
    SELFPROMO = 981906662791184434
    MARKETPLACE = 992738361410326538
    ACTIVITIES = 993969929927798836
    CASINO = 993988870888755220
    VOICE_CATEGORY = 769858189814005760
    INVITE = 994270688472993832
    NEW_VC_SESSION = 979460123498016858
    MUSIC = 840654726999179265
    PUBLIC = 769985941171339304

class Emoji:
    VERIFY = '<:verifyy:867000676452925450>'
    FOLLOW = '<:notiff:867001613990363159>'
    UNFOLLOW = '<:notiffoff:867082989363658773>'
    DOWNLOAD = '<:download:908033302345179136>'
    PURCHASE = '<:purchase:992740103992660038>'


class DB:
    HOST = 'localhost'
    USERNAME = 'gamauser'
    PASSWORD = '8rf98hre8439dwqdqw20dwkffewf'
    DATABASE = 'gamabuild'