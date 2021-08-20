import re
import json
import sys
import requests
import urllib.request
import os
import time
from discord_webhook import DiscordWebhook, DiscordEmbed


INSTAGRAM_USERNAME = 'gamabuild'
TIME_LOOP = 30
WEBHOOK_URL = 'https://discord.com/api/webhooks/856481513225846805/CnXtxeh6GXZ_wMIr4KA7Xg4uO3p28jrZZAnoxZ-pDrcCkfb1SuiZFwq06XY2nYwxjB75'


def get_user_fullname(html):
    return html.json()["graphql"]["user"]["full_name"]


def get_total_photos(html):
    return int(html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["count"])


def get_last_publication_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]

def get_last_thumb_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["thumbnail_src"]

def get_description_photo(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]


def webhook(html):
    try:
        webhook = DiscordWebhook(url=WEBHOOK_URL)
        des_link = "https://www.instagram.com/p/"+get_last_publication_url(html)
        embed = DiscordEmbed(title='**:bell: Check out our new post on instagram!**', description=des_link, color='FB005C')
        embed.set_image(url= get_last_thumb_url(html))
        embed.set_footer(text= 'GamaBuild Team' , icon_url='https://media.discordapp.net/attachments/841291473332207662/841736355847077888/Gama.png')
        webhook.add_embed(embed)
        webhook.execute()
    except:
        print('error')
def get_instagram_html(INSTAGRAM_USERNAME):
    headers = {
        "Host": "www.instagram.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    html = requests.get("https://www.instagram.com/" +
                        INSTAGRAM_USERNAME + "/feed/?__a=1", headers=headers)
    return html


def main():
    try:
        html = get_instagram_html(INSTAGRAM_USERNAME)
        if(os.environ.get("LAST_IMAGE_ID") == get_last_publication_url(html)):
            print("Not new image to post in discord.")
        else:
            os.environ["LAST_IMAGE_ID"] = get_last_publication_url(html)
            print("New image to post in discord.")
            webhook(html)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    if WEBHOOK_URL != None:
        while True:
            main()
            time.sleep(float(TIME_LOOP))
    else:
        print('Please configure environment variables properly!')