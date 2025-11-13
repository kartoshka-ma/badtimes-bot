from discord.ext import commands
from calculator import ceval
import discord


class Maths(commands.Cog):
    @commands.slash_command(description="Провести подсчёты")
    async def calculate(self, ctx: discord.ApplicationContext, expr: str) -> None:
        res = ceval(expr)
        embed=discord.Embed(title=f"{expr}", description=f"**Результат:** \n```{res}```", color=0xff0000)
        await ctx.respond(embed=embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Maths(bot))