import time
import zipfile
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from threading import Thread

from concurrent.futures import ThreadPoolExecutor


def create_proxyauth_extension(proxy_host, proxy_port,
                               proxy_username, proxy_password,
                               scheme='http', plugin_path=None):

    if plugin_path is None:
        plugin_path = r'proxy_auth_plugin.zip'

    manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

    background_js = string.Template(
        """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                  },
                  bypassList: ["foobar.com"]
                }
              };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path


def process(index: int):
    proxyauth_plugin_path = create_proxyauth_extension(
        proxy_host="gw-g-sg.ntnt.io",
        proxy_port=5959,
        proxy_username='martinhou-res-fr-sid-' + str(1000+index),
        proxy_password="jBK92eBvu6Dpjht",
    )
    
    url = 'https://rendezvousparis.hermes.com/client/register'
    # url = 'https://www.baidu.com/'
    
    # username = 'martinhou-res-fr-sid-' + str(1000+index)
    # password = 'jBK92eBvu6Dpjht'
    # server = 'gw-g-sg.ntnt.io'
    # port = '9595'
    
    # proxy_server = f'socks5://{server}:{port}'
    # auth = f'{username}:{password}'
    # print(proxy_server,auth)
    
    options = webdriver.ChromeOptions()
    options.add_extension(proxyauth_plugin_path)
    # options.add_argument(f'--proxy-server={proxy_server}')
    # options.add_argument(f'--proxy-auth={auth}')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")
    options.add_argument("--enable-webgl")
    options.add_argument("window-size=1200x600")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(30)
    time.sleep(300)
    
    surname = driver.find_element(value='surname')
    surname.send_keys('John')
    
    name = driver.find_element(value='name')
    name.send_keys('Smith')
    
    phone = driver.find_element(value='phone_number')
    phone.send_keys('17766669999')
    
    email = driver.find_element(value='email')
    email.send_keys('martinhou@foxmail.com')
    
    passport = driver.find_element(value='passport_id')
    passport.send_keys('EG5152423')
    
    driver.find_element(value='cgu').click()
    driver.find_element(value='processing').click()
    driver.implicitly_wait(30)
    driver.find_element(by=By.CSS_SELECTOR, value='input[type="submit"]').click()
    driver.close()
    return 1
    

def main():

    total, succ = 0, 0
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = []
        
        while succ < 1:
            future = executor.submit(process, total)
            futures.append(future)
            
            succ += future.result()
            
            total += 1
            if total % 4 == 0:
                # Wait for the group of four threads to complete and process results
                for future in futures:
                    try:
                        succ += future.result()
                        # Process the result as needed
                    except Exception as e:
                        print(f"An error occurred: {e}")
                
                futures = []

    
    # while succ<10000:
    #     thead_list = []
    #     t1 = Thread(target=process, args=(f'http://{username % 1000+total}:{password}@{server}:{port}'))
    #     t1.start()
    #     total += 1
    #     t2 = Thread(target=process, args=(f'http://{username % 1000+total}:{password}@{server}:{port}'))
    #     t2.start()
    #     total += 1
    #     t3 = Thread(target=process, args=(f'http://{username % 1000+total}:{password}@{server}:{port}'))
    #     t3.start()
    #     total += 1
    #     t4 = Thread(target=process, args=(f'http://{username % 1000+total}:{password}@{server}:{port}'))
    #     t4.start()
    #     total += 1
    #     thead_list.append(t1)
    #     thead_list.append(t2)
    #     thead_list.append(t3)
    #     thead_list.append(t4)
    #     for t in thead_list:
    #         t.join()
    
if __name__=='__main__':
    main()