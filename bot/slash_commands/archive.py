from modals.archive_modal import ArchiveModal
from discord.ext import commands
import discord
import bot.database.db as db


class Archive(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.conn = db.connection()
        self.curs = self.conn.cursor()

    main = discord.SlashCommandGroup("archive", "Архивация данных", parent=None, slash_command=None)

    @main.command(description="Внести данные об историческом событии в единый архив")
    @commands.has_permissions(moderate_members=True)
    async def add(self, ctx: discord.ApplicationContext) -> None:
        """Shows an example of a modal dialog being invoked from a slash command."""
        modal = ArchiveModal(title="📝 | Регистрация события")
        print(modal)
        await ctx.send_modal(modal)
    
    @main.command(description="Убрать данные о событии из единого архива")
    @commands.has_permissions(moderate_members=True)
    async def remove(self, ctx: discord.ApplicationContext, id: discord.Option(int, "ID-ключ события")) -> None: # type: ignore
        if self.curs.execute("SELECT * FROM archive WHERE id=?", (id,)).fetchall():
            self.curs.execute("DELETE FROM archive WHERE id=?", (id,))
            self.conn.commit()
            await ctx.respond(f"✅ | Запись с ID #{id} успешно удалена!")
            self.conn.close()
            self.curs.close()
        else:
            await ctx.respond(f"❌ | Ошибка! Проверьте указанный ID и повторите попытку!")
    
    @main.command(description="Просмотреть событие с ID")
    async def view(self, ctx: discord.ApplicationContext, id: discord.Option(int, "ID-ключ события")) -> None: # type: ignore
        event = self.curs.execute("SELECT * FROM archive WHERE id=?", (id,)).fetchall()
        if event:
            print(event)
            event = event[0]
            embed = discord.Embed(title=f"📝 | Информация о событии {event[0]} | #{event[3]}", description=None, color=0xff0033)
            embed.add_field(name="Описание", value=f"{event[2]}", inline=False)
            embed.add_field(name="Дата", value=f"{event[1]}", inline=False)
            await ctx.respond(embed=embed)
        else:
            print(event)
            await ctx.respond("❌ | Запись с таким ID не найдена!")
    
    @main.command(description="Список всех событий")
    async def all(self, ctx: discord.ApplicationContext) -> None:
        records = self.curs.execute("SELECT * FROM archive ORDER BY id").fetchall()
        # print(records, records[0], records[0][0])
        msg = ""
        if len(records) > 0:
            for record in records:
                name = record[0]
                date = record[1]
                description = record[2]
                id = record[3]
                msg += f"{id}. {name}, {date}\n"
        else: 
            msg = "На данный момент в базе отсутсвуют данные."
        embed = discord.Embed(title=f"📅 | Список событий", description=msg, color=0xe3ff57)
        await ctx.respond(embed=embed)
    
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Archive(bot))