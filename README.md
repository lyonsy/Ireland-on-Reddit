# Ireland-on-Reddit

A Reddit bot that monitors Reddit for mentions of Ireland and cross-posts them to [r/IrelandOnReddit](https://reddit.com/r/IrelandOnReddit).

I use [fly.io](https://fly.io) to deploy as with the hobby plan, it's free to run 3 256mb machines, which is more than enough for this app.

## Usage

See `app/config.py` for all available configuration options, including:

- Subreddits to monitor
- Expressions to watch for
- Wait time between checks

## Deploying with Fly.io

1. Install the Fly CLI:
   ```
   curl -L https://fly.io/install.sh | sh
   ```
   
   Or on macOS with Homebrew:
   ```
   brew install flyctl
   ```

2. Login to Fly:
   ```
   flyctl auth login
   ```

3. Deploy
   ```
   flyctl deploy
   ```
