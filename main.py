import discord
import os
import asyncio
from discord import app_commands
from discord.ext import commands

# تفعيل الأذونات المطلوبة
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(
    command_prefix="!", 
    intents=intents,
    shard_count=1,
    heartbeat_timeout=150.0,
    reconnect=True
)

# ملف لحفظ الساعات بشكل دائم حتى لا تضيع عند الريستارت
HOURS_FILE = "hours.txt"

def load_hours():
    if os.path.exists(HOURS_FILE):
        try:
            with open(HOURS_FILE, "r") as f:
                return float(f.read().strip())
        except:
            return 0.0
    return 0.0

def save_hours(hours):
    with open(HOURS_FILE, "w") as f:
        f.write(str(hours))

# متغير لتتبع الساعات محلياً
total_hours = load_hours()
is_tracking = False

async def track_voice_time():
    global total_hours, is_tracking
    is_tracking = True
    while is_tracking:
        await asyncio.sleep(60) # يحسب كل دقيقة
        # التأكد أن البوت لا يزال متصلاً بروم صوتي
        connected = any(guild.voice_client is not None for guild in bot.guilds)
        if connected:
            total_hours += 1 / 60.0 # إضافة دقيقة محسوبة بالساعات
            save_hours(total_hours) # حفظها فوراً في الملف لكي لا تضيع أبداً

@bot.event
async def on_ready():
    global is_tracking
    synced = await bot.tree.sync()
    print(f'تم مزامنة {len(synced)} أمر سلاش.')
    print(f'البوت {bot.user.name} جاهز! الساعات المحفوظة حالياً: {round(total_hours, 2)} ساعة.')
    
    if not is_tracking:
        bot.loop.create_task(track_voice_time())

@bot.tree.command(name="join voice", description="يجعل البوت يدخل للروم الصوتي ويستقر فيه")
@app_commands.checks.has_permissions(administrator=True)
async def join(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    channel_id = 1207653737280307250
    channel = bot.get_channel(channel_id)

    if channel:
        try:
            if interaction.guild.voice_client:
                await interaction.guild.voice_client.disconnect()
            
            voice_client = await channel.connect(self_deaf=True)
            await interaction.followup.send("تم تشغيل البوت ودخوله للروم الصوتي بنجاح (بوضع الصامت).")
        except Exception as e:
            await interaction.followup.send(f"حدث خطأ أثناء الدخول: {e}")
    else:
        await interaction.followup.send("لم أجد الروم الصوتي! تأكد من الـ ID.")

@bot.tree.command(name="leave voice", description="يجعل البوت يخرج من الروم الصوتي")
@app_commands.checks.has_permissions(administrator=True)
async def leave(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.followup.send("تم إيقاف البوت وخروجه من الروم الصوتي.")
    else:
        await interaction.followup.send("البوت ليس موجوداً في أي روم صوتي حالياً.")

# أمر جديد لمعرفة كم ساعة قضى البوت في الروم بدون أن تضيع أبداً
@bot.tree.command(name="hours", description="يعرض عدد الساعات الإجمالية التي قضاها البوت بالروم")
async def hours_command(interaction: discord.Interaction):
    current_hours = load_hours()
    await interaction.response.send_message(f"⏱️ إجمالي الساعات التي قضاها البوت في الروم الصوتي: **{round(current_hours, 2)}** ساعة.", ephemeral=False)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("عذراً، هذا الأمر مخصص للمسؤولين فقط", ephemeral=True)
    else:
        print(f"خطأ غير متوقع: {error}")

bot.run(os.getenv('TOKEN'))
