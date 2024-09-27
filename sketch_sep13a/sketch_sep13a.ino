#include <ArdusatSDK.h>

Luminosity lum;
Temperature temp;

void setup(void) {
  Serial.begin(9600);
  lum.begin();
  temp.begin();
}

void loop(void) {
  
  Serial.println(temp.readToJSON("ambient_temp"));
  
  Serial.println(lum.readToJSON("Luminosity")); // >> ~{"sensorName": "Luminosity", "unit": "lux", "value": 123.5, "cs": 43}|

  delay(5000);
}
