import discord
import random
import aiohttp
import html
import asyncio
from discord.ext import commands
import pytz
from datetime import datetime

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True


async def get_bot_mention_prefix(bot, message):
    return [f'<@!{bot.user.id}> ', f'<@{bot.user.id}> ']

bot = commands.Bot(command_prefix=get_bot_mention_prefix, intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')


@bot.command()
async def echo(ctx, *, message: str):
    await ctx.send(message)


@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    server_age = (ctx.message.created_at - server.created_at).days
    member_count = len([member for member in server.members if not member.bot])

    embed = discord.Embed(
        title=server.name, description=f"Created {server_age} days ago", color=discord.Color.blue())
    embed.add_field(name="Total Members", value=str(server.member_count))
    embed.add_field(name="Human Members", value=str(member_count))
    embed.add_field(name="Bot Members", value=str(
        server.member_count - member_count))

    if server.icon:
        embed.set_thumbnail(url=server.icon.url)
    else:
        embed.set_thumbnail(url="https://via.placeholder.com/150")

    await ctx.send(embed=embed)


@bot.command()
async def poll(ctx, question, *options: str):
    if len(options) <= 1:
        await ctx.send("You must provide at least two options for the poll.")
        return
    if len(options) > 10:
        await ctx.send("You cannot have more than 10 options for a poll.")
        return

    emoji_numbers = [
        "\u0030\u20E3", "\u0031\u20E3", "\u0032\u20E3", "\u0033\u20E3", "\u0034\u20E3",
        "\u0035\u20E3", "\u0036\u20E3", "\u0037\u20E3", "\u0038\u20E3", "\u0039\u20E3"
    ]

    description = []
    for i, option in enumerate(options):
        description.append(f"{emoji_numbers[i+1]} {option}\n")

    embed = discord.Embed(title=question, description="".join(
        description), color=discord.Color.blue())
    poll_message = await ctx.send(embed=embed)

    for i in range(len(options)):
        await poll_message.add_reaction(emoji_numbers[i+1])


@bot.command()
async def diceroll(ctx, sides: int = 6):
    if sides < 1:
        await ctx.send("The number of sides must be at least 1.")
        return

    roll = random.randint(1, sides)
    await ctx.send(f"{ctx.author.mention} rolled a {roll} on a {sides}-sided dice.")


async def fetch_trivia_question():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            question_data = data['results'][0]

    return question_data


@bot.command()
async def trivia(ctx):
    while True:
        question_data = await fetch_trivia_question()
        question = html.unescape(question_data['question'])
        correct_answer = html.unescape(question_data['correct_answer'])
        incorrect_answers = [html.unescape(
            answer) for answer in question_data['incorrect_answers']]
        all_answers = [correct_answer] + incorrect_answers
        random.shuffle(all_answers)

        answer_options = "\n".join(
            [f"{i + 1}. {answer}" for i, answer in enumerate(all_answers)])

        await ctx.send(f"**Question:** {question}\n\n**Options:**\n{answer_options}")

        def answer_check(m):
            return m.author == ctx.author and m.content.isdigit() and 1 <= int(m.content) <= 4

        try:
            response = await bot.wait_for("message", check=answer_check, timeout=20)
        except asyncio.TimeoutError:
            await ctx.send(f"Time's up! The correct answer was: {correct_answer}")
        else:
            user_answer = all_answers[int(response.content) - 1]
            if user_answer == correct_answer:
                await ctx.send("Correct! Good job!")
            else:
                await ctx.send(f"Sorry, that's incorrect. The correct answer was: {correct_answer}")

        # Prompt the user to play again
        await ctx.send("Would you like to play again? (yes/no)")

        def play_again_check(m):
            return m.author == ctx.author and m.content.lower() in ['yes', 'no']

        try:
            play_again_response = await bot.wait_for('message', check=play_again_check, timeout=20)
            if play_again_response.content.lower() == 'no':
                await ctx.send("Thanks for playing!")
                break
        except asyncio.TimeoutError:
            await ctx.send("No response, ending the trivia game.")
            break


@bot.command()
async def time(ctx, timezone: str):
    try:
        target_timezone = pytz.timezone(timezone)
    except pytz.UnknownTimeZoneError:
        await ctx.send(f"Unknown timezone: {timezone}")
        return

    current_time = datetime.now(target_timezone)
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S %Z')
    embed = discord.Embed(
        title=f"Current Time in {timezone}",
        description=formatted_time,
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)


TOKEN = ''

bot.run(TOKEN)
