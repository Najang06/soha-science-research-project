# pip install pySerial
import serial
import time

arduino = serial.Serial('com3', 9600)

serial_send = '0' # 얘는 str
serial_receive = 0 # 얘는 int

category = 'temp', 'humid', 'dust', 'gnd_humid', 'pres', 'bright'

time_now = time.strftime('%H:%M') # 23:45 이런 형식으로 시간 확인
date_now = time.strftime("%Y-%m-%d") # 날짜 변수, 2024-11-14 이런 형식으로 확인

def serial_send_fn(req):
	global arduino
	serial_send = req
	serial_send = serial_send.encode('utf-8')
	arduino.write(serial_send)

data_dict = {} # 받은 데이터를 저장할 딕셔너리

def serial_receive_fn(catgry, rcv_data, data_dict): # 카테고리, 받은 데이터, 딕셔너리를 인풋으로 
	while(sts = 'reading'):
		data_dict[catgry] = rcv_data # 카테고리 key에 받은 데이터를 value로 넣음
		return data_dict 

if (time_now == "03:00") or (time_now == "06:00") or (time_now == "09:00") or (time_now == "12:00" or (time_now == "15:00") or (time_now == "18:00") or (time_now == "21:00"): # 시간대별로 센서 데이터 수집 후 딕셔너리에 저장
	for catgry in category:
		if catgry == 'temp': # 온도 정보 내놔
			serial_send_fn('1')

		if catgry == 'humid': # 습도 정보 내놔
			serial_send_fn('2')

		if catgry == 'dust': # 미세먼지 정보 내놔
			serial_send_fn('3')

		if catgry == 'gnd_humid': # 토양 수분 정보 내놔
			serial_send_fn('4')

		if catgry == 'pres': # 대기압 정보 내놔
			serial_send_fn('5')

		if catgry == 'bright': # 밝기 정보 내놔
			serial_send_fn('6')

'''
시리얼 통신으로 받은 데이터를 딕셔너리에 집어넣는 코드 쓰기(완료/위에 함수 만든 거 참고)
pandas를 이용해서 df로 전환한 다음 csv파일로 저장하는 코드를 짜면 끝
'''