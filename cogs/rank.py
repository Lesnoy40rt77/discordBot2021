import discord
from discord.ext import commands


class User_Rank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # Тут ранк, листай дальше
    # @commands.Cog.listener()
    # async def on_message(self, bot, message=discord.Message):
    #     if message.author == bot.user:
    #         return
    #     else:
    #         username = message.author
    #         userid = message.author.id
    #         name = f'{username}'
    #         result = bot.rankcollection.find_one(userid)
    #         print(result)
    #         # No match found
    #         if result is None:
    #             level = 0
    #             xp = 10
    #             member_rank = {"_id": userid,
    #                            "name": name,
    #                            "userid": userid,
    #                            "level": level,
    #                            "xp": xp
    #                            }
    #             bot.rankcollection.insert_one(member_rank)
    #         # Match found
    #         elif result is not None:
    #             print('qq')


def setup(bot):
    bot.add_cog(User_Rank(bot))
