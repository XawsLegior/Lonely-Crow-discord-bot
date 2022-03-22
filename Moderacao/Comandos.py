async def listar(ctx):
    print(f"[+] Lista de comandos executada no servidor {ctx.guild}")
    await ctx.channel.send(" Bot desenvolvido por Welson#1110!\n"
                           " Esse código é open source apenas para teste\n"

                           "**Sistema de Mute** \n```"
                           "• !mutar @usuario tempo(m/h - exemplo: 10m) - Muta o usuário por um tempo determinado\n"
                           "• !desmutar @usuario - Desmuta o usuário\n"
                           "• !mutados - Lista os usuários mutados e o tempo ``` \n"

                           "**Sistema de cargo por reação** \n```"
                           "• !role mensagem_id - Cargo por reação, define a mensagem\n"
                           "• !roleadd @cargo emoji - Seta o emoji que da o cargo X ``` \n"

                           "**Outros comandos de moderação** \n```"
                           "• !ticket mensagem_id - Define a mensagem de ticket\n"
                           "• !limpar quantidade - Apaga mensagens sem limite\n"
                           "• !autorole @cargo - Seta o cargo automaticamente ao entrar no servidor ``` \n"
                           "> Caso o sistema de ticket/cargo por reação não esteja funcionando mude o cargo do bot para o topo!")
