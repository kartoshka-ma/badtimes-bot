from discord.ext import commands
from datetime import datetime
import discord
import asyncpg  # обязательно для asyncpg
import bot.database.db as db  # твой модуль с инициализацией пула

date_format = "%Y-%m-%d %H:%M:%S"

main_ideologies = [
    "Автократия", "Демократия", "Зеленая идеология (экологизм)",
    "Коммунизм", "Консерватизм", "Либерализм", "Либертарианство",
    "Национализм", "Социал-демократия", "Социализм", "Фашизм"
]
adv_ideologies = ["Гуманизм", "Феминизм", "Маскулизм", "Трансгуманизм", "Экологизм"]
govs = [
    "Абсолютная монархия", "Анархия", "Автократия", "Конституционная монархия",
    "Олигархия", "Парламентская республика", "Племенное правление",
    "Президентская республика", "Смешанная республика", "Теократия", "Тоталитаризм"
]

class Registration(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    def log_entry(self, user: discord.User, author: discord.User, positive: bool, action: str, error: str | None = None) -> None:
        now = datetime.now().strftime(date_format)
        log_action = "added to" if action == "add" else "deleted from"
        if positive:
            log_msg = f"\n[{now}] [+] Player ({user.id}) - {user} was {log_action} the database by {author} ({author.id})!"
        else:
            log_msg = f"\n[{now}] [-] Player ({user.id}) - {user} could not be {log_action} the database by {author} ({author.id})! Reason: {error}"
        with open("./bot/logs/regs.txt", "a", encoding="utf-8") as file:
            file.write(log_msg)
            print(log_msg)

    @commands.slash_command(name="registration", description="Регистрация участника сервера")
    @commands.has_permissions(moderate_members=True)
    async def reg(
        self, ctx: discord.ApplicationContext,
        user: discord.Option(discord.User, description='Кого вы хотите зарегистрировать?'), 
        country_name: discord.Option(str, description='Название страны'),
        leader_name: discord.Option(str, description='ФИО лидера страны'),
        ideology: discord.Option(str, description='Идеология государства', choices=main_ideologies),
        government: discord.Option(str, description='Форма правления', choices=govs),
        gdp: discord.Option(int, description='ВВП'),
        territories: discord.Option(str, description='Территории страны'),
        s: discord.Option(int, description='Площадь территории'),
        population: discord.Option(int, description="Население"),
        second_ideology: discord.Option(str, description='Дополнительная идеология', choices=adv_ideologies, required=False)
    ) -> None:
        embed = discord.Embed(title="Регистрация", color=discord.Color.blurple())
        try:
            conn = await db.connection()
            async with conn.transaction():
                await conn.execute(
                    """
                    INSERT INTO countries(user_id, country_name, leader_name, ideology, second_ideology, government, gdp, territories, s, population)
                    VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
                    """,
                    user.id, country_name, leader_name, ideology, second_ideology, government, gdp, territories, s, population
                )
            embed = discord.Embed(
                title="🏳️ | Страна зарегистрирована",
                description=f"Вы зарегистрировали {user.mention} за {country_name}!",
                color=0x08000
            )
            self.log_entry(user, ctx.author, True, "add")

        except asyncpg.exceptions.UniqueViolationError as i:
            self.log_entry(user, ctx.author, False, "add", str(i))
            embed = discord.Embed(
                description="**❌ | Пользователь уже зарегистрирован!**",
                color=0xff0000
            )
        except Exception as e:
            self.log_entry(user, ctx.author, False, "add", str(e))
            embed = discord.Embed(
                description="**❌ | Неизвестная ошибка!**",
                color=0xff0000
            )
        finally:
            await conn.close()
            await ctx.respond(embed=embed)

    @commands.slash_command(name="unregistration", description="Снять со страны участника сервера")
    @commands.has_permissions(moderate_members=True)
    async def unreg(
        self, ctx: discord.ApplicationContext,
        user: discord.Option(discord.User, description="Кого вы хотите снять?")
    ) -> None:
        try:
            async with self.bot.db_pool.acquire() as conn:
                async with conn.transaction():
                    result = await conn.execute("DELETE FROM countries WHERE user_id=$1", user.id)
            deleted_count = int(result.split(" ")[1])
            if deleted_count == 0:
                raise ValueError("User not found")

            self.log_entry(user, ctx.author, True, "remove")
            embed = discord.Embed(
                title="✅ | Игрок снят",
                description=f"Вы сняли игрока под ником {user} со страны!",
                color=0x08000
            )

        except Exception as e:
            self.log_entry(user, ctx.author, False, "remove", str(e))
            embed = discord.Embed(
                title="❌ | Игрок не снят",
                description=f"Игрок под ником {user} не был снят со страны! Возможно, он не зарегистрирован!",
                color=0xff0000
            )
        finally:
            await ctx.respond(embed=embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Registration(bot))
