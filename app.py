from urllib.request import urlopen
from bs4 import BeautifulSoup

year = input("예약 검색하고 싶은 년도를 입력하세요: ")
month = input("예약 검색하고 싶은 달을 입력하세요: ")
day = input("예약하고 싶은 날을 입력하세요: ")

reservation_url = f'https://www.mangsangcamping.or.kr/reservation/02.htm?code=&year={year}&month={month}#body_content'

result = urlopen(reservation_url)
html = result.read()

soup = BeautifulSoup(html, 'html.parser')

td_elements = soup.select('table td')

reservation_data = {}  # 날짜별 정보를 담을 딕셔너리

for td in td_elements:
    date_div = td.find('div', class_='date')
    if date_div:
        date = date_div.text
        reservation_data[date] = []  # 각 날짜별 정보를 담을 리스트 초기화

    cont_div = td.find('div', class_='cont')
    if cont_div:
        zones = cont_div.find_all('ul')
        for zone in zones:
            zone_name = zone.find('b')
            if zone_name:
                zone_info = zone_name.text
                unable_items = zone.find_all('li', class_='unable')
                unable_info = [item.text for item in unable_items]
                
                if not unable_info:
                    unable_info = ["예약가능"]
                reservation_data[date].append((zone_info, unable_info))

'''
for date, info_list in reservation_data.items():
    #print(date)
    for info in info_list:
        #print(info[0])  # zone_name
        for item in info[1]:  # unable_info
            #print(item)
'''

search_data = reservation_data.get(day)
final_data = []

if search_data:
    print('\n')
    print(f"{year}년 {month}월 {day}일에 해당하는 예약입니다.")
    
    for info in search_data:
       # print(info[0])  # zone_name

        for item in info[1]:  # unable_info
            pass
    
        
        final_data.append((info[0],info[1]))

    print(f"캐라반 4인승 {final_data[0][0]} {final_data[0][1]}")
    print(f"캐라반 6인승 {final_data[1][0]} {final_data[1][1]}")
    print(f"데크 {final_data[2][0]} {final_data[2][1]}")
    print('\n')
    print("조회가 완료 되었습니다.")
else:
    print(f"{year}년 {month}월 {day}일에 해당하는 예약은 존재하지 않습니다.")
