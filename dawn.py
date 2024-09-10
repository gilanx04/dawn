import requests
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

keepalive_url = "https://www.aeropres.in/chromeapi/dawn/v1/userreward/keepalive"
get_points_url = "https://www.aeropres.in/api/atom/v1/userreferral/getpoint"

def display_welcome_message():
    print(r"""
       _ _                  _____    ___ 
      (_) |                |  _  |  /   |
  __ _ _| | __ _ _ __ __  _| |/' | / /| |
 / _` | | |/ _` | '_ \\ \/ /  /| |/ /_| |
| (_| | | | (_| | | | |>  <\ |_/ /\___  |
 \__, |_|_|\__,_|_| |_/_/\_\\___/     |_/
  __/ |                                  
 |___/                                   
    """)

def read_data_file(filename):
    accounts = []
    with open(filename, 'r') as file:
        for line in file:
            email, token = line.strip().split('|')
            accounts.append({'email': email, 'token': token})
    return accounts

def get_total_points(headers):
    try:
        response = requests.get(get_points_url, headers=headers, verify=False)
        if response.status_code == 200:
            json_response = response.json()
            if json_response.get("status"):
                reward_point_data = json_response["data"]["rewardPoint"]
                referral_point_data = json_response["data"]["referralPoint"]

                total_points = (
                    reward_point_data.get("points", 0) +
                    reward_point_data.get("registerpoints", 0) +
                    reward_point_data.get("signinpoints", 0) +
                    reward_point_data.get("twitter_x_id_points", 0) +
                    reward_point_data.get("discordid_points", 0) +
                    reward_point_data.get("telegramid_points", 0) +
                    reward_point_data.get("bonus_points", 0) +
                    referral_point_data.get("commission", 0)
                )
                
                return total_points
            else:
                print(f"\033[91mError fetching points: {json_response.get('message', 'Unknown error')}\033[0m")
        else:
            print(f"\033[91mFailed to retrieve points. Status code: {response.status_code}\033[0m")  # Red
    except requests.exceptions.RequestException as e:
        print(f"\033[91mAn error occurred while fetching points: {e}\033[0m")
    return 0

def make_request(headers, email):
    keepalive_payload = {
        "username": email,
        "extensionid": "fpdkjdnhkakefebpekbdhillbhonfjjp",
        "numberoftabs": 0,
        "_v": "1.0.7"
    }
    
    try:
        response = requests.post(keepalive_url, headers=headers, json=keepalive_payload, verify=False)
        print(f"Status Code: \033[94m{response.status_code}\033[0m")

        if response.status_code == 200:
            json_response = response.json()
            if 'message' in json_response:
                print(f"\033[92mSukses: {json_response['message']}\033[0m")
                return True
            else:
                print("\033[91mMessage not found in response.\033[0m")
        
        elif response.status_code == 502:
            print("\033[93m502 Bad Gateway. gpp nanti bisa, lanjut aja ke akun berikutnya...\033[0m")

        return False
    except requests.exceptions.RequestException as e:
        print(f"\033[91mAn error occurred: {e}\033[0m") 
        return False

def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"\033[95mRestarting in: {i} seconds\033[0m", end='\r')
        time.sleep(1)
    print("\n\033[92mRestarting the process...\033[0m\n")

def main():
    display_welcome_message() 
    while True:
        accounts = read_data_file("data.txt")
        total_accumulated_points = 0

        for account in accounts:
            email = account['email']
            token = account['token']

            headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
            }

            print(f"\033[96mMemproses akun: {email}\033[0m") 

            points = get_total_points(headers)
            total_accumulated_points += points

            success = make_request(headers, email)
            if success:
                print(f"\033[92mRequest untuk {email} sukses.\033[0m\n")
            else:
                print(f"\033[91mRequest untuk {email} gagal bjir.\033[0m\n")

        print(f"\033[93mSemua akun telah diproses.\033[0m")
        print(f"\033[92mTotal poin dari semua user: {total_accumulated_points}\033[0m")
        countdown(181)

if __name__ == "__main__":
    main()
