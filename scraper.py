import bs4 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date 
import time 
import random

def setup_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu') 
    driver = webdriver.Chrome('{Insert path for chromedrive}', chrome_options=options)
    return driver 

def get_scores(game, total_drives): 
    week = get_week()
    if(week > 17):
        week = 'post-' + week - 17

    else: 
        week = 'reg-' + week 
    year = date.today().year
    teams = game.split(' at ') 
    url = f'https://www.nfl.com/games/{teams[0]}-at-{teams[1]}-{year}-{week}'
    print(url)
    driver = setup_driver()
    driver.get(url)
    time.sleep(3)
    html = driver.execute_script("return document.documentElement.outerHTML")
    page = bs4.BeautifulSoup(html, 'lxml')
    score = page.find_all("div" , {"class": "css-1hyoz7m"})
    score = score[0].text + ' ' + '-' + ' ' + score[1].text
    drives = page.find_all("div" , {"class": "css-view-1dbjc4n r-backgroundColor-14lw9ot r-flex-kgf08f r-flexDirection-18u37iz r-position-bnwqim r-width-13qz1uu"})
    if(len(drives) <= total_drives):
        return -1 
    id_team = page.find_all("div", {"class": ["css-view-1dbjc4n r-borderLeftColor-855088 r-borderRightColor-114ovsg r-borderStyle-1phboty r-height-1pi2tsx r-left-1d2f490 r-position-u8s1d", "css-view-1dbjc4n r-borderLeftColor-855088 r-borderRightColor-114ovsg r-borderStyle-1phboty r-height-1pi2tsx r-position-u8s1d r-right-zchlnj"] })
    
    drives = drives[total_drives: len(drives)]
    id_team = id_team[total_drives: len(id_team)]
   

    result = []
    for d, i in zip(drives, id_team):
        if(i['class'][-1] == 'r-position-u8s1d'):
            x = 0 
        else:
            x = 1  
        drive = d.get_text(separator = '/')
        drive = drive.split('/')
        result.append([ teams[x], drive[0],  drive[1], drive[3], drive[5], drive[7], len(drives)])

    driver.quit()
    return [score, result]

def get_week():
    season_start = date(2020, 9, 7)
    days = season_start - date.today()

    if(days % 7 != 0):
        week =  int(days/7) + 1

    else:
        week =  int(days/7)

def active_games():
    week = get_week()
    year = date.today().year
    if(week > 17):
        week = 'POST' + week - 17

    else: 
        week = 'REG' + week 
    url = f"https://www.nfl.com/scores/{year}/{week}"
    driver = setup_driver()
    driver.get(url)
    time.sleep(3)
    html = driver.execute_script("return document.documentElement.outerHTML")
    page = bs4.BeautifulSoup(html, 'lxml')
    games = page.find_all("div", {"class" : "css-text-901oao r-color-1khnkhu r-fontFamily-1fdbu1n r-fontSize-ubezar" })
    result = []
    for i in range(0, len(games) - 1, 2): 
       result.append(games[i].text + ' at ' + games[i+1].text) 

    driver.quit()

    return result 


def exercise():
    exercises = ['Pushups: ', 'Plank: ', 'Situps: ', 'Squats: ', 'Wall Sit: ']
    exercise = random.choice(exercises)
    reps = str(random.randrange(1,60))
    if(exercise == 'Plank: ' or exercise == 'Wall Sit: '): 
        return exercise + reps + ' seconds'

    else: 
        return exercise + reps + ' reps'




