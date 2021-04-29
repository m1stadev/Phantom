from discord.ext import commands
import asyncio
import discord
import glob
import random


class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='8ball')
	@commands.guild_only()
	async def _8ball(self, ctx, *, question):
		responses = ('It is certain.',
					'It is decidedly so.',
					'Without a doubt.',
					'Yes - definitely.',
					'You may rely on it',
					'As I see it, yes.',
					'Most likely.',
					'Outlook good.',
					'Yes.',
					'Signs point to yes.',
					'Reply hazy, try again.',
					'Ask again later.',
					'Cannot predict now.',
					'Concentrate and ask again',
					"Don't count on it.",
					'My reply is no.',
					'My sources say no.',
					'Outlook not so good.',
					'Very doubtful.',
					'No.',
					'Most likely not',
					'Definitely not.',
					'Signs point to no.',
					'No - absolutely not.')

		embed = discord.Embed(title=':8ball: 8ball', description=random.choice(responses))
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

	@commands.command()
	@commands.guild_only()
	async def approve(self, ctx): await ctx.send(file=discord.File(random.choice(glob.glob('Assets/Reactions/reaction_*.mp4'))))

	@commands.command(aliases=['choice'])
	@commands.guild_only()
	async def choose(self, ctx, *, choices):
		choices = choices.split(', ')
		if len(choices) < 2:
			embed = discord.Embed(title='Choose')
			embed.add_field(name='Error', value='You only gave one choice!')
			await ctx.send(embed=embed)
			return

		embed = discord.Embed(title='Choose')
		embed.add_field(name='List of Choices:', value=f"**{'**, **'.join(choices)}**")
		embed.add_field(name='Selected Choice:', value=f'**{random.choice(choices)}**')
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

	@commands.command(aliases=['HOL'])
	@commands.guild_only()
	async def hol(self, ctx, guess):
		number = random.randint(1, 100)
		guesses = 1

		exit_embed = discord.Embed(title=':x: Higher or Lower :x:', description='Game quit.')
		higher_embed = discord.Embed(title=':arrow_up: Higher or Lower :arrow_down:', description=f':arrow_up: Higher :arrow_up:\n{ctx.author.mention}, guess a new number!\nType `cancel` to quit the game.')
		invalid_embed = discord.Embed(title=':arrow_up: Higher or Lower :arrow_down:')
		invalid_embed.add_field(name='Error', value='That is not a valid number between 1-100!')
		lower_embed = discord.Embed(title=':arrow_up: Higher or Lower :arrow_down:', description=f':arrow_down: Lower :arrow_down:\n{ctx.author.mention}, guess a new number!\nType `cancel` to quit the game.')
		timeout_embed = discord.Embed(title=':arrow_up: Higher or Lower :arrow_down:', description='No answer given in 1 minute, quitting.')

		for x in (exit_embed, higher_embed, invalid_embed, lower_embed, timeout_embed):
			x.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))

		try:
			guess = int(guess)
		except ValueError:
			await ctx.send(embed=invalid_embed)
			return

		if not 1 <= guess <= 100:
			await ctx.send(embed=invalid_embed)
			return

		if guess > number:
			game_message = await ctx.send(embed=lower_embed)
		elif guess < number:
			game_message = await ctx.send(embed=higher_embed)
		else:
			game_message = await ctx.send(embed=win_embed)

		while True:
			try:
				new_message = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
				guess = new_message.content
			except asyncio.exceptions.TimeoutError:
				await game_message.edit(embed=timeout_embed)
				return

			if guess == 'cancel':
				await game_message.edit(embed=exit_embed)
				await new_message.delete()
				return

			try:
				guess = int(guess)
			except ValueError:
				await ctx.send(embed=invalid_embed)
				await new_message.delete()
				return

			if not 1 <= guess <= 100:
				await ctx.send(embed=invalid_embed)
				await new_message.delete()
				return

			if guess < number:
				await game_message.edit(embed=higher_embed)
				guesses += 1
			elif guess > number:
				await game_message.edit(embed=lower_embed)
				guesses += 1
			else:
				win_embed = discord.Embed(title=':arrow_up: Higher or Lower :arrow_down:', description=f":tada: {ctx.author.mention}, you got it! The number was **{number}**!\n It took you **{guesses}** tr{'ies' if guesses != 1 else 'y'} to guess it correctly!")
				win_embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))

				await game_message.edit(embed=win_embed)
				await new_message.delete()
				return

			await new_message.delete()

	@commands.command()
	@commands.guild_only()
	async def love(self, ctx, member: discord.Member=None):
		if member:
			message = f'loves {member.mention} :flushed: :flushed:'
		else:
			message = 'love you too :kissing_heart: :kissing_heart:'
			
		await ctx.send(file=discord.File('Assets/Gifs/danny_love.gif'), content=f'{ctx.author.mention} {message}')

	@commands.command()
	@commands.guild_only()
	async def rps(self, ctx, answer):
		answer = answer.replace('paper', 'page_facing_up')
		rps_dict = {
			'rock': {
				'rock': 'We tied!',
				'page_facing_up': 'You lose!',
				'scissors': 'You win!'
			},
			'page_facing_up': {
				'rock': 'You win!',
				'page_facing_up': 'We tied!',
				'scissors': 'You lose!'
			},
			'scissors': {
				'rock': 'You lose!',
				'page_facing_up': 'You win!',
				'scissors': 'We tied!'
			}
		}

		bot_answer = random.choice(('rock', 'page_facing_up', 'scissors'))

		if answer not in ('rock', 'page_facing_up', 'scissors'):
			await ctx.send(f'Incorrect syntax you dumb fuck, use `{ctx.prefix}rps <rock/paper/scissors>`')
		
		embed = discord.Embed(title='Rock Paper Scissors', description=f'You chose :{answer}:, I chose :{bot_answer}:. {rps_dict[answer][bot_answer]}')
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Fun(bot))
