import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
import sys
import os
from multiprocessing import Pool, cpu_count

provider_map = {"MICROGAMING":"MGS"}


chromeOptions = webdriver.ChromeOptions()
prefs = {
    "profile.default_content_setting_values.plugins": 1,
    "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
    "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
    "PluginsAllowedForUrls": "https://www.vbet.com/#/casino/?lang=eng"
}
chromeOptions.add_experimental_option("prefs", prefs)
fdriver = webdriver.Chrome(chrome_options=chromeOptions, executable_path="/home/harut/Documents/chromedriver")
fdriver.get("https://www.vbet.com/#/casino/?lang=eng")
fdriver.maximize_window()
fdriver.implicitly_wait(10)

fdriver.find_element_by_xpath('//*[@id="signin-reg-buttons"]/ul/li[1]/button').click()
fdriver.find_element_by_xpath('//*[@id="signinform-login-input"]').send_keys("usd")
fdriver.find_element_by_xpath('//*[@id="signinform-password-input"]').send_keys("Testtest")
fdriver.find_element_by_xpath('//*[@id="block-slider-container"]/div[7]/div/div/div/div/div/div/div['
                                  '1]/div/div/div[1]/form/div[3]/button').click()
time.sleep(3)
fdriver.find_element_by_xpath("//div[@class='more-button-prviter-nav']//span").click()
fdriver.implicitly_wait(5)
provider_list = fdriver.find_elements_by_xpath("//div[@id='providerMenu']//li")
provider_list.pop(0)
providers = []
for l in provider_list:
    providers.append(l.text)
fdriver.close()


def providers_func(provider):
    if provider not in provider_map:
        return None
    driver =webdriver.Chrome(chrome_options=chromeOptions, executable_path="/home/harut/Documents/chromedriver")

    driver.get("https://www.vbet.com/#/casino/?lang=eng&category=all&provider="+provider_map[provider])
    driver.maximize_window()
    driver.implicitly_wait(10)


    driver.find_element_by_xpath('//*[@id="signin-reg-buttons"]/ul/li[1]/button').click()
    driver.find_element_by_xpath('//*[@id="signinform-login-input"]').send_keys("usd")
    driver.find_element_by_xpath('//*[@id="signinform-password-input"]').send_keys("Testtest")
    driver.find_element_by_xpath('//*[@id="block-slider-container"]/div[7]/div/div/div/div/div/div/div['
                                  '1]/div/div/div[1]/form/div[3]/button').click()
    time.sleep(3)
      # Removes All providers from providers list
    # provider_list.pop(0)  # Removes Netent provider
    # provider_list.pop(0)  # Removes DLV provider
    # provider_list.pop(0)  # Removes Betconstruct provider
    # provider_list.pop(0)  # Removes EGT provider
    # provider_list.pop(0)  # Removes Microgaming provider
    # provider_list.pop(0)  # Removes Spinomenal provider
    # provider_list.pop(0)  # Removes Pragmatic Play provider
    # provider_list.pop(0)  # Removes Booming games provider
    # provider_list.pop(0)  # Removes Fazi provider
    driver.implicitly_wait(20)

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(0.5)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    driver.execute_script("window.scrollTo(0, 0)")
    games_list = driver.find_elements_by_xpath('//*[@id="casinoScrollable"]/div[3]/div[2]/div/div['
                                                        '1]/div/ul/li')

    for game in games_list:
        print("Game name: " + game.text)
        hover = ActionChains(driver).move_to_element(game)
        hover.perform()
        time.sleep(5)

        try:
            if provider == "NETENT":
                game.click()
                try:
                    driver.switch_to.frame(driver.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/div/div/div/div/iframe'))
                    time.sleep(5)
                    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="gameFrame"]'))
                    time.sleep(5)
                    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="neGameClient"]'))
                    driver.find_element_by_xpath('//*[@id="undefined"]').click()  #Clicking on Continue button
                    time.sleep(3)
                    print("iframe is loaded successfully")
                except:
                    print("iframe isn't loaded successfully")
                    pass

            elif provider == "BETCONSTRUCT":
                game.click()
                try:
                    driver.switch_to.frame(driver.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/div/div/div/div/iframe'))
                    time.sleep(3)
                    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="gameFrame"]'))
                    time.sleep(5)
                    driver.find_element_by_xpath('//*[@id = "as-navigation"]/div[6]').click()  #Clicking on Spin button
                except:
                    print("iframe isn't loaded successfully")
                    pass

            elif provider == "EGT" or provider.text == "SPINOMENAL":
                game.click()
                try:
                    driver.switch_to.frame(driver.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/div/div/div/div/iframe'))
                    time.sleep(3)
                    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="gameFrame"]'))
                    time.sleep(5)
                    print("iframe is loaded successfully")
                    # Can't have access to buttons of the games
                except:
                    print("iframe isn't loaded successfully")
                    pass

            elif provider == "MICROGAMING":
                game.click()
                try:
                    driver.switch_to.frame(driver.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/div/div/div/div/iframe'))
                    time.sleep(3)
                    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="gameFrame"]'))
                    time.sleep(5)
                    # driver.find_element_by_xpath('//*[@id="tw-ui-layer"]/div/div/div[4]/div[4]/div').click()  # Clicking on Spin button
                    print("iframe is loaded successfully")
                except:
                    print("iframe isn't loaded successfully")
                    pass

            elif provider == "FAZI":
                game.click()
                try:
                    driver.switch_to.frame(driver.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/div/div/div/div/iframe'))
                    time.sleep(3)
                    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="gameFrame"]'))
                    time.sleep(5)
                    driver.find_element_by_xpath('//*[@id="cancel-audio"]').click()
                    time.sleep(3)
                    driver.find_element_by_xpath('//*[@id="start-button"]').click()  # Clicking on Spin button except Roulette game
                    print("iframe is loaded successfully")
                except:
                    print("iframe isn't loaded successfully")
                    pass

                # try:
                #     driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
                #     time.sleep(3)
                # except:
                #     pass
            elif provider == "DLV" or provider.text == "PRAGMATIC PLAY" or \
                            provider.text == "BOOMING GAMES" or provider.text == "NEXTGEN GAMING" or \
                            provider.text == "WORLDMATCH":
                try:
                    driver.switch_to.frame(driver.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/div/div/div/div/iframe'))
                    time.sleep(5)
                    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="gameFrame"]'))
                    time.sleep(5)
                    canvas = driver.find_element_by_tag_name('canvas')
                    # Can't have access to buttons of the games
                    print("iframe is loaded successfully")
                except:
                    print("iframe is loaded successfully")
                    pass

            elif provider == "RED TIGER":
                try:
                    driver.switch_to.frame(driver.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/div/div/div/div/iframe'))
                    time.sleep(5)
                    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="gameFrame"]'))
                    time.sleep(5)
                    driver.find_element_by_tag_name('canvas')
                    time.sleep(3)
                    # driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[1]/div[1]/div/div['
                    #                                   '1]/div/div[3]/div[2]/div[3]/div/div/div[1]/div['
                    #                                   '2]/i').click()  # Clicking on Spin button. This works for Laser Fruit game
                    print("iframe is loaded successfully")
                except:
                    print("iframe is loaded successfully")
                    pass


        except:
            print("iframe isn't loaded successfully")
            pass

        time.sleep(5)
        driver.switch_to.default_content()
        time.sleep(5)
        driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/div/div['
                                          '2]/div/div/div/div/div/div[1]/div[1]/a').click()
        time.sleep(2)


def provider_async():
    pool = Pool(cpu_count())
    pool.map(providers_func, providers)


provider_async()