from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

# region Methods

def parse_players():
    players_link_list = find_players()
    player_career_list = []
    for link in players_link_list:
        driver.get(link)
        time.sleep(2)
        player_meta = driver.find_element(By.ID, "meta")
        player_name = player_meta.find_element(By.TAG_NAME, "span").text
        if len(driver.find_elements(By.ID, "div_per_game")) == 0:
            print(link)
            continue
        content = driver.find_element(By.ID, "div_per_game")
        table = content.find_element(By.TAG_NAME, "table")
        careerTable = table.find_element(By.TAG_NAME, "tbody")
        tr = careerTable.find_elements(By.TAG_NAME, "tr")
        print(link)
        for tr in tr:
            player_data = []
            try:
                player_data.append(player_name)
                player_data.append(tr.find_element(By.TAG_NAME, "th").text)
                td = tr.find_elements(By.TAG_NAME, "td")
                for td in td:
                    player_data.append(td.text)
            except Exception as e:
                print(e)
            player_career_list.append(player_data)

    return player_career_list



def save_to_csv(career_list, filename="career_data.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ['Name', 'Season', 'Age', 'Team', 'League', 'Position', 'Games', 'Games Started', 'Minutes Played Per Game',
                  'Field Goals Per Game', 'Field Goal Attempts Per Game', 'Field Goal Percentage', '3-Point Field Goals Per Game',
                  '3-Point Field Goals Attempts Per Game', '3-Point Field Goals Percentage', '2-Point Field Goals Per Game',
                  '2-Point Field Goals Attempts Per Game', '2-Point Field Goals Percentage', 'Effective Field Goals Percentage',
                  'Free Throws Per Game', 'Free Throws Attempts Per Game', 'Free Throws Percentage', 'Offensive Rebounds Per Game',
                  'Defensive Rebounds Per Game', 'Total Rebounds Per Game', 'Assists Per Game', 'Steals Per Game',
                  'Blocks Per Game', 'Turnovers Per Game', 'Personal Fouls Per Game', 'Points Per Game', 'Awards']
        writer.writerow(header)

        for row in career_list:
            writer.writerow(row)
    print(filename)



def find_players():
    season_link_list = find_teams_season()
    players_link_list = []
    for link in season_link_list:
        driver.get(link)
        time.sleep(2)
        content = driver.find_element(By.ID, "div_roster")
        table = content.find_element(By.TAG_NAME, "table")
        playersTable = table.find_element(By.TAG_NAME, "tbody")
        tr = playersTable.find_elements(By.TAG_NAME, "tr")
        for t in tr:
            a = t.find_element(By.TAG_NAME, "a")
            playerLink = a.get_attribute("href")
            players_link_list.append(playerLink)
    print(players_link_list)
    print(len(players_link_list))
    return players_link_list



def find_teams_season():
    teams_link_list = get_teams_links()
    season_link_list = []
    for link in teams_link_list:
        driver.get(link)
        time.sleep(2)
        content = driver.find_element(By.ID, "content")
        table = content.find_element(By.TAG_NAME, "table")
        teamTable = table.find_element(By.TAG_NAME, "tbody")
        row = teamTable.find_element(By.TAG_NAME, "tr")
        a = row.find_element(By.TAG_NAME, "a")
        seasonLink = a.get_attribute("href")
        season_link_list.append(seasonLink)
    print(season_link_list)
    return season_link_list



def get_teams_links():
    table = driver.find_element(By.ID, "div_teams_active")
    mainTable = table.find_element(By.TAG_NAME, "tbody")
    rows = mainTable.find_elements(By.CLASS_NAME, "full_table")
    print(len(rows))

    teams_link_list = []
    for row in rows:
        a = row.find_element(By.TAG_NAME, "a")
        teamLink = a.get_attribute("href")
        teams_link_list.append(teamLink)
    print(teams_link_list)
    return teams_link_list

# endregion
driver = webdriver.Chrome()

try:
    driver.get("https://www.basketball-reference.com/teams/")
    career_list = parse_players()
    save_to_csv(career_list, "career_data_new.csv")
except Exception as e:
    print(e)
finally:
    driver.quit()