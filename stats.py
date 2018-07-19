import re
import time

import mechanicalsoup

def get_hosts():
  hosts = {}

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
        hosts[host['name']] = host

  return hosts

if __name__ == '__main__':
  print("Getting start state...")
  start = get_hosts()

  interval = 60
  
  for secs in range(interval,0,-5):
    print("Waiting %d seconds..." % secs)
    time.sleep(5)
    
  print("Getting final state...")
  end = get_hosts()
  print("")

  for host in end.values():
    name = host['name']
    deltas = {n: int(end[name][n]) - int(start[name][n]) for n in ['rx_bytes','tx_bytes']}
  
    print(name)
    print("%.2f KiBps rx" % (deltas['rx_bytes'] / interval / 1024,))
    print("%.2f KiBps tx" % (deltas['tx_bytes'] / interval / 1024,))
    print("")