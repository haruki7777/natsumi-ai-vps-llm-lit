import os
import aiohttp
import discord
from discord import app_commands

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
NATSUMI_API_URL = os.getenv("NATSUMI_API_URL", "http://127.0.0.1:7860").rstrip("/")

if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN 환경변수를 넣어줘.")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

async def ask_natsumi(user_id: str, message: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{NATSUMI_API_URL}/assistant",
            json={"user_id": user_id, "message": message},
            timeout=aiohttp.ClientTimeout(total=90),
        ) as resp:
            if resp.status < 200 or resp.status >= 300:
                return f"AI 서버 오류야: {resp.status} 😿"
            data = await resp.json()
            return data.get("reply") or "답변이 비었어 😾"

@tree.command(name="나츠미", description="나츠미 AI에게 물어봅니다.")
@app_commands.describe(메시지="예: 서울 한강 온도는 어때")
async def natsumi_command(interaction: discord.Interaction, 메시지: str):
    await interaction.response.defer()
    try:
        reply = await ask_natsumi(str(interaction.user.id), 메시지)
        await interaction.followup.send(reply[:2000])
    except Exception as e:
        print(e)
        await interaction.followup.send("나츠미 AI 서버랑 연결이 안 돼 😿")

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")

client.run(DISCORD_TOKEN)
