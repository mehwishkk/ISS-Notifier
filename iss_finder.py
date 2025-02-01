import requests
import  datetime
import smtplib
my_lat=17.385044
my_long=78.486671

my_email = 'test20@gmail.com'
password = 'test'

def is_iss_overhead():
    response = requests.get(url = "http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    print(response.status_code)
    # print(response)
    data=response.json()
    # print(data)
    iss_pos_long = float(response.json()['iss_position']['longitude'])
    iss_pos_lat = float(response.json()['iss_position']['latitude'])
    print(iss_pos_lat)
    print(iss_pos_long)
    if my_long-5 <= iss_pos_long <= my_long+5 and my_lat-5<= iss_pos_lat<=my_lat+5:
        print('near')
    return True

def is_night():
    parameters={"lat":my_lat,
                "lng":my_long,
                'formatted':0,
                'tzid':"Asia/Calcutta"}
    response1 = requests.get("https://api.sunrise-sunset.org/json",params = parameters)
    response1.raise_for_status()
    data1=response1.json()
    # print(data1)
    sunrise = int(data1['results']['sunrise'].split('T')[1].split(":")[0])
    sunset = int(data1['results']['sunset'].split('T')[1].split(":")[0])
    # print(sunrise)
    # print(sunset)
    time_now = datetime.datetime.now()
    print(time_now.hour)
    if sunrise <=time_now.hour <= sunset:
        print('day')
        return False
    return True



if is_night():
    print('night')

if is_iss_overhead() and is_night():
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()  # tls enables for security
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email, to_addrs=my_email,
                        msg=f'Subject:ISS overhead \n\nLook up, ISS is above you in the sky, ')
    connection.close()
