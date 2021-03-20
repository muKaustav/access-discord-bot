import discord
from discord.ext import commands, tasks
from discord.utils import get
import os

intents = discord.Intents.all()
client = commands.Bot(command_prefix="--", intents=intents)
#client = commands.Bot(command_prefix="--")


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

        # movieEmbed.add_field()

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
    # takenGuild = ctx.message.channel.guild
    global category
    category = client.get_channel(809286493272801290)
    # category = ctx.message.channel.category

    myEmbed = discord.Embed(
        title="CREATE A NEW PROJECT", color=0xff3838)
    myEmbed.add_field(name="1. Enter project name:",
                      value="EG: test-bot", inline=False)
    # myEmbed.add_field(name="Enter deadline:",
    #                 value="EG: 12/02/21", inline=False)
    myEmbed.add_field(name="2. React on the embed for roles:",
                      value="React with ✅ to gain access to isolated Text channel and VC.", inline=False)
    myEmbed.add_field(name="WARNING ⛔️",
                      value="PLEASE DON'T REACT ON PROJECTS YOU'RE NOT A PART OF.", inline=False)
    myEmbed.set_footer(text="Made with ❤️ by Kaustav M.")

    msg = await ctx.send(embed=myEmbed)
    await msg.add_reaction('✅')

    global reaction_message_id
    reaction_message_id = str(msg.id)

    project_name = []
    # project_deadline = []
    # project_users = []

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for("message", timeout=60.0, check=check)
    inputs = msg.content.split()

    project_name.append(inputs[0])
    global x
    x = inputs[0]
    # project_deadline.append(inputs[1])
    # # y = inputs[0]
    # project_users.append(inputs[2])
    # z = inputs[0]

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
