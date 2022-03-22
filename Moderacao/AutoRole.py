async def Setar(ctx, role, staff, autoRole):
    print(f"[+] Comando autorole executado no servidor {ctx.guild}")
    if staff is True:
        try:
            f = open(f"Servidores/Roles/{ctx.guild.id}_auto", "w")
            f.write(str(role.id))
            f.close()
            autoRole[f"{ctx.guild.id}"] = str(role.id)
            await ctx.channel.send("Auto role setado com sucesso!")
        except:
            return False
