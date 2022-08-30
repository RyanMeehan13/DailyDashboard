import requests



#CONSTANTS

#coords of gtown uni. 
LAT = 38.9076 
LON = -77.0723 
#months
MONTHS = ['-', 'January', 'February', 'March', 
    'April', 'May', 'June', 'July', 'August', 'September','October', 
    'November', 'December']



#-------------------------------------------------------------------------------------------------------------|
#get_data() function                                                                                          |
#                                                                                                             |
#arguments: none                                                                                              |
#returns: JSON obj with weather data. Includes data for range (yesterday, One week later)                     |
#Source: Open-meteo, a free weather api                                                                       |
#-------------------------------------------------------------------------------------------------------------|
def get_data(lat = LAT, lon = LON):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,rain,showers,snowfall,cloudcover,windspeed_10m&daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,rain_sum,showers_sum,snowfall_sum,precipitation_hours,windspeed_10m_max&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&timezone=America%2FNew_York&past_days=1")
    data = response.json()
    return data


#-------------------------------------------------------------------------------------------------------------|
#find_yesterday_avg(data, measurement) function                                                               |
#                                                                                                             |
#arguments: data (json object), measurement(string, what needs to be averaged)                                |
#returns: average of the measured quantity for yesterday  (only really used for temp)                         |
#                                                                                                             |
#-------------------------------------------------------------------------------------------------------------|

def find_yesterday_avg(data, measurement = 'temperature_2m'):
    sum = 0
    for i in range(0, 24):
        sum = sum + data['hourly'][measurement][i]
    return sum/24


#recognize that index 0-23 is yesterday, 24-47 is today. 

#-------------------------------------------------------------------------------------------------------------|
#find_today_total(data, measurement) function                                                                 |
#                                                                                                             |
#arguments: data (json object), measurement(string, what needs to be summed)                                  |
#returns: total of the measured quantity for today                                                            |
#                                                                                                             |
#-------------------------------------------------------------------------------------------------------------|

def find_today_total(data, measurement):
    sum = 0
    for i in range(24, 48):
        sum = sum + data['hourly'][measurement][i]
    return sum


#-------------------------------------------------------------------------------------------------------------|
#find_today_avg(data, measurement) function                                                                   |
#                                                                                                             |
#arguments: data (json object), measurement(string, what needs to be averaged)                                |
#returns: average of the measured quantity for today                                                          |
#                                                                                                             |
#-------------------------------------------------------------------------------------------------------------|

def find_today_avg(data, measurement):
    return find_today_total(data, measurement)/24

#-------------------------------------------------------------------------------------------------------------|
#get_date(data) function                                                                                      |
#                                                                                                             |
#arguments: data (json object)                                                                                |
#returns: year, month, day (ints)                                                                             |
#                                                                                                             |
#-------------------------------------------------------------------------------------------------------------|

def get_date(data):
    date = data['daily']['time'][1]
    year = int(date.split('-')[0])
    month = int(date.split('-')[1])
    day = int(date.split('-')[2])
    return year, month, day


#-------------------------------------------------------------------------------------------------------------|
#get_high_low(data) function                                                                                  |
#                                                                                                             |
#arguments: data (json object)                                                                                |
#returns: high temp/ low temp (ints)                                                                          |
#                                                                                                             |
#-------------------------------------------------------------------------------------------------------------|
def get_high_low(data):
    high = data['daily']['temperature_2m_max'][1]
    low = data['daily']['temperature_2m_min'][1]
    return high,low


#-------------------------------------------------------------------------------------------------------------|
#get_relation(avg, yest_avg) function                                                                         |
#                                                                                                             |
#arguments: avg, yest_avg : the avg temps from today and yesterday                                            |
#returns: relation (a string)                                                                                 |
#                                                                                                             |
#-------------------------------------------------------------------------------------------------------------|
def get_relation(avg_temp, yest_avg_temp):
    temp_adjective = ''
    if(avg_temp-yest_avg_temp >= 2): #today it is 2 deg hotter than yesterday, on average
        if(avg_temp-yest_avg_temp >= 5):
            temp_adjective = 'significantly hotter than'
        else:
            temp_adjective = 'warmer than'
    elif(avg_temp-yest_avg_temp < 2 and avg_temp - yest_avg_temp >-2):
        temp_adjective = 'about the same as'
    else: #avg_temp - yest_avg_temp <= -2
        if(avg_temp-yest_avg_temp <= -5):
            temp_adjective = 'significantly colder than'
        else:
            temp_adjective = 'cooler than'
    return temp_adjective


