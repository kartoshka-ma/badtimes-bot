from discord.ext import commands
import discord
import bot.database.db as db

class ArchiveModal(discord.ui.Modal):
    """Модальное окно для добавления события в архив"""
    def __init__(self):
        super().__init__(title="📝 | Регистрация события")

        self.add_item(discord.ui.InputText(
            label="Название события", 
            placeholder="Битва под Ивановском (1904)"
        ))
        self.add_item(discord.ui.InputText(
            label="Дата (ДД.ММ.ГГГГ)", 
            min_length=10, 
            max_length=10, 
            placeholder="02.10.1904"
        ))
        self.add_item(discord.ui.InputText(
            label="Описание события", 
            style=discord.InputTextStyle.long, 
            placeholder="Оборона города Ивановск. Провальный штурм революционеров и большие потери до **5000** солдат..."
        ))

    async def callback(self, interaction: discord.Interaction):
        """Обработка данных из модалки"""
        try:
            conn = await db.connection()
            async with conn.transaction():
                # Получаем максимальный ID
                max_id = await conn.fetchval("SELECT MAX(id) FROM archive")
                new_id = (max_id or 0) + 1

                # Добавляем новую запись
                await conn.execute(
                    "INSERT INTO archive (id, name, date, description) VALUES ($1, $2, $3, $4)",
                    new_id,
                    self.children[0].value,  # title
                    self.children[1].value,  # date
                    self.children[2].value   # description
                )

            await conn.close()

        except Exception as e:
            await interaction.response.send_message(
                f"❌ | Ошибка при добавлении: `{e}`", ephemeral=True
            )
            return

        embed = discord.Embed(
            title="✅ Событие добавлено!",
            color=0x2ecc71
        )
        embed.add_field(name="Название", value=self.children[0].value)
        embed.add_field(name="Дата", value=self.children[1].value)
        embed.add_field(name="Описание", value=self.children[2].value, inline=False)

        await interaction.response.send_message(embed=embed)
