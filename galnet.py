import asyncio
import discord
from discord.ext import commands

import json
import certifi
import urllib3
http = urllib3.PoolManager(num_pools=1000,cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
#in the future maybe move over to aiohttp - fuck me thats going to be annoying
header = {'User-Agent': 'Various Discord Bot Variants (@psymons#8386)'}

import MySQLdb

import vars
import utils

class Galnet:
        def __init__(self, client):
            self.client = client
            self.db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="psymons",         # your username
                     passwd="Software185Spectrum!",  # your password
                     db="elite_dangerous",              # name of the data base
                     charset="utf8")       #character set

            self.cursor = self.db.cursor()
            self.db.set_character_set('utf8')
            self.cursor.execute('SET NAMES utf8;')
            self.cursor.execute('SET CHARACTER SET utf8;')
            self.cursor.execute('SET character_set_connection=utf8;')

        @commands.command(pass_context=True)
        async def galnet(self, ctx, ):
            response = http.request('GET', "https://www.alpha-orbital.com/galnet-feed")
            galnetnews = json.loads(response.data.decode('utf-8'))
            message = ""
            for articles in galnetnews:
                message = message + "**" + articles['title'] + "**"
                message = message + articles['date'] + "\n"
                message = message + articles['content'].replace("<br />", "\n") + "\n"

            chunks = []
            chunks = utils.split_lines(str=message, limit=1900)
            for bits in chunks:
                print(bits)
                await self.client.say(bits)


        @commands.command(pass_context=True)
        async def stationstatus(self, ctx, ):

            self.cursor.execute("SELECT * from galnet_data where Title='Starport Status Update' ORDER BY RealDate DESC LIMIT 1;")
            for row in self.cursor:
                #print(row[1])
                #print(row[2])
                #print(row[3])
                message = "**" + row[1] + "**"
                message = message + " - " + row[2] + "\n"
                tempmessage = row[3].replace("<br />", "\n").replace("\n\n", "\n") + "\n"
                tempmessage = tempmessage.replace("The following starports are currently closed:", "\n**The following starports are currently closed:**")
                tempmessage = tempmessage.replace("Meanwhile, the following starports are on the brink of closure:", "\n**Meanwhile, the following starports are on the brink of closure:**")
                message = message + tempmessage

            chunks = []
            chunks = utils.split_lines(str=message, limit=1900)
            for bits in chunks:
                #print(bits)
                await self.client.say(bits)

def setup(client):
    client.add_cog(Galnet(client))
