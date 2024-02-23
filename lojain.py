import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
start_date = datetime(2024, 1, 15)
end_date = datetime.now()
delta = end_date - start_date
with open("cookie.json", "r") as cookie:
    cookie_list = json.load(cookie)
cookies_my_account = {cookie["name"]: cookie["value"] for cookie in cookie_list}
days_list = []
print('Loading...')
for day in reversed(range(delta.days+1)):
    response = requests.get(
            f"https://learn-hub-api.datacamp.com/leaderboard?group=gaza-sky-geeks-23-24&page=1&days={day}&sortField=xp&sortOrder=desc",
            cookies=cookies_my_account,
        )
    
    respons = requests.get(
            f"https://learn-hub-api.datacamp.com/leaderboard?group=gaza-sky-geeks-23-24&page=1&days={day-1}&sortField=xp&sortOrder=desc",
            cookies=cookies_my_account,
        )
    if response.status_code == 200:
        with open("cookies.json", "w") as file:
            json.dump(response.json(), file)
        with open("cookies.json", "r") as file:
            cookies_listt = json.load(file)
        cookies = [
            (entry["user"]["fullName"], entry["xp"])
            for entry in cookies_listt["entries"]
        ]
    if respons.status_code == 200:
        with open("cookiess.json", "w") as file:
            json.dump(respons.json(), file)
        with open("cookiess.json", "r") as file:
            cookies_list = json.load(file)
        cookiess = [
            (entry["user"]["fullName"], entry["xp"])
            for entry in cookies_list["entries"]
        ]
    sum1,sum2=(0,0)
    for name,xp in cookies:
        sum1+=xp
    for name,xp in cookiess:
        sum2+=xp
    sum = sum1 - sum2
    new_date = datetime.now() - timedelta(days=day)
    formatted_date = new_date.strftime("%m-%d")
    days_list.append({'Date':formatted_date,'xp':sum})

df = pd.DataFrame(days_list)
print(df)
plt.plot(df['Date'],df['xp'],color='blue')
plt.scatter(df['Date'],df['xp'],color='yellow')
plt.plot(df['Date'],[df["xp"].mean() for d in df['Date']],color='green')
plt.title('Total XP for all Students per day')
plt.ylabel('total XP')
plt.xlabel('Date')
plt.grid()
plt.show()