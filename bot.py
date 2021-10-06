import os

import discord
import json
import requests

# from discord.ext import commands
# второй вариант работы бота

TOKEN = 'ODkzNTMzNTkzMjMyNjA5MzIw.YVc2AQ.eYfuWZl2Vmokt2QGw3iKei9rl1s'

# bot = commands.Bot(command_prefix='!')
bot = discord.Client()


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# эта команда сломалась из за следующей за ней
# @bot.event
# async def on_message(message):
#    if message.author == bot.user:
#        return
    # команда сделана через костыль (честно взята из статьи для теста)
#    if message.content.startswith('!hello'):
#        author = message.author
#        await message.channel.send(f'Hello, {author.mention}!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!anime_hug'):
        author = message.author
        response = requests.get('https://some-random-api.ml/animu/hug')
        json_data = json.loads(response.text)

        embed = discord.Embed(color=0xff9900, title=f'Anime for {author.mention}')
        embed.set_image(url=json_data['link'])
        await message.channel.send(embed=embed)
    elif message.content.startswith('!test'):
        await message.channel.send('Test')


# тестовая команда, при написании !hello вернет hi с пингом
# @bot.command()
# async def hello(ctx):
#    author = ctx.message.author
#    await ctx.send(f'Hello, {author.mention}!')
# Вырезано тк не работало

bot.run(TOKEN)
