import requests
from bs4 import BeautifulSoup

# Souping the main url.
url_main = 'http://www.owgr.com/ranking?pageNo=1&pageSize=All&country=All'
response = requests.get(url_main)
data = response.text
soup = BeautifulSoup(data, 'html.parser')

# Find the urls of each players.
urls_players = soup.find('table').find_all('a')
# print(len(urls_players))
# Records: 8869
i = 0
for url_players in urls_players:
    # Monitor the progress.
    i += 1
    print(i)
    # print('http://www.owgr.com/' + url_players.get('href'))
    # Tested. Good.

    # Souping each url of players.
    response_player = requests.get('http://www.owgr.com/' + url_players.get('href'))
    data_player = response_player.text
    soup_player = BeautifulSoup(data_player, 'html.parser')

    # Grab player's identity.
    href = url_players.get('href')
    position_equal = href.rfind('=')
    player_id = href[position_equal + 1:]
    player_name = soup_player.find('h2').text
    position_space = player_name.rfind(' ')
    p_lastname = player_name[position_space + 1:]
    p_othername = player_name[:position_space]
    # print(player_id, player_name, p_lastname, p_othername)

    # Find the required table.
    tables = soup_player.find_all('table')
    # print(len(tables))
    # Records: 3
    i_table = 0
    for table in tables:
        # Skip the first 2 tables.
        if i_table != 2:
            i_table += 1
            continue
        else:
            print(table)
            rows = table.find_all('tr')
            i_row = 0
            for row in rows:
                # Skip the last row (total).
                if i_row + 1 == len(rows):
                    break
                # Skip the first row (header).
                elif i_row == 0:
                    i_row += 1
                    continue
                else:
                    i_row += 1
                    # Belum selesai di sini. ==================================
    break
