import time

import itertools
import requests
from PIL import Image
from io import BytesIO
from selenium import webdriver

from multiprocessing import Pool

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

import GameConfigs
from ImgCompare import is_equal

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(executable_path='/home/harut/Documents/chromedriver', options=chrome_options)


def open_game(gameid, provider):
    conf = getattr(GameConfigs, provider)
    driver.get("https://games.vbet.com/authorization.php?partnerId=4&gameId=" + gameid +
               "&language=en&openType=fun&devicetypeid=1")
    time.sleep(3)
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="gameFrame"]'))
    canvas = driver.find_element_by_tag_name('canvas')
    actions = ActionChains(driver)
    location = canvas.location
    size = canvas.size
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    flag = True
    while flag:
        png = driver.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        im = im.crop((left, 50, right, 100))  # defines crop points
        im.save('current.png')  # saves new cropped image
        if not is_equal('screenshot.png', 'current.png'):
            flag = False
            print "load ended"
    for k in conf[gameid]:
        x_offset = k[0]
        y_offset = k[1]
        actions.move_to_element_with_offset(canvas, x_offset, y_offset)
        actions.click_and_hold()
        actions.release()
        actions.perform()
        time.sleep(2)
    # game automation goes here...


def open_game_star(gameid_provider):
    return open_game(*gameid_provider)


def async_open_game(current_games_list, provider):
    pool = Pool(1)
    pool.map(open_game_star, itertools.izip(current_games_list, itertools.repeat(provider)))


def main_test(partner_id, provider):
    current_games_list = []
    link = "https://www.cmsbetconstruct.com/casino/getGames?partner_id=" + partner_id + \
           "&lang=eng&provider=" + provider + "&country=AM&offset=0&limit=600"
    response = requests.get(link)
    games = response.json()['games']
    for i in games:
        current_games_list.append(i['extearnal_game_id'])
    async_open_game(current_games_list, provider)


main_test("4", "TPG")
