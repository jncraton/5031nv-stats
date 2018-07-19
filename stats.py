import mechanicalsoup
import re

def get_hosts():
  hosts = []

  col_names = [
    "name","mac","ssid","rssi",
    "tx_frames","tx_bytes","rx_frames","rx_bytes"
  ]

  with mechanicalsoup.StatefulBrowser() as browser:
    browser.open("http://192.168.1.254/xslt?PAGE=C_2_5")
    soup = browser.get_current_page()
    
    for row in soup.find_all('tr'):
      try:
        cols = [row.contents[i].contents for i in range(1,23,2)]
      except IndexError:
        continue
    
      host = {n: cols[i][0] for i,n in enumerate(col_names)}
      if re.match("..:..:..:..:..:..", host['mac']):
        hosts.append(host)

  return hosts

print(get_hosts())