from discord.ext import commands
import asyncio
import discord


class Mod(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.guild_only()
	@commands.has_guild_permissions(kick_members=True)
	async def kick(self, ctx, member_id, *, reason=None):
		if not ctx.guild.me.guild_permissions.kick_members:
			embed = discord.Embed(title='Kick')
			embed.add_field(name='Error', value="I don't have permission to kick users. Please ask an administrator to fix this!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		if '<@' in member_id:
			member_id = int(member_id[2:-1].replace('!', ''))
		
		kicked_member = ctx.guild.get_member(member_id)
		if kicked_member is None:
			embed = discord.Embed(title='Kick')
			embed.add_field(name='Error', value="This member doesn't exist!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		elif kicked_member not in ctx.guild.members:
			embed = discord.Embed(title='Kick')
			embed.add_field(name='Error', value="This member isn't in this server!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		elif kicked_member == ctx.author:
			embed = discord.Embed(title='Kick')
			embed.add_field(name='Error', value="Silly goose, you can't kick yourself!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		if ctx.guild.roles.index(ctx.author.top_role) < ctx.guild.roles.index(kicked_member.top_role):
			embed = discord.Embed(title='Kick')
			embed.add_field(name='Error', value=f"You don't have permission to kick {kicked_member.mention}!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		if ctx.guild.roles.index(ctx.guild.me.top_role) < ctx.guild.roles.index(kicked_member.top_role):
			embed = discord.Embed(title='Kick')
			embed.add_field(name='Error', value=f"I don't have permission to kick {kicked_member.mention} because the {kicked_member.top_role.mention} role that {kicked_member.mention} has is above the {ctx.guild.me.top_role.mention} role that I have!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		try:
			kick_embed = discord.Embed(title='Kick', description=f"You've been kicked from `{ctx.guild.name}`{f' for `{reason}`' if reason else ''}.")
			kick_embed.set_footer(text=ctx.guild.me.nick if ctx.guild.me.nick is not None else self.bot.user.name, icon_url=self.bot.user.avatar_url_as(static_format='png'))
			await kicked_member.send(embed=kick_embed)

		except discord.errors.HTTPException:
			pass

		await ctx.guild.kick(kicked_member, reason=reason)
		for x in await ctx.guild.invites():
			if x.inviter.id == kicked_member.id:
				await x.delete(reason=f"{kicked_member.mention} has been kicked from `{ctx.guild.name}`{f' for `{reason}`' if reason else ''}.")

		embed = discord.Embed(title='Kick', description=f"{kicked_member.mention} has been kicked from `{ctx.guild.name}`{f' for `{reason}`' if reason else ''}.")
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

	@commands.command()
	@commands.guild_only()
	@commands.has_guild_permissions(ban_members=True)
	async def ban(self, ctx, member_id, *, reason=None):
		if not ctx.guild.me.guild_permissions.ban_members:
			embed = discord.Embed(title='Ban')
			embed.add_field(name='Error', value="I don't have permission to ban users. Please ask an administrator to fix this!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		if '<@' in member_id:
			member_id = int(member_id[2:-1].replace('!', ''))
		
		banned_member = ctx.guild.get_member(member_id)
		if banned_member is None:
			embed = discord.Embed(title='Ban')
			embed.add_field(name='Error', value="This member doesn't exist!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		elif banned_member not in ctx.guild.members:
			embed = discord.Embed(title='Ban')
			embed.add_field(name='Error', value="This member isn't in this server!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		elif banned_member == ctx.author:
			embed = discord.Embed(title='Ban')
			embed.add_field(name='Error', value="Silly goose, you can't ban yourself!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		if ctx.guild.roles.index(ctx.author.top_role) < ctx.guild.roles.index(banned_member.top_role):
			embed = discord.Embed(title='Ban')
			embed.add_field(name='Error', value=f"You don't have permission to ban {banned_member.mention}!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		if ctx.guild.roles.index(ctx.guild.me.top_role) < ctx.guild.roles.index(banned_member.top_role):
			embed = discord.Embed(title='Ban')
			embed.add_field(name='Error', value=f"I don't have permission to ban {banned_member.mention} because the {banned_member.top_role.mention} role that {banned_member.mention} has is above the {ctx.guild.me.top_role.mention} role that I have!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		try:
			ban_embed = discord.Embed(title='Ban', description=f"You've been banned from `{ctx.guild.name}`{f' for `{reason}`' if reason else ''}.")
			ban_embed.set_footer(text=ctx.guild.me.nick if ctx.guild.me.nick is not None else self.bot.user.name, icon_url=self.bot.user.avatar_url_as(static_format='png'))
			await banned_member.send(embed=ban_embed)

		except discord.errors.HTTPException:
			pass

		await ctx.guild.ban(banned_member, reason=reason)
		for x in await ctx.guild.invites():
			if x.inviter.id == banned_member.id:
				await x.delete(reason=f"{banned_member.mention} has been banned from `{ctx.guild.name}`{f' for `{reason}`.' if reason else '.'}")

		embed = discord.Embed(title='Ban', description=f"{banned_member.mention} has been banned from `{ctx.guild.name}`{f' for `{reason}`.' if reason else '.'}")
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

	@commands.command()
	@commands.guild_only()
	@commands.has_guild_permissions(ban_members=True)
	async def unban(self, ctx, member_id, *, reason=None):
		if not ctx.guild.me.guild_permissions.ban_members:
			embed = discord.Embed(title='Unban')
			embed.add_field(name='Error', value="I don't have permission to unban users. Please ask an administrator to fix this!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		if '<@' in member_id:
			member_id = int(member_id[2:-1].replace('!', ''))
		
		unbanned_member = await self.bot.fetch_user(member_id)
		if unbanned_member is None:
			embed = discord.Embed(title='Unban')
			embed.add_field(name='Error', value="This member doesn't exist!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		elif unbanned_member in ctx.guild.members:
			embed = discord.Embed(title='Unban')
			embed.add_field(name='Error', value="This member is in this server!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		elif unbanned_member == ctx.author:
			embed = discord.Embed(title='Unban')
			embed.add_field(name='Error', value="Silly goose, you can't unban yourself, especially if you're not already banned!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		try:
			unban_embed = discord.Embed(title='Unban', description=f"You've been unbanned from `{ctx.guild.name}`{f' for `{reason}`' if reason else ''}.")
			unban_embed.set_footer(text=ctx.guild.me.nick if ctx.guild.me.nick is not None else self.bot.user.name, icon_url=self.bot.user.avatar_url_as(static_format='png'))
			await unbanned_member.send(embed=unban_embed)

		except discord.errors.HTTPException:
			pass
	
		try:
			await ctx.guild.unban(unbanned_member, reason=reason)
		except discord.errors.Forbidden:
			embed = discord.Embed(title='Unban')
			embed.add_field(name='Error', value=f"You don't have permission to unban {unbanned_member.mention}.")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		embed = discord.Embed(title='Unban', description=f"{banned_member.mention} has been unbanned from `{ctx.guild.name}`{f' for `{reason}`' if reason else ''}.")
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

	@commands.command(aliases=['purge'])
	@commands.has_guild_permissions(manage_messages=True)
	@commands.guild_only()
	async def clear(self, ctx, amount: int):
		if not ctx.guild.me.guild_permissions.manage_messages:
			embed = discord.Embed(title=ctx.invoked_with.capitalize())
			embed.add_field(name='Error', value=f"I don't have permission to {ctx.invoked_with} messages. Please ask an administrator to fix this!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		await ctx.message.delete()
		await ctx.channel.purge(limit=amount)

		embed = discord.Embed(title=ctx.invoked_with.capitalize(), description=f"`{amount}` message{'s' if amount != 1 else ''} deleted.")
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		message = await ctx.send(embed=embed)

		await asyncio.sleep(3)
		await message.delete()

	@commands.command()
	@commands.guild_only()
	@commands.has_guild_permissions(mention_everyone=True)
	async def announce(self, ctx, *, message):
		if not ctx.guild.me.guild_permissions.mention_everyone:
			embed = discord.Embed(title='Announce')
			embed.add_field(name='Error', value="I don't have permission to announce messages. Please ask an administrator to fix this!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)

		embed = discord.Embed(title='Announcement', description=message)
		embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(static_format='png'))
		await ctx.send('@everyone', embed=embed)

def setup(bot):
	bot.add_cog(Mod(bot))
