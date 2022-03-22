import os, discord
from discord_components import ComponentsBot

import Eventos.On_Member_Join
from Scripts import IsAdmin # Verificar permissões
from Moderacao import Limpar, Mute, Ticket, Role, AutoRole, Comandos
from Eventos import Ready, On_Member_Join, On_Message, On_Raw_Button_Click, On_Raw_Reaction_Add

intents = discord.Intents().all()
bot = ComponentsBot("!", intents=intents)
bot.remove_command('help')

############################################## KEYS ##############################################
#KEY = "SEU BOT TOKEN AQUI" # TOKEN, VOCÊ ENCONTRA ISSO EM DISCORD DEVELOPERS, NA ÁREA BOT. 
##################################################################################################

listaMutados = [] # Lista de usuários listaMutados
ticketIds = {} # IDs das salas & mensagens de ticket dict(guild.id_sala / guild.id_mensagem, guild.id_categoria)
reactionRole = {} # Adicionar cargo por reação dict()
autoRole = {} # Adicionar cargo automaticamente ao entrar no servidor

### EVENTOS ###
@bot.event
async def on_ready():
   await Eventos.Ready.ready(listaMutados, bot, autoRole, reactionRole, ticketIds)

@bot.event
async def on_guild_join(guild):
    status = f"[+] Bot entrou no servidor {guild}"
    print(status)

@bot.event
async def on_guild_remove(guild):
    status = f"[-] Bot foi expulso do servidor {guild}"
    print(status)

@bot.event
async def on_member_join(member):
    await Eventos.On_Member_Join.join(member, bot, autoRole)

@bot.event
async def on_message(ctx):
    await Eventos.On_Message.onmessage(listaMutados, ctx, bot)

@bot.event
async def on_raw_button_click(interaction):
    await Eventos.On_Raw_Button_Click.onrawclick(interaction, bot)

@bot.event
async def on_raw_reaction_add(reaction):
    global ticketIds
    await Eventos.On_Raw_Reaction_Add.reactionadd(bot, reactionRole, reaction, ticketIds)

### COMANDOS ESPECIAIS ###
@bot.command()
async def atualizar(ctx):
    if int(ctx.author.id) == 00000000000: # SUBSTITUA OS 0 PELO SEU ID
        await ctx.message.delete()
        os.system("pip install -r requirements.txt")
        os.system("title Lonely")
        os.system("start main.py")
        os.system("taskkill /fi \"WindowTitle eq Lonely\"")


### COMANDOS PARA USUÁRIOS ###
@bot.command()
async def help(ctx):
    await ctx.channel.send("Use !comandos")

@bot.command()
async def comandos(ctx):
    await Comandos.listar(ctx)


### COMANDOS PARA MODERAÇÃO DO SERVIDOR ###
@bot.command()
async def limpar(ctx, quantidade):
    staff = IsAdmin.verificar(ctx.author)
    await Limpar.Deletar(ctx, quantidade, staff)

@bot.command()
async def autorole(ctx, role: discord.Role):
    staff = IsAdmin.verificar(ctx.author)
    await AutoRole.Setar(ctx, role, staff, autoRole)

@bot.command()
async def role(ctx, mensagem): # Definir mensagem de receber cargo por reação
    print(f"[+] Comando role executado no servidor {ctx.guild}")
    if IsAdmin.verificar(ctx.author) is True:
        await Role.Role.Setar(ctx, mensagem, bot)

@bot.command()
async def roleadd(ctx, role: discord.Role, emoji): # Adicionar emoji ao sistema de receber cargo por reação
    global reactionRole
    print(f"[+] Comando roleadd executado no servidor {ctx.guild}")
    if IsAdmin.verificar(ctx.author) is True:
        reactionRole = await Role.Role.AdicionarEmoji(ctx, role, emoji, bot, reactionRole)


@bot.command()
async def mutar(ctx, infrator: discord.Member, tempo): # Mutar usuário
    global listaMutados
    print(f"[+] Comando mutar executado no servidor {ctx.guild}")
    if IsAdmin.verificar(ctx.author) is True:
        await Mute.Mute.mutar(ctx, infrator.id, tempo, infrator.display_name, listaMutados)

@bot.command()
async def desmutar(ctx, user: discord.Member): #Desmutar o usuário
    global listaMutados
    print(f"[+] Comando desmutar executado no servidor {ctx.guild}")
    if IsAdmin.verificar(ctx.author) is True:
        listaMutados = await Mute.Mute.desmutar(ctx, listaMutados, user)


@bot.command()
async def mutados(ctx): # Listar usuários mutados
    global listaMutados
    print(f"[+] Comando mutados executado no servidor {ctx.guild}")
    if IsAdmin.verificar(ctx.author) is True:
        await Mute.Mute.listarMutados(ctx, listaMutados, bot)

@bot.command()
async def ticket(ctx, MensagemID):
    global ticketIds
    print(f"[+] Comando ticket executado no servidor {ctx.guild}")
    if IsAdmin.verificar(ctx.author) is True:
        CanalID = ctx.channel.id
        ticketIds = await Ticket.Gerar(ctx, CanalID, MensagemID, bot, ticketIds)

############
bot.run(KEY)