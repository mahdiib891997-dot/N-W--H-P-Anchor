import discord
import os
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # هذا السطر يخبر ديسكورد بتحديث الأوامر فوراً
    synced = await bot.tree.sync()
    print(f'تمت مزامنة {len(synced)} أمر سلاش.')
    print(f'البوت {bot.user.name} جاهز!')

# أمر السلاش لدخول البوت
@bot.tree.command(name="join", description="يجعل البوت يدخل للروم الصوتي")
async def join(interaction: discord.Interaction):
    channel_id = 1207652837463425054  # ضع ID الروم الصوتي هنا
    channel = bot.get_channel(channel_id)
    
    if channel:
        voice_client = await channel.connect()
        await voice_client.edit(mute=True)
        await interaction.response.send_message("تم تشغيل البوت ودخوله للروم.")
    else:
        await interaction.response.send_message("لم أجد الروم الصوتي!")

# أمر السلاش لخروج البوت
@bot.tree.command(name="leave", description="يجعل البوت يخرج من الروم الصوتي")
async def leave(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("تم إيقاف البوت وخروجه من الروم.")
    else:
        await interaction.response.send_message("البوت ليس موجوداً في أي روم حالياً.")

bot.run(os.getenv('TOKEN'))