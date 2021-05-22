import asyncio
import discord
from discord.ext import commands

import json
import certifi
import urllib3
http = urllib3.PoolManager(num_pools=1000,cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
#in the future maybe move over to aiohttp - fuck me thats going to be annoying
header = {'User-Agent': 'Various Discord Bot Variants (@psymons#8386)'}

import math

import vars
import utils

import datetime
import time

class Core:

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def distance(self, ctx, *, arg : str):

        try:
            system1, system2 = map(str, arg.split(' & ')) #check two systems seperated by an '&' if not explain
        except Exception:
            await self.client.say('Format has to be distance System Name & System Name i.e. `?distance sol & wolf 359`')
            return

        response = http.request('GET', "https://elitebgs.app/api/ebgs/v5/systems", fields={"name":system1})
        res = json.loads(response.data.decode('utf-8'))
        utils.api_increment()

        if len(res['docs']) != 1: #if this is not 1 then multiple systems found or none !! error check
            await self.client.say(system1 + ' Was not found ?')
            return
        for sys in res['docs'][:1]: #for the only system get position and correct name
            system1_name = sys['name']
            system1_x = sys['x']
            system1_y = sys['y']
            system1_z = sys['z']

        response = http.request('GET', "https://elitebgs.app/api/ebgs/v5/systems", fields={"name":system2})
        res = json.loads(response.data.decode('utf-8'))
        utils.api_increment()

        if len(res['docs']) != 1: #if this is not 1 then multiple systems found or none !! error check
            await self.client.say(system2 + ' Was not found ?')
            return
        for sys in res['docs'][:1]: #for the only system get position and correct name
            system2_name = sys['name']
            system2_x = sys['x']
            system2_y = sys['y']
            system2_z = sys['z']

        x_len = system2_x - system1_x
        y_len = system2_y - system1_y
        z_len = system2_z - system1_z

        hyp_1 = math.sqrt(math.pow(x_len, 2) + math.pow(y_len, 2))
        hyp_2 = math.sqrt(math.pow(z_len, 2) + math.pow(hyp_1, 2))

        hyp_2 = float("{0:.2f}".format(hyp_2))

        await self.client.say("Distance Between " + system1_name + " & " + system2_name + " is " + str(hyp_2) + " ly's")

    @commands.command(pass_context=True)
    async def factioninf(self, ctx, *, arg : str):
        """Gives current Faction Information"""
        #if str(ctx.message.channel) != common.OPS_CHANNEL:
            #return
        response = http.request('GET', "https://elitebgs.app/api/ebgs/v5/factions", fields={"name":arg})
        res = json.loads(response.data.decode('utf-8'))
        utils.api_increment()
        if len(res['docs']) != 1: #if this is not 1 then multiple factions found or none !! error check
            await self.client.say(arg + ' - Faction was not found or is simlar to numerous factions?')
            return

        embed = discord.Embed()

        for lists in res['docs'][:1]:
            faction = lists['name']
            embed.title = "__**" + faction + " Current Influence**__"
            sortedlist = sorted(lists['faction_presence'], key=lambda k: k['influence'], reverse=True)
            for systems in sortedlist:
                inf = float("{0:.2f}".format(100*systems['influence']))
                system = systems['system_name']
                utils.api_increment()
                state = systems['state'].title()

                active = ''
                for actives in systems['active_states']:
                    active = active + actives['state'].title() + ' '

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


                embed.add_field(name=system, value="Influence :" + str(inf) + "% " + utils.inf_emoji(inf) + "\nCurrent State: " + state + "\nActive States: " + actives + "\nPending States: " + pending +"\nRecovering States: " + recovering + "\n \n", inline=False)

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def systeminf(self, ctx, *, arg : str):
        """Gives current System Information"""
        #if str(ctx.message.channel) != common.OPS_CHANNEL:
            #return
        response = http.request('GET', "http://edsm.net/api-system-v1/factions", fields={"systemName":arg})
        res = json.loads(response.data.decode('utf-8'))
        utils.api_increment()
        if len(res) == 0: #if this is not 0 then system not found or none !! error check
            await self.client.say(arg + ' - System was not found ?')
            return
        if len(res['factions']) == 0:
            await self.client.say(res['name'] + ' has no factions present ?')
            return

        embed = discord.Embed()
        #upto here now below is from faction inf needs changing to system so loop through

        system = res['name']

        embed.title = "__**" + system + " System Current Influence**__"
        sortedlist = sorted(res['factions'], key=lambda k: k['influence'], reverse=True)
        for faction in sortedlist:
            inf = float("{0:.2f}".format(100*faction['influence']))
            name = faction['name']
            if faction['isPlayer']:
                name = name + ' :busts_in_silhouette:'
            if faction['name'] == res['controllingFaction']['name']:
                name = name + ' :crown:'
            utils.api_increment()
            state = faction['state'].title()
            pending = ""
            for pendings in faction['pendingStates']: #loop through all pending states highlight by trend
                if pendings['trend'] == -1:
                    pending = pending + '_' + pendings['state'].title() + '_ '
                if pendings['trend'] == 0:
                    pending = pending + pendings['state'].title() + ' '
                if pendings['trend'] == 1:
                    pending = pending + '__' + pendings['state'].title() + '__ '
            recovering = ""
            for recoverings in faction['recoveringStates']: #loop through all recovering states highlight by trend
                if recoverings['trend'] == -1:
                    recovering = recovering + '_' + recoverings['state'].title() + '_ '
                if recoverings['trend'] == 0:
                    recovering = recovering + recoverings['state'].title() + ' '
                if recoverings['trend'] == 1:
                    recovering = recovering + '__' + recoverings['state'].title() + '__ '

            embed.add_field(name=name, value="Influence :" + str(inf) + "% " + "\nCurrent State: " + state + "\nPending States: " + pending +"\nRecovering States: " + recovering + "\n \n", inline=False)

        await self.client.say(embed=embed)


    @commands.command(pass_context=True)
    async def expansecheck(self, ctx, *, arg : str):
        author = ctx.message.author

        try:
            lightyears, system = map(str, arg.split('ly from ')) #check correct santax
        except Exception:
            await self.client.say('Format has to be ?expansecheck #ly from system')
            return
        if int(lightyears) > 50:
            await self.client.say('#ly must be 50 or lower')
            return

        skip = False
        response = http.request('GET', "https://www.edsm.net/api-v1/system", fields={"systemName":system})
        start = json.loads(response.data.decode('utf-8'))
        utils.api_increment()

        response = http.request('GET', "https://www.edsm.net/api-v1/sphere-systems", fields={"systemName":system, "radius":lightyears})
        sphere = json.loads(response.data.decode('utf-8'))
        utils.api_increment()

        if len(sphere) == 0:
            await self.client.say(system + ' not found ?')
            return
        await self.client.say('This may take some time bear with me')

        title = "__**Possible Expansion Locations " + lightyears + "lys From " + start['name'] + "**__\n"
        message = ""
        efields = 0
        #print(start['name'])
        sphere = sorted(sphere, key=lambda k: k['distance'])
        for possystem in sphere:
            await asyncio.sleep(0.1)
            response = http.request('GET', "http://elitebgs.kodeblox.com/api/eddb/v3/systems", fields={"name":possystem['name']}, headers=header)
            permitcheck = json.loads(response.data.decode('utf-8'))
            utils.api_increment()

            for sys in permitcheck['docs'][:1]:

                if sys['is_populated'] and not sys['needs_permit']:
                    response = http.request('GET', "http://eddbapi.kodeblox.com/api/eddb/v3/populatedsystems", fields={"name":possystem['name']}, headers=header)

                    factioncheck = json.loads(response.data.decode('utf-8'))
                    utils.api_increment()

                    for popsys in factioncheck['docs'][:1]:

                        if len(popsys['minor_faction_presences']) != 0 and len(popsys['minor_faction_presences']) < 8:
                            num_factions = len(popsys['minor_faction_presences'])

                            for check in popsys['minor_faction_presences']:
                                if str(check['minor_faction_id']) in vars.PRISON_FAC_ID or possystem['name'] == start['name']:
                                    skip = True

                                if str(check['minor_faction_id']) == "75799":
                                    num_factions = num_factions - 1

                            if not skip and num_factions < 7 :
                                efields = efields + 1
                                message = message + "__**" + possystem['name'] + "**__ \nDistance :" + str(possystem['distance']) + "ly\nCurrent Factions: " + str(num_factions) +"\n"

                            skip = False
                            num_factions = 0


        if efields == 0:
            message = "No systems to display. Try larger distance."

        message = title + message

        chunks = []
        chunks = utils.split_lines(str=message, limit=1900)
        for bits in chunks:
            await self.client.say(bits)

    #@bot.command(pass_context=True)
    #async def testroute(ctx, ):

    	#process = subprocess.Popen(['python3', 'edts.py', '-j', '35.2', '--start="Sol/Galileo"', '--end="Alioth/Golden Gate"', '"Wolf 359/Powell High"', '"Agartha/Enoch Port"', '"Alpha Centauri"'],cwd='/home/edts', stdout=subprocess.PIPE)
    	#args = shlex.split('python3 edts.py -j 35.2 --start="Sol/Galileo" --end="Alioth/Golden Gate" "Wolf 359/Powell High" "Agartha/Enoch Port" "Alpha Centauri"')
    	#process = subprocess.Popen(args, cwd='/home/edts', stdout=subprocess.PIPE)
    	#stdout, _ = process.communicate()
    	#stdout = stdout.decode('ascii')
    	#await bot.say(stdout)

def setup(client):
    client.add_cog(Core(client))
