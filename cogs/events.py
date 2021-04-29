from discord.ext import commands
import aiosqlite
import discord
import os
import time

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		await self.bot.wait_until_ready()

		embed = discord.Embed(title='Hey!', description="I'm Phantom, a do-it-all bot that aims to replace all other bots in your Discord!")
		embed.add_field(name='Prefix', value='My prefix is `p!`. Run `p!help` to see what I can do!')
		embed.set_thumbnail(url=self.bot.user.avatar_url_as(static_format='png'))

		if guild.system_channel:
			try:
				await guild.system_channel.send(embed=embed)
			except discord.errors.Forbidden:
				pass

		else:
			for x in range(len(guild.text_channels)):
				try:
					await guild.text_channels[x].send(embed=embed)
					break
				except discord.errors.Forbidden:
					continue
			
		await self.bot.change_presence(activity=discord.Game(name=f"Ping me for help! | Terrorizing {len(self.bot.guilds)} server{'s' if len(self.bot.guilds) != 1 else ''}"))

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		await self.bot.wait_until_ready()
		await self.bot.change_presence(activity=discord.Game(name=f"Ping me for help! | Terrorizing {len(self.bot.guilds)} server{'s' if len(self.bot.guilds) != 1 else ''}"))

	@commands.Cog.listener()
	async def on_ready(self):
		os.makedirs('Data', exist_ok=True)

		async with aiosqlite.connect('Data/phantom.db') as db:
			await db.execute('''CREATE TABLE IF NOT EXISTS logging(guild INTEGER, enabled BOOL)''')
			await db.commit()

			await db.execute('''CREATE TABLE IF NOT EXISTS prefix(guild INTEGER, prefix TEXT)''')
			await db.commit()

			await db.execute('''CREATE TABLE IF NOT EXISTS timer(user INTEGER, is_running TEXT)''')
			await db.commit()

			await db.execute('''CREATE TABLE IF NOT EXISTS snipe(guild INTEGER, channel INTEGER, message TEXT, member INTEGER)''')
			await db.commit()

			await db.execute('''CREATE TABLE IF NOT EXISTS uptime(start_time REAL)''')
			await db.commit()

		await self.bot.change_presence(activity=discord.Game(name=f"Ping me for help! | Terrorizing {len(self.bot.guilds)} server{'s' if len(self.bot.guilds) != 1 else ''}"))
		print('Phantom is now online.')

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		await self.bot.wait_until_ready()
		if isinstance(error, commands.CommandNotFound):
			if ctx.prefix == f'<@!{self.bot.user.id}> ':
				prefix = f'{ctx.prefix}`'
			else:
				prefix = f'`{ctx.prefix}'

			embed = discord.Embed(title='Error', description=f"That command doesn't exist! Use {prefix}help` to see all the commands I can run.")
			embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
		
		elif isinstance(error, commands.MissingPermissions):
			pass

		else:
			raise error

def setup(bot):
	bot.add_cog(Events(bot))
