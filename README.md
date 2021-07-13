# Phantom
Phantom is my personal Discord bot written with [discord.py](https://discordpy.readthedocs.io/en/stable/) aimed at replacing the functionality of other major Discord bots!

You can invite Phantom into any Discord server using [this](https://discord.com/api/oauth2/authorize?client_id=736756253333913670&permissions=1279257670&scope=bot) link.

## Setup
To host your own instance, you'll need a Discord bot with "Server Members" intent enabled.

1. Download the project using Git (or any other method)

2. Install the required Python libraries. You'll need Python 3.9 or later

        # Linux/macOS
        pip3 install -U -r requirements.txt

        # Windows
        pip install -U -r requirements.txt

    You might want to create and use a virtual environment before installing the requirements

        # Linux/macOS
        python3 -m venv --upgrade-deps env; source env/bin/activate

        # Windows
        py -m venv --upgrade-deps env; .\env\Scripts\activate

3. Set the `PHANTOM_TOKEN` environment variable to your token

    For Linux/macOS, you can export the variable inside your shell configuration file

    For Windows, you'll need to find a way to get to your "Environment Variables" panel. It can be found within Control Panel

4. Run the bot script

        # Linux/macOS
        python3 bot.py

        # Windows
        py bot.py

    If everything was set up correctly, your instance should start

## Support
For any questions/issues you have, join my [Discord](https://m1sta.xyz/discord) server.
