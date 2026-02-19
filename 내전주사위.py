import discord
from discord.ext import commands
import random
import os

# ───── 봇 설정 ─────
intents = discord.Intents.default()
intents.message_content = True  # !명령어 필수
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"로그인 완료: {bot.user}")

# ───── 주사위 명령어 ─────
@bot.command(name="주사위")
async def dice(ctx):

    # ❌ 허용 채널이 아닐 때
    if ctx.channel.name != "내전-주사위":
        warning = await ctx.send(
            "❌ 이 채널에서는 사용 불가입니다.\n"
            "👉 `내전-주사위` 채널에서 사용해주세요."
        )

        # 메시지 삭제는 권한 없으면 에러 날 수 있으니 안전 처리
        try:
            await ctx.message.delete()
        except:
            pass

        # 안내 메시지도 3초 후 자동 삭제 (선택)
        # await warning.delete(delay=3)

        return

    # ✅ 특정 채널에서만 실행
    if ctx.channel.name != "내전-주사위":
        return  # 다른 채널에서는 아무 반응도 안 함

    user_name = ctx.author.display_name
    result = random.randint(1, 6)

    # 절대 경로 (경로 문제 방지)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, "dice_images", f"dice_{result}.png")

    file = discord.File(image_path, filename="dice.png")

    embed = discord.Embed(
        title="🎲 주사위",
        description=f"**{user_name}** 님이 주사위를 굴려 **({result}️⃣)** 이 나왔어요!"
    )
    embed.set_image(url="attachment://dice.png")

    await ctx.send(embed=embed, file=file)

access_token = os.environ["BOT_TOKEN"]
bot.run(access_token)
