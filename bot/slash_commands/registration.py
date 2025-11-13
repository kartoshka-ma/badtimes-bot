from discord.ext import commands
from main import IntegrityError
from datetime import datetime
import discord
import bot.database.db as db

date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

main_ideologies = ["Автократия", 
              "Демократия", 
              "Зеленая идеология (экологизм)", 
              "Коммунизм",
              "Консерватизм", 
              "Либерализм", 
              "Либертарианство", 
              "Национализм", 
              "Социал-демократия", 
              "Социализм", 
              "Фашизм"]
adv_ideologies = ["Гуманизм",
                  "Феминизм",
                  "Маскулизм",
                  "Трансгуманизм",
                  "Экологизм"]

govs = ["Абсолютная монархия", 
        "Анархия", 
        "Автократия",
        "Конституционная монархия", 
        "Олигархия", 
        "Парламентская республика", 
        "Племенное правление", 
        "Президентская республика", 
        "Смешанная республика", 
        "Теократия",
        "Тоталитаризм"]

class Registration(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.conn = db.connection()
        self.curs = self.conn.cursor()

    def log_entry(
            self, 
            user: discord.User, 
            author: discord.User, 
            positive: bool, 
            action: str,  
            error: str | None = None
            ) -> str:
        log_action = "added to" if action == "add" else "deleted from"
        log_msg_dict = {True: f"\n[{date}] [+] Player ({user.id}) - {user} was {log_action} the database by {author} ({author.id})!", False: f"\n[{date}] [-] Player ({user.id}) - {user} could not be {log_action} the database by {author} ({author.id})! Reason: {error}"}
        log_msg = log_msg_dict[positive]

        with open("./logs/regs.txt", "a") as file:
            file.write(log_msg)
            print(log_msg)

    @commands.slash_command(
            name="registration", 
            description="Регистрация учасника сервера"
            )
    @commands.has_permissions(moderate_members=True)
    async def reg(
        self, 
        ctx: discord.ApplicationContext, 
        user: discord.Option(discord.User, description='Кого вы хотите зарегистрировать?'), #type: ignore
        country_name: discord.Option(str, description='Название страны'), #type: ignore
        leader_name: discord.Option(str, description='ФИО лидера страны'), #type: ignore
        ideology: discord.Option(str, description='Идеология государства', 
                                 choices=main_ideologies), #type: ignore
        government: discord.Option(str, description='Форма правления', 
                                 choices=govs), #type: ignore
        gdp: discord.Option(int, description='ВВП'), #type: ignore
        territories: discord.Option(
            str, 
            description='Названия стран/регионов (если таковы взяты отдельно) ' \
            'на которых расположена страна игрока'), #type: ignore
        s: discord.Option(int, description='Площадь территории'), #type: ignore
        population: discord.Option(int, description="Население"), #type: ignore
        second_ideology: discord.Option(
            str, 
            description='Дополнительная идеология (если есть)', 
            choices=adv_ideologies,
            required=False
        )) -> None: #type: ignore

        try:
            self.curs.execute("INSERT INTO countries VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user.id, country_name, leader_name, ideology, second_ideology, government, gdp, territories, s, population))
            self.conn.commit()
            embed=discord.Embed(title="🏳️ | Страна зарегистрирована", description=f"Вы зарегистрировали {user.mention} за {country_name}!", color=0x08000)
            self.log_entry(user, ctx.author, True, "add")
        except db.sql.IntegrityError as i:
            self.log_entry(user, ctx.author, False, "add", i)
            embed=discord.Embed(description="**❌ | Пользователь УЖЕ зарегистрирован!**", color=0xff0000)
        except Exception as e:
            self.log_entry(user, ctx.author, False, "add", e)
            embed = discord.Embed(description="**❌ | Неизвестная ошибка!**", color=0xff0000)
        finally:
            await ctx.respond(embed=embed)
    
    @commands.slash_command(name="unregistration", description="Снять со страны участника сервера")
    @commands.has_permissions(moderate_members=True)
    async def unreg(
        self, 
        ctx: discord.ApplicationContext,
        user: discord.Option(discord.User,
                            description="Кого вы хотите снять?") #type: ignore
        ) -> None: 
        try:
            self.curs.execute("DELETE FROM countries WHERE user_id = ?", (user.id,))
            self.conn.commit()

            if self.curs.rowcount == 0:
                raise ValueError("Something went wrong! Check the datebase or request")
            else:
                self.log_entry(user, ctx.author, True, "remove")
            
            embed=discord.Embed(title="✅ | Игрок снят", description=f"Вы сняли игрока под ником {user} со страны!", color=0x08000)

        except Exception as e:
            self.log_entry(user, ctx.author, False, "remove", e)
            embed=discord.Embed(title="❌ | Игрок не снят", description=f"Игрок под ником {user} не был снят со страны! Возможно, он не зарегистрирован!", color=0xff0000)
        finally:
            await ctx.respond(embed=embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Registration(bot))