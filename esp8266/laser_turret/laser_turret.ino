/*
    This sketch sends a string to a TCP server, and prints a one-line response.
    You must run a TCP server in your local network.
    For example, on Linux you can use this command: nc -v -l 3000
*/

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <string.h>
#include <Servo.h>

#ifndef STASSID
#define STASSID "hudnet"
#define STAPSK  "7950295932"
#endif

String client_name = "laser_turret";

const char* ssid     = STASSID;
const char* password = STAPSK;

const char* host = "192.168.18.1";
const uint16_t port = 8587;

ESP8266WiFiMulti WiFiMulti;

Servo servo_x;  // create servo object to control a servo
Servo servo_y;  // create servo object to control a servo

// pins
int servo_x_pin = 5;
int servo_y_pin = 4;
int laser_pin = 16;

void setup() {
  Serial.begin(115200);

  // We start by connecting to a WiFi network
  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP(ssid, password);

  Serial.println();
  Serial.println();
  Serial.print("Wait for WiFi... ");

  while (WiFiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  servo_x.attach(servo_x_pin);  
  servo_y.attach(servo_y_pin);
  pinMode(laser_pin, OUTPUT);
}


void loop() {
  WiFiClient client;

  if (!client.connect(host, port)) {
    Serial.println("connection failed");
    Serial.println("wait 5 sec...");
    delay(5000);
    return;
  }

  // This will send the request to the server
  String string = client_name;
  client.println(string);

  unsigned long timeout = millis();
  
  while(client.available() == 0) // ждёт ответ от сервера
  {
    if(millis() - timeout > 5000) // если нет ответа в течении 5 сек, то разрывает соединение
    {
      Serial.println("Client Timeout");
      client.stop();
      return;
    }
  }

  String line = client.readStringUntil('\r');
  if (line == "on"){
    digitalWrite(laser_pin, HIGH);
    Serial.println("Laser ON");  
  }else if (line == "off"){
    digitalWrite(laser_pin, LOW);
    Serial.println("Laser OFF");
  }else if (line == "none"){
    delay(15);
  }else{
    int x_cord = 181;
    int y_cord = 181;
    char cord[8] = "";
    line.toCharArray(cord, 8);
    sscanf(cord, "%d %d", &x_cord, &y_cord);

    Serial.println(String(x_cord) + " "+String(y_cord));
    if (x_cord < 181 && y_cord < 181){
      servo_x.write(x_cord);
      servo_y.write(y_cord);   
    }
  }
 
  client.stop();
}
