#run.py
import discord
from discord.ext import commands
import asyncio
import random
import requests
import os

#봇 접두사 .
bot = commands.Bot(command_prefix='.',intents=discord.Intents.all())

#경고기록을 저장할 리스트
warnings = {}

# 벤 목록을 저장할 리스트
banned_members = []

# 각 사용자의 돈을 저장할 딕셔너리
user_balances = {}

# 딕셔너리를 사용하여 정보를 저장합니다.
learning_dict = {}

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name=".명령어"))

@bot.event
async def on_message(msg):
    if msg.author.bot:
        return

    # 사용자의 잔고가 없으면 초기화
    if msg.author.id not in user_balances:
        user_balances[msg.author.id] = 100  # 초기 잔고: 100

    await bot.process_commands(msg)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot)) #봇이 실행되면 콘솔창에 표시

@bot.event
async def on_ready():

  
    await bot.change_presence(activity=discord.Game(name=".명령어"))

@bot.event
async def on_message(msg):
    if msg.author.bot: return None
    await bot.process_commands(msg)

@bot.command()
async def 명령어(ctx):
    command_list = """
    **명령어 목록:**
    1. .청소 [지울_갯수] - 메시지를 삭제합니다.
    2. .경고 [사용자멘션] - 경고 1개를 부여합니다.
    3. .경고취소 [사용자멘션] - 경고를 1개 삭제합니다.
    4. .경고확인 [사용자멘션] - 사용자의 경고수를 보여줍니다.
    5. .벤 [사용자멘션] - 사용자를 벤합니다.
    6. .벤취소 [사용자멘션] - 사용자 벤을 취소합니다.
    7. .벤목록 - 벤 목록을 보여줍니다.
    8. .play [제목] - 노래를 재생합니다.
    9. .leave - 봇이 음성 채팅을 나갑니다.
    10. .skip - 노래를 스킵합니다.
    11. .스킵 - 현재 재생중인 곡을 스킵합니다.
    12. .도박 [금액] - 돈을 걸고 도박을 합니다.
    13. .내돈 - 자신의 돈을 보여줍니다.
    14. .가바보 - 가위바위보를 돈을 걸고 합니다.
    15. .로또 [숫자] - 로또를 합니다.
    16. .송금 [멘션] [금액] - 상대방에게 송금을 합니다.
    17. .로블검색 [유저명] - 로블록스 캐릭터를 조회합니다.
    18. .배워 [키워드] [내용] - 봇에게 말을 가르칩니다.
    19. .알려 [키워드] - 저장된 말을 말합니다.
    """
    await ctx.send(command_list)


@bot.command()
async def 조까(ctx):
    await ctx.channel.send('어떻게 그런말을..ㅠ')

async def 씨발(ctx):
    await ctx.channel.send('ㅁ..ㅁ.뭐라구요?')


@bot.command()
async def 청소(ctx, amount : int):
    await ctx.channel.purge(limit=amount)

@bot.command()
async def 경고(ctx, member: discord.Member, *, reason=""):
    if ctx.message.author.guild_permissions.administrator:
        if member.id not in warnings:
            warnings[member.id] = 0
        warnings[member.id] += 1
        await ctx.send(f"{member.mention}님에게 경고를 부여했습니다. 이유: {reason}")
    else:
        await ctx.send("권한이 없습니다.")

# !unwarn 명령어: 사용자의 경고 취소
@bot.command()
async def 경고취소(ctx, member: discord.Member, *, reason=""):
    if ctx.message.author.guild_permissions.administrator:
        if member.id in warnings and warnings[member.id] > 0:
            warnings[member.id] -= 1
            await ctx.send(f"{member.mention}님의 경고를 취소했습니다.")
        else:
            await ctx.send(f"{member.mention}님의 경고가 없습니다.")
    else:
        await ctx.send("권한이 없습니다.")

# !warnings 명령어: 사용자의 경고 확인
@bot.command()
async def 경고확인(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.administrator:
        if member.id in warnings:
            await ctx.send(f"{member.mention}님의 경고 횟수: {warnings[member.id]}")
        else:
            await ctx.send(f"{member.mention}님의 경고가 없습니다.")
    else:
        await ctx.send("권한이 없습니다.")

# !ban 명령어: 사용자를 벤
@bot.command()
async def 벤(ctx, member: discord.Member, *, reason=""):
    if ctx.message.author.guild_permissions.administrator:
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention}님을 벤했습니다. 이유: {reason}")
    else:
        await ctx.send("권한이 없습니다.")  

        # !unban 명령어: 사용자의 벤 해제
