import asyncio

import discord

async def Gerar(ctx, CanalID, MensagemID, bot, ticketIds):
    canal = await bot.fetch_channel(CanalID)
    mensagem = await canal.fetch_message(MensagemID)

    embed = discord.Embed(title=ctx.guild.name, color=discord.Color.green())
    embed.add_field(name="Suporte", value=f"{mensagem.content}")
    avatar = bot.user.avatar_url
    embed.set_footer(text="• Desenvolvido por Worrigan Soft •", icon_url=avatar)
    msg = await canal.send(embed=embed)

    # Salvar dados no arquivo
    try:
        linhas = sum(1 for linha in open(f"Servidores/Ticket/{ctx.guild.id}.txt"))  # Contar número de linhas no arquivo
    except:
        linhas = 0

    f = open(f"Servidores/Ticket/{ctx.guild.id}.txt", "w+")
    dados = f"{CanalID}\n{msg.id}\n"
    f.write(dados)
    categoria = 0
    if int(linhas) < 3:
        categoria = await ctx.guild.create_category("Suporte Lonely")
        categoria = categoria.id
    else:
        categoria = discord.utils.get(ctx.guild.categories, name="Suporte Lonely")
        if categoria is None:
            categoria = await ctx.guild.create_category("Suporte Lonely")
            print(categoria)
            categoria = categoria.id
        else:
            categoria = categoria.id
    f.write(str(categoria))
    f.close()

    await msg.add_reaction('✉')
    await ctx.channel.send("Ticket pronto!")

    try:
        ticketIds[f"{ctx.guild.id}_sala"] = CanalID
        ticketIds[f"{ctx.guild.id}_mensagem"] = msg.id
        ticketIds[f"{ctx.guild.id}_categoria"] = categoria
        print(f"[+] Ticket gerado no servidor {ctx.guild}")
        return ticketIds
    except Exception as erro:
        print(f"[!] O seguinte erro ocorreu em {ctx.guild} ao tentar definir o canal de ticket\n{erro}")
        await ctx.channel.send(
            "**Um erro ocorreu, verifique se está fazendo tudo certo e se continuar procure o suporte!**\n"
            "> • Primeiro ID é do canal de texto\n"
            "> • Segundo ID é da mensagem\n"
            "> • A mensagem não pode ter sido escrita por bots.")