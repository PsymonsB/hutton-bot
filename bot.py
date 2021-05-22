import asyncio
import discord
from discord.ext import commands
description = '''Hutton Bot'''
bot = commands.Bot(command_prefix='?', description=description)
bot.remove_command('help')

token = ''
version = 'v1.0.0b'
channel = 'hutton-bot'
help_file = 'help.txt'


import json
import certifi
import urllib3
http = urllib3.PoolManager(num_pools=1000,cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
#in the future maybe move over to aiohttp - fuck me thats going to be annoying
header = {'User-Agent': 'Various Discord Bot Variants (@psymons#8386)'}


import datetime as dt
import time
start_time = time.time()

import logging
logging.basicConfig(filename='/home/elite-bots/hutton_bot.log', format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

import psutil
import shlex, subprocess

import vars
from utils import *

extensions = ['core', 'hutton', 'graphs', 'galnet']

@bot.event
async def on_ready():
    print(bot.user.name + ' ' + version + ' IS ALIVE !!')
    print(bot.user.id)
    print('------')
    logging.info(bot.user.name + ' ' + version + ' IS ALIVE !!')

@bot.event
async def on_message(message):

    author = message.author
    if str(message.channel) != channel and author.id not in vars.ADMINS:
        return
    message.content = message.content.lower()
    await bot.process_commands(message)

@bot.command(pass_context=True)
async def about(ctx, ):

    cpuused = psutil.cpu_percent(interval=1, percpu=True)
    vmem = psutil.virtual_memory()
    swpmem = psutil.swap_memory()
    cores = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent()


    message = "**" + bot.user.name + " " + version + "**\n"
    message = message + "Been Alive for: " + display_time(time.time() - start_time) + "\n"
    message = message + "**System Info**\n"
    message = message + progress(cpu_percent, 100) + "CPU\n"
    message = message + progress(vmem.percent, 100) + "RAM\n"
    message = message + progress(swpmem.percent, 100) + "SWAP\n"
    message = message + "Number of API calls made: " + str(api_count) + "\n"
    message = message + "Number of Graphs made: " + str(graph_count) + "\n"

    await bot.say(message)


@bot.command(pass_context=True)
async def help(ctx, ):

    with open(help_file) as file:
        data = file.read()

    await bot.send_message(ctx.message.author, data)
    await bot.say(ctx.message.author.mention + " Help information PM'd")

@bot.command(pass_context=True)
async def adminload(ctx, extension):
    try:
        bot.load_extension(extension)
        await bot.say('Loaded {}'.format(extension))
    except Exception as error:
        await bot.say('{} cannot be loaded. [{}]'.format(extension, error))

@bot.command(pass_context=True)
async def adminunload(ctx, extension):
    try:
        bot.unload_extension(extension)
        await bot.say('Unloaded {}'.format(extension))
    except Exception as error:
        await bot.say('{} cannot be loaded. [{}]'.format(extension, error))

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

    bot.run(token)
