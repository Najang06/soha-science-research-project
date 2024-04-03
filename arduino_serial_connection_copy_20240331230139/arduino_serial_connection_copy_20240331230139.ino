// 업로드할 때 프로세서를 "Old Bootloader"인 거로 설정 해야 함

// 라이브러리를 이용 DHT 안되면 dht 써보기
#include <DHT.h>
// dht DHT; // 에러 뜨면 이거 지우고 run 시켜보기

#define DHT22_PIN 5 // 아두이노의 5번 핀을 인터페이스로 사용
#define DHTTYPE DHT22 
DHT dht(DHT22_PIN, DHTTYPE);

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define SEALEVELPRESSURE_HPA (1013.25) // 해수면 기압 (현재 위치의 기압에 대한 보정값으로 사용됨)

Adafruit_BME280 bme; // BME280 객체 생성

// DHT22 센서로부터 데이터를 읽어 오도록 함수를 호출
// int chk = dht.read(DHT22_PIN);

//read22() 함수로 읽은 온습도데이터가 저장된 변수

int temp = 0; // 기온 변수 정의
int humid = 0; // 습도 변수 정의
int dust = 0; // 미세먼지 변수 정의
int gnd_humid = 0; // 토양 수분 변수 정의
float pres = 0; // 대기압 변수 정의
int bright = 0; // 밝기 변수 정의

unsigned long duration;   //지속 시간
unsigned long starttime;  //시작 시간
unsigned long sampletime_ms = 5000;   //샘플시간 5초 마다 업데이트
unsigned long lowpulseoccupancy = 0;   //Low 신호가 지속된 시간을 초기화
float ratio = 0;  //비율
float concentration = 0;  //입자 농도 0으로 초기화
float pcsPerCF = 0;  //한 입자당 CF를 0으로 초기화
float ugm3 = 0;  //최종 값으로 세제곱미터 당 마이크로 그램(㎍/㎥)


char serial_receive; // 시리얼 통신으로 받는 변수 정의
char serial_send; // 시리얼 통신으로 보낼 데이터 변수 정의

// 시리얼 신호로 어떤 신호를 보낼 것인가
// {‘1’ : ‘온도‘, ’2‘ : ’습도‘, ’3‘ : ’미세먼지‘, ’4‘ : ’토양 수분‘, ’5‘ : ’대기압‘, ‘6’ : ‘광량’}
void setup()
{
	Serial.begin(9600);
	pinMode(6, INPUT); // fine dust sensor
	starttime = millis();
	bme.begin();
        dht.begin();
}

void loop()
{
	while(Serial.available())
	{
		char serial_command = Serial.read();
	}

	if(serial_receive == '1') // 온도
	{
		float temp = dht.readTemperature();
		float serial_send = temp;
		Serial.println(serial_send);
	}

	if(serial_receive == '2') // 습도
	{
		float humid = dht.readHumidity();
		float serial_send = humid;
		Serial.println(serial_send);
	}

	if(serial_receive == '3') // 미세먼지
	{
		duration = pulseIn(12, LOW); 
  	lowpulseoccupancy = lowpulseoccupancy+duration;
  
  	if ((millis()-starttime) >= sampletime_ms)  {   //만약 샘플 시간이 5초라면(위에서 정한 샘플 시간)
    	ratio = lowpulseoccupancy/(sampletime_ms*10.0);  // 정수 백분율
    	concentration = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62; // 미세먼지 센서 사양 시트 곡선 사용
    	pcsPerCF = concentration * 100;  // 입자 농도에 100을 곱하면 입자당 CF값
    	ugm3 = pcsPerCF / 13000;  //입자당 CF를 13000으로 나누면 미터세제곱당 마이크로그람의 미세먼지 측정값
		}
		dust = ugm3;
		serial_send = dust;
		Serial.println(serial_send);
  } 

	if(serial_receive == '4') // 토양 수분
	{
		int humid = analogRead(A1);
		int serial_send = humid;
		Serial.println(serial_send);
	}

	if(serial_receive == '5') // 대기압
	{
		float pres = bme.readPressure() / 100.0F;
		float serial_send = pres;
		Serial.println(serial_send);
	}

	if(serial_receive == '6')
	{
		int bright = analogRead(A0);
		int serial_send = bright;
		Serial.println(serial_send);
	}
}
