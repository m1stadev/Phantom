from discord.ext import commands
import aiofiles
import aiohttp
import asyncio
import asynctempfile as tempfile #TODO: switch to aiofiles once 0.7.0 releases
import discord
import os
import shutil


class Emoji(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def download_file(self, url, filename):
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as response:
				async with aiofiles.open(filename, 'wb') as f:
					while True:
						chunk = await response.content.read(1024)
						if not chunk:
							break

						await f.write(chunk)

				await response.release()

	async def upload_to_pstyio(self, filepath, upload_name):
		async with aiofiles.open(filepath, 'rb') as f:
			async with aiohttp.ClientSession() as session:
				async with session.put(f'https://up.psty.io/{upload_name}', data=f) as response:
					resp = await response.text()
					await response.release()

		return resp.splitlines()[-1].split(':', 1)[1][1:]

	@commands.group(invoke_without_command=True)
	@commands.is_owner()
	async def emoji(self, ctx):
		if ctx.prefix == f'<@!{self.bot.user.id}> ':
			prefix = f'{ctx.prefix}`'
		else:
			prefix = f'`{ctx.prefix}'

		embed = discord.Embed(title='Emoji Commands')
		if ctx.guild.me.guild_permissions.manage_emojis:
			embed.add_field(name=f'{prefix}emoji add <name> <url>`', value='Add an emoji', inline=False)
			embed.add_field(name=f'{prefix}emoji delete <emoji>`', value='Delete an emoji', inline=False)
		embed.add_field(name=f'{prefix}emoji download`', value='Download all custom emojis', inline=False)
		embed.add_field(name=f'{prefix}emoji list`', value='List all emojis', inline=False)
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

	@emoji.command()
	@commands.guild_only()
	@commands.has_guild_permissions(manage_emojis=True)
	async def add(self, ctx, name, url):
		if not ctx.guild.me.guild_permissions.manage_emojis:
			embed = discord.Embed(title='Add Emoji')
			embed.add_field(name='Error', value="I don't have permission to add emojis. Please ask an administrator to fix this!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		filename = url.split('/')[-1].split('q')[0]

		async with tempfile.TemporaryDirectory() as tmp:
			await self.download_file(url, f'{tmp}/{filename}')

			async with aiofiles.open(f'{tmp}/{filename}', 'rb') as f:
				try:
					emoji = await ctx.guild.create_custom_emoji(name=name, image=await f.read())
				except discord.errors.HTTPException:
					embed = discord.Embed(title='Add Emoji')
					embed.add_field(name='Error', value='Failed to add emoji.')
					embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
					await ctx.send(embed=embed)
					return
	

		embed = discord.Embed(title='Add Emoji', description=f'Emoji {emoji} added.')
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

	@emoji.command()
	@commands.guild_only()
	@commands.has_guild_permissions(manage_emojis=True)
	async def delete(self, ctx, emoji: discord.Emoji):
		if not ctx.guild.me.guild_permissions.manage_emojis:
			embed = discord.Embed(title='Delete Emoji')
			embed.add_field(name='Error', value="I don't have permission to delete emojis. Please ask an administrator to fix this!")
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		await emoji.delete()

		embed = discord.Embed(title='Delete Emoji', description='Emoji deleted.')
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

	@emoji.command()
	@commands.guild_only()
	async def download(self, ctx):
		embed = discord.Embed(title='Emoji Download', description='Downloading all custom emojis. This may take a moment, please wait...')
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		message = await ctx.send(embed=embed)

		async with tempfile.TemporaryDirectory() as tmp:
			await asyncio.to_thread(os.makedirs, f'{tmp}/emojis/emojis')

			for emoji in ctx.guild.emojis:
				await emoji.url_as(static_format='png').save(f"{tmp}/emojis/emojis/{str(emoji.url_as(static_format='png')).split('/')[-1]}")

			await asyncio.to_thread(shutil.make_archive, f'{tmp}/emojis', 'zip', f'{tmp}/emojis')
			url = await self.upload_to_pstyio(f'{tmp}/emojis.zip', f'{ctx.guild.name}-emojis.zip')

		embed = discord.Embed(title='Emoji Download', description=f'[Download]({url})')
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))

		await message.edit(embed=embed)

	@emoji.command(name='list')
	@commands.guild_only()
	async def _list(self, ctx):
		split_emojis = [str()] # Combine emojis into strings that are under 1024 characters for embeds

		for emoji in ctx.guild.emojis:
			if len(split_emojis[-1]) + len(str(emoji)) > 1024:
				split_emojis.append(str())

			split_emojis[-1] += str(emoji)

		embed = discord.Embed(title='All Emojis', description=f'**{len(ctx.guild.emojis)}** total emojis in **{ctx.guild.name}**.')
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))

		for x in [x for x in range(len(split_emojis)) if split_emojis[x] != str()]:
			embed.add_field(name=f"Emojis{' (cont.)' if x != 0 else ''}", value=split_emojis[x], inline=False)

		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Emoji(bot))
