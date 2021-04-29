from discord.ext import commands
import aiosqlite
import datetime
import discord
import math
import time


class Misc(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		async with aiosqlite.connect('Data/phantom.db') as db:
			async with db.execute('SELECT start_time from uptime') as cursor:
				if await cursor.fetchone() is None:
					start_time  = 'INSERT INTO uptime(start_time) VALUES(?)'
				else:
					start_time = 'UPDATE uptime SET start_time = ?'

			await db.execute(start_time, (time.time(),))
			await db.commit()

	@commands.command()
	@commands.guild_only()
	async def avatar(self, ctx, user_id=None):
		if user_id:
			if '<@' in user_id:
				user_id = int(user[2:-1].replace('!', ''))
			
			user = await self.bot.fetch_user(user_id)
		else:
			user = ctx.author

		embed = discord.Embed(title=f"{user.name}#{user.discriminator}'s Avatar")
		embed.set_image(url=user.avatar_url_as(static_format='png'))
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

	@commands.command()
	@commands.guild_only()
	async def invite(self, ctx):
		embed = discord.Embed(title='Phantom Invite', description=f'Add Phantom to your server with [this](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=3229084742&scope=bot) link.')
		embed.set_thumbnail(url=self.bot.user.avatar_url_as(static_format='png'))
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

	@commands.command()
	@commands.guild_only()
	async def ping(self, ctx):
		embed = discord.Embed(title='Pong!')
		embed.add_field(name='API Ping', value=f'`{round(self.bot.latency * 1000)}ms`')
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		message = await ctx.send(embed=embed)
		
		embed.add_field(name='Message Ping', value=f'`{round((datetime.datetime.utcnow().timestamp() - message.created_at.timestamp()) * 1000)}ms`')
		await message.edit(embed=embed)

	@commands.command()
	@commands.guild_only()
	async def uptime(self, ctx):
		async with aiosqlite.connect('Data/phantom.db') as db:
			async with db.execute('SELECT start_time from uptime') as cursor:
				start_time = (await cursor.fetchone())[0]

		hours, minutes, seconds = time.strftime("%H:%M:%S", time.gmtime(math.floor(time.time() - float(start_time)))).split(':')

		embed = discord.Embed(title='Uptime', description=f"**{int(hours)}** hour{'s' if int(hours) != 1 else ''}, **{int(minutes)}** minute{'s' if int(minutes) != 1 else ''}, **{int(seconds)}** second{'s' if int(seconds) != 1 else ''}")
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Misc(bot))