#-------------------------------------------------------------------------------------------------------------|
#get_humid_report(avg_humidity) function                                                                      |
#                                                                                                             |
#arguments: avg_humidity : the avg humidity                                                                   |
#returns: report (a string)                                                                                   |
#                                                                                                             |
#-------------------------------------------------------------------------------------------------------------|
def get_humid_report(avg_humidity):
    humidity_report = ''
    if(avg_humidity<50):
        humidity_report = 'Don\'t worry about humidity today, as it is not expected to be very humid at all. '
    elif(avg_humidity<70):
        humidity_report = 'It\'s going to be humid today, which could make it feel hotter out than it actually is. '
    else:
        humidity_report = 'It\'s going to be very humid today, so expect sticky conditions. '
    return humidity_report


#-------------------------------------------------------------------------------------------------------------|
#get_cloud_report(avg_cloud) function                                                                         |
#                                                                                                             |
#arguments: avg_cloud : the avg cloudcover                                                                    |
#returns: report (a string)                                                                                   |
#                                                                                                             |
#-------------------------------------------------------------------------------------------------------------|
def get_cloud_report(avg_cloud):
    cloud_report = ''
    if(avg_cloud<35):
        cloud_report = 'A lack of significant cloud cover means that the sky will be mostly clear today. '
    elif(avg_cloud<75):
        cloud_report = 'Expect partly-cloudly conditions for today. '
    else:
        cloud_report = 'Today will be a cloudly one, with significant cloud cover for most of the day. '
    return cloud_report



#-------------------------------------------------------------------------------------------------------------|
#get_wind_report(avg_wind) function                                                                           |
#                                                                                                             |
#arguments: avg_wind : the avg windspeed                                                                      |
#returns: report (a string)                                                                                   |
#                                                                                                             |
#-------------------------------------------------------------------------------------------------------------|
def get_wind_report(avg_windspeed):
    windspeed_report = ''
    if(avg_windspeed>24):
        windspeed_report = 'Today will be very windy, so much so that handling umbrellas may be difficult. '
    elif(avg_windspeed>15):
        windspeed_report = f'Be prepared for windy conditions today, as speeds will reach {avg_windspeed} mph. '
    return windspeed_report


#-------------------------------------------------------------------------------------------------------------|
#get_rain_report(total_precip) function                                                                       |
#                                                                                                             |
#arguments: total_precip : the total precipitation                                                            |
#returns: report (a string)                                                                                   |
#                                                                                                             |
#-------------------------------------------------------------------------------------------------------------|
def get_rain_report(total_precip):
    rain_report = ''
    if(total_precip >= .75 ):
        rain_report = 'Expect large amounts of rain today, with the portential to leave long lasting and deep puddles. '
    elif(total_precip >=.25):
        rain_report = 'Expect today to be a moderately rainy day. '
    elif(total_precip >0):
        rain_report = 'Be prepared for some light rain today. '
    return rain_report

#-------------------------------------------------------------------------------------------------------------|
#get_snow_report(total_snow) function                                                                         |
#                                                                                                             |
#arguments: total_snow : the total snowfall                                                                   |
#returns: report (a string)                                                                                   |
#                                                                                                             |
#-------------------------------------------------------------------------------------------------------------|
def get_snow_report(total_snow):
    snow_report = ''
    if(total_snow>10):
        snow_report = 'A large amount of snowfall, in excess of ten inches, is on the forcast for today, so be sure to plan accordingly. '
    elif(total_snow>6):
        snow_report = 'A significant amount of snow is expected to fall today, with accumulations exceeding six inches. '
    elif(total_snow>3):
        snow_report = 'Look out for snow today, as forcasts predict a few inches will accumulate. '
    elif(total_snow>0):
        snow_report = 'Be on the lookout for snowflakes today, as a few flurries are expected to pass through the area. '
    return snow_report


