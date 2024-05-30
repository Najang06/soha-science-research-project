# pip install pySerial
import serial
import time
import pandas as pd

arduino = serial.Serial('com3', 9600)

serial_send = '0' # 얘는 str
serial_receive = 0 # 얘는 int

category = 'temp', 'humid', 'dust', 'gnd_humid', 'bright'

time_now = time.strftime('%H:%M') # 23:45 이런 형식으로 시간 확인
date_now = time.strftime("%Y-%m-%d") # 날짜 변수, 2024-11-14 이런 형식으로 확인

def serial_send_fn(req):
	global arduino
	serial_send = req
	serial_send = serial_send.encode('utf-8') # 인코딩함
	arduino.write(serial_send) # 시리얼 통신으로 보냄
	time.sleep(3) # 3초 대기
	if arduino.in_waiting > 0:
		incoming_data = arduino.readline().decode('utf-8').rstrip()
	else:
		incoming_data = 'nan'
	return incoming_data

df = pd.DataFrame({'time' : [0],
				'temp' : [0],
		   		'humid' : [0],
		   		'dust' : [0],
		   		'gnd_humid' : [0],
		   		'bright' : [0]})

if (time_now == "03:00") or (time_now == "06:00") or (time_now == "09:00") or (time_now == "12:00" or (time_now == "15:00") or (time_now == "18:00") or (time_now == "21:00"): # 시간대별로 센서 데이터 수집 후 딕셔너리에 저장
	data_list = [] # 받은 데이터를 저장할 리스트
	data_list.append(date_now + '/' + time_now) # 시간 내놔
	for catgry in category:
		if catgry == 'temp': # 온도 정보 내놔
			data_list.append(serial_send_fn('1'))

		if catgry == 'humid': # 습도 정보 내놔
			data_list.append(serial_send_fn('2'))

		if catgry == 'dust': # 미세먼지 정보 내놔
			data_list.append(serial_send_fn('3'))

		if catgry == 'gnd_humid': # 토양 수분 정보 내놔
			data_list.append(serial_send_fn('4'))

		if catgry == 'bright': # 밝기 정보 내놔
			data_list.append(serial_send_fn('5'))

	df.loc[len(df)] = data_list # df의 마지막 행에 리스트 데이터 추가
	df.to_csv("weather_measurements.csv", index_label=True) #csv 저장