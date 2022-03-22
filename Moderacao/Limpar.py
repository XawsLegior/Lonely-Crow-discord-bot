import discord
async def Deletar(ctx, quantidade, staff):
    print(f"[+] Comando limpar executado no servidor {ctx.guild}")
    if staff is True:
        if int(quantidade) <= 1:
            return await ctx.channel.send("Mínimo de 2 mensagens para apagar, não seja preguiçoso.")
    await ctx.channel.purge(limit=int(quantidade)+1)
    await ctx.channel.send("%s mensagens foram removidas!" % quantidade)
    print(f"[+] {quantidade} mensagens foram removidas por {ctx.author} no servidor {ctx.guild}")