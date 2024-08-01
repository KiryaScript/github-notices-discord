# GitHub-Discord Update Bot

Этот бот отслеживает обновления в указанных GitHub репозиториях и отправляет уведомления о новых коммитах в Discord канал.

## Возможности

- Отслеживание нескольких GitHub репозиториев
- Отправка уведомлений о новых коммитах в Discord
- Отображение информации о коммите, включая автора, сообщение и измененные файлы
- Логирование действий бота
- Проверка ограничений GitHub API

## Установка

1. Клонируйте репозиторий:
   git clone https://github.com/KiryaScript/github-notices-discord.git
   
   cd github-notices-discord

2. Установите зависимости:

pip install -r requirements.txt

3. Создайте файл .env в корневой директории проекта и добавьте следующие переменные:

DISCORD_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_discord_channel_id

## Настройка

В файле bot.py измените следующие переменные в соответствии с вашими репозиториями:

GITHUB_OWNER = "YourGitHubUsername"
GITHUB_REPO1 = "your-repo-1"
GITHUB_REPO2 = "your-repo-2"
GITHUB_REPO3 = "your-repo-3"

## При необходимости настройте интервал проверки обновлений, изменив значение в строке:

await asyncio.sleep(30)

## Запуск
Запустите бота командой:

# python bot.py

## Логи

Логи бота сохраняются в файл bot.log в директории проекта.
