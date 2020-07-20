#!/usr/bin/env python
import sys
import configparser
import requests
import re
from bs4 import BeautifulSoup

config = configparser.ConfigParser()

try:
    config.read("mirkolisty.conf")
except configparser.MissingSectionHeaderError:
    print("Error: bad format of config file.")

option_list = {
    "baseurl_tag": None,
    "post_pattern": None,
    "how_many_last_posts_to_analyze": None,
    "how_many_upvotes_for_recent_posts": None,
    "how_many_upvotes_needed_for_prolonged_call": None,
    "detail_report": None,
    "baseurl_post": None,
    "voters_endpoint": None,
    "postid_regex": None,
    "login_regex": None,
}

there_was_config_error = False

for opt in option_list.keys():
    try:
        option_list[opt] = config['DEFAULT'][opt]
    except KeyError as exc:
        print("Error: missing config option: ", exc)
        there_was_config_error = True

if there_was_config_error:
    sys.exit(1)

req = requests.get(option_list.get("baseurl_tag"))
soup = BeautifulSoup(req.content, 'html.parser')
posts_html = soup.find_all('div', class_="lcontrast")
psoup = BeautifulSoup(str(posts_html), 'html.parser')

posts_found = 0
posts = []
for post in soup.find_all('div', class_="lcontrast"):
    if str(option_list.get("post_pattern")) in str(post):
        post_id_regex = re.search(option_list.get("postid_regex"), str(post))
        try:
            posts_found = posts_found + 1
            post_id = post_id_regex.group(1)
            posts.append(post_id)
        except AttributeError as exc:
            print("there is a problem with extracting post_id, exiting: ", exc)
            sys.exit(1)
    if posts_found == int(option_list.get("how_many_last_posts_to_analyze")):
        break

total_voters_found = dict()
voters_recent = []

first_analyzed_post = 0
temp_users_list = []

# We analyze from oldest to newest post (website gives us "normal" order)
posts.reverse()

for post_num, post_id in enumerate(posts):
    req = requests.get(option_list.get("voters_endpoint") + post_id)
    soup = BeautifulSoup(req.content, 'html.parser')

    for link in soup.find_all('a'):
        # Soup returns strange escape chars - TODO fix instead this shit
        html = str(link).replace('\/', '/')
        try:
            login_regex = re.search(option_list.get("login_regex"), html)
            wykop_login = login_regex.group(1)
            try:
                total_voters_found[wykop_login] = total_voters_found[wykop_login] + 1
            except KeyError:
                total_voters_found[wykop_login] = 1

            if len(posts)-post_num <= int(option_list.get("how_many_upvotes_for_recent_posts")):
                if first_analyzed_post == post_id or first_analyzed_post == 0:
                    first_analyzed_post = post_id
                    voters_recent.append(wykop_login)

                if first_analyzed_post != post_id and first_analyzed_post != 0:
                    if wykop_login in voters_recent:
                        temp_users_list.append(wykop_login)

        except AttributeError:
            pass

    if len(temp_users_list) > 0:
        voters_recent = [user for user in voters_recent if user in temp_users_list]
        temp_users_list = []

# Add recent voters to the call list
to_call_usernames = voters_recent

# Now add "prolonged" voters to the call list, skip duplicates
for username in total_voters_found.keys():
    if total_voters_found[username] > int(option_list.get("how_many_upvotes_needed_for_prolonged_call")):
        if username not in to_call_usernames:
            to_call_usernames.append(username)

# Posts list to mention
posts = [option_list.get("baseurl_post") + post_id for post_id in posts]

# How many users to call
how_many_users = len(to_call_usernames)

# Preparing the final message
try:
    to_call_usernames[0] = '@' + to_call_usernames[0]
    usernames = ' @'.join(to_call_usernames)
    analyzed_posts_report = ', '.join(posts)

    if option_list.get('detail_report') == 'off':
        post_message_with_call = usernames
    else:
        post_message_with_call = f'''
        Wołam **{how_many_users}** osób na podstawie algorytmu: wołanie za plusy dla {option_list.get("how_many_upvotes_for_recent_posts")} ostatnich materiałów lub plusy dla 
        minimum {option_list.get("how_many_upvotes_needed_for_prolonged_call")} z {option_list.get("how_many_last_posts_to_analyze")} ostatnich materiałów. Jeśli plusowałeś/aś tylko {option_list.get("how_many_upvotes_for_recent_posts")} ostatnie materiały - nie plusuj posta 
        rozpoczynającego ten wątek, aby wyłączyć wołanie przy kolejnych wpisach. 

        Jeśli plusowałeś/aś {option_list.get("how_many_upvotes_needed_for_prolonged_call")} (lub więcej) poprzednich materiałów - nie plusuj tego i 
        ewentualnego kolejnego rozpoczynającego posta wątku, aby wyłączyć to wołanie.

        Wołanych wytypowano na podstawie analizy plusów dla tych wpisów: {analyzed_posts_report}

        Analizowano jedynie wpisy, które mają w treści: **{option_list.get("post_pattern")}**

        Wołam: {usernames}
        '''
except IndexError:
    post_message_with_call = "Nikogo nie wołam na podstawie takiej konfiguracji lub nikt nie plusuje :-("

print(post_message_with_call)
