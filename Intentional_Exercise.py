# Importing get function from requests module #
from requests import get as get_request
# Getting CTF ID fron User #
ctf_id = input("[1] Enter your ctf id: ")
# Handling Exceptions #
try:
    # Getting Flag fron CTF #
    response = get_request(f"https://{ctf_id}.ctf.hacker101.com/appRoot/flagBearer?&hash=8743a18df6861ced0b7d472b34278dc29abba81b3fa4cf836013426d6256bd5e")
    # If flag found successfully print flag, if not then show error #
    if response.status_code == 200:
        print(f"\033[32m[2] Your flag is: {response.text}\033[0m")
    else:
        print("\033[33m[2] Wrong ctf id check and try again.\033[0m")
except Exception as e:
    # Printing Exception #
    print(f"\033[32m[2] {str(e)}\033[0m")