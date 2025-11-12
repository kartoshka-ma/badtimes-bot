from discord.ext import commands
import platform
import discord
import json


class BotInfo(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    def load_json(self) -> dict:
        try:
            with open("./bot/configuration.json", "r") as config:
                data = json.load(config)
                versions = {"version": data["version"], 
                            "detail_version": data["detail_version"]}
            return versions
        except Exception as e:
            raise Exception("Возникла следующая ошибка при работе с конфигом:" + str(e))

    @commands.slash_command(name="bot", description="Вовзращает инфомрацию о боте")
    async def _bot(self, ctx: discord.ApplicationContext) -> None:
        versions = BotInfo.load_json(self)

        embed = discord.Embed(title="🤖 | «Bad Times»", color=0xfdff80)
        embed.add_field(name="🏷 | Никнейм бота", value=f"Bad Times Bot#4037", inline=True)
        embed.add_field(name="🔩 | Версия бота", value=f"v{versions['version']} (v{versions['detail_version']})", inline=True)
        embed.add_field(name="🧸 | Разработчик(-и) бота", value=f"<@958077120612032612> (kartoshka_ma)", inline=False)
        embed.add_field(name="📠 | Язык программирования / библиотека", value=f"<:python:1171934736776691864> Python {platform.python_version()} / <:pycord:1319417976990208060> Pycord {discord.__version__}", inline=False)
        embed.add_field(name="💿 | Операционная система хоста", value=f"{platform.platform()}")
        await ctx.respond(embed=embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(BotInfo(bot))