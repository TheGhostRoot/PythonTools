import discord
import json

client = discord.Client(intents=discord.Intents.all())
#------------------------
channel_id = 1038922375615492197 # sends application to when it is done
token = ""
# ------------------------
prefix = '?'
questions = {
    1: "How old are you?",
    2: "How are you today?",
    3: "What is 9+1?",
    4: "What is your name?"
}
max_questions = len(questions)
is_open = True

@client.event
async def on_message(message):
    global is_open
    if not message.content.startswith(prefix) or message.author.bot:
        return

    args = message.content[len(prefix):].split()
    command = args.pop(0).lower()

    if command == 'apply':
        if not is_open:
            await message.channel.send("Applications are currently closed.")
            return

        user = await message.author.create_dm()
        await user.send("Hey! Your application has started. You have 300 seconds to complete it.")

        application = {'userId': message.author.id}
        for i in range(1, max_questions+1):
            embed = discord.Embed(title=f'Question [{i}/{max_questions}]', description=questions[i])
            await user.send(embed=embed)
            response = await client.wait_for('message', check=lambda m: m.author == message.author and m.channel == user, timeout=300)
            application[f'question{i}'] = response.content

        try:
            with open('applications.json', 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(application)
        with open('applications.json', 'w') as f:
            json.dump(data, f)

        channel = client.get_channel(channel_id)
        embed = discord.Embed(title='Application: ' + message.author.display_name)
        for i in range(1, max_questions+1):
            embed.add_field(name=f'Question {i}: ', value=application[f'question{i}'], inline=False)
        await channel.send(embed=embed)

        await user.send('Thank you for applying!')

    elif command == 'open' and message.author.guild_permissions.administrator:
        is_open = True
        await message.channel.send("Applications are now open.")

    elif command == 'close' and message.author.guild_permissions.administrator:
        is_open = False
        await message.channel.send("Applications are now closed.")

client.run(token)