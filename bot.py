import os

import asyncio
import time
import discord
import json
import requests
import logging
import aiohttp

from discord.ext import commands
from requests import get
from os import getcwd

from config import TOKEN
from config import api_key

# попытка пнуть лог что бы он работал
# после переписания бота на нормальный режим поменять .DEBUG на .INFO !!!
logging.basicConfig(level=logging.DEBUG, filename='discord.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Подключен как {0.user}'.format(bot))


# попытка сделать Welcome image через SRA
@bot.event
async def on_member_join():
    URL = f'https://some-random-api.ml/welcome/img/1/stars?type=join&username={discord.User.name}&discriminator=4038&guildName=Some%20random%20api&memberCount=799&avatar=https://cdn.discordapp.com/avatars/560789882738573324/bc220b0eeeabbe234026e4881f3c3b9c.png&textcolor=white'
    resp = get(URL)

    async with aiohttp.ClientSession() as session:
        async with session.get(


@bot.command(aliases=['a.hug', 'anime.hug'])
async def ahug(ctx):
    author = ctx.message.author
    response = requests.get('https://some-random-api.ml/animu/hug')
    json_data = json.loads(response.text)

    embed = discord.Embed(color=0xff9900, title=f'Anime for {author.mention}')
    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)


bot.run(TOKEN)
