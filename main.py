import time
from selenium import webdriver

# proxyHost = "www.16yun.cn"
# proxyPort = "3111"
# proxyUser = "16YUN"
# proxyPass = "16IP"

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument(f'--proxy-server=http://{proxyUser}:{proxyPass}@{proxyHost}:{proxyPort}')
driver = webdriver.Chrome()    # options=chrome_options

driver.get('https://developer.aliyun.com/article/1291010')

time.sleep(5)

driver.close()
