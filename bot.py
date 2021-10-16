import discord
from discord.ext import commands, tasks
import random

bot = commands.Bot(command_prefix = "$", description = "le plus fidèle serviteur")

@bot.event
async def on_ready():
   print("ready !")
   changeStatus.start()

@bot.command()
async def bonjour(ctx):
    await ctx.send(f"salut a toi jeune ombre, sais tu pourquoi ce serveur est le meilleur? \n*parce que je suis dedans^^*")
@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    serverDescription = server.description
    numberOfPerson = server.member_count
    serverName = server.name
    message = f"Le serveur **{serverName}** contien *{numberOfPerson}* membres. \nla description du serveur: **{serverDescription}**. \nce serveur propose égualement *{numberOfTextChannels}* salons textuel et *{numberOfVoiceChannels}* salons vocaux"
    await ctx.send(message)

@bot.command()
async def say(ctx,*texte):
    await ctx.send(" ".join(texte))

@bot.command()
async def chinese(ctx, *text):
    chineseChar = "丹书ㄈ力已下呂廾工丿片乚爪ㄇ口尸厶尺ㄎ丁凵人山父了乙"
    chineseText = []
    for word in text:
        for char in word:
            if char.isalpha():
                index = ord(char) - ord("a")
                transformed = chineseChar[index]
                chineseText.append(transformed)
            else:
                chineseText.append(char)
        chineseText.append(" ")
    await ctx.send("".join(chineseText))

@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, nombre : int):
    messages = await ctx.channel.history(limit = nombre + 1).flatten()
    for message in messages:
        await message.delete()

@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason = reason)
    await ctx.send(f"{user} à été kick")

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.ban(user, reason = reason)
    await ctx.send(f"{user} à été ban")

@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    userName, userId = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:
            await ctx.guild.unban(i.user, reason = reason)
            await ctx.send(f"{user} à été débanni")
            return
    await ctx.send(f"L'utilisateur {user} n'est pas ban")

status = ["bonne appétit",
        "A votre service",
        "twitch.tv/sangrioB",
        "sangrioB est mon créateur",
        "vive les tacos",
        "DZ"]
@tasks.loop(minutes = 30)
async def changeStatus():
    game = discord.Game(random.choice(status))
    await bot.change_presence(status = discord.Status.dnd, activity = game)

async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "creation du role muted")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles :
        if role.name == "Muted":
            return role
    return await createMutedRole(ctx)

@bot.command()
@commands.has_permissions(ban_members = True)
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole,reason = reason)
    await ctx.send(f"{member.mention} a été mute !")

@bot.command()
@commands.has_permissions(ban_members = True)
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été démute !")
bot.run("ODk3MTQ2NjU4NTcwMjUyMzA4.YWRa7w.DDCUHCaAlupvqBa79d9dF4CpYcE")