import os

import asyncio
import pymongo
import srv as srv
import time
import discord
import json
import requests
import logging
import aiohttp
import io
import easy_pil

# импорт нужных классов
from pymongo import MongoClient
from discord.ext import commands
from requests import get
from os import getcwd
from PIL import Image, ImageDraw, ImageFont, ImageOps

# конфигурация бота
from config import TOKEN
from config import api_key
from config import mongopass
from config import welcomechannelid

# переменные MongoDB
# Я не делал тут переменные для конфига потому что мне лень :>
cluster = MongoClient(
    f'mongodb+srv://admin:{mongopass}@cluster0.ahygo.mongodb.net/pythonbot2021?retryWrites=true&w=majority')
db = cluster.pythonbot2021
rankcollection = db.ranked

# попытка пнуть лог что бы он работал
# после переписания бота на нормальный режим поменять .DEBUG на .INFO !!!
logging.basicConfig(level=logging.DEBUG, filename='discord.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('Подключен как {0.user}'.format(bot))


# user = 'testuser#2255'
# userid = 88005553535
# level = 100
# xp = 150
# member_rank = {"user": user,
#                "userid": userid,
#                "level": level,
#                "xp": xp
#                }
# rankcollection.insert_one(member_rank)

# Тут ранк, листай дальше
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    else:
        username = message.author
        userid = message.author.id
        name = f'{username}'
        result = rankcollection.find_one(userid)
        print(result)
        # No match found
        if result is None:
            level = 0
            xp = 10
            member_rank = {"_id": userid,
                           "name": name,
                           "userid": userid,
                           "level": level,
                           "xp": xp
                           }
            rankcollection.insert_one(member_rank)
        # Match found
        elif result is not None:
            print('qq')


# попытка сделать Welcome image через SRA
@bot.event
async def on_member_join(member: discord.Member):
    username = member.name
    discriminator = member.discriminator
    avatar = member.avatar_url_as(format='png')
    guildname = member.guild.name
    membercount = len(member.guild.members)

    url = f'https://some-random-api.ml/welcome/img/1/stars?key={api_key}&type=join&username={username}&discriminator={discriminator}&guildName={guildname}&memberCount={membercount}&avatar={avatar}&textcolor=white'
    resp = get(url)

    if resp.status_code == 200:
        channel = bot.get_channel(welcomechannelid)

        if not channel:
            print('An error was caught at line 101')
            return

        open('image.png', 'wb').write(resp.content)
        print(f'File saved in {getcwd()}')

        await channel.send(file=discord.File('image.png'))

    elif resp.status_code != 200:
        jsonresp = resp.json()

        print(resp.status_code)
        print(jsonresp)


# Аналогично с welcome только на выход пользователя
@bot.event
async def on_member_remove(member: discord.Member):
    username = member.name
    discriminator = member.discriminator
    avatar = member.avatar_url_as(format='png')
    guildname = member.guild.name
    membercount = len(member.guild.members)

    url = f'https://some-random-api.ml/welcome/img/1/stars?key={api_key}&type=leave&username={username}&discriminator={discriminator}&guildName={guildname}&memberCount={membercount}&avatar={avatar}&textcolor=white'
    resp = get(url)

    if resp.status_code == 200:
        channel = bot.get_channel(welcomechannelid)

        if not channel:
            print('An error was caught at line 132')
            return

        open('image.png', 'wb').write(resp.content)
        print(f'File saved in {getcwd()}')

        await channel.send(file=discord.File('image.png'))

    elif resp.status_code != 200:
        jsonresp = resp.json()

        print(resp.status_code)
        print(jsonresp)


@bot.command(aliases=['a.hug', 'anime.hug'])
async def ahug(ctx):
    author = ctx.message.author
    response = requests.get('https://some-random-api.ml/animu/hug')
    json_data = json.loads(response.text)

    embed = discord.Embed(color=0xff9900, title=f'Anime for {author.mention}')
    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)


@bot.command(aliases=['funny', 'gen.m'])
async def meme(ctx, *, arg1=None):
    if ctx.message.attachments:
        url = ctx.message.attachments[0].url
        if arg1 is None:
            return Exception
        else:
            if arg1 is not None:
                img = Image.open('blackman.png')
                img = img.resize((3000, 3000))
                # 1) Цвет белый
                # 2) Шрифт для надписи
                # 3) Инструмент для рисования
                t_c = "#FFF"
                headline = ImageFont.truetype('a_MachinaOtro.ttf', size=190)
                Idraw = ImageDraw.Draw(img)

                response = requests.get(url, stream=True)
                response = Image.open(io.BytesIO(response.content))
                response = response.convert('RGBA')

                response = response.resize((1500, 1400), Image.ANTIALIAS)

                img.paste(response, (765, 850))

                Idraw.text((1050, 2550), f"{arg1}", t_c, font=headline)
                img = ImageOps.expand(img, border=15, fill='#fff')
                img.save(f"meme_{ctx.author.id}.png")
                await ctx.send(file=discord.File(fp=f"meme_{ctx.author.id}.png"))

            else:
                print('Passing through')
                pass
    else:
        await ctx.send('No image!')


bot.run(TOKEN)
