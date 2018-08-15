from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType

prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.http_proxy = "82.1.185.172:8080"
prox.socks_proxy = "82.1.185.172:8080"
prox.ssl_proxy = "82.1.185.172:8080"

capabilities = webdriver.DesiredCapabilities.CHROME
prox.add_to_capabilities(capabilities)

driver = webdriver.Chrome(desired_capabilities=capabilities, executable_path="/home/harut/Documents/chromedriver")


driver.get('https://www.royalpanda.com/sports/')
driver.implicitly_wait(5)
