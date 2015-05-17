# Convert pseudo-CSV password file to an XML format suitable for use with
# KeePassX.

from datetime import datetime

with open("test.txt") as f:
    pws = f.readlines()

print("<!DOCTYPE KEEPASSX_DATABASE>")
print("<database>")
print("  <group>")
print("    <title>Internet</title>")
print("    <icon>1</icon>")

for line in pws:
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    line = line.split(",")

    try:
        title = line[0].strip().title()
    except: 
        title = ""
    try:
        username = line[1].strip()
    except: 
        username = ""
    try:
        password = line[2].strip()
    except: 
        password = ""
    try:
        comment = line[3].strip()
    except: 
        comment = ""

#   print(title)
#   print(username)
#   print(password)
#   print(comment)

    print("    <entry>")
    print("      <title>" + title + "</title>")
    print("      <username>" + username + "</username>")
    print("      <password>" + password + "</password>")
    print("      <url></url>")
    print("      <comment>" + comment + "</comment>")
    print("      <icon>1</icon>")
    print("      <creation>" + str(now) + "</creation>")
    print("      <lastaccess>" + str(now) + "</lastaccess>")
    print("      <lastmod>" + str(now) + "</lastmod>")
    print("      <expire>" + "Never" + "</expire>")
    print("    </entry>")

print("  </group>")
print("</database>")

