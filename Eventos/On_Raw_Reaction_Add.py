from discord_components import Button, ButtonStyle
import re, discord

async def reactionadd(bot, reactionRole, reaction, ticketIds):
    try:
        user = await bot.fetch_user(reaction.user_id)
        ### SISTEMA DE CARGO POR REAÇÃO
        try:
            mensagemID = reactionRole[f'{reaction.guild_id}_mensagem']
            mensagemID = ticketIds[f'{reaction.guild_id}_mensagem']

            if int(reaction.message_id) == int(mensagemID) and user.bot is False:
                servidor = await bot.fetch_guild(reaction.guild_id)
                user = reaction.member
                emoji = str(reaction.emoji).encode()
                roleID = reactionRole[f'{reaction.guild_id}_{emoji}']
                role = servidor.get_role(int(roleID))

                if role in user.roles: # Checar se já tem o cargo e remover
                    await user.remove_roles(role)
                else: # Caso não tenha adicionar
                    await user.add_roles(role)

                # Remover reação
                canal = await bot.fetch_channel(reaction.channel_id)
                mensagem = await canal.fetch_message(reaction.message_id)
                await mensagem.remove_reaction(reaction.emoji, user)
                return
        except:
            pass

        ### SISTEMA DE TICKET
        # Fechar ticket
        if str(reaction.emoji) == '🔒':
            userName = str(user).replace("#", "").lower()
            userSala = await bot.fetch_channel(reaction.channel_id)
            categoriaID = userSala.category.id
            servidor = await bot.fetch_guild(reaction.guild_id)
            #if str(userSala) == userName and int(categoriaID) == int(ticketIds[f"{reaction.guild_id}_categoria"]):
            if user.bot is False and int(categoriaID) == int(ticketIds[f"{reaction.guild_id}_categoria"]):
                await userSala.set_permissions(user, view_channel=False)
                await userSala.edit(name="Ticket fechado.")
                await userSala.send(content=f"\n**Suporte fechado por {user}**\n", components=[Button(style=ButtonStyle.red, label="Deletar Sala", custom_id="button")])
                print(f"[+] Suporte fechado por {user} no servidor {servidor}")

        # Checar se a reação é na mensagem de ticket
        if int(ticketIds[f'{reaction.guild_id}_mensagem']) == int(reaction.message_id):
            canal = await bot.fetch_channel(reaction.channel_id)
            mensagem = await canal.fetch_message(reaction.message_id)
            await mensagem.remove_reaction(reaction.emoji, user)

            # Checar se o usuário já tem um suporte aberto
            guild = await bot.fetch_guild(reaction.guild_id)
            categoria = ticketIds[f"{reaction.guild_id}_categoria"]
            #tratar nome do usuário
            userSala = re.sub(r"[^\w]", "", str(user)).lower()
            if discord.utils.get(bot.get_all_channels(), name=f"{userSala}"):
                return
            else:
                # Criar sala de suporte pro usuário
                categoria = await bot.fetch_channel(categoria)
                ticketSala = await categoria.create_text_channel(f"{userSala}")
                await ticketSala.set_permissions(guild.default_role, view_channel=False)
                await ticketSala.set_permissions(user, read_messages=True, send_messages=True, add_reactions=True,
                                                 view_channel=True, embed_links=True, attach_files=True, read_message_history=True)
                msg = await ticketSala.send(f"<@{user.id}>, **escreva aqui**\n> Você será respondido em breve!\n> Para fechar seu pedido de suporte reaja com 🔒")
                await msg.add_reaction('🔒')
    except:
        pass