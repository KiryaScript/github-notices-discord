import requests
import discord
import asyncio
import os
import logging
import json
from dotenv import load_dotenv
import threading

load_dotenv()

logging.basicConfig(filename='bot.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/commits"
GITHUB_OWNER = "KiryaScript"
GITHUB_REPO1 = "kir-browser"
GITHUB_REPO2 = "github-notices-discord"

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def check_rate_limit():
    response = requests.get("https://api.github.com/rate_limit")
    if response.status_code == 200:
        data = response.json()
        remaining = data['resources']['core']['remaining']
        if remaining < 10:
            logging.warning(f"GitHub API rate limit is low: {remaining} requests remaining")
    else:
        logging.error("Failed to check GitHub API rate limit")

def load_last_commits():
    try:
        with open('last_commits.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_last_commits(commits):
    with open('last_commits.json', 'w') as f:
        json.dump(commits, f)

async def check_github_updates():
    await client.wait_until_ready()
    discord_channel = client.get_channel(DISCORD_CHANNEL_ID)
    
    last_commits = load_last_commits()

    while not client.is_closed():
        try:
            check_rate_limit()

            for repo in [GITHUB_REPO1, GITHUB_REPO2]:
                logging.info(f"Checking updates for {repo}")
                response = requests.get(GITHUB_API_URL.format(owner=GITHUB_OWNER, repo=repo))
                commits = response.json()

                if commits and isinstance(commits, list) and commits[0]['sha'] != last_commits.get(repo):
                    last_commits[repo] = commits[0]['sha']
                    await send_update(discord_channel, commits[0], repo)
                    save_last_commits(last_commits)

        except Exception as e:
            logging.error(f"Error occurred: {e}")

        await asyncio.sleep(30)

async def send_update(discord_channel, commit, repo):
    commit_message = commit['commit']['message']
    commit_url = commit['html_url']
    author = commit['commit']['author']['name']

    embed = discord.Embed(
        title="Новый коммит в репозитории GitHub",
        description=f"Репозиторий: {GITHUB_OWNER}/{repo}",
        color=discord.Color.blue()
    )
    embed.add_field(name="Автор", value=author, inline=False)
    embed.add_field(name="Сообщение", value=commit_message, inline=False)
    embed.add_field(name="URL", value=commit_url, inline=False)

    # Добавляем информацию об измененных файлах
    files_changed = commit.get('files', [])
    if files_changed:
        files_list = "\n".join([f.get('filename', 'Unknown file') for f in files_changed[:5]])
        embed.add_field(name="Измененные файлы (до 5)", value=files_list, inline=False)

# отправка
    try:
        await discord_channel.send(embed=embed)
    except discord.errors.HTTPException as e:
        logging.error(f"Failed to send message to Discord: {e}")
    except Exception as e:
        logging.error(f"Unexpected error when sending message to Discord: {e}")

async def send_message(channel_id, message):
    channel = client.get_channel(int(channel_id))
    if channel:
        await channel.send(message)
        print(f"Сообщение отправлено в канал {channel.name}")
    else:
        print("Канал не найден")

def user_input():
    while True:
        channel_id = input("Введите ID канала: ")
        message = input("Введите сообщение: ")
        asyncio.run_coroutine_threadsafe(send_message(channel_id, message), client.loop)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    logging.info(f'Bot {client.user} has connected to Discord!')
    client.loop.create_task(check_github_updates())
    
    # Запускаем поток для пользовательского ввода
    threading.Thread(target=user_input, daemon=True).start()

client.run(DISCORD_TOKEN)