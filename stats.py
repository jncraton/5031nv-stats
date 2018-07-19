import mechanicalsoup
import re

def get_hosts():
  hosts = []

  browser = mechanicalsoup.StatefulBrowser(
      soup_config={'features': 'lxml'},  # Use the lxml HTML parser
      raise_on_404=True,
      user_agent='MyBot/0.1: mysite.example.com/bot_info',
  )
  
  browser.open("http://192.168.1.254/xslt?PAGE=C_2_5")
  
  soup = browser.get_current_page()
  
  for row in soup.find_all('tr'):
    try:
      cols = [row.contents[i].contents for i in range(1,23,2)]
    except IndexError:
      cols = None
  
    if cols:
      host = {n: cols[i][0] for i,n in enumerate(["name","mac","ssid","rssi","tx_frames","tx_bytes","rx_frames","rx_bytes"])}
      if re.match("..:..:..:..:..:..", host['mac']):
        hosts.append(host)
  
  browser.close()

  return hosts

print(get_hosts())