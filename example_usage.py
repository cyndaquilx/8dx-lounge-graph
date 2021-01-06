import discord
from discord.ext import commands

import gspread_asyncio
from oauth2client.service_account import ServiceAccountCredentials

import plotting

def get_creds():
    return ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json",
        [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/spreadsheets",
        ],
    )
agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)

class mmr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def stats(self, ctx, *, name):
        agc = await agcm.authorize()
        sh = await agc.open_by_key("1guMKAgkORdeeSs3SZYcsiJ385JNpLvngZR3eP2Nc-Kg")
        botSheet = await sh.worksheet("stats bot sheet")

        await botSheet.update_cell(1, 2, name)
        
        gotBatch = await botSheet.batch_get(["F9:G9"])

        base = int(gotBatch[0][0][0])
        matches = gotBatch[0][0][1]
        history = [int(match) for match in matches.split(",")]

        file = plotting.create_plot(base, history)

        f=discord.File(fp=file, filename='stats.png')
        await ctx.send(file=f)

        
        

def setup(bot):
    bot.add_cog(mmr(bot))
