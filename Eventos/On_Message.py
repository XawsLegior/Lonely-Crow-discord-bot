from datetime import datetime
import re

async def onmessage(listaMutados, ctx, bot):
    try:
        if ctx.content == "💩":
            mensagem = await ctx.channel.fetch_message(ctx.id)
            await mensagem.delete()
        # Verificar se está mutado
        isMuted = f"{ctx.author.id}/{ctx.guild.id}/"
        index = 0
        # Verificar se está na lista de listaMutados & mutado ainda
        for verif in listaMutados:
            if re.search(fr"{isMuted}", verif):
                infrator = verif.split("/")
                infrator[2] = infrator[2].replace("\n", "")
                if datetime.timestamp(datetime.now()) <= float(infrator[2]):
                    try:
                        mensagem = await ctx.channel.fetch_message(ctx.id)
                        await mensagem.delete()
                    except:
                        pass
                elif datetime.timestamp(datetime.now()) >= float(infrator[2]):
                    listaMutados.pop(index) # Limpar da lista de listaMutados
                    fnew = open("Servidores/mutados.txt", "w+")
                    for user in listaMutados:
                        fnew.write(user)
                    fnew.close()
            index+=1
        await bot.process_commands(ctx)
    except:
        pass