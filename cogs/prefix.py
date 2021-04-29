from discord.ext import commands
import aiosqlite
import discord


class Prefix(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		await self.bot.wait_until_ready()
		async with aiosqlite.connect('Data/phantom.db') as db:
			await db.execute('INSERT INTO prefix(guild, prefix) VALUES(?,?)', (guild.id, 'p!'))
			await db.commit()

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		await self.bot.wait_until_ready()
		async with aiosqlite.connect('Data/phantom.db') as db:
			await db.execute('DELETE from prefix where guild = ?', (guild.id,))
			await db.commit()

	@commands.Cog.listener()
	async def on_message(self, message):
		await self.bot.wait_until_ready()
		if message.channel.type is discord.ChannelType.private:
			return

		async with aiosqlite.connect('Data/phantom.db') as db:
			async with db.execute('SELECT prefix from prefix WHERE guild = ?', (message.guild.id,)) as cursor:
				try:
					prefix = (await cursor.fetchone())[0]
				except TypeError:
					await db.execute('INSERT INTO prefix(guild, prefix) VALUES(?,?)', (message.guild.id, 'p!'))
					await db.commit()

					prefix = 'p!'

		if message.content in (f'<@!{self.bot.user.id}>', f'<@{self.bot.user.id}>'):
			embed = discord.Embed(title='Hey!', description=f'My prefix is `{prefix}`. Run `{prefix}help` to see what I can do!')
			embed.set_footer(text=message.author.name, icon_url=message.author.avatar_url_as(static_format='png'))

			await message.channel.send(embed=embed)
			return

	@commands.command()
	@commands.guild_only()
	async def prefix(self, ctx, new_prefix):
		if not ctx.author.guild_permissions.administrator and not await ctx.bot.is_owner(ctx.author):
			embed = discord.Embed(title='Prefix')
			embed.add_field(name='Error', value='You do not have permission to run this command!')
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		if len(new_prefix) > 4:
			embed = discord.Embed(title='Prefix')
			embed.add_field(name='Error', description=f'Prefixes must be under 4 characters.')
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		async with aiosqlite.connect('Data/phantom.db') as db:
			await db.execute('UPDATE prefix SET prefix = ? WHERE guild = ?', (new_prefix, ctx.guild.id))
			await db.commit()

		embed = discord.Embed(title='Prefix', description=f"My prefix has been changed to `{new_prefix}`!")
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Prefix(bot))
