import pymysql
import requests
import xml.etree.ElementTree as ET
import datetime
url = "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=1159068000"

text = requests.get(url).text
root = ET.fromstring(text)

description = root.find('channel').find('item').find('description')
body = description.find('body')
header = description.find('header')
db = pymysql.connect(
    user='kdw9502',
    passwd='rkdehddnr1',
    host='18.232.93.89',
    db='kdw9502_db',
    charset='utf8'
)
cursor = db.cursor()

 
time_string = header.find("tm").text
year = int(time_string[0:4])
month = int(time_string[4:6])
day = int(time_string[6:8])
hour = int(time_string[8:10])
minute = int(time_string[10:12])

for data in body.findall('data')[:3]:

    base_datetime = datetime.datetime(year, month, day, hour, minute)
    diff_hour = int(data.find('hour').text)
    result_datetime = base_datetime + datetime.timedelta(hours=diff_hour)

    temperature = float(data.find("temp").text)

    datetime_text = result_datetime.strftime('%Y-%m-%d %H:%M:%S')

    query = f"INSERT INTO temperature(datetime, temperature) VALUES ('{datetime_text}', {temperature}) ON DUPLICATE KEY UPDATE temperature='{temperature}';"
    cursor.execute(query)
    db.commit()
