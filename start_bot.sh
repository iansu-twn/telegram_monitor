pkill -f /Users/ian/Desktop/github/telegram_monitor/src/bot.py

source /Users/ian/Desktop/github/asset/bin/activate

nohup caffeinate -s /Users/ian/Desktop/github/asset/bin/python3 /Users/ian/Desktop/github/telegram_monitor/src/bot.py --keywords tsla tesla nvda nvidia pltr palantir 特斯拉 輝達 --exclude_group_keywords keyword > /Users/ian/Desktop/github/telegram_monitor/logs/bot.log 2>&1 &
