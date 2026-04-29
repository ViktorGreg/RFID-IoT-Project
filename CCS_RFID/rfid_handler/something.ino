#include <SPI.h>
#include <MFRC522.h>
#include <WiFiS3.h>
#include <HttpClient.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 rfid(SS_PIN, RST_PIN);

// ===== CHANGE THESE 3 LINES =====
const char* ssid = "PLDTHOMEFIBRU6Xcu";        // Your WiFi name
const char* password = "PLDTWIFIYENUh"; // Your WiFi password
const char* serverUrl = "https://CCS.pythonanywhere.com/api/receive-rfid/";
// =================================

WiFiSSLClient wifi;
HttpClient http = HttpClient(wifi, serverUrl);

String lastCardUID = "";

void setup() {
  Serial.begin(9600);
  delay(1000);
  
  Serial.println("Arduino RFID + WiFi Starting...");
  
  SPI.begin();
  rfid.PCD_Init();
  
  connectToWiFi();
}

void connectToWiFi() {
  Serial.print("Connecting to WiFi");
  
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("ERROR: WiFi module not found!");
    return;
  }
  
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(1000);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ WiFi Connected!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n❌ WiFi Failed!");
  }
}

void sendRFIDToCloud(String uid) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("No WiFi, can't send!");
    return;
  }
  
  Serial.print("Sending to cloud: ");
  Serial.println(uid);
  
  String postData = "{\"rfid_tag\":\"" + uid + "\"}";
  
  http.post(serverUrl, "application/json", postData);
  int statusCode = http.responseStatusCode();
  String response = http.responseBody();
  
  Serial.print("HTTP Status: ");
  Serial.println(statusCode);
  
  http.stop();
  
  if (statusCode == 200) {
    Serial.println("✅ Sent to cloud!");
  } else {
    Serial.println("❌ Failed to send");
  }
}

void loop() {
  if (rfid.PICC_IsNewCardPresent()) {
    if (rfid.PICC_ReadCardSerial()) {
      
      String uid = "";
      for (byte i = 0; i < rfid.uid.size; i++) {
        if (rfid.uid.uidByte[i] < 0x10) uid += "0";
        uid += String(rfid.uid.uidByte[i], HEX);
        if (i < rfid.uid.size - 1) uid += " ";
      }
      uid.toUpperCase();
      
      if (uid != lastCardUID) {
        Serial.println("Card tapped: " + uid);
        sendRFIDToCloud(uid);
        lastCardUID = uid;
      }
      
      rfid.PICC_HaltA();
      delay(1000);
    }
  }
  delay(50);
}