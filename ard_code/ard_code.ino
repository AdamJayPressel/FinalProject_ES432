#include <Adafruit_Sensor.h>
#include "DHT.h"
#include <LiquidCrystal.h>

#define DHTPIN 7     // what digital pin we're connected to
#define DHTTYPE DHT11   // DHT 11
#define rs 8
#define en 2
#define d4 3
#define d5 4
#define d6 5
#define d7 6

char c;
char name[16];
char message[16];
char temp;

LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);

  dht.begin();
  lcd.begin(16,2);
  
}

void loop() {
  // Wait a few seconds between measurements.
  delay(1000);

  // Reading temperature or humidity takes about 250 milliseconds!
  
  if (Serial.available() > 0){
    c = Serial.read();
    if (c == 'p'){ //print to serial line
      // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
      float h = dht.readHumidity();
      // Read temperature as Celsius (the default)
      float t = dht.readTemperature();
      // Read temperature as Fahrenheit (isFahrenheit = true)
      float f = dht.readTemperature(true);
      Serial.print(h);
      Serial.print(",");
      Serial.print(t);
      Serial.print(",");
      Serial.println(f);
    }
    else if(c == 'c'){//display on LCD
      lcd.clear();
      lcd.setCursor(0,0);
      for(int i=0; i<16; i++){
        temp = Serial.read();
        if(temp!=';'){
          name[i]=temp;
        }else{
          break;
        }
      }
      for(int i=0; i<16; i++){
        temp = Serial.read();
        if(temp!=':'){
          message[i]=temp;
        }else{
          break;
        }
      }
      
      lcd.print(name);
      lcd.print(" cheeps:");
      lcd.setCursor(0,1);
      lcd.print(message);
      for(int i=0; i<16; i++){
        name[i] = NULL;
        message[i] = NULL;
      }
    }
  }

}
