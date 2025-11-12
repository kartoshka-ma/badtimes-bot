import discord
from discord.ext import commands
import json
import bot.database.db as db

intents = discord.Intents.all()
intents.message_content = True

with open("./bot/configuration.json", "r") as config:
    data = json.load(config)
    token = data["token"]
    prefix = data["prefix"]

bot = commands.Bot(command_prefix=prefix, intents=intents, application_id=1206660906621341737)

@bot.event
async def on_ready():
    print(f"Bot {bot.user} is online!")

    # инициализация БД
    conn = await db.connection()
    await db.create_tables(conn)
    await conn.close()

    # загрузка когов
    import os
    for folder in ["commands", "slash_commands"]:
        for filename in os.listdir(f"./bot/{folder}"):
            if filename.endswith(".py"):
                try:
                    bot.load_extension(f"bot.{folder}.{filename[:-3]}")
                    print(f"Loaded {folder}.{filename[:-3]}")
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    await bot.sync_commands()

# Всё что ниже - удалить
@bot.command()
async def oops(ctx):
    await ctx.send(f'Упс... {ctx.author.mention} бзданул на весь сервер')

@bot.command()
async def hello(ctx):
    if ctx.author.id == 1024624095293345874:
        await ctx.send('Привет уебан! Пошёл нахуй!')
    else:
        await ctx.send(f'Привет {ctx.author.mention} !')

@bot.command()
async def reg(ctx, a1: int = None, a2: int = None, a3: int = None):
    AMERICAN_GDP = 736.75
    if not a1:
        await ctx.send(embed=discord.Embed(title='⚠Ошибка', description='Вы не указали ВВП вашей страны.', color=discord.Colour.red()))
        return
    if not a2:
        await ctx.send(embed=discord.Embed(title='⚠Ошибка', description='Вы не указали резерв вашей страны.', color=discord.Colour.red()))
        return
    if not a3:
        await ctx.send(embed=discord.Embed(title='⚠Ошибка', description='Вы не указали долг вашей страны.', color=discord.Colour.red()))
        return
    if ctx.guild.id == 874384683968917584:
        await ctx.send(embed=discord.Embed(
            title='⚠Ошибка',
            description='Регистрация валюты на этом сервере не требуется.',
            color=discord.Colour.dark_red()))
        return
    if ctx.author.guild_permissions.administrator:
        conn = await db.connection()
        try:
            z = await conn.fetchrow("SELECT * FROM servers WHERE id=$1", ctx.guild.id)
            if z['population'] == 0:
                await ctx.send(embed=discord.Embed(
                    title='⚠Ошибка',
                    description='Администрация еще не установила население для сервера.',
                    color=discord.Colour.dark_red()))
            else:
                await conn.execute("UPDATE servers SET bud=$1, crzp=$2 WHERE id=$3", a1, a2, ctx.guild.id)
                wl = (a1 + a2 - a3) / AMERICAN_GDP
                await conn.execute("UPDATE servers SET well=$1 WHERE id=$2", round(wl, 1), ctx.guild.id)
                await ctx.send(embed=discord.Embed(
                    title='Успешно',
                    description=f'Вы успешно зарегистрировали валюту: бюджет {a1}, зарплата {a2}.',
                    color=discord.Colour.dark_green()))
        finally:
            await conn.close()
    else:
        await ctx.send(embed=discord.Embed(
            title='⚠Ошибка',
            description='У вас недостаточно прав для использования этой команды.',
            color=discord.Colour.dark_red()))

# Событие присоединения к серверу
@bot.event
async def on_guild_join(guildD):
    conn = await db.connection()
    try:
        await conn.execute("INSERT INTO servers(id, bud, crzp, population, well, sanctions) VALUES($1, 0, 0, 0, 0, 0)", guildD.id)
        log_channel = discord.utils.get(bot.get_guild(874384683968917584).channels, name='▹〘💽〙•├─логи-бота')
        if log_channel:
            await log_channel.send(embed=discord.Embed(
                title='Новый сервер',
                description=f'Бот добавлен на сервер {guildD.name} ({guildD.id}). Овнер: {guildD.owner.mention}',
                color=discord.Colour.dark_green()))
    finally:
        await conn.close()

# Событие удаления с сервера
@bot.event
async def on_guild_remove(guildD):
    conn = await db.connection()
    try:
        await conn.execute("DELETE FROM servers WHERE id=$1", guildD.id)
        log_channel = discord.utils.get(bot.get_guild(874384683968917584).channels, name='▹〘💽〙•├─логи-бота')
        if log_channel:
            await log_channel.send(embed=discord.Embed(
                title='Кик бота',
                description=f'Бота кикнули с сервера {guildD.name} ({guildD.id}). Овнер: {guildD.owner.mention}',
                color=discord.Colour.dark_green()))
    finally:
        await conn.close()

# Пример команды set
@bot.command()
async def set(ctx, id1, p):
    alw = [958077120612032612, 635539371205984281]
    if ctx.author.id not in alw:
        await ctx.send(embed=discord.Embed(title='⚠Ошибка', description='У вас недостаточно прав.', color=discord.Colour.red()))
        return
    conn = await db.connection()
    try:
        await conn.execute("UPDATE servers SET population=$1 WHERE id=$2", int(p), int(id1))
        k = bot.get_guild(int(id1))
        await ctx.send(embed=discord.Embed(title='Успешно', description=f'Население сервера {k} установлено в {p}', color=discord.Colour.green()))
    finally:
        await conn.close()


# Запуск бота
bot.run(token)