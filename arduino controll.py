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
	serial_send = serial_send.encode('utf-8')
	arduino.write(serial_send)

df = pd.DataFrame({'temp' : [0],
		   'humid' : [0],
		   'dust' : [0],
		   'gnd_humid' : [0],
		   'bright' : [0]})

def serial_receive_fn(catgry, rcv_data, data_dict): # 카테고리, 받은 데이터, 딕셔너리를 인풋으로 
	while (sts = 'reading'):
		data_dict[catgry] = rcv_data # 카테고리 key에 받은 데이터를 value로 넣음
		return data_dict 

if (time_now == "03:00") or (time_now == "06:00") or (time_now == "09:00") or (time_now == "12:00" or (time_now == "15:00") or (time_now == "18:00") or (time_now == "21:00"): # 시간대별로 센서 데이터 수집 후 딕셔너리에 저장
	data_list = [] # 받은 데이터를 저장할 리스트
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

'''
csv파일로 저장하는 코드를 짜면 끝
'''
