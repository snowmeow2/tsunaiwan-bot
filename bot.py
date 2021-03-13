#-*- coding: utf-8 -*-
'''！這是發送粗乃丸圖片的專屬機器人，不要搞混！'''
import random, time, discord, asyncio, traceback, datetime, requests, os
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from discord.ext import commands

prefix = '~'
bot = commands.Bot(command_prefix=prefix)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/22.0'}

#Channel ID
debug_room = '560811425275314176'
general_kitchen = '546573997870022657'
DEG = bot.get_channel(debug_room)

def check_pic():
    f = open('resource/maru_url.txt')
    maru_url = list(f.read().split("\n"))
    maru_url.pop()
    f.close()
    return maru_url

def imgbox_raw(url): 
    req = Request(url=url, headers=headers)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")
        
    images = soup.find_all('img')
    for image in images:
        continue
    img_url = image['src']
    img = requests.get(img_url)
    return img, img_url

#顯示文章功能已停用
'''async def out_mes(text, url, message):
    if len(text)< 2:
        await ctx.send(text[0]+"...")
    elif len(text)< 3:
        await ctx.send(text[0]+"\n"+text[1]+"...")
    elif len(text)< 4:
        await ctx.send(text[0]+"\n"+text[1]+"\n"+text[2]+"...")
    elif len(text)> 4:
        await ctx.send(text[0]+"\n"+text[1]+"\n"+text[2]+"\n"+text[3]+"...")
    if url != None:
        await ctx.send("Check! ===> "+url)'''

@bot.event
async def on_ready():
    embed=discord.Embed(title='**[Bot 重新啟動]**', description='Bot 回歸崗位：\n'+bot.user.name+' 以 '+str(bot.user.id), color=0xfef8ab, timestamp=datetime.datetime.utcfromtimestamp(time.time()))
    embed.add_field(name="粗乃丸存量", value=len(pics), inline=True)
    embed.add_field(name="隨機數", value=ran_num, inline=True)
    embed.set_footer(text="粗乃丸圖庫", icon_url=bot.user.avatar_url)

    await DEG.send(embed=embed)
    await bot.change_presence(game=discord.Game(name="丸")) 

@bot.event
async def on_error(event, *args, **kwargs):	#觸發事件引起的錯誤回饋
    embed=discord.Embed(title='**鋪能丸惹...**', description='詳細除錯資訊已通知 <@362130692311875591>', color=0xfef8ab, timestamp=datetime.datetime.utcfromtimestamp(time.time()))
    embed.add_field(name="類型", value=event, inline=True)
    embed.add_field(name="內容", value=message.content, inline=True)
    embed.set_footer(text="粗乃丸圖庫", icon_url=bot.user.avatar_url)
    await message.channel.send(embed=embed)

    await bot.AppInfo.owner.send("開始回傳錯誤訊息：```\n"+str(traceback.format_exc())+"\n```")

@bot.event
async def on_command_error(ctx, error):	#觸發命令引起的錯誤回饋
    if isinstance(error, commands.CommandNotFound):
        return
    embed=discord.Embed(title='**鋪能丸惹...**', description='詳細除錯資訊已通知 <@362130692311875591>', color=0xfef8ab, timestamp=datetime.datetime.utcfromtimestamp(time.time()))
    embed.add_field(name="類型", value='command', inline=True)
    embed.add_field(name="內容", value=ctx.message.content, inline=True)
    embed.set_footer(text="粗乃丸圖庫", icon_url=bot.user.avatar_url)
    await message.channel.send(embed=embed)
    await bot.AppInfo.owner.send("開始回傳錯誤訊息：```\n"+str(error)+"\n```")

@bot.event
async def on_message(message):
    if message.author == bot.user:	#防止讀取自己的訊息
        return
    await bot.process_commands(message)	#先進行是否為指令的判斷
	
    if message.content == "tttt":	#Debug用
        await message.channel.send(bot.get_channel(a), "Xixixi...")

    if message.content.startswith('!'):	#複製文詢問功能已停用
        if message.content.replace("!", "").replace("?", "") != '':
            await message.channel.send("您好，因使用政策的更動，此聊天機器人不再支援圖庫之外的其他功能，敬請見諒。\n欲查詢已停用之服務列表，請輸入`~disable`；欲查閱使用說明，請輸入`~help`。")
        return
        
    if "丸".encode("utf-8") in message.content.encode("utf-8"):#正在測試圖庫
        img_url = str(pics[random.randint(0,len(pics)-1)])
        img, img_raw_url = imgbox_raw(img_url)

        f = open('maru.png','wb') 
        f.write(img.content)
        f.close()
        
        #await message.channel.send("通通鋪蠢丸！！！:rage:")
        await message.channel.send(file=discord.File('maru.png'))
        await asyncio.sleep(5)
        return
        
@bot.command()
async def stop(ctx, password=0):
    if int(password) == ran_num:
        await bot.logout()
    else:
        await ctx.send("權限不足！:rage:")        

@bot.command()
async def tttt(ctx):
    await ctx.send(bot.get_channel(a), "Xixixi...")

@bot.command()
async def disable(ctx):
    await ctx.send("下列是因使用政策變更而停用的服務清單：```\
    中文翻譯（使用Google Translation）\n\
    Arxiv論文自動索引、摘要翻譯節錄\n\
    Komica綜合版討論串結構分析、文字雲生成\n\
    Komica綜合版討論串 Pick up\n\
    複製文搜尋\n\
    簡易對話、圖片互動\n\
    簡易文字小遊戲\n\
    基於句向量的自動回文演算法（使用Bert中文模型） ```")

bot.remove_command('help')
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="**＜粗乃丸圖庫 Bot＞**", description="這是一隻專門散佈粗乃丸口愛豪丸的聊天機器人。下面是功能清單：", color=0xeee657, timestamp=datetime.datetime.utcfromtimestamp(time.time()))
    
    embed.add_field(name="***丸***", value="開始丸囉！！！", inline=False)
    embed.add_field(name="tttt、~tttt", value="故意引發程式錯誤。", inline=False)
    embed.add_field(name="~stop", value="關閉機器人（僅限管理者使用）。", inline=False)
    embed.add_field(name="~disable", value="顯示機器人停用的服務。", inline=False)
    embed.set_footer(text="粗乃丸圖庫", icon_url=bot.user.avatar_url)
    await ctx.send(embed=embed)
    
    await ctx.send("**<@362130692311875591> https://komicapy.blogspot.com/**")
    return    

ran_num = random.randint(101, 999)
pics = check_pic()
bot.run(os.getenv('DISCORD_TOKEN'))
