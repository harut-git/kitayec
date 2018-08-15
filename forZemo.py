import json
import requests
import time
import websocket
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

import GameConfigs
from ImgCompare import is_equal


class Session(object):
    URL = "ws://eu-swarm-ws.betconstruct.com"

    def __init__(self, provider, username, password, vpn_country, lang='eng', site_id='4', url=None):
        request_session = {"command": "request_session",
                           "params": {
                               "language": lang,
                               "site_id": site_id
                           }
                           }

        # main parameters

        self.vpn_country = vpn_country
        self.site_id = site_id
        self.username = username
        self.password = password
        self.provider = provider
        self.ws = websocket.WebSocket()
        self.ws.connect(url or self.URL)
        self.call(request_session)
        login_response = self.login()
        self.token = login_response['data']['auth_token']
        get_user_response = self.get_user()
        profile = get_user_response['data']['data']['profile']
        profile_id = profile.keys()[0]
        self.balance = profile[profile_id]['balance']
        print self.balance

        # proxy settings

        # prox = Proxy()
        # prox.proxy_type = ProxyType.MANUAL
        # prox.http_proxy = self.vpn_country
        # prox.socks_proxy = self.vpn_country
        # prox.ssl_proxy = self.vpn_country
        # capabilities = webdriver.DesiredCapabilities.CHROME
        # prox.add_to_capabilities(capabilities)

        # ---------------------------------------------------------

        # Chrome Options

        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")

        # ---------------------------------------------------------

        self.driver = webdriver.Chrome(executable_path='/home/harut/Documents/chromedriver', options=chrome_options)

    def call(self, data):
        self.ws.send(json.dumps(data))
        response = json.loads(self.ws.recv())
        return response

    #

    def login(self):
        return self.call({"command": "login",
                          "params": {
                              "username": self.username,
                              "password": self.password
                          }
                          })

    def get_user(self):
        return self.call({"command": "get", "params": {"source": "user", "what": {"profile": []}, "subscribe": True},
                          "rid": "152785175500217"})

    def open_game(self, gameid):
        conf = getattr(GameConfigs, self.provider)

        self.driver.get("https://games.vbet.com/authorization.php?partnerId=4&gameId=" + gameid +
                        "&language=en&openType=real&devicetypeid=1&token=" + self.token)
        time.sleep(3)
        self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="gameFrame"]'))
        canvas = self.driver.find_element_by_tag_name('canvas')
        actions = ActionChains(self.driver)
        location = canvas.location
        size = canvas.size
        left = location['x']
        right = location['x'] + size['width']
        flag = True
        while flag:
            png = self.driver.get_screenshot_as_png()
            im = Image.open(BytesIO(png))
            im = im.crop((left, 50, right, 100))  # defines crop points
            im.save('current.png')  # saves new cropped image
            if not is_equal(self.provider + '.png', 'current.png'):
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

    def get_games(self):

        current_games_list = []
        link = "https://www.cmsbetconstruct.com/casino/getGames?partner_id=" + self.site_id + \
               "&lang=eng&provider=" + self.provider + "&country=AM&offset=0&limit=600"
        response = requests.get(link)
        games = response.json()['games']
        for i in games:
            current_games_list.append(i['extearnal_game_id'])
        return current_games_list


s = Session("TPG", "test8888", "Testik8888", "82.1.185.172:8080", site_id='4')
for i in s.get_games():
    s.open_game(i)
s.driver.close()
