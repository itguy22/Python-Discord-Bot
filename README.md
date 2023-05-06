# My Discord Bot

This bot is a multi-purpose Discord bot that includes various commands and features to enhance your Discord server experience. Below is a list of some of the bot's functions:

## Commands

### `/ping`
Responds with "Pong!" to check if the bot is online and responsive.

### `/echo <message>`
Repeats the given message.

### `/serverinfo`
Displays information about the current server, such as the creation date, total members, human members, and bot members.

### `/poll <question> <option1> <option2> [<option3> ...]`
Creates a poll with the given question and options. You must provide at least two options and can have a maximum of 10 options.

### `/diceroll [sides]`
Rolls a dice with the specified number of sides (default is 6).

### `/trivia`
Starts a trivia game where the bot asks a multiple-choice question, and the user has to answer within 20 seconds.

### `/time <timezone>`
Displays the current time in the specified timezone.

### `/news <query>`
Fetches news articles related to the given query (requires a NewsAPI.org API key).

### `/remind <duration in seconds> <reminder text>`
Sets a reminder that will send a direct message to the user after the specified duration.

## Installation

To install and run the bot, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies with `pip install -r requirements.txt`.
3. Set your Discord bot token and NewsAPI.org API key in the script.
4. Run the bot script with `python your_bot_script.py`.

## Contributing

Feel free to submit a pull request or open an issue if you have any suggestions or encounter any issues.
