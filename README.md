# 42-leaderboard
My wonderful leaderboard script with some webdisplay

## Installation

Create the .env file with the variables UID and SECRET defined.

Then:

```sh
python -m venv env
```
```sh
source env/bin/activate
```
```sh
pip install -r requirements.txt
```
```sh
python leaderboard.py --update-user-list --update-leaderboard
```
Wait for it to finish...
```sh
python -m http.server 8000 
```
Then go to `localhost:8000` and enjoy!