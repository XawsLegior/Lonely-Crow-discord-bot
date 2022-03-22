import discord

async def ready(listaMutados, bot, autoRole, reactionRole, ticketIds):
    print("[+] Bot online")
    ### Carregar usuários listaMutados ###
    try:
        f = open("Servidores/mutados.txt", "r")
        for mutado in f:
            listaMutados.append(mutado)
        f.close()
    except:
        open("Servidores/mutados.txt", "w").close()
        print("[+] Arquivo de usuários listaMutados gerado com sucesso.")

    for guild in bot.guilds:
        ### Carregar auto role
        try:
            autoRole[f"{guild.id}"] = open(f"Servidores/Roles/{guild.id}_auto", "r").read()
        except:
            pass
        ### Carregar cargos por reação
        try:
            print(f"[+] Bot ficou online no servidor {guild}")
            f = open(f"Servidores/Roles/{guild.id}.txt", "r+")
            mensagemID = 0
            for index, item in enumerate(f):
                if index == 0:
                    item = item.split("/")
                    item = item[1]
                    mensagemID = item
                elif index > 0 and item is not None:
                    item = item.split("/")
                    role = item[1]  # cargo
                    item = item[0]  # reação
                    reactionRole[f'{guild.id}_{item}'] = role
                    reactionRole[f'{guild.id}_mensagem'] = mensagemID
        except:
            pass
    ### Carregar lista de tickets (sala e mensagens - ids)
    for guild in bot.guilds:
        try:
            f = open(f"Servidores/Ticket/{guild.id}.txt", "r+")
            linhas = sum(1 for linha in open(f"Servidores/Ticket/{guild.id}.txt"))  # Contar número de linhas no arquivo

            categoria = 0
            for index, id in enumerate(f):
                id = id.replace("\n", "")
                if index == 0:
                    ticketIds[f"{guild.id}_sala"] = id
                elif index == 1:
                    ticketIds[f"{guild.id}_mensagem"] = id
                    if int(linhas) < 3:
                        if discord.utils.get(guild.categories, name="Suporte Lonely") is None:
                            categoria = await guild.create_category("Suporte Lonely")
                            f.write(str(categoria.id))
                            ticketIds[f"{guild.id}_categoria"] = categoria.id
                else:
                    ticketIds[f"{guild.id}_categoria"] = id
                    print(f"[+] Ticket do servidor {guild} carregado.")
            f.close()
        except:
            pass