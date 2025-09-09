import requests
from dotenv import load_dotenv
import json
from time import sleep
import os

def get_access_token():
	load_dotenv()
	data = {
		"grant_type": "client_credentials",
		"client_id": os.getenv("UID"),
		"client_secret": os.getenv("SECRET")
	}
	response = requests.post(TOKEN_URL, data=data)
	if response.status_code == 200:
		token_data = response.json()
		access_token = token_data["access_token"]
		return (access_token)
	else:
		print("Error:", response.status_code, response.text)
		exit()

def get_endpoint_list(endpoint, access_token):
	elements_count = 0
	page = 1
	headers = {
		"Authorization": f"Bearer {access_token}" 
	}
	all_data = []
	while True:
		params = {"page": page, "per_page": 100}
		response = requests.get(BASE_URL + endpoint, headers=headers, params=params)
		if response.status_code != 200:
			print("Error:", response.status_code, response.text)
			break
		data = response.json()
		elements_count += len(data)
		if not data:
			break
		print(f"Page {page}")
		all_data.extend(data)
		page += 1
		sleep(0.5)
	print(f"Found {elements_count} elements")
	return all_data

def get_endpoint(endpoint, access_token):
	headers = {
		"Authorization": f"Bearer {access_token}" 
	}
	response = None
	while response is None or response.status_code == 429:
		response = requests.get(BASE_URL + endpoint, headers=headers)
		if response.status_code != 200 and response.status_code != 429:
			print(f"Error with {endpoint} : {response.status_code} {response.text}")
			return ""
	return response.json()

TOKEN_URL = "https://api.intra.42.fr/oauth/token"
BASE_URL = "https://api.intra.42.fr"
# BASE_URL = "https://intrapy.intra.42.fr"

USER_LIST_FILE = "userlist.json"
USER_INFO_FILE = "userinfo.json"
OUTPUT_FILE = "output.json"

CAMPUS_ID = "48"
POOL_YEAR = "2025"
POOL_MONTH = "september"

if (__name__ == "__main__"):

	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument("--update-user-list", action="store_true", help="Updates the list of users")
	parser.add_argument("--update-leaderboard", action="store_true", help="Updates the leaderboard")
	args = parser.parse_args()
	
	print("Requesting access token...")
	access_token = get_access_token()

	if (args.update_user_list):
		print(f"Updating users from campus {CAMPUS_ID}...")
		with open(USER_LIST_FILE, "w") as f:
			f.write(json.dumps(get_endpoint_list(f"/v2/campus/{CAMPUS_ID}/users", access_token)))

	if (args.update_leaderboard):
		print(f"Loading users from {USER_LIST_FILE}")
		with open(USER_LIST_FILE, "r") as f:
			campus_users_data = json.loads(f.read())

		print(f"Retrieving user from {POOL_MONTH} {POOL_YEAR}'s pool...")
		pool_users = []
		for user in campus_users_data:
			if (user.get("pool_month") == POOL_MONTH and user.get("pool_year") == POOL_YEAR):
				pool_users.append(user)
		print(f"Found {len(pool_users)}")

		counter = 0
		print("Requesting users level...")
		with open(USER_INFO_FILE, "w") as f:
			for user in pool_users:
				print(f"{counter} - {user.get("login")}")
				user_data = get_endpoint(f"/v2/users/{user.get("id")}/cursus_users", access_token)
				f.write(json.dumps(user_data))
				f.write("\n")
				counter += 1

	print(f"Loading user informations from {USER_INFO_FILE}")
	with open(USER_INFO_FILE, "r") as f:
		users_infos = []
		for line in f:
			users_infos.append(json.loads(line)[0])
	print("Sorting user by levels")
	leaderboard = sorted(users_infos, key=lambda user: user.get("level", 0), reverse=True)
	print(f"Writing output in {OUTPUT_FILE}")
	with open(OUTPUT_FILE, "w") as f:
		f.write(json.dumps(leaderboard))
	print("Done!")
