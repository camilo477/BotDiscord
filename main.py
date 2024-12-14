import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

contador_confesiones = 0


@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}!")
    await bot.tree.sync()


@bot.tree.command(name="confesar")
async def confesar(interaction: discord.Interaction, mensaje: str):
    global contador_confesiones  # Acceder a la variable global para el contador
    try:
        # Incrementar el contador con cada confesión
        contador_confesiones += 1
        # Buscar los canales por nombre
        canal_confesiones = discord.utils.get(interaction.guild.channels, name="confesiones")
        canal_admin = discord.utils.get(interaction.guild.channels, name="confesiones_admin")

        # Validar si los canales existen
        if canal_confesiones and canal_admin:
            # Estilizar el mensaje para hacerlo más bonito
            mensaje_confesion = f"** Confesión #{contador_confesiones} **\n```fix\n{mensaje}\n```"
            mensaje_admin = f"**🛠 Confesión #{contador_confesiones} 🛠**\n**Usuario:** {interaction.user.name}#{interaction.user.discriminator}\n\n```fix\n{mensaje}\n```"

            # Enviar la confesión anónima al canal #confesiones
            await canal_confesiones.send(mensaje_confesion)

            # Enviar la información al canal de administración
            await canal_admin.send(mensaje_admin)

            # Mensaje privado (ephemeral) para confirmar al usuario que la confesión se envió
            await interaction.response.send_message(
                f"Tu **Confesión** (número {contador_confesiones}) ha sido enviada exitosamente.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "No se encontraron los canales necesarios para enviar la confesión.", ephemeral=True
            )
    except discord.Forbidden:
        await interaction.response.send_message(
            "No tengo permisos para enviar la confesión.", ephemeral=True
        )


# Ejecutar el bot
bot.run(TOKEN)
