from discord.ext import commands
from datetime import datetime
import discord
import json
import os
import bot.database.db as db

# datetime part
now = datetime.now()
date = now.strftime("[%Y-%m-%d %H:%M:%S]")

# intents part
intents = discord.Intents.all()
intents.message_content = True

# Get configuration.json
with open("configuration.json", "r") as config:
    data = json.load(config)
    token = data["token"]
    prefix = data["prefix"]
    #exts = data["extensions"]["slash_commands"] 
    #print(exts)

bot = commands.Bot(prefix, intents=intents)

@bot.event
async def on_ready():
    with db.connection() as conn:
        db.create_tables(conn)
        curs = conn.cursor()
        for guild in bot.guilds:
            curs.execute(
                f"INSERT OR IGNORE INTO servers VALUES({guild.id}, 0, 0, 0, 0, 0)")
    print(f"Bot - {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"Israel attacks Lebanon live | {bot.command_prefix}help"))
    print(discord.__version__)
    bot.remove_command("help")
    await bot.sync_commands()

@bot.event
async def on_connect():
    try:
        for filename in os.listdir('./slash_commands'): #checking files inside the ./cogs directory.
            if filename.endswith('.py'): #checking for .py files inside ./cogs directory.
                bot.load_extension(f'slash_commands.{filename[:-3]}') #loading every .py files.
                print(f"Loaded Cog: {filename[:-3]}")
        for filename in os.listdir('./commands'): #checking files inside the ./cogs directory.
           if filename.endswith('.py'): #checking for .py files inside ./cogs directory.
                bot.load_extension(f'commands.{filename[:-3]}') #loading every .py files.
                print(f"Loaded Cog: {filename[:-3]}")
        
    except Exception as e:
        print("Error: {}".format(e))
    
    '''for ext in exts:

        bot.load_extension(f'slash_commands.{ext}') #loading every .py files.
        print("+", ext)'''

# Всё что ниже - удалить

@bot.command()
async def oops(ctx):
    await ctx.send('Упс... ' + ctx.message.author.mention + ' бзданул на весь сервер')

@bot.command()
async def hello(ctx):
    if ctx.author.id == 1024624095293345874:
        await ctx.send('Привет уебан! Пошёл нахуй!')
    else:
        await ctx.send('Привет ' + ctx.message.author.mention + ' !')

@bot.command()
async def reg(ctx, a1: int = None, a2: int = None, a3: int = None):
    AMERICAN_GDP = 736.75

    if not a1:
        emb = discord.Embed(
            title='⚠Ошибка',
            description=f'Вы не указали ВВП вашей страны.',
            color=discord.Colour.red())
        await ctx.send(embed=emb)
    else:
        if not a2:
            emb = discord.Embed(
                title='⚠Ошибка',
                description=f'Вы не указали резерв вашей страны.',
                color=discord.Colour.red())
            await ctx.send(embed=emb)
        else:
            if not a3:
                emb = discord.Embed(
                    title='⚠Ошибка',
                    description=f'Вы не указали долг вашей страны.',
                    color=discord.Colour.red())
                await ctx.send(embed=emb)
            else:
                if ctx.guild.id == 874384683968917584:
                    emb = discord.Embed(
                        title='⚠Ошибка',
                        description=
                        f'Вы находитесь на сервере, к валюте которого ведется подсчет курсов конвертаций других серверов. Регистрировать здесь валюту не нужно.',
                        color=discord.Colour.dark_red())
                    await ctx.send(embed=emb)
                else:
                    if ctx.author.guild_permissions.administrator:
                        conn = db.connection()
                        cursor = conn.cursor()
                        z = cursor.execute(
                            f"SELECT * FROM servers WHERE id = {ctx.guild.id}"
                        ).fetchone()
                        if z[3] == 0:
                            await ctx.send(embed=discord.Embed(
                                title='⚠Ошибка',
                                description=
                                'Пункт "population" является обязательным аргументом для конвертации курса.\n\nК сожалению, администрация еще не установила значения населения для вашего сервера. Ожидайте. ',
                                color=discord.Colour.dark_red()))
                        else:
                            cursor.execute(
                                f"UPDATE servers SET bud = {a1} WHERE id = {ctx.guild.id}"
                            )
                            cursor.execute(
                                f"UPDATE servers SET crzp = {a2} WHERE id = {ctx.guild.id}"
                            )
                            wl = (float(a1) + float(a2) - float(a3)) / AMERICAN_GDP
                            o = round(wl, 1)
                            cursor.execute(
                                f"UPDATE servers SET well = {o} WHERE id = {ctx.guild.id}"
                            )
                            await ctx.send(embed=discord.Embed(
                                title='Успешно',
                                description=
                                f'Вы успешно зарегистрировали свою валюту с исходным бюджетом в **{a1}** и средней заработной платой в **{a2}**. ',
                                color=discord.Colour.dark_green()))
                            conn.commit()
                            cursor.close()
                            conn.close()
                    else:
                        emb = discord.Embed(
                            title='⚠Ошибка',
                            description=
                            f'У вас недостаточно прав для использовании этой команды. Ее могут использовать только овнер и администратор данного сервера.',
                            color=discord.Colour.dark_red())
                        await ctx.send(embed=emb)


@bot.event
async def on_guild_join(guildD):
    conn = db.connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO servers VALUES('{guildD.id}', 0, 0, 0, 0, 0)")
    for ch in bot.get_guild(874384683968917584).channels:
        if ch.name == '▹〘💽〙•├─логи-бота':
            await ch.send(embed=discord.Embed(
                title='Новый сервер',
                description=
                f'Бот был добавлен на новый сервер **{guildD.name}** ({guildD.id}). Овнер нового сервера: {guildD.owner.mention}. ',
                color=discord.Colour.dark_green()))
    conn.commit()
    cursor.close()
    conn.close()

@bot.event
async def on_guild_remove(guildD):
    conn = db.connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM servers WHERE id = {guildD.id}")
    for ch in bot.get_guild(874384683968917584).channels:
        if ch.name == '▹〘💽〙•├─логи-бота':
            await ch.send(embed=discord.Embed(
                title='Кик бота',
                description=
                f'Бота кикнули с сервера **{guildD.name}** ({guildD.id}). Овнер данного сервера: {guildD.owner.mention}. ',
                color=discord.Colour.dark_green()))
    conn.commit()
    cursor.close()
    conn.close()


@bot.command()
async def set(ctx, id1, p):
    alw = [958077120612032612, 635539371205984281]
    if ctx.author.id in alw:
        conn = db.connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE servers SET population = {p} WHERE id = {id1}")
        k = bot.get_guild(int(id1))
        await ctx.send(embed=discord.Embed(
            title='Успешно',
            description=
            f'Вы успешно установили значение населения для сервера **{k}** в **{p}**',
            color=discord.Colour.green()))
        conn.commit()
        cursor.close()
        conn.close()
    else:
        emb = discord.Embed(
            title='⚠Ошибка',
            description=
            f'У вас недостаточно прав для использовании этой команды.',
            color=discord.Colour.red())
        await ctx.send(embed=emb)


@bot.command()
async def check(ctx, id6=None):
    if not id6:
        emb = discord.Embed(
            title='⚠Ошибка',
            description=
            f'Вы не указали id сервера, курс конвертации которого хотите посмотреть.',
            color=discord.Colour.red())
        await ctx.send(embed=emb)
    else:
        conn = db.connection()
        cursor = conn.cursor()
        l = cursor.execute(
            f"SELECT * FROM servers WHERE id = {id6}").fetchone()
        if l[4] == 0:
            await ctx.send(embed=discord.Embed(
                title='⚠Ошибка',
                description=
                'Указанного вами сервера не существует, или его создатель еще не зарегистрировал свою валюту. ',
                color=discord.Colour.dark_red()))
        else:
            k = bot.get_guild(int(id6))
            await ctx.send(embed=discord.Embed(
                title='Курс конвертации',
                description=
                f'Внимание! Курс расчитывается непосредственно в моменте конвертации, поэтому при резком изменение количества денежной массы он может сильно изменится.\n\nКурс конвертации **{l[4]}** к 1 единице валюты сервера 874384683968917584. Чтобы получить 1$, потребуется потратить **{l[4]}** единиц валюты сервера **{k}**. ',
                color=discord.Colour.gold()))
        conn.commit()
        cursor.close()
        conn.close()


@bot.command()
async def checkall(ctx):
    conn = db.connection()
    cursor = conn.cursor()
    a = ''
    for i in bot.guilds:
        l = cursor.execute(
            f"SELECT * FROM servers WHERE id = {i.id}").fetchone()
        if l[4] == 0:
            pass
        else:
            a = a + f'**{i.name}**: {str(l[4])} к 1$\n'
    emb = discord.Embed(title='Курс валют',
                        description=f'{a}',
                        color=discord.Colour.red())
    await ctx.send(embed=emb)
    conn.commit()
    cursor.close()
    conn.close()


@bot.command()
async def servall(ctx):
    a = ''
    g = 1
    for i in bot.guilds:
        a = a + f'**{g}**. {i.name} ({i.id})\n'
        g = g + 1
    emb = discord.Embed(title='Сервера',
                        description=f'{a}',
                        color=discord.Colour.red())
    await ctx.send(embed=emb)


@bot.command()
async def add_sanctions(ctx, idf=None):
    if not idf:
        emb = discord.Embed(
            title='⚠Ошибка',
            description=
            f'Вы не указали id сервера, на который хотите наложить санкции.',
            color=discord.Colour.red())
        await ctx.send(embed=emb)
    else:
        alw = [958077120612032612, 635539371205984281]
        if ctx.author.id in alw:
            conn = db.connection()
            cursor = conn.cursor()
            z = cursor.execute(
                f"SELECT * FROM servers WHERE id = {idf}").fetchone()
            a = z[4] * 12
            m = z[5] + 1
            cursor.execute(f"UPDATE servers SET well = {a} WHERE id = {idf}")
            cursor.execute(
                f"UPDATE servers SET sanctions = {m} WHERE id = {idf}")
            k = bot.get_guild(int(idf))
            emb = discord.Embed(
                title='Успешно',
                description=f'На сервер **{k}** были добавлены санкции. ',
                color=discord.Colour.green())
            await ctx.send(embed=emb)
            conn.commit()
            cursor.close()
            conn.close()
        else:
            emb = discord.Embed(
                title='⚠Ошибка',
                description=
                f'У вас недостаточно прав для использовании этой команды.',
                color=discord.Colour.red())
            await ctx.send(embed=emb)


@bot.command()
async def rem_sanctions(ctx, idf=None):
    if not idf:
        emb = discord.Embed(
            title='⚠Ошибка',
            description=
            f'Вы не указали id сервера, с которого хотите снять санкции.',
            color=discord.Colour.red())
        await ctx.send(embed=emb)
    else:
        alw = [958077120612032612, 635539371205984281]
        if ctx.author.id in alw:
            conn = db.connection()
            cursor = conn.cursor()
            z = cursor.execute(
                f"SELECT * FROM servers WHERE id = {idf}").fetchone()
            if z[5] > 0:
                a = z[4] / 12
                m = z[5] - 1
                cursor.execute(
                    f"UPDATE servers SET well = {a} WHERE id = {idf}")
                cursor.execute(
                    f"UPDATE servers SET sanctions = {m} WHERE id = {idf}")
                k = bot.get_guild(int(idf))
                emb = discord.Embed(
                    title='Успешно',
                    description=f'С сервера **{k}** были сняты санкции. ',
                    color=discord.Colour.green())
                await ctx.send(embed=emb)
            else:
                k = bot.get_guild(int(idf))
                emb = discord.Embed(
                    title='⚠Ошибка',
                    description=f'На сервер {k} еще не было наложено санкций. ',
                    color=discord.Colour.red())
                await ctx.send(embed=emb)
            conn.commit()
            cursor.close()
            conn.close()
        else:
            emb = discord.Embed(
                title='⚠Ошибка',
                description=
                f'У вас недостаточно прав для использовании этой команды.',
                color=discord.Colour.red())
            await ctx.send(embed=emb)

@bot.command()
async def setr(ctx, id: int = None, a1: int = None, a2: int = None):
    if not id:
        emb = discord.Embed(title='⚠Ошибка',
                            description=f'Вы не указали id сервера.',
                            color=discord.Colour.red())
        await ctx.send(embed=emb)
    else:
        if not a1:
            emb = discord.Embed(title='⚠Ошибка',
                                description=f'Вы не указали бюджет сервера.',
                                color=discord.Colour.red())
            await ctx.send(embed=emb)
        else:
            if not a2:
                emb = discord.Embed(
                    title='⚠Ошибка',
                    description=f'Вы не указали среднню зарплату сервера.',
                    color=discord.Colour.red())
                await ctx.send(embed=emb)
            else:
                alw = [958077120612032612, 635539371205984281]
                if ctx.author.id in alw:
                    conn = db.connection()
                    cursor = conn.cursor()
                    z = cursor.execute(
                        f"SELECT * FROM servers WHERE id = {id}").fetchone()
                    if z[3] == 0:
                        await ctx.send(embed=discord.Embed(
                            title='⚠Ошибка',
                            description=
                            'Пункт "population" еще не установлен для указанного вами сервера. ',
                            color=discord.Colour.red()))
                    else:
                        if a1 >= z[3] * 60:
                            cursor.execute(
                                f"UPDATE servers SET bud = {a1} WHERE id = {id}"
                            )
                            cursor.execute(
                                f"UPDATE servers SET crzp = {a2} WHERE id = {id}"
                            )
                            wl = float(a1) / (float(z[3]) * float(a2)) * 10000
                            o = round(wl, 1)
                            k = bot.get_guild(int(id))
                            cursor.execute(
                                f"UPDATE servers SET well = {o} WHERE id = {id}"
                            )
                            await ctx.send(embed=discord.Embed(
                                title='Успешно',
                                description=
                                f'Вы успешно установили значение бюджета в **{a1}** и значение средней заработной платы в **{a2}** для сервера **{k}**.',
                                color=discord.Colour.green()))
                            conn.commit()
                            cursor.close()
                            conn.close()
                        else:
                            await ctx.send(embed=discord.Embed(
                                title='⚠Ошибка',
                                description=
                                'Аргумент "Budget" должен быть больше население в 60 раз для успешной конвертации.',
                                color=discord.Colour.dark_red()))
                else:
                    emb = discord.Embed(
                        title='⚠Ошибка',
                        description=
                        f'У вас недостаточно прав для использовании этой команды.',
                        color=discord.Colour.red())
                    await ctx.send(embed=emb)

if __name__ == '__main__':
    bot.run(token)