#-------------------------------------------------------------------------------------------------------------|
#recommend_clothing(max_temp, avg_temp, total_precip)function                                                 |
#                                                                                                             |
#arguments: max/avg temps, total precipitation                                                                |
#returns: recommendation, a string                                                                            |
#                                                                                                             |
#-------------------------------------------------------------------------------------------------------------|
def recommend_clothing(max_temp, avg_temp, total_precip):
    recommendation = ''
    #pants
    if(avg_temp>=60 and avg_temp<70): #boundary zone
        recommendation+='Given that today won\'t be too cold, it might be preferable to wear shorts instead of pants'
        if(max_temp>=75):
            recommendation+=' ,especially given the fact that temperatures will peak above 75\u00B0F'
        recommendation+='. '
    elif(avg_temp>70):
        recommendation+='It\'ll be warm today, so it might be best to wear shorts. '
    else: #avg temps less than 60
        recommendation+='Considering today\'s weather, long-pants seem like a comfortable choice. '
    
    #upper body
    if(avg_temp>=60 and avg_temp<70):
        recommendation+='Today\'s mild temperatures allow for either a short sleeve or long sleeve shirt'
        if(max_temp>=75):
            recommendation+=' ,but a short sleeve might be the best option, as a long sleeve could become uncomfortable during the hottest part of the day'
        recommendation+='. '
    elif(avg_temp>70):
        recommendation+='During a warmer day, like today, it\'s best to stick with a short sleeve shirt. '
    elif(avg_temp>=45):
        recommendation+='You can probably get away with a long sleeve shirt today, but you have a few other options. You can layer a short and long sleeve shirt or add a sweatshirt for some extra warmth. '
    else: #avg<45
        recommendation+='On cold days like these, a sweatshirt is almost mandatory - stay warm! '
    
    #outerwear
    if(total_precip>.1):
        recommendation+='Don\'t forget to bring a jacket or an umbrella, you don\'t want to get caught in the rain. '
    elif(total_precip>0):
        recommendation+='A jacket or umbrella might be useful today, but it shouldn\'t be necessary. '

    return recommendation
    
    



#-------------------------------------------------------------------------------------------------------------|
#generate_content() function                                                                                  |
#                                                                                                             |
#arguments: none                                                                                              |
#returns: content, a string                                                                                   |
#                                                                                                             |
#-------------------------------------------------------------------------------------------------------------|

def generate_content():
    data = get_data()

    #date components
    year,month,day = get_date(data)

    

    #grab highs and lows 
    max_temp,min_temp = get_high_low(data)

    #grab precip
    total_rain = data['daily']['rain_sum'][1]
    total_showers = data['daily']['showers_sum'][1]
    total_precip = total_rain+total_showers
    total_snow = data['daily']['snowfall_sum'][1]
    
    


    #get avgs
    avg_temp = find_today_avg(data, 'temperature_2m')
    yest_avg_temp = find_yesterday_avg(data)
    avg_feel = find_today_avg(data, 'apparent_temperature')
    avg_humidity = find_today_avg(data, 'relativehumidity_2m')
    avg_cloud = find_today_avg(data, 'cloudcover')
    avg_windspeed = find_today_avg(data, 'windspeed_10m')

    #determine relation
    temp_adjective = get_relation(avg_temp, yest_avg_temp)
    
    #generate reports 
    
    #humidity
    humidity_report = get_humid_report(avg_humidity)

    #cloudcover
    cloud_report = get_cloud_report(avg_cloud)

    #windspeed 
    windspeed_report = get_wind_report(avg_windspeed)

    #rain
    rain_report = get_rain_report(total_precip)
    
    #snow
    snow_report = get_snow_report(total_snow)
    

    #clothing
    clothing_recommendation = recommend_clothing(max_temp, avg_temp, total_precip)
        

    content = f'''Today is {MONTHS[month]} {day}, {year}. 
Temperatures today will be {temp_adjective} yesterday. The high today will be {int(max_temp)}\u00B0F 
and the low will be {int(min_temp)}\u00B0F. Throughout the day, the average temperature will be {int(avg_temp)}\u00B0F, but it will feel like {int(avg_feel)}\u00B0F.
{rain_report}{snow_report}{humidity_report}{cloud_report}{windspeed_report}
    
{clothing_recommendation}'''

    return content

    
