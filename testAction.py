#!/usr/bin/python

import csv
import random

from datetime import date
import time
import os
import subprocess

def commit_and_push():
    print("Commit + Push sur GitHub...")
    subprocess.run(["git", "config", "--global", "user.meysam.shamsi@gmail.com", "actions@github.com"])
    subprocess.run(["git", "config", "--global", "user.exofri", "GitHub Actions"])
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"Update files {datetime.now().strftime('%Y-%m-%d')}"])
    subprocess.run(["git", "push"])
    print("TOUT PUSHÉ SUR GIT !")
    
def update_city(city):

    t = time.localtime()
    current_time = time.strftime(" %H:%M:%S", t)
    today = date.today()
    # dd/mm/YY
    today_date = today.strftime('%Y-%m-%d')
    
    text_code = subprocess.run(['curl', f"wttr.in/{city}?format=+%t+%h"], stdout=subprocess.PIPE).stdout.decode()
     # +16°C 94%
    try:
        print(int(text_code[text_code.index('°C')-3:text_code.index('°C')]))
        tmp=int(text_code[text_code.index('°C')-3:text_code.index('°C')])
    except:
        print("/!\ error in reading")
        tmp="Unknown"
    try:
        print(int(text_code[text_code.index('%')-2:text_code.index('%')]))
        humidity=text_code[text_code.index('%')-2:text_code.index('%')]
    except:
        humidity="Unknown"
    
    
    if random.random()>0.01:
        paris_humadity=humidity
    else:
        paris_humadity="Unknown"
    if random.random()>0.015:
        paris_tmp=tmp
    else:
        paris_tmp="Unknown"
    
    file=[]
    # Read CSV file
    if os.path.isfile(f"{city}.txt"):
        with open(f"{city}.txt") as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                file.append([r for r in row])
    else:
        header=["Date","Temperature","Humidity"]

    file.append([today_date+current_time,
                 paris_tmp,
                 paris_humadity])

    # Write CSV file
    with open(f"{city}.txt", "wt") as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerow(i for i in headers)
        writer.writerows(file[-24*30:])

    return tmp,humidity

# while True:
    
#     t = time.localtime()
#     current_time = time.strftime(" %H:%M:%S", t)
#     today = date.today()
#     # dd/mm/YY
#     today_date = today.strftime('%Y-%m-%d')
    
#     for c in ["Paris","Strasbourg","Marseille","Lille"]:
#         tmp,humidity=update_city(c)
#         print(f"City:{c}, T:{tmp}, H:{humidity}\n\n")
    
#     print(today_date+current_time)
#     os.system('git commit -a -m "now"')
#     os.system('git push')

#     time.sleep(3600)

if __name__ == "__main__":
    t = time.localtime()
    current_time = time.strftime(" %H:%M:%S", t)
    today = date.today()
    # dd/mm/YY
    today_date = today.strftime('%Y-%m-%d')
    
    for c in ["Paris","Strasbourg","Marseille","Lille"]:
        tmp,humidity=update_city(c)
        print(f"City:{c}, T:{tmp}, H:{humidity}\n\n")
    
    print(today_date+current_time)
    commit_and_push()
    print("successfuly commited!")

    # os.system('git commit -a -m "now"')
    # os.system('git push')
