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

# конфигурация бота
from config import TOKEN
from config import mongopass


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
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Подключен как {0.user}'.format(bot))


# Корги какие то
# Загружаем корги
@bot.command()
async def load(ctx, extension):
    if ctx.author.id == 321612071382941696:
        bot.load_extension(f"cogs.{extension}")
        await ctx.send("Cogs loaded")
    else:
        await ctx.send("Acces denied. Please contact dev to other help. Lesnoy40rt77#5494")


# Отггружаем корги
@bot.command()
async def unload(ctx, extension):
    if ctx.author.id == 321612071382941696:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.send("Cogs loaded")
    else:
        await ctx.send("Acces denied. Please contact dev to other help. Lesnoy40rt77#5494")


# Перезагружаем корги
@bot.command()
async def reload(ctx, extension):
    if ctx.author.id == 321612071382941696:
        bot.unload_extension(f"cogs.{extension}")
        bot.load_extension(f"cogs.{extension}")
        await ctx.send("Cogs loaded")
    else:
        await ctx.send("Acces denied. Please contact dev to other help. Lesnoy40rt77#5494")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(TOKEN)
