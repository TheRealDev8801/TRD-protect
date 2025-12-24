import discord
from discord.ext import commands
import sqlite3
import datetime
import os
import sys
import re

# ==========================================
# CONFIGURATION CLOUD-NATIVE
# ==========================================
# On récupère le Token via les variables d'environnement de Koyeb
TOKEN = os.getenv('DISCORD_TOKEN') 
PREFIX = "+" 
OWNER_ID = 1139568990943985694 
VERSION = "V12.0-CLOUD"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# ==========================================
# BASE DE DONNÉES (Auto-initialisation)
# ==========================================
def init_db():
    conn = sqlite3.connect('therealdev_master.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS global_stats (key TEXT PRIMARY KEY, value INTEGER)''')
    c.execute("INSERT OR IGNORE INTO global_stats VALUES ('attacks_blocked', 0)")
    c.execute('''CREATE TABLE IF NOT EXISTS log_channels (guild_id TEXT PRIMARY KEY, chan_id TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ==========================================
# COMMANDES DE PRESTIGE
# ==========================================
@bot.event
async def on_ready():
    bot.start_time = datetime.datetime.now()
    await bot.change_presence(activity=discord.Streaming(name="ULTRAOS CLOUD 🇫🇷", url="https://twitch.tv/therealdev"))
    print(f"Souverain {OWNER_ID} connecté sur l'infrastructure Cloud.")

@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(title="🛡️ THE REAL DEV-PROTECT CLOUD", color=0x00ffcc)
    embed.add_field(name="🛠️ SÉCURITÉ", value=f"`{PREFIX}setup-automod`\n`{PREFIX}log-setup`", inline=True)
    embed.add_field(name="📊 RÉSEAU", value=f"`{PREFIX}global-status`\n`{PREFIX}info`", inline=True)
    if ctx.author.id == OWNER_ID:
        embed.add_field(name="👑 SOUVERAIN", value=f"`{PREFIX}restart`\n`{PREFIX}maintenance`", inline=False)
    embed.set_footer(text=f"Propulsé par UltraOS | Version {VERSION}")
    await ctx.send(embed=embed)

@bot.command(name="global-status")
async def global_status(ctx):
    if ctx.author.id != OWNER_ID: return
    conn = sqlite3.connect('therealdev_master.db')
    c = conn.cursor()
    c.execute("SELECT value FROM global_stats WHERE key='attacks_blocked'")
    blocked = c.fetchone()[0]
    conn.close()
    
    uptime = str(datetime.datetime.now() - bot.start_time).split('.')[0]
    embed = discord.Embed(title="🌍 MONITORING MONDIAL", color=0x00ffcc)
    embed.add_field(name="📡 État", value="`ONLINE (CLOUD)`", inline=True)
    embed.add_field(name="⚔️ Blocs", value=f"`{blocked}`", inline=True)
    embed.add_field(name="⏳ Uptime", value=f"`{uptime}`", inline=True)
    await ctx.send(embed=embed)

# ==========================================
# LOGIQUE AUTOMOD
# ==========================================
@bot.command(name="setup-automod")
@commands.has_permissions(administrator=True)
async def setup_automod(ctx):
    try:
        await ctx.guild.create_automod_rule(
            name="TRD-Protect Cloud Shield",
            event_type=discord.AutoModRuleEventType.message_send,
            trigger_metadata=discord.AutoModTriggerMetadata(keyword_filter=["*nitro*", "*gift*", "bit.ly*"]),
            actions=[discord.AutoModRuleAction(type=discord.AutoModRuleActionType.block_message)],
            enabled=True
        )
        await ctx.send("✅ **Bouclier Cloud activé.**")
    except Exception as e: await ctx.send(f"❌ Erreur : {e}")

# Lancement
if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("ERREUR : DISCORD_TOKEN manquant dans les variables d'environnement.")
