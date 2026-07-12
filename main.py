import discord
import os
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f'تمت مزامنة {len(synced)} أمر سلاش.')
    print(f'البوت {bot.user.name} جاهز!')

@bot.tree.command(name="join", description="يجعل البوت يدخل للروم الصوتي")
@app_commands.checks.has_permissions(administrator=True)
async def join(interaction: discord.Interaction):
    # رد فوري لتجنب خطأ عدم الاستجابة
    await interaction.response.defer(ephemeral=True) 
    
    channel_id = 1207652837463425054 
    channel = bot.get_channel(channel_id)
    
    if channel:
        try:
            # محاولة الاتصال بالروم
            voice_client = await channel.connect()
            await voice_client.edit(mute=True)
            await interaction.followup.send("تم تشغيل البوت ودخوله للروم الصوتي.")
        except Exception as e:
            await interaction.followup.send(f"حدث خطأ أثناء الدخول: {e}")
    else:
        await interaction.followup.send("لم أجد الروم الصوتي! تأكد من الـ ID.")

@bot.tree.command(name="leave", description="يجعل البوت يخرج من الروم الصوتي")
@app_commands.checks.has_permissions(administrator=True)
async def leave(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.followup.send("تم إيقاف البوت وخروجه من الروم الصوتي.")
    else:
        await interaction.followup.send("البوت ليس موجوداً في أي روم صوتي حالياً.")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("عذراً، هذا الأمر مخصص للمسؤولين فقط! ❌", ephemeral=True)
    else:
        print(f"خطأ غير متوقع: {error}")

bot.run(os.getenv('TOKEN'))
