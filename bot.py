import os

import asyncio
import time
import discord
import json
import requests

from discord.ext import commands
# второй вариант работы бота

from config import TOKEN

bot = commands.Bot(command_prefix='!')


# bot = discord.Client()


@bot.event
async def on_ready():
    print('Подключен как {0.user}'.format(bot))


@bot.command(aliases=['a.hug', 'anime.hug'])
async def ahug(ctx):
    author = ctx.message.author
    response = requests.get('https://some-random-api.ml/animu/hug')
    json_data = json.loads(response.text)

    embed = discord.Embed(color=0xff9900, title=f'Anime for {author.mention}')
    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)


# @bot.event
# async def on_message(message):
#    if message.author == bot.user:
#        return
#
#    if message.content.startswith('!anime_hug'):
#        author = message.author
#        response = requests.get('https://some-random-api.ml/animu/hug')
#        json_data = json.loads(response.text)
#
#        embed = discord.Embed(color=0xff9900, title=f'Anime for {author.mention}')
#        embed.set_image(url=json_data['link'])
#        await message.channel.send(embed=embed)
#    elif message.content.startswith('!test'):
#        await message.channel.send('Test')


bot.run(TOKEN)
