import asyncio
import discord
from discord.ext import commands

import json
import certifi
import urllib3
http = urllib3.PoolManager(num_pools=1000,cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
#in the future maybe move over to aiohttp - fuck me thats going to be annoying
header = {'User-Agent': 'Various Discord Bot Variants (@psymons#8386)'}

import matplotlib
matplotlib.use('Agg')

import random
import datetime as dt
import time

import vars
import utils

class Graphs:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def piesystem(self, ctx, *, system : str):

        response = http.request('GET', "http://edsm.net/api-system-v1/factions", fields={"systemName":system})
        res = json.loads(response.data.decode('utf-8'))
        utils.api_increment()

        if len(res) == 0:
            await self.client.say(system + ' not found ?')
            return
        factionnames = []
        factioninf = []
        if len(res['factions']) == 0:
            await self.client.say(res['name'] + ' has no factions present ?')
            return
        for faction in res['factions']:
            if faction['influence'] > 0:
                factionnames.append(faction['name'])
                factioninf.append(float("{0:.2f}".format(100*faction['influence'])))

        import matplotlib.pyplot as pltpie

        colors = ['#96BCF0','#E8F096','#F0C796','#F09699','#F096EE','#B196F0','#96F0E2','#9CF096']
        pie = pltpie.pie(factioninf, colors=colors, startangle=90)
        #bbox_to_anchor=(1,0.5),
        #pltpie.legend(pie[0], title=res['name'] + ' Influence', labels=['%s - %1.2f %%' % (l, s) for l, s in zip(factionnames, factioninf)], loc='upper center', bbox_transform=pltpie.gcf().transFigure)
        pltpie.legend(pie[0], title=res['name'] + ' Influence', labels=['%s - %1.2f %%' % (l, s) for l, s in zip(factionnames, factioninf)], loc="best")
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        pltpie.axis('equal')
        pltpie.tight_layout()
        #pltpie.subplots_adjust(left=0.0, bottom=0.1, right=0.45)

        #plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        pltpie.savefig('pie.png', transparent=True, bbox_inches='tight')
        with open('pie.png', 'rb') as f:
            await self.client.send_file(ctx.message.channel, f)

        utils.graph_increment()
        pltpie.close()



    @commands.command(pass_context=True)
    async def linesystem(self, ctx, *, arg : str):

        try:
            system, timescale = map(str, arg.split(' & '))
        except Exception:
            system = arg
            timescale = 'week'

        now = dt.datetime.now()
        response = http.request('GET', "http://edsm.net/api-system-v1/factions", fields={"systemName":system, "showHistory":"1"})
        res = json.loads(response.data.decode('utf-8'))
        utils.api_increment()

        if len(res) == 0:
            await self.client.say(system + ' not found ?')
            return

        factionnames = []
        factioninf = []

        import matplotlib.cbook as cbook
        import matplotlib.image as image
        import matplotlib.pyplot as pltline
        import matplotlib.dates as mdates
        from cycler import cycler

        wmark, ax = pltline.subplots(figsize=(6, 4))

        if len(res['factions']) == 0:
            await self.client.say(res['name'] + ' has no factions present ?')
            return

        for faction in res['factions']:
            if len(faction['influenceHistory']) == 0:
                factioninf = (faction['influence'])
                y = factioninf * 100
                x = dt.datetime.fromtimestamp(int(faction['lastUpdate'])).strftime('%d/%m/%Y %H:%M')
                x = dt.datetime.strptime(x,'%d/%m/%Y %H:%M').date()
            else:
                factioninf = (faction['influenceHistory'])
                sortedinf = sorted(factioninf.items())
                x, y = zip(*sortedinf)
                y = [float(i) * 100 for i in y]
                x = [dt.datetime.fromtimestamp(int(j)).strftime('%d/%m/%Y %H:%M') for j in x]
                x = [dt.datetime.strptime(d,'%d/%m/%Y %H:%M').date() for d in x]

            factionname = faction['name']
            factionname = factionname[:25] + (factionname[25:] and '..')

            ax.plot(x ,y, label=factionname, marker='o')


        pltline.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))


        pltline.ylabel('%')
        pltline.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand", borderaxespad=0, title=res['name'] + ' Influence History', ncol=2)

        if timescale == 'week':
            pltline.gca().set_xlim([dt.datetime.now() - dt.timedelta(days=7), dt.datetime.now()])
        elif timescale == 'month':
            pltline.gca().set_xlim([dt.datetime.now() - dt.timedelta(days=31), dt.datetime.now()])
        elif timescale == 'max':
            pltline.gca().set_xlim([dt.datetime.now() - dt.timedelta(days=182), dt.datetime.now()])
        else:
            await self.client.say('Format Incorrect not a known time scale, see `?help` for more info')
            return

        pltline.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        pltline.gcf().autofmt_xdate()


        pltline.savefig('line.png', bbox_inches='tight')
        with open('line.png', 'rb') as f:
            await self.client.send_file(ctx.message.channel, f)

        utils.graph_increment()
        pltline.close()

def setup(client):
    client.add_cog(Graphs(client))
