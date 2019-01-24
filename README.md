# telegram-bot-namex
Building a Telegram bot to send history of prices for sugar contract on namex.org.
This bot will contain such main parts as:
1. The bot itself as a way to communicate with users, meaning getting requests and sending responses.
2. Database of history of prices (DB_prices_history).
3. Database of user requests.
4. Code to process requests.
4. Code to keep DB_prices_history updated.

2019-01-24
	How to handle with subscribtion to mailing list
Filter database table <user_data> column <user_request> by pattern <*@*.*> to choose e-mail addresses. Or use any more sofisticated took to pick up e-mail address.