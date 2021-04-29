from datetime import datetime
from discord.ext import commands
import aiosqlite
import ast
import discord
import random


class Snipe(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		await self.bot.wait_until_ready()
		if message.channel.type is discord.ChannelType.private or message.author.bot or await self.bot.is_owner(message.author):
			return

		message_data = {
			'message': message.content,
			'timestamp': message.created_at.timestamp()
		}

		async with aiosqlite.connect('Data/phantom.db') as db:
			async with db.execute('SELECT * from snipe WHERE guild = ? AND channel = ?', (message.guild.id, message.channel.id)) as cursor:
				if await cursor.fetchone() is None:
					set_msg = 'INSERT INTO snipe(message, member, guild, channel) VALUES(?,?,?,?)'
				else:
					set_msg = 'UPDATE snipe SET message = ?, member = ? WHERE guild = ? AND channel = ?'

			await db.execute(set_msg, (str(message_data), message.author.id, message.guild.id, message.channel.id))
			await db.commit()

	@commands.command()
	@commands.guild_only()
	async def snipe(self, ctx):
		async with aiosqlite.connect('Data/phantom.db') as db:
			async with db.execute('SELECT * from snipe WHERE guild = ? AND channel = ?', (ctx.guild.id, ctx.channel.id)) as cursor:
				data = await cursor.fetchone()

		try:
			member = await self.bot.fetch_user(data[3])
		except discord.NotFound:
			member = None

		message_data = ast.literal_eval(data[2])
		message_time = datetime.fromtimestamp(message_data['timestamp']).strftime('%m-%d-%y %I:%M:%S %p')

		embed = discord.Embed(description=message_data['message'])
		embed.set_author(name=f"{'User not found' if member is None else f'{member.name}#{member.discriminator}'} | {message_time} UTC", icon_url=self.bot.user.default_avatar_url if member is None else member.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Snipe(bot))
