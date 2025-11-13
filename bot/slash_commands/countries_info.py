from discord.ext import commands
from main import IntegrityError
import discord
import bot.database.db as db


class Countries(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.conn = db.connection()
        self.curs = self.conn.cursor()

    @commands.slash_command(name="countries", description="Посмотреть список зарегистрированных стран")
    async def countries(self, ctx: discord.ApplicationContext) -> None:
        countries_req = self.curs.execute("SELECT country_name FROM countries ORDER BY country_name ASC").fetchall()
        countries_ = ""
        count = 0
        if len(countries_req) != 0:
            for i in countries_req:
                count += 1
                countries_ += f"{count}. {i[0]}\n"
            embed=discord.Embed(title="🗺 | Список стран", description=countries_, color=discord.Colour.green())
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("None")
    @commands.slash_command(name="country", description="Посмотреть информацию про страну")
    async def country(self, ctx: discord.ApplicationContext, user: discord.Option(discord.User, description="Пользователь, информацию о стране которого хотите узнать")) -> None: # type: ignore
        try:
            country_req = self.curs.execute("SELECT * FROM countries WHERE user_id = ?", (user.id,)).fetchall()[0]
            
            ideology = ", ".join(country_req[4]) if country_req[4] else ""
            population = country_req[9] / 1_000_000
            s = country_req[8] / 1_000
            gdp = country_req[6] / 1_000_000_000

            if gdp.is_integer():
                gdp_str = f"{int(gdp)} миллиардов" if gdp != 1 else "1 миллиард"
            else:
                gdp_str = f"{gdp:.2f} миллиарда" if 0.2 <= gdp % 1 < 0.5 else f"{gdp:.2f} миллиардов"
            embed=discord.Embed(title="🏳 | Информация о стране", description=
                                f"**🎭 | > Общие сведения < **"
                                f"\n**🎌 | Название страны:** {country_req[1]}"
                                f"\n**📇 | Игрок: {user.mention}**"
                                f"\n\n**⚖️ | > Правление < **"
                                f"\n**👑 | Правитель:** {country_req[2]}"
                                f"\n**💡 | Идеология:** {country_req[3]}{ideology}"
                                f"\n**🛂 | Форма правления:** {country_req[5]}"
                                f"\n\n**💰 | > Экономика < **"
                                f"\n**🪙 | Номинальный валовой внутренний продукт (ВВП номинал):** ${gdp_str}"
                                f"\n**💸 | Номинальный валовой внутренний продукт на душу населения (ВВП номинал на душу населения):** ${country_req[6] / country_req[9]:.2f}"
                                f"\n**📊 | Население:** {population:.2f} млн."
                                f"\n**🗺 | Территории:** {country_req[7]}"
                                f"\n**📑 | Площадь страны:** {s:.2f} тысч. км²", color=0xff0000)
            await ctx.respond(embed=embed)
        except IndexError as e:
            errro_embed = embed=discord.Embed(title="❌ | Участник не найден", description="Указанный вами человек не зарегистрирован либо произошел сбой!", color=0xff0000)
            await ctx.respond(embed=errro_embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Countries(bot))
    