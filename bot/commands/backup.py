from discord.ext import commands
from datetime import datetime
from shutil import copyfile
import discord

class backup_db(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.date = datetime.now().strftime('%Y-%m-%d')
        self.log_date = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    @commands.command(name="backup")
    @commands.has_permissions(administrator=True)
    async def bakcup(self, ctx: discord.ApplicationContext) -> None:
        try:
            if await self.bot.is_owner(ctx.author):
                copyfile("data.db", f"backups/databases/data_{self.date}.db")
                print(f"[{self.log_date}] [+] New backup saved in item database_{self.date}.db")
                await ctx.send("Успешно!")
            else:
                await ctx.send("У вас нет права на выполнение этой команды!")
        except Exception as e:
            print(e)

def setup(bot):
    bot.add_cog(backup_db(bot))