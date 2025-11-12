from bot.modals.archive_modal import ArchiveModal
from discord.ext import commands
import discord
import bot.database.db as db
import asyncio

class Archive(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    main = discord.SlashCommandGroup("archive", "Архивация данных", parent=None, slash_command=None)

    @main.command(description="Внести данные об историческом событии в единый архив")
    @commands.has_permissions(moderate_members=True)
    async def add(self, ctx: discord.ApplicationContext) -> None:
        """Показывает модальное окно для добавления события."""
        modal = ArchiveModal()
        print(modal)
        await ctx.send_modal(modal)

    @main.command(description="Убрать данные о событии из единого архива")
    @commands.has_permissions(moderate_members=True)
    async def remove(self, ctx: discord.ApplicationContext, id: discord.Option(int, "ID-ключ события")) -> None: # type: ignore
        conn = await db.connection()
        try:
            result = await conn.fetchrow("SELECT * FROM archive WHERE id=$1", id)
            if result:
                await conn.execute("DELETE FROM archive WHERE id=$1", id)
                await ctx.respond(f"✅ | Запись с ID #{id} успешно удалена!")
            else:
                await ctx.respond(f"❌ | Ошибка! Проверьте указанный ID и повторите попытку!")
        finally:
            await conn.close()

    @main.command(description="Просмотреть событие с ID")
    async def view(self, ctx: discord.ApplicationContext, id: discord.Option(int, "ID-ключ события")) -> None: # type: ignore
        conn = await db.connection()
        try:
            event = await conn.fetchrow("SELECT * FROM archive WHERE id=$1", id)
            if event:
                embed = discord.Embed(
                    title=f"📝 | Информация о событии {event['name']} | #{event['id']}",
                    color=0xff0033
                )
                embed.add_field(name="Описание", value=f"{event['description']}", inline=False)
                embed.add_field(name="Дата", value=f"{event['date']}", inline=False)
                await ctx.respond(embed=embed)
            else:
                await ctx.respond("❌ | Запись с таким ID не найдена!")
        finally:
            await conn.close()

    @main.command(name="list", description="Список всех событий")
    async def all(self, ctx: discord.ApplicationContext) -> None:
        conn = await db.connection()
        try:
            records = await conn.fetch("SELECT * FROM archive ORDER BY id")
            if records:
                msg = "\n".join([f"{r['id']}. {r['name']}, {r['date']}" for r in records])
            else:
                msg = "На данный момент в базе отсутствуют данные."
            embed = discord.Embed(title="📅 | Список событий", description=msg, color=0xe3ff57)
            await ctx.respond(embed=embed)
        finally:
            await conn.close()

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Archive(bot))
