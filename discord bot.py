import discord
import psutil
from discord.ext import commands
from datetime import datetime

token = 'Your_token'

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='하이 박스비 ', intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name}이(가) 성공적으로 봇이 실행되었습니다.')

@client.command()
async def 테스트(ctx):
    await ctx.send("성공!!")

@client.command()
async def 초대(ctx):
    await ctx.send("https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot")

@client.command()
async def 핑(ctx):
    Latency = round(client.latency * 1000)
    Ping = f'{str(Latency)}ms'

    if Latency <= 200:
        status = '매우 좋음'
        status_color = 0x0100ff
        status_emogi = '@(^v^)@'
    elif 200 < Latency <= 400:
        status = '좋음'
        status_color = 0x1ddb16
        status_emogi = '(^o^)'
    elif 400 < Latency <= 600:
        status = '나쁨'
        status_color = 0xffe400
        status_emogi = '(-_-);;'
    else:
        status = '매우 나쁨'
        status_color = 0xff0000
        status_emogi = '(╯°□°）╯︵ ┻━┻'

    cpu = psutil.cpu_freq()
    cpu_current_ghz = round(cpu.current / 1000, 2)
    cpu_p = psutil.cpu_percent(interval=1)
    cpu_core = psutil.cpu_count(logical=False)
    
    memory = psutil.virtual_memory()
    memory_total = round(memory.total / 1024**3)
    memory_avail = round(memory.available/1024**3, 1)

    embed = discord.Embed(title='봇 지연 시간(핑)', color=status_color)
    embed.add_field(name="핑(레이턴시)", value=Ping, inline=False)
    embed.add_field(name='봇 상태', value=status, inline=False)
    embed.add_field(name='CPU 속도', value=str(cpu_current_ghz) + "GHz", inline=True)
    embed.add_field(name='CPU 사용량', value=str(cpu_p) + "%", inline=True)
    embed.add_field(name='CPU 코어 개수', value=str(cpu_core) + "개", inline=True)
    embed.add_field(name='총 메모리 용량', value=str(memory_total) + "GB", inline=True)
    embed.add_field(name='사용 가능한 메모리 용량', value=str(memory_avail) + "GB", inline=True)
    embed.set_footer(text=status_emogi)
    await ctx.send(embed=embed)

@client.command()
async def 날씨등록(ctx, 날씨: str):
    if 날씨 in ['맑음', '흐림', '비']:
        now = datetime.now()
        today_date = f"{now.year}/{now.month}/{now.day}"
        weather_dict = {'맑음': 'clean', '흐림': 'cloudy', '비': 'rain'}
        날씨_영문 = weather_dict[날씨]
        with open("weather_status.csv", "r+") as weather_file:
            lines = weather_file.readlines()
            last_line = lines[-1].strip()
            if last_line != "":
                weather_file.write("\n")
            weather_file.write(f"{today_date},{날씨_영문}")
        await ctx.send("성공적으로 오늘의 날씨 정보를 저장했습니다.")
        await ctx.send(f"```날짜 : {today_date}, 날씨 : {날씨_영문}```")
    else:
        await ctx.send("```하이 박스비 날씨등록 ([맑음, 흐림, 비] 중 하나를 입력하세요.)```")

client.run(token)
