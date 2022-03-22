import discord

class Role:
    async def Setar(self, mensagem, bot):
        f = open(f"Servidores/Roles/{self.guild.id}.txt", "w")
        dados = f"{self.channel.id}/{mensagem}\n"
        f.write(dados)
        f.close()
        msg = await self.channel.fetch_message(self.message.id)
        await msg.delete()
        await self.channel.send("Mensagem definida com sucesso, use !roleadd @cargo emoji")

    async def AdicionarEmoji(self, role, emoji, bot, reactionRole):
        try:
            f = open(f"Servidores/Roles/{self.guild.id}.txt", "r+")
            dados = f.readline()
            dados = dados.split("/")
            canal = dados[0]
            mensagem = dados[1]
            canal = await bot.fetch_channel(canal)
            msg = await canal.fetch_message(mensagem)

            await msg.add_reaction(emoji)
            reaction = f"{str(emoji.encode())}/{role.id}"
            f.write(reaction)
            f.write("\n")
            f.close()

            reactionRole[f'{self.guild.id}_{emoji.encode()}'] = role.id
            reactionRole[f'{self.guild.id}_mensagem'] = mensagem
            await self.message.delete()
            await self.channel.send("Reação adicionada.")
            return reactionRole
        except Exception as erro:
            print(f"[!] O seguinte erro ocorreu em {self.guild} ao tentar criar reação por emoji\n{erro}")
            await self.channel.send("Sete a mensagem de reação primeiro!\n> !role mensagem_id")
