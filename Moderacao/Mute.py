import re
from datetime import datetime

import discord


class Mute:
    async def mutar(ctx, infrator, tempo, infratorNome, listaMutados):
        tipo = str()
        if re.search("h", tempo):
            tempo = tempo.split("h")[0]
            tipo = "hora"
        elif re.search("m", tempo):
            tempo = tempo.split("m")[0]
            tipo = "minuto"
        else:
            return await ctx.channel.send(
                "**Uso correto: !mutar @usuário tempo**\n> O tempo deve ser informado com número seguido "
                "do tipo\n> m para minutos e h para horas, exemplo:\n!mutar @Xaws Legior 1h")

        ### Tratar tempo
        tempoAtual = datetime.timestamp(datetime.now())
        if tipo == "minuto":
            tempoMutado = tempoAtual + (int(tempo) * 60)
        elif tipo == "hora":
            tempoMutado = tempoAtual + (int(tempo) * 3600)

        ### SALVAR MUTE
        try:
            dados = f"{infrator}/{ctx.guild.id}/{tempoMutado}\n"
            f = open("Servidores/mutados.txt", "a+")
            f.write(dados)
            f.close()

            #LIMPAR E SALVAR NOVA LISTA
            try:
                listaMutados.clear()
            except:
                pass
            f = open("Servidores/mutados.txt", "r")
            for mutado in f:
                listaMutados.append(mutado)
            f.close()
            await ctx.channel.send(f"O staff <@{ctx.author.id}> mutou o usuário <@{infrator}> por {tempo} {tipo}(s)")
        except Exception as erro:
            print(f"[!] O seguinte erro ocorreu em {ctx.guild} ao tentar mutar um usuário\n{erro}")
            await ctx.channel.send("Erro ao mutar o usuário, caso persista contate o desenvolvedor!")


    async def desmutar(ctx, listaMutados, user):
        try:
            servidor = ctx.guild.id
            listaMutados = filter(None, [re.sub(fr"{user.id}/{servidor}[\/\d.]+", "\0", i) for i in listaMutados])
            listaMutados = list(listaMutados)
            f = open("Servidores/mutados.txt", "w")
            for mutado in listaMutados:
                if str(mutado) != "\x00\n":
                    f.write(str(mutado))
            f.close()
            await ctx.channel.send(f"O staff <@{ctx.author.id}> desmutou <@{user.id}>")
            return listaMutados
        except Exception as e:
            print(f"[!] O seguinte erro ocorreu em {ctx.guild} ao tentar desmutar um usuário\n{e}")
            pass

    async def listarMutados(ctx, listaMutados, bot):
        isMuted = f"{ctx.guild.id}/"

        # Verificar se está na lista de listaMutados & mutado ainda
        embedlistaMutados = discord.Embed(title="**Usuários Mutados**", color=0x0703fc)
        embedlistaMutados.set_thumbnail(url=bot.user.avatar_url)
        for verif2 in listaMutados:
            if re.search(f"{isMuted}", verif2):
                infrator = verif2.split("/")
                infrator[2] = infrator[2].replace("\n", "")
                if datetime.timestamp(datetime.now()) <= float(infrator[2]):
                    try:
                        usuario = await bot.fetch_user(int(infrator[0]))
                        mutadoAte = datetime.fromtimestamp(float(infrator[2]))
                        embedlistaMutados.add_field(name=f"{usuario}", value=f"{mutadoAte}", inline=False)
                    except Exception as erro:
                        print(f"[!] Ocorreu o seguinte erro no servidor {ctx.guild} • {erro}")
        embedlistaMutados.set_footer(text=f"Comando executado por • {ctx.author}")
        await ctx.channel.send(embed=embedlistaMutados)