async def join(member, bot, autoRole):
    ### Setar auto role
    try:
        servidor = await bot.fetch_guild(int(member.guild.id))
        role = servidor.get_role(int(autoRole[f"{member.guild.id}"]))
        await member.add_roles(role)
    except:
        pass