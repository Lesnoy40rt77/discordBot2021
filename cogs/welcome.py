import discord
from discord.ext import commands
from requests import get
from os import getcwd
from config import api_key, welcomechannelid


class User_welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # попытка сделать Welcome image через SRA
    @commands.Cog.listener()
    async def on_member_join(self, bot, member: discord.Member):
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
    @commands.Cog.listener()
    async def on_member_remove(self, bot, member: discord.Member):
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


def setup(bot):
    bot.add_cog(User_welcome(bot))
