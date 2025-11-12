from discord.ext import commands
import discord
import bot.database.db as db

class Countries(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(name="countries", description="Посмотреть список зарегистрированных стран")
    async def countries(self, ctx: discord.ApplicationContext) -> None:
        conn = await db.connection()
        try:
            countries_req = await conn.fetch("SELECT country_name FROM countries ORDER BY country_name ASC")
            if countries_req:
                countries_ = "\n".join(f"{i+1}. {row['country_name']}" for i, row in enumerate(countries_req))
                embed = discord.Embed(title="🗺 | Список стран", description=countries_, color=discord.Colour.green())
                await ctx.respond(embed=embed)
            else:
                await ctx.respond("На данный момент нет зарегистрированных стран.")
        finally:
            await conn.close()

    @commands.slash_command(name="country", description="Посмотреть информацию про страну")
    async def country(self, ctx: discord.ApplicationContext, user: discord.Option(discord.User, description="Пользователь, информацию о стране которого хотите узнать")) -> None: # type: ignore
        conn = await db.connection()
        try:
            country_req = await conn.fetchrow("SELECT * FROM countries WHERE user_id=$1", user.id)
            if not country_req:
                embed = discord.Embed(
                    title="❌ | Участник не найден",
                    description="Указанный вами человек не зарегистрирован либо произошел сбой!",
                    color=0xff0000
                )
                await ctx.respond(embed=embed)
                return

            ideology = ", ".join(country_req['second_ideology']) if country_req['second_ideology'] else ""
            population = country_req['population'] / 1_000_000
            s = country_req['s'] / 1_000
            gdp = country_req['gdp'] / 1_000_000_000

            if gdp.is_integer():
                gdp_str = f"{int(gdp)} миллиардов" if gdp != 1 else "1 миллиард"
            else:
                gdp_str = f"{gdp:.2f} миллиарда" if 0.2 <= gdp % 1 < 0.5 else f"{gdp:.2f} миллиардов"

            embed = discord.Embed(
                title="🏳 | Информация о стране",
                description=(
                    f"**🎭 | > Общие сведения < **"
                    f"\n**🎌 | Название страны:** {country_req['country_name']}"
                    f"\n**📇 | Игрок:** {user.mention}"
                    f"\n\n**⚖️ | > Правление < **"
                    f"\n**👑 | Правитель:** {country_req['leader_name']}"
                    f"\n**💡 | Идеология:** {country_req['ideology']}{(' / ' + ideology) if ideology else ''}"
                    f"\n**🛂 | Форма правления:** {country_req['government']}"
                    f"\n\n**💰 | > Экономика < **"
                    f"\n**🪙 | Номинальный ВВП:** ${gdp_str}"
                    f"\n**💸 | ВВП на душу населения:** ${country_req['gdp'] / country_req['population']:.2f}"
                    f"\n**📊 | Население:** {population:.2f} млн."
                    f"\n**🗺 | Территории:** {country_req['territories']}"
                    f"\n**📑 | Площадь страны:** {s:.2f} тыс. км²"
                ),
                color=0xff0000
            )
            await ctx.respond(embed=embed)
        finally:
            await conn.close()

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Countries(bot))
