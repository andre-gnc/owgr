import requests
import xlsxwriter
from bs4 import BeautifulSoup


def make_soup(ms_url):
    # Make soups of each url.
    response = requests.get(ms_url)
    data = response.text
    ms_soup = BeautifulSoup(data, 'html.parser')
    return ms_soup


def xlsxwriter_write(xw_items, xw_index_row, xw_worksheet, xw_start, xw_format):
    for xw_counter_col, xw_item in enumerate(xw_items, xw_start):
        xw_worksheet.write(xw_index_row, xw_counter_col, xw_item, xw_format)


GENDER = 'Male'

workbook = xlsxwriter.Workbook('data.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})
index_row = 0

# Write the headers.
col_headers = ('Player ID', 'Player Name', 'Last name', 'Other Name', 'Gender', 'Year', 'Events Played', '1st',
               '2nd', '3rd', '4th-10th', 'MC', 'Year End Rank')
xlsxwriter_write(col_headers, index_row, worksheet, 0, bold)

url_main = 'http://www.owgr.com/ranking?pageNo=1&pageSize=All&country=All'

soup = make_soup(url_main)

# Find the urls of each players.
urls_players = soup.find('table').find_all('a')

for counter_up, url_players in enumerate(urls_players, 1):
    # Monitor the progress.
    print(counter_up)

    soup_player = make_soup('http://www.owgr.com/' + url_players.get('href'))

    # Grab player's identity.
    href = url_players.get('href')
    position_equal = href.rfind('=')
    player_id = href[position_equal + 1:]
    player_name = soup_player.find('h2').text
    position_space = player_name.rfind(' ')
    p_lastname = player_name[position_space + 1:]
    p_othername = player_name[:position_space]

    value_cols = [player_id, player_name, p_lastname, p_othername, GENDER]

    # Find the required table.
    tables = soup_player.find_all('table')
    for counter_tables, table in enumerate(tables, 1):
        # The required table is the 3rd.
        if counter_tables != 3:
            continue
        else:
            rows = table.find_all('tr')

            # Remove the last row (Total).
            rows.pop()

            for counter_row, row in enumerate(rows, 1):
                # The required rows are from the 2nd.
                # Skip the header.
                if counter_row == 1:
                    continue
                else:
                    index_row += 1

                    # Write the values of the first 5 columns.
                    xlsxwriter_write(value_cols, index_row, worksheet, 0, None)

                    column_urls = row.find_all('td')
                    columns = []
                    # Get the content as text from each column.
                    for column_url in column_urls:
                        columns.append(column_url.text)

                    # Write the last values of other columns from the 6th.
                    # It's 5 since start at 0.
                    xlsxwriter_write(columns, index_row, worksheet, 5, None)
    break
workbook.close()
