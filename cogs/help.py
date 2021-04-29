from discord.ext import commands
import discord

class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(name='help', invoke_without_command=True)
	async def help_cmd(self, ctx):
		if ctx.prefix == f'<@!{self.bot.user.id}> ':
			prefix = f'{ctx.prefix}`'
		else:
			prefix = f'`{ctx.prefix}'

		embed = discord.Embed(title='Commands')
		if await ctx.bot.is_owner(ctx.author):
			embed.add_field(name='Admin Commands', value=f'{prefix}help admin`', inline=False)

		embed.add_field(name='Fun Commands', value=f'{prefix}help fun`', inline=False)
		embed.add_field(name='Miscellaneous Commands', value=f'{prefix}help misc`', inline=False)
		embed.add_field(name='Moderation Commands', value=f'{prefix}help mod`', inline=False)
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

	@help_cmd.command(name='admin')
	@commands.is_owner()
	async def admin_cmds(self, ctx):
		if ctx.prefix == f'<@!{self.bot.user.id}> ':
			prefix = f'{ctx.prefix}`'
		else:
			prefix = f'`{ctx.prefix}'

		embed = discord.Embed(title='Admin Commands')
		embed.add_field(name=f'{prefix}module`', value='See module subcommands.')
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

	@help_cmd.command(name='fun')
	async def fun_cmds(self, ctx):
		if ctx.prefix == f'<@!{self.bot.user.id}> ':
			prefix = f'{ctx.prefix}`'
		else:
			prefix = f'`{ctx.prefix}'

		embed = discord.Embed(title='Fun Commands')
		embed.add_field(name=f'{prefix}8ball <question>`', value='Ask the mystical 8ball a question!', inline=False)
		embed.add_field(name=f'{prefix}approve`', value='Have knuckles approve your meme!', inline=False)
		embed.add_field(name=f'{prefix}choose <choice 1, choice 2, choice 3, etc>`', value='Have Phantom choose something for you!', inline=False)
		embed.add_field(name=f'{prefix}emoji`', value='See emoji subcommands.', inline=False)
		embed.add_field(name=f'{prefix}hol <number>`', value='Play Higher or Lower with Phantom!', inline=False)
		embed.add_field(name=f'{prefix}love`', value='Show your love for Phantom (or someone else)!', inline=False)
		embed.add_field(name=f'{prefix}rps <rock/paper/scissors>`', value='Play Rock Paper Scissors with Phantom!', inline=False)
		embed.add_field(name=f'{prefix}snipe`', value='Send the last message that was deleted.', inline=False)
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

	@help_cmd.command(name='misc')
	async def misc_cmds(self, ctx):
		if ctx.prefix == f'<@!{self.bot.user.id}> ':
			prefix = f'{ctx.prefix}`'
		else:
			prefix = f'`{ctx.prefix}'

		embed = discord.Embed(title='Miscellaneous Commands')
		embed.add_field(name=f'{prefix}invite`', value='Gives the invite for this bot.', inline=False)
		embed.add_field(name=f'{prefix}ping`', value='Send the latency of the bot.', inline=False)
		embed.add_field(name=f'{prefix}say <message>`', value='Repeats any message given.', inline=False)
		embed.add_field(name=f'{prefix}uptime`', value='See how long this bot has been online for.', inline=False)
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

	@help_cmd.command(name='mod')
	async def mod_cmds(self, ctx):
		if ctx.prefix == f'<@!{self.bot.user.id}> ':
			prefix = f'{ctx.prefix}`'
		else:
			prefix = f'`{ctx.prefix}'

		embed = discord.Embed(title='Moderation Commands')
		if ctx.guild.me.guild_permissions.ban_members:
			embed.add_field(name=f'{prefix}ban <user>`', value='Ban a user.', inline=False)
			embed.add_field(name=f'{prefix}unban <user>`', value='Unban a user.', inline=False)

		if ctx.guild.me.guild_permissions.kick_members:
			embed.add_field(name=f'{prefix}kick <user>`', value='Kick a user.', inline=False)

		if ctx.guild.me.guild_permissions.mention_everyone:
			embed.add_field(name=f'{prefix}everyone <message>`', value='Send an announcement from Phantom.', inline=False)
		
		if len(embed.fields) == 0:
			return

		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Help(bot))
