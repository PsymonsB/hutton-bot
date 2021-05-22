import asyncio
import discord
from discord.ext import commands

import json
import certifi
import urllib3
http = urllib3.PoolManager(num_pools=1000,cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
#in the future maybe move over to aiohttp - fuck me thats going to be annoying
header = {'User-Agent': 'Various Discord Bot Variants (@psymons#8386)'}

import vars
import utils

class Hutton:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def hotcol_inf(self, ctx, ):
        """Gives current HOTCOL Faction Information"""

        response = http.request('GET', "http://elitebgs.kodeblox.com/api/ebgs/v4/factions?name=HOTCOL")
        res = json.loads(response.data.decode('utf-8'))
        utils.api_increment()
        embed = discord.Embed()
        embed.title = "__**HOTCOL Influence**__"
        for lists in res['docs'][:1]:
            sortedlist = sorted(lists['faction_presence'], key=lambda k: k['influence'], reverse=True)
            for systems in sortedlist:
                inf = float("{0:.2f}".format(100*systems['influence']))
                system = systems['system_name']
                state = systems['state'].title()
                pending = ''
                for pendings in systems['pending_states']: #loop through all pending states highlight by trend
                    if pendings['trend'] == -1:
                        pending = pending + '_' + pendings['state'].title() + '_ '
                    if pendings['trend'] == 0:
                        pending = pending + pendings['state'].title() + ' '
                    if pendings['trend'] == 1:
                        pending = pending + '__' + pendings['state'].title() + '__ '
                recovering = ""
                for recoverings in systems['recovering_states']: #loop through all recovering states highlight by trend
                    if recoverings['trend'] == -1:
                        recovering = recovering + '_' + recoverings['state'].title() + '_ '
                    if recoverings['trend'] == 0:
                        recovering = recovering + recoverings['state'].title() + ' '
                    if recoverings['trend'] == 1:
                        recovering = recovering + '__' + recoverings['state'].title() + '__ '

                embed.add_field(name=system, value="Influence :" + str(inf) + "% " + utils.inf_emoji(inf) + "\nCurrent State: " + state + "\nPending States: " + pending +"\nRecovering States: " + recovering + "\n \n ", inline=False)

        await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def hutton_inf(self, ctx, ):
        """Gives current Hutton Orbital Truckers Faction Information"""

        response = http.request('GET', "http://elitebgs.kodeblox.com/api/ebgs/v4/factions?name=Hutton%20Orbital%20Truckers%20Co-Operative")
        res = json.loads(response.data.decode('utf-8'))
        utils.api_increment()
        embed = discord.Embed()
        embed.title = "__**Hutton Orbital Truckers Co-Operative Influence**__"
        for lists in res['docs'][:1]:
            sortedlist = sorted(lists['faction_presence'], key=lambda k: k['influence'], reverse=True)
            for systems in sortedlist:
                inf = float("{0:.2f}".format(100*systems['influence']))
                system = systems['system_name']
                state = systems['state'].title()
                pending = ''
                for pendings in systems['pending_states']: #loop through all pending states highlight by trend
                    if pendings['trend'] == -1:
                        pending = pending + '_' + pendings['state'].title() + '_ '
                    if pendings['trend'] == 0:
                        pending = pending + pendings['state'].title() + ' '
                    if pendings['trend'] == 1:
                        pending = pending + '__' + pendings['state'].title() + '__ '
                recovering = ""
                for recoverings in systems['recovering_states']: #loop through all recovering states highlight by trend
                    if recoverings['trend'] == -1:
                        recovering = recovering + '_' + recoverings['state'].title() + '_ '
                    if recoverings['trend'] == 0:
                        recovering = recovering + recoverings['state'].title() + ' '
                    if recoverings['trend'] == 1:
                        recovering = recovering + '__' + recoverings['state'].title() + '__ '

                embed.add_field(name=system, value="Influence :" + str(inf) + "% " + utils.inf_emoji(inf) + "\nCurrent State: " + state + "\nPending States: " + pending +"\nRecovering States: " + recovering + "\n \n ", inline=False)

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def dongkum_inf(self, ctx, ):
        """Gives current Dongkum Faction Information"""

        response = http.request('GET', "http://elitebgs.kodeblox.com/api/ebgs/v4/factions?name=Independent%20Dongkum%20Green%20Party")
        res = json.loads(response.data.decode('utf-8'))
        utils.api_increment()
        embed = discord.Embed()
        embed.title = "__**Independent Dongkum Green Party Influence**__"
        for lists in res['docs'][:1]:
            sortedlist = sorted(lists['faction_presence'], key=lambda k: k['influence'], reverse=True)
            for systems in sortedlist:
                inf = float("{0:.2f}".format(100*systems['influence']))
                system = systems['system_name']
                state = systems['state'].title()
                pending = ''
                for pendings in systems['pending_states']: #loop through all pending states highlight by trend
                    if pendings['trend'] == -1:
                        pending = pending + '_' + pendings['state'].title() + '_ '
                    if pendings['trend'] == 0:
                        pending = pending + pendings['state'].title() + ' '
                    if pendings['trend'] == 1:
                        pending = pending + '__' + pendings['state'].title() + '__ '
                recovering = ""
                for recoverings in systems['recovering_states']: #loop through all recovering states highlight by trend
                    if recoverings['trend'] == -1:
                        recovering = recovering + '_' + recoverings['state'].title() + '_ '
                    if recoverings['trend'] == 0:
                        recovering = recovering + recoverings['state'].title() + ' '
                    if recoverings['trend'] == 1:
                        recovering = recovering + '__' + recoverings['state'].title() + '__ '

                embed.add_field(name=system, value="Influence :" + str(inf) + "% " + utils.inf_emoji(inf) + "\nCurrent State: " + state + "\nPending States: " + pending +"\nRecovering States: " + recovering + "\n \n ", inline=False)

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def mug(self, ctx, ):

        author = ctx.message.author
        if author.id != "196614818399125504": # test protocol for specific users !
            await self.client.say("You're not draxxor !!!! :unamused:")
            return

        response = http.request('GET', "http://hot.forthemug.com:4567/draxxorsmission.json")
        res = json.loads(response.data.decode('utf-8'))
        utils.api_increment()

        await self.client.say('Hello Draxxor !')
        mugtotal = int(res['mugsremaining'])

        if mugtotal > 666:
            await self.client.say('**' + str(mugtotal) + '** Mugs remaining :joy:')
        elif mugtotal < 666:
            await self.client.say('**' + str(mugtotal) + '** Mugs remaining :stuck_out_tongue_winking_eye: :thumbsup: ')
        elif mugtotal == 666:
            await self.client.say('**' + str(mugtotal) + '** Mugs remaining :japanese_ogre: DEVIL NUMBER :japanese_ogre: ')
        else:
            await self.client.say('** MISSION COMPLETE **')

    @commands.command(pass_context=True)
    async def huttonrun(self, ctx, ):

        response = http.request('GET', "http://forthemug.com:4567/besthuttonrun.json/hutton_bot")
        res = json.loads(response.data.decode('utf-8'))
        utils.api_increment()

        await self.client.say('The Fastest Hutton Run to date was completed by **' + res['commandername'] + '** in a time of **' + res['TravelTime'] + ' **')
        await self.client.say('If you think you can beat it make sure to download the Hutton Helper from http://hot.forthemug.com')

def setup(client):
    client.add_cog(Hutton(client))
