# esmarket-media

## Installation & Setup
* **Install dependencies**
```shell
pip install -r requirements.txt
```
* **Configure .env file**
```shell
cp ./.env.example ./.env
```

## For developers
* **Format code to PEP standards**
```shell
inv format
```
* **Check code for bad blocks**
```shell
inv check
```
* **Create migrations by sqlalchemy models**
```shell
inv makemigartions some_message
```
* **Migrate migrations**
```shell
inv migrate
```

## Usage
* **Scrape players**
```python
from esmarket_media import ESMarketPlayers


players = ESMarketPlayers()
players.get(pages=1)  # set the count of web pages which should be scraped

print(players.scraped)  # Get scraped players as dict
print(players.serialize())  # Get serialized players
```