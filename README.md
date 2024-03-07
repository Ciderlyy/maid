# Project Inu Discord Bot

Welcome to Project Inu! This Discord bot is designed to provide various features for your server, including ticket creation, moderation commands, and more. This is my first time making a bot, so updates are to be expected.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [Commands](#commands)
- [Contributing](#contributing)
- [License](#license)

## Features

- Ticket creation system for support and other purposes.
- Moderation commands (ban, kick, mute, unmute).
- Role selection through reactions.
- Apex Coins information and promotion.

## Getting Started

### Prerequisites

- [Python](https://www.python.org/downloads/) (Version 3.8 or higher)
- [Git](https://git-scm.com/downloads/) (Optional but recommended)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/project-inu-discord-bot.git
   ```

2. Navigate to the project folder:

   ```bash
   cd project-inu-discord-bot
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

#### Configuration

1. Create a `config.json` file in the project root and fill in the required information:

   ```json
   {
     "token": "YOUR_DISCORD_BOT_TOKEN",
     "prefix": "!",
     "owner_id": "YOUR_DISCORD_USER_ID",
     "tickets_channel_id": "YOUR_TICKETS_CHANNEL_ID",
     "mod_logs_channel_id": "YOUR_MOD_LOGS_CHANNEL_ID"
   }
   ```

   - Replace placeholders with your actual values.

2. Run the bot:

   ```bash
   python bot.py
   ```

##### Usage

1. Invite the bot to your server.
2. Configure roles and channels as needed.
3. Start using commands and features.

### Commands

- `!help`: Display a list of available commands.
- `!rules`: Display server rules.
- `!ban @user [reason]`: Ban a user.
- `!kick @user [reason]`: Kick a user.
- `!mute @user [time]`: Mute a user for a specified duration.
- `!unmute @user`: Unmute a user.
- `!ticket`: Create a new support ticket.

### Contributing

Feel free to contribute to the project! Open issues for bug reports or new feature suggestions. Pull requests are welcome.

## License


This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Credits

- [Ciderlyy (GitHub)](https://github.com/Ciderlyy)
- Discord: Ciderly
```

Remember to replace placeholder texts such as `YOUR_DISCORD_BOT_TOKEN`, `YOUR_DISCORD_USER_ID`, `YOUR_TICKETS_CHANNEL_ID`, and `YOUR_MOD_LOGS_CHANNEL_ID` with your actual Discord bot token, user ID, and channel IDs.

Feel free to enhance or modify the README based on your project's unique features and requirements.

