# Halloween Discord Bot

## Overview

This is a Discord bot built with Python that implements a Halloween-themed gamification system. The bot reacts to messages with random Halloween emojis (ghosts, zombies, skulls, knives, wolves, and pumpkins) at variable intervals. Each emoji has different rarity levels and point values, creating an engaging collection game for server members. The bot includes a Flask web server for health monitoring and keepalive functionality, making it suitable for deployment on cloud platforms like Render or Replit.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Structure

The application follows a simple modular architecture with two main components:

**Bot Module (`bot.py`)**: The core Discord bot implementation that handles message events, emoji reactions, user data tracking, and game logic. This is the main entry point that runs the Discord client.

**Web Server Module (`app.py`)**: A lightweight Flask application providing HTTP endpoints for health checks and keepalive functionality. This runs in a separate daemon thread to maintain bot uptime on hosting platforms that require active HTTP services.

### Game Mechanics Design

**Probability-Based Reward System**: Uses a weighted random selection algorithm with cumulative probability distribution. Each emoji has a different spawn rate (ranging from 40% for common ghosts to 0.09% for rare pumpkins) and corresponding point values (4-31 points). This creates a balanced risk/reward economy.

**Variable Reaction Intervals**: The bot triggers reactions at random message intervals (15-30 messages) rather than fixed timing, preventing predictability and maintaining user engagement.

**Persistent Data Storage**: User statistics (points, collections, achievements) are stored in a JSON file (`data.json`) using file-based persistence. This approach was chosen for simplicity over database solutions, suitable for small to medium-scale Discord servers.

### Discord Integration

**Intent Configuration**: Uses specific Discord gateway intents (guilds, guild_messages, message_content) to minimize unnecessary event processing and reduce resource usage. The bot requires message content intent to track message counts for reaction triggers.

**Command Prefix System**: Implements a command-based interface with `!` prefix for user interactions. The default help command is disabled, suggesting custom help implementation.

**Event-Driven Architecture**: Relies on Discord.py's event loop to handle asynchronous message processing and reactions. The bot monitors all messages to increment counters and trigger emoji reactions at appropriate intervals.

### Deployment Strategy

**Multi-Threading Approach**: The Flask web server runs in a daemon thread separate from the main Discord bot thread. This allows simultaneous operation of HTTP endpoints and Discord event handling without blocking.

**Health Check Endpoints**: Provides two HTTP endpoints (`/` and `/health`) that return status confirmations. These are essential for:
- Platform keepalive requirements (prevents dyno/container sleep)
- Monitoring and alerting systems
- Load balancer health checks

**Port Configuration**: Web server binds to `0.0.0.0:5000`, making it accessible from external networks. The Render deployment configuration suggests cloud platform compatibility.

### Data Flow

1. Discord messages increment a global counter
2. When counter matches random threshold, emoji selection occurs
3. Weighted random algorithm selects emoji based on probability distribution
4. Bot reacts to message with selected emoji
5. User reaction events would trigger data updates (implementation appears incomplete in provided code)
6. User data persists to JSON file
7. Counter resets with new random threshold

### Error Handling & Resilience

The data loading function includes try-except blocks for graceful handling of missing or corrupted data files. The daemon thread approach ensures the web server continues running even if it encounters errors, maintaining platform connectivity.

## External Dependencies

### Core Framework
- **discord.py (v2.3.2)**: Official Discord API wrapper for Python, provides bot framework, event handling, and gateway connection management

### Web Server
- **Flask (v3.0.0)**: Lightweight WSGI web application framework used for health check endpoints and keepalive server

### HTTP Client Libraries
- **requests (v2.32.0)**: HTTP library for potential webhook calls or external API interactions
- **aiohttp (v3.12.15)**: Asynchronous HTTP client/server framework, likely used by discord.py for async operations

### Standard Library Dependencies
- **json**: User data serialization and persistence
- **random**: Probability-based emoji selection and interval randomization
- **threading**: Multi-threaded execution for web server
- **pathlib**: Cross-platform file path handling

### Platform Integration
- **Render**: Cloud deployment platform (configuration in `render.yaml`)
  - Worker service type for continuous bot operation
  - Environment variable for Discord bot token
  - Python 3.11 runtime environment

### Environment Configuration
- **DISCORD_TOKEN**: Required environment variable for bot authentication (must be provided securely through platform settings)