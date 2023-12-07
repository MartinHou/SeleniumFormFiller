
    # to use this example you must have 'requests' installed: pip install requests
import requests

username = 'martinhou-res-fr-sid-0200'
password = 'jBK92eBvu6Dpjht'
server = 'gw-g-sg.ntnt.io'
port = '5959'
proxy = {
  'http': f'socks5://{username}:{password}@{server}:9595',
  'https': f'socks5://{username}:{password}@{server}:9595'
}

print(requests.get('https://www.baidu.com/', proxies=proxy).text)
    