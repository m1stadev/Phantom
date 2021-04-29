from datetime import datetime
from discord.ext import commands
import aiofiles
import aiohttp
import aiosqlite
import asyncio
import asynctempfile as tempfile # switch to aiofiles once 0.7.0 releases
import discord
import os
import shutil


class Logging(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def upload_to_pstyio(self, filepath, upload_name):
		async with aiofiles.open(filepath, 'rb') as f:
			async with aiohttp.ClientSession() as session:
				async with session.put(f'https://up.psty.io/{upload_name}', data=f) as response:
					resp = await response.text()
					await response.release()

		return resp.splitlines()[-1].split(':', 1)[1][1:]

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		await self.bot.wait_until_ready()
		async with aiosqlite.connect('Data/phantom.db') as db:
			await db.execute('INSERT INTO logging(guild, enabled) VALUES(?,?)', (guild.id, False))
			await db.commit()

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		await self.bot.wait_until_ready()
		async with aiosqlite.connect('Data/phantom.db') as db:
			await db.execute('DELETE * FROM logging WHERE guild = ?', (guild.id,))
			await db.commit()

		await asyncio.to_thread(shutil.rmtree, f'Data/Servers/{guild.id}')

	@commands.Cog.listener()
	async def on_member_join(self, member):
		await self.bot.wait_until_ready()

		async with aiosqlite.connect('Data/phantom.db') as db:
			async with db.execute('SELECT enabled from logging WHERE guild = ?', (member.guild.id,)) as cursor:
				if (await cursor.fetchone())[0] == False:
					return

		await asyncio.to_thread(os.makedirs, f'Data/Servers/{member.guild.id}/Members', exist_ok=True)

		current_time = datetime.now().astimezone()
		formatted_date = current_time.strftime('%m-%d-%y')
		formatted_time = current_time.strftime('%I:%M:%S %p %Z')

		async with aiofiles.open(f'Data/Servers/{member.guild.id}/Members/{formatted_date}.log', 'a') as f:
			await f.write(f"[{formatted_time} | {member.guild.name}] {member.name}#{member.discriminator}{' (Bot)' if member.bot else ''} has joined the server.\n")

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		await self.bot.wait_until_ready()

		async with aiosqlite.connect('Data/phantom.db') as db:
			async with db.execute('SELECT enabled from logging WHERE guild = ?', (member.guild.id,)) as cursor:
				if (await cursor.fetchone())[0] == False:
					return

		await asyncio.to_thread(os.makedirs, f'Data/Servers/{member.guild.id}/Members', exist_ok=True)

		current_time = datetime.now().astimezone()
		formatted_date = current_time.strftime('%m-%d-%y')
		formatted_time = current_time.strftime('%I:%M:%S %p %Z')

		async with aiofiles.open(f'Data/Servers/{member.guild.id}/Members/{formatted_date}.log', 'a') as f:
			await f.write(f"[{formatted_time} | {member.guild.name}] {member.name}#{member.discriminator}{' (Bot)' if member.bot else ''} has left the server.\n")

	@commands.Cog.listener()
	async def on_message(self, message):
		await self.bot.wait_until_ready()
		if message.channel.type is discord.ChannelType.private:
			return

		async with aiosqlite.connect('Data/phantom.db') as db:
			async with db.execute('SELECT enabled from logging WHERE guild = ?', (message.guild.id,)) as cursor:
				if (await cursor.fetchone())[0] == False:
					return

		current_time = datetime.now().astimezone()
		formatted_date = current_time.strftime('%m-%d-%y')
		formatted_time = current_time.strftime('%I:%M:%S %p %Z')

		filepath = f'Data/Servers/{message.guild.id}/Messages/{message.channel.id}/{formatted_date}.log'
		await asyncio.to_thread(os.makedirs, filepath.rsplit('/', 1)[0], exist_ok=True)

		for x in range(len(message.attachments)):
			async with aiofiles.open(filepath, 'a') as f:
				await f.write(f"[{formatted_time} | {message.author.name}#{message.author.discriminator}{' (Bot)' if message.author.bot else ''}] Attachment - {message.attachments[x].url}\n")

		if len(message.content) > 0:
			async with aiofiles.open(filepath, 'a') as f: 
				await f.write(f"[{formatted_time} | {message.author.name}#{message.author.discriminator}{' (Bot)' if message.author.bot else ''}] - {message.content}\n")

	@commands.group(invoke_without_command=True)
	@commands.has_guild_permissions(administrator=True)
	async def log(self, ctx):
		if ctx.prefix == f'<@!{self.bot.user.id}> ':
			prefix = f'{ctx.prefix}`'
		else:
			prefix = f'`{ctx.prefix}'

		async with aiosqlite.connect('Data/phantom.db') as db:
			async with db.execute('SELECT enabled from logging WHERE guild = ?', (ctx.guild.id,)) as cursor:
				logging_enabled = (await cursor.fetchone())[0]

		embed = discord.Embed(title='Log Commands')
		embed.add_field(name='Enable/Disable Logging', value=f'{prefix}log toggle`', inline=False)
		embed.add_field(name='Download Logs', value=f'{prefix}log download`', inline=False)
		embed.add_field(name='Note', value=f"Logging is currently **{'enabled' if logging_enabled == True else 'disabled'}**.", inline=False)
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

	@log.command()
	@commands.has_guild_permissions(administrator=True)
	@commands.guild_only()
	async def download(self, ctx):
		async with tempfile.TemporaryDirectory() as tmpdir:
			await asyncio.to_thread(shutil.make_archive, tmpdir + ctx.guild.id, 'zip', f'Data/Servers/{ctx.guild.id}')
			download_url = await self.upload_to_pstyio(f'{tmpdir + ctx.guild.id}.zip', 'Logs.zip')

		embed = discord.Embed(title='Logging', description=f'All logs from {ctx.guild.name}: [Download]({download_url})')
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))

	@log.command()
	@commands.has_guild_permissions(administrator=True)
	@commands.guild_only()
	async def toggle(self, ctx):
		async with aiosqlite.connect('Data/phantom.db') as db:
			async with db.execute('SELECT enabled from logging WHERE guild = ?', (ctx.guild.id,)) as cursor:
				logging_enabled = (await cursor.fetchone())[0]
				if logging_enabled == True:
					await db.execute('UPDATE logging SET enabled = ? WHERE guild = ?', (False, ctx.guild.id))
					logging_enabled = False
				else:
					await db.execute('UPDATE logging SET enabled = ? WHERE guild = ?', (True, ctx.guild.id))
					logging_enabled = True

				await db.commit()

		embed = discord.Embed(title='Logging', description=f"Logging has been {'enabled' if logging_enabled == True else 'disabled'}.")
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Logging(bot))
