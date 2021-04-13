import discord
from discord.ext import commands, tasks
from discord.utils import get
import pandas as pd
import os
from bs4 import BeautifulSoup
import requests

intents = discord.Intents.all()
client = commands.Bot(command_prefix="--", intents=intents)


@client.command(name='e')
async def pepe(ctx, arg1):

    url = "https://raw.githubusercontent.com/muKaustav/access-discord-bot/main/emoji.csv"
    df = pd.read_csv(url, sep=",")

    for line in df['SRC']:
        if str(arg1).lower() in line.lower():
            x = line.split(",")
            await ctx.send(x[0])
            break


@client.command(name='count')
async def count(ctx, role: discord.Role):

    depths = [[] for i in range(5)]
    n = 0
    for member in role.members:
        if n <= 100:
            depths[0].append(str(member))
        elif n <= 200:
            depths[1].append(str(member))
        elif n <= 300:
            depths[2].append(str(member))
        elif n <= 200:
            depths[3].append(str(member))
        elif n <= 300:
            depths[4].append(str(member))
        n += 1

    await ctx.send("List: ")

    for i in depths:
        if len(i) != 0:
            await ctx.send(i)

    await ctx.send("Number of users: " + str(n))


@client.command(name="recc")
async def recc(ctx, arg1):

    if arg1 == "short":
        source = source = requests.get(
            f'https://www.imdb.com/search/title/?genres=short&title_type=feature&explore=genres').text
    elif arg1 == "noir":
        source = source = requests.get(
            f'https://www.imdb.com/search/title/?genres=film-noir&title_type=feature&explore=genres').text
    else:
        source = requests.get(
            f'https://www.imdb.com/search/title/?genres={arg1.lower()}&title_type=feature&explore=genres').text

    soup = BeautifulSoup(source, 'lxml')

    global movies_names, movie_title, img_src

    movies_names = []
    movie_title = []
    img_src = []

    for item in soup.find_all('div', class_='lister-item-content'):
        movies_names.append(item.find('a').text)

    for movie in soup.find_all('h3', class_="lister-item-header"):
        for title in movie.find_all('a', href=True):
            movie_title.append(title['href'].split("/")[2])

    for i in range(5):

        img_source = requests.get(
            f'https://www.imdb.com/title/{movie_title[i]}/?ref_=adv_li_i').text

        img_soup = BeautifulSoup(img_source, 'html.parser')

        for image in img_soup.find_all('div', class_="poster"):
            img_src.append(image.find('img')['src'])

    global reccEmbed

    for k in range(5):

        reccEmbed = discord.Embed(
            title=f"TOP 5 RECENT\nRECCOMENDATIONS\nFOR {arg1.upper()} FROM IMDB",
            color=15158332
        )

        reccEmbed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/812229820938453022/822813081499467826/Untitled-1.png")

        reccEmbed.set_image(
            url=img_src[k]
        )

        reccEmbed.set_footer(text="KIIT FILM SOCIETY")

        reccEmbed.add_field(
            name=str(k+1) + ". " + movies_names[k], value="Give it a watch!", inline=False)

        await ctx.send(embed=reccEmbed)


@client.command(name='embed')
async def embed(ctx, arg1, arg2, arg3, arg4, arg5):
    if arg1 == "movie":

        movieEmbed = discord.Embed(
            title="MOVIE NIGHT  🎬",
            color=15844367
        )

        movieEmbed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/812229820938453022/822813081499467826/Untitled-1.png")

        movieEmbed.set_image(
            url=f"{arg5}"
        )

        movieEmbed.set_footer(text="KIIT FILM SOCIETY")

        movieEmbed.add_field(
            name=f"Tonight we're watching {arg2}!", value=f"Directed by {arg3}.", inline=False)

        movieEmbed.add_field(
            name="Hoping to see all of you there!", value=f"@ {arg4}!", inline=False)

    await ctx.send(embed=movieEmbed)


@client.command(name='version')
async def version(ctx):
    myEmbed = discord.Embed(title="Current Version",
                            description="The bot is in v1.2", color=0xff3838)
    myEmbed.add_field(name="Version Code", value="v1.2.1", inline=False)
    myEmbed.add_field(name="Last Update",
                      value="20/03/2021", inline=False)
    myEmbed.add_field(name="Date Released",
                      value="11/02/2021", inline=False)
    myEmbed.set_footer(text="Made with ❤️ by Kaustav M.")

    await ctx.message.channel.send(embed=myEmbed)


@client.command(name='get_data')
async def get_data(ctx):
    data = ctx.guild.members
    for i in data:
        await ctx.message.channel.send(i)


@client.command(name='project')
async def project(ctx):
    global takenGuild
    takenGuild = client.get_guild(809275451322269728)

    global category
    category = client.get_channel(809286493272801290)

    myEmbed = discord.Embed(
        title="CREATE A NEW PROJECT", color=0xff3838)
    myEmbed.add_field(name="1. Enter project name:",
                      value="EG: test-bot", inline=False)

    myEmbed.add_field(name="2. React on the embed for roles:",
                      value="React with ✅ to gain access to isolated Text channel and VC.", inline=False)
    myEmbed.add_field(name="WARNING ⛔️",
                      value="PLEASE DON'T REACT ON PROJECTS YOU'RE NOT A PART OF.", inline=False)
    myEmbed.set_footer(text="Made with ❤️ by Kaustav M.")

    msg = await ctx.send(embed=myEmbed, delete_after=60.0)
    await msg.add_reaction('✅')

    global reaction_message_id
    reaction_message_id = str(msg.id)

    project_name = []

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for("message", timeout=60.0, check=check)
    inputs = msg.content.split()

    project_name.append(inputs[0])
    global x
    x = inputs[0]

    await takenGuild.create_role(name=x)
    new_role = get(ctx.guild.roles, name=x)
    overwrites = {
        takenGuild.default_role: discord.PermissionOverwrite(read_messages=False),
        takenGuild.me: discord.PermissionOverwrite(read_messages=True),
        new_role: discord.PermissionOverwrite(read_messages=True)
    }
    await takenGuild.create_text_channel(x, overwrites=overwrites, category=category)

    overwrites2 = {
        takenGuild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
        takenGuild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        new_role: discord.PermissionOverwrite(
            read_messages=True, send_messages=True)
    }
    await takenGuild.create_voice_channel(x, overwrites=overwrites2, category=category)


@client.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        message = reaction.message
        if str(message.id) == reaction_message_id:
            if reaction.emoji == '✅':
                pvt_role = discord.utils.get(user.guild.roles, name=x)
                await user.add_roles(pvt_role)

    # Bot status set (online, offline, DND)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("--help"))


client.run(os.environ['DISCORD_TOKEN'])