@bot.command()
async def 벤취소(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.administrator:
        if member in banned_members:
            banned_members.remove(member)
            await member.unban()
            await ctx.send(f"{member.mention}님의 벤을 해제했습니다.")
        else:
            await ctx.send(f"{member.mention}님은 벤되지 않았습니다.")
    else:
        await ctx.send("권한이 없습니다.")  

# !bans 명령어: 벤된 사용자 목록 확인
@bot.command()
async def 벤목록(ctx):
    if ctx.message.author.guild_permissions.administrator:
        if banned_members:
            banned_list = "\n".join([member.name for member in banned_members])
            await ctx.send(f"벤된 사용자 목록:\n{banned_list}")
        else:
            await ctx.send("벤된 사용자가 없습니다.")
    else:
        await ctx.send("권한이 없습니다.")

@bot.command()
async def 도박(ctx, amount: int):
    if amount <= 0:
        await ctx.send("금액은 0보다 커야 합니다.")
        return

    if amount > user_balances[ctx.author.id]:
        await ctx.send("돈이 부족합니다.")
        return

    outcome = random.choice(['win', 'lose'])
    if outcome == 'win':
        user_balances[ctx.author.id] += amount
        await ctx.send(f'{ctx.author.mention}, 도박에 이겼습니다! 현재 잔고: {user_balances[ctx.author.id]}')
    else:
        user_balances[ctx.author.id] -= amount
        await ctx.send(f'{ctx.author.mention}, 도박에 졌습니다... 현재 잔고: {user_balances[ctx.author.id]}')

@bot.command()
async def 내돈(ctx):
    await ctx.send(f'{ctx.author.mention}, 현재 잔고: {user_balances.get(ctx.author.id, 0)}')

@bot.command()
async def 가바보(ctx, choice: str):
    if choice not in ['가위', '바위', '보']:
        await ctx.send("가위, 바위, 보 중에서 선택해주세요.")
        return

    if user_balances[ctx.author.id] <= 0:
        await ctx.send("돈이 부족합니다.")
        return

    computer_choice = random.choice(['가위', '바위', '보'])

    result = ""

    if choice == computer_choice:
        result = "무승부"
    elif (choice == '가위' and computer_choice == '보') or \
         (choice == '바위' and computer_choice == '가위') or \
         (choice == '보' and computer_choice == '바위'):
        user_balances[ctx.author.id] *= 2
        result = "이겼습니다!"
    else:
        user_balances[ctx.author.id] = user_balances[ctx.author.id] // 2
        result = "졌습니다..."

    await ctx.send(f'당신: {choice}, 컴퓨터: {computer_choice}. {result} 현재 잔고: {user_balances[ctx.author.id]}')

@bot.command()
async def 로또(ctx, number: int):
    if number <= 0 or number > 10:
        await ctx.send("1부터 10까지의 숫자를 선택해주세요.")
        return

    if user_balances[ctx.author.id] <= 0:
        await ctx.send("돈이 부족합니다.")
        return

    # 랜덤 로또 번호 생성
    lotto_number = random.randint(1, 10)

    if number == lotto_number:
        user_balances[ctx.author.id] *= 2
        await ctx.send(f'로또 번호는 {lotto_number}입니다. 일치하여 돈이 2배로 증가했습니다! 현재 잔고: {user_balances[ctx.author.id]}')
    else:
        user_balances[ctx.author.id] = user_balances[ctx.author.id] // 2
        await ctx.send(f'로또 번호는 {lotto_number}입니다. 일치하지 않아 돈이 반으로 감소했습니다... 현재 잔고: {user_balances[ctx.author.id]}')

@bot.command()
async def 송금(ctx, member: discord.Member, amount: int):
    if amount <= 0:
        await ctx.send("금액은 0보다 커야 합니다.")
        return
    
@bot.command()
async def 돈줘(ctx):
    amount = 1000
    user_balances[ctx.author.id] += amount
    await ctx.send(f'{ctx.author.mention}, {amount}원을 받았습니다! 현재 잔고: {user_balances[ctx.author.id]}')

@bot.command()
async def 로블검색(ctx, username):
    try:
        url = f'https://api.roblox.com/users/get-by-username?username={username}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if 'Id' in data:
                user_id = data['Id']
                profile_url = f'https://www.roblox.com/users/{user_id}/profile'
                character_url = f'https://www.roblox.com/Thumbs/Avatar.ashx?x=100&y=100&username={username}'
                await ctx.send(f"**{username}**님의 프로필: {profile_url}\n캐릭터 이미지: {character_url}")
            else:
                await ctx.send("해당 사용자를 찾을 수 없습니다.")
        else:
            await ctx.send("API에서 데이터를 검색하는 중 오류가 발생했습니다.")

    except Exception as e:
        await ctx.send(f"캐릭터를 검색하는 중 오류가 발생했습니다: {e}")

@bot.command()
async def 배워(ctx, keyword, *, content):
    # 사용자가 입력한 키워드와 내용을 딕셔너리에 저장합니다.
    learning_dict[keyword] = content
    await ctx.send(f"'{keyword}'에 대한 정보를 배웠어요!")

@bot.command()
async def 알려(ctx, keyword):
    # 딕셔너리에서 해당 키워드에 대한 내용을 찾고 전송합니다.
    if keyword in learning_dict:
        await ctx.send(f"'{keyword}'에 대한 정보: {learning_dict[keyword]}")
    else:
        await ctx.send(f"'{keyword}'에 대한 정보를 찾을 수 없어요.")

# 봇 실행

access_token = os.environ["BOT_TOKEN"]
bot.run(access_token) #토큰
