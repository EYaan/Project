#include <MsTimer2.h>
#include <LiquidCrystal.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "my_arduino_lib.h"

#define trigPin A0
#define echoPin A1
#define BUZZER  9
#define LED    10

#define ring() tone(BUZZER, 800)

const int rs = 3, en = 4, d4 = 5, d5 = 6, d6 = 7, d7 = 8;
//const int BUZZER = 10;


LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

int ad_buf1, ad_buf2; 
char d_buf[20]; // 거리1
char d_buf2[20]; // 거리2
long dist1, dist2; // 거리1, 거리2
int spd, del = 100; // 속력

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
  DDRD = 0xff;
  DDRB = 0xff;
  // PORTD = 0x00;
  // PORTB = 0x00;

  Serial.begin(9600);
  //pinMode(BUZZER,OUTPUT);

  
  lcd.begin(16,2);

  // 거리 1 측정
  digitalWrite(trigPin,HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin,LOW);
  
  dist1 = pulseIn(echoPin,HIGH) / 58;
}

void loop() {
  // put your main code here, to run repeatedly:
  
  // 거리2 측정
  digitalWrite(trigPin,HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin,LOW);
  
  dist2 = pulseIn(echoPin,HIGH) / 58;


  // 거리출력
  Serial.print(dist2,DEC); //DEC == 10진수
  Serial.println("CM");
  lcd.setCursor(0, 0);
  sprintf(d_buf," DIST : %4d CM",dist1);
  lcd.print(d_buf);

  //속력출력 -- 추후 시간 조정 필요
  
  // 속력 계산
  if(dist2>dist1) spd = (dist2-dist1)/2;
  else spd = (dist1-dist2)/2;
  // 출력
  lcd.setCursor(0, 1);
  sprintf(d_buf2," Speed : %4d CM/S",spd);

  lcd.print(d_buf2);
  dist1 = dist2;

  if(dist2<10)
  {
    del = 10;
  }

  // led & buzze
  if (dist2 < 5) {
    digitalWrite(LED, ON);
    ring();
    delay(50);
    digitalWrite(LED, OFF);
    noTone(BUZZER);
    delay(50);
  }
  else if (dist2 < 10) {
    digitalWrite(LED, ON);
    ring();
    delay(100);
    digitalWrite(LED, OFF);
    noTone(BUZZER);
    delay(100);
  } else if (dist2 < 30) {
    digitalWrite(LED, ON);
    ring();
    delay(500);
    digitalWrite(LED, OFF);
    noTone(BUZZER);
    delay(500);
  } else delay (500);
  
}
