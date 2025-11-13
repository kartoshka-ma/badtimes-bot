from discord.ext import commands
import discord
import db

class ArchiveModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.conn = db.connection()
        self.curs = self.conn.cursor()

        self.add_item(discord.ui.InputText(label="Название события", placeholder="Битва под Ивановском (1904)"))
        self.add_item(discord.ui.InputText(label="Дата (mm/DD/yy)", min_length=10, max_length=10, placeholder="02.10.1904"))
        self.add_item(discord.ui.InputText(label="Описание события", style=discord.InputTextStyle.long, placeholder="Оборона города Ивановск. Провальный штурм революционеров и большие потери до **5000** солдат..."))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Добавлено событие!")
        embed.add_field(name="Название", value=self.children[0].value)
        embed.add_field(name="Дата", value=self.children[1].value)
        embed.add_field(name="Описание", value=self.children[2].value, inline=False)

        try:
            max_id = self.curs.execute("SELECT MAX(id) FROM archive").fetchone()[0]
            if max_id != None:
                print(max_id)
                max_id = max_id + 1
            else:
                max_id = 0

            self.curs.execute("INSERT INTO archive VALUES(?, ?, ?, ?)", (self.children[0].value, self.children[1].value, self.children[2].value, max_id))
            self.conn.commit()
        except Exception as e:
            print(e)
        await interaction.response.send_message(embeds=[embed])