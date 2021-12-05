import discord
import requests
import json
import io
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps


class MainCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['a.hug', 'anime.hug'])
    async def ahug(self, ctx, message):
        author = ctx.message.author
        response = requests.get('https://some-random-api.ml/animu/hug')
        json_data = json.loads(response.text)

        embed = discord.Embed(color=0xff9900, title=f'Anime for {author.mention}')
        embed.set_image(url=json_data['link'])
        await ctx.send(embed=embed)

    @commands.command(aliases=['funny', 'gen.m'])
    async def meme(self, ctx, *, arg1=None):
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


def setup(bot):
    bot.add_cog(MainCommands(bot))
