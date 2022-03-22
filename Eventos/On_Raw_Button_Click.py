import re

async def onrawclick(interaction, bot):
    try:
        if re.search("Deletar Sala", str(interaction["message"])):
            canal = await bot.fetch_channel(interaction["message"]["channel_id"])
            await canal.delete()
    except:
        pass