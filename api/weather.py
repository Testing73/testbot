from bs4 import BeautifulSoup as bs
import requests
import re

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 " \
             "Safari/537.36 "
# US english
LANGUAGE = "en-US,en;q=0.5"


def get_weather_data(url):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(url)
    # create a new soup
    soup = bs(html.text, "html.parser")
    # store all results on this dictionary
    result = {}
    # extract region
    # print(soup.find("div", attrs={"id": "wob_loc"}))
    result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
    # extract temperature now
    result['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
    # get the day and hour now
    result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
    # get the actual weather
    result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
    # get the precipitation
    result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
    # get the % of humidity
    result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
    # extract the wind
    result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text
    # get next few days' weather
    next_days = []
    days = soup.find("div", attrs={"id": "wob_dp"})
    for day in days.findAll("div", attrs={"class": "wob_df"}):
        # extract the name of the day
        day_name = day.find("div", attrs={"class": "vk_lgy"}).attrs['aria-label']
        # get weather status for that day
        weather = day.find("img").attrs["alt"]
        temp = day.findAll("span", {"class": "wob_t"})
        # maximum temparature in Celsius, use temp[1].text if you want fahrenheit
        max_temp = temp[0].text
        # minimum temparature in Celsius, use temp[3].text if you want fahrenheit
        min_temp = temp[2].text
        next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp})
    # append to result
    result['next_days'] = next_days
    return result


def weather(region, day_time):
    URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather+"
    URL += region
    # get data
    data = get_weather_data(URL)
    # print data
    if day_time.lower() in ["today", "now", None]:
        data["next_days"] = []
    elif day_time.lower() in ["tomorrow", "next day", "next 1 day", "next 1 days", "nextday", "next1day", "next1days"]:
        data = data["next_days"][1]
    elif day_time.lower() in ["day after tomorrow", "dayafter tomorrow", "dayaftertomorrow", "day-after-tomorrow",
                              "day-after tomorrow", "day after-tomorrow"]:
        data = data["next_days"][2]
    elif day_time.lower() in ["this weekend", "weekend", "week end", "coming weekend", "next weekend", "next week-end",
                              "coming week-end", "next week end", "coming week end", "week-end", "this week-end",
                              "this week end"]:
        data["next_days"] = data["next_days"][1:7]
    elif re.match("(|for)?(|\s+)?(next?(\s+|)|coming?(\s+|)|upcoming?(\s+|)|this?(\s+|))?\d+(\s+|)?(days|day)?",
                  day_time, re.I):
        if int(re.search("\d", day_time, re.I).group()) < 8:
            data["next_days"] = data["next_days"][:int(re.search("\d+", day_time, re.I).group())]
    elif "monday" in day_time.lower():
        for each_day in data["next_days"]:
            if each_day["name"].lower() == "monday":
                data["next_days"] = each_day
                break
    elif "tuesday" in day_time.lower():
        for each_day in data["next_days"]:
            if each_day["name"].lower() == "tuesday":
                data["next_days"] = each_day
                break
    elif "wednesday" in day_time.lower():
        for each_day in data["next_days"]:
            if each_day["name"].lower() == "wednesday":
                data["next_days"] = each_day
                break
    elif "thursday" in day_time.lower():
        for each_day in data["next_days"]:
            if each_day["name"].lower() == "thursday":
                data["next_days"] = each_day
                break
    elif "friday" in day_time.lower():
        for each_day in data["next_days"]:
            if each_day["name"].lower() == "friday":
                data["next_days"] = each_day
                break
    elif "saturday" in day_time.lower():
        for each_day in data["next_days"]:
            if each_day["name"].lower() == "saturday":
                data["next_days"] = each_day
                break
    elif "sunday" in day_time.lower():
        for each_day in data["next_days"]:
            if each_day["name"].lower() == "sunday":
                data["next_days"] = each_day
                break
    else:
        data = data

    # print(data)
    # print("Weather for:", data["region"])
    # print("Now:", data["dayhour"])
    # print(f"Temperature now: {data['temp_now']}°C")
    # print("Description:", data['weather_now'])
    # print("Precipitation:", data["precipitation"])
    # print("Humidity:", data["humidity"])
    # print("Wind:", data["wind"])
    # print("Next days:")
    # for dayweather in data["next_days"]:
    #     print("=" * 40, dayweather["name"], "=" * 40)
    #     print("Description:", dayweather["weather"])
    #     print(f"Max temperature: {dayweather['max_temp']}°C")
    #     print(f"Min temperature: {dayweather['min_temp']}°C")

    return data

# print(weather("chennai", "monday"))