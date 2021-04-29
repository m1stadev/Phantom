#!/usr/bin/env python3

from discord.ext import commands
import aiosqlite
import discord
import glob
import platform
import os
import sys
import time


def bot_token(): return os.getenv('PHANTOM_TOKEN') if os.getenv('PHANTOM_TOKEN') is not None else sys.exit(f"[ERROR] Bot token not set in 'PHANTOM_TOKEN' environment variable.")

async def get_prefix(client, message):
	if message.channel.type is discord.ChannelType.private:
		return 'p!'

	async with aiosqlite.connect('Data/phantom.db') as db:
		async with db.execute('SELECT prefix FROM prefix WHERE guild = ?', (message.guild.id,)) as cursor:
			try:
				guild_prefix = (await cursor.fetchone())[0]
			except TypeError:
				await db.execute('INSERT INTO prefix(guild, prefix) VALUES(?,?)', (message.guild.id, 'p!'))
				await db.commit()
				guild_prefix = 'p!'

		await db.execute('SELECT prefix FROM prefix WHERE guild = ?', (message.guild.id,))

	return commands.when_mentioned_or(guild_prefix)(client, message)

if __name__ == '__main__':
	if not (sys.version_info.major >= 3 and sys.version_info.minor >= 9):
		sys.exit('[ERROR] Phantom requires Python 3.9 or higher.')

	intents = discord.Intents.default()
	intents.members = True
	client = commands.Bot(command_prefix=get_prefix, help_command=None, intents=intents)

	if platform.system() == 'Windows':
		cogs = glob.glob('cogs\*.py')
	else:
		cogs = glob.glob('cogs/*.py')

	for x in [cog.replace('/', '.').replace('\\', '.')[:-3].split('.')[1] for cog in cogs]:
		try:
			client.load_extension(f'cogs.{x}')
		except commands.ExtensionFailed:
			sys.exit(f"[ERROR] Module '{x}' failed to load.")


	try:
		client.run(bot_token())
	except discord.LoginFailure:
		sys.exit("[ERROR] Token invalid, make sure the 'PHANTOM_TOKEN' environment variable is set to your bot token.")
