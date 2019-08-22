#include "opc.h"

#include <memory>

#include <PBDriverAdapter.hpp>
#include <ESP8266WiFi.h>

// For wifi manager
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>

// #define DEBUG 1
// #define DEBUG_WAIT 1

#define COLOR_CHANNELS 4
#define CHANNEL_PIXELS 150
#define COLOR_ORDER 1, 0, 2, 3

// const char* ssid     = "MySpectrumWiFi4b-2G";
// const char* password = "wagongenius158";

// const char* ssid     = "ESPap";
// const char* password = "thereisnospoon";

// const char* ssid     = "doodleedoo";
// const char* password = "7758469943";

const char* ssid = "RingMyBell";
const char* password = NULL;

PBDriverAdapter driver;
WiFiServer server(7890);

void setup() {
  Serial.begin(115200);
  delay(100);

  //WiFiManager wifiManager;
  //wifiManager.autoConnect("flipper", "woopwoop");

  PBChannelHeader chan_header({COLOR_CHANNELS, COLOR_ORDER, CHANNEL_PIXELS});
  driver.configureChannels(std::unique_ptr<std::vector<PBChannel>>(new std::vector<PBChannel>({
        PBChannel{chan_header, 0, 0},
        PBChannel{chan_header, 0, 1},
        PBChannel{chan_header, 0, 2},
        PBChannel{chan_header, 0, 3},
        PBChannel{chan_header, 0, 4},
        PBChannel{chan_header, 0, 5},
        PBChannel{chan_header, 0, 6},
        PBChannel{chan_header, 0, 7},
        PBChannel{chan_header, 0, 8},
        PBChannel{chan_header, 0, 9},
        PBChannel{chan_header, 0, 10},
        PBChannel{chan_header, 0, 11},
        PBChannel{chan_header, 0, 12},
        PBChannel{chan_header, 0, 13},
        PBChannel{chan_header, 0, 14},
        PBChannel{chan_header, 0, 15},
  })));

  driver.begin();


  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  driver.show([](uint16_t index, uint8_t rgbw[]) {
    if (index % 5 == 0) {
      rgbw[0] = 32;
      rgbw[1] = 0;
      rgbw[2] = 0;
      rgbw[3] = 0;
    } else {
      rgbw[0] = 0;
      rgbw[1] = 0;
      rgbw[2] = 0;
      rgbw[3] = 0;
    }
  });
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  driver.show([](uint16_t index, uint8_t rgbw[]) {
    if (index % 5 == 0) {
      rgbw[0] = 0;
      rgbw[1] = 32;
      rgbw[2] = 0;
      rgbw[3] = 0;
    } else {
      rgbw[0] = 0;
      rgbw[1] = 0;
      rgbw[2] = 0;
      rgbw[3] = 0;
    }
  });
  delay(500);
  //*/

  server.begin();
}

byte readByte(WiFiClient &client) {
  while (client.available() == 0) { }

  return client.read();
}

int ReadMessageHeader(WiFiClient &client, OPCMessageHeader &h) {
  uint8_t header[4];
  if (client.readBytes(header, sizeof(header)) != sizeof(header)) {
    return 0;
  }

  //byte b = client.read();

  uint8_t b = header[0];
  // #ifdef DEBUG
  // Serial.print("channel ");
  // Serial.println(b);
  // #endif
  if (b < 0) {
    return -1;
  }
  h.channel = (uint8_t) b;

  //b = client.read();
  b = header[1];
  // #ifdef DEBUG
  // Serial.print("command ");
  // Serial.println(b);
  // #endif
  if (b < 0) {
    return -1;
  }
  h.command = (uint8_t) b;

  //b = client.read();
  b = header[2];
  // #ifdef DEBUG
  // Serial.print("length 1 ");
  // Serial.println(b);
  // #endif
  if (b < 0) {
    return -1;
  }
  h.length = ((uint8_t) b) << 8;

  //b = client.read();
  b = header[3];
  // #ifdef DEBUG
  // Serial.print("length 2 ");
  // Serial.println(b);
  // #endif
  if (b < 0) {
    return -1;
  }
  h.length = h.length | ((uint8_t) b);

  return 0;
}

void waitSerial() {
  while (Serial.available() == 0)
    {}
  Serial.read();
}

void loop() {
  WiFiClient client = server.available();
  if (!client || !client.connected()) {
    return;
  }
  client.setNoDelay(1);
  client.setTimeout(5000);

  Serial.println("Connected to client");

  bool skipframe = false;
  while (1) {
  uint16_t pixels;
  uint8_t pixeldata[450];
  driver.show([&client, &pixels, &pixeldata, &skipframe](uint16_t index, uint8_t rgbw[]) {
    if (skipframe) {
      return;
    }
    if (index == 0) {
#ifdef DEBUG_WAIT
      waitSerial();
#endif

      if (!client || !client.connected()) {
        Serial.println("client no longer connected");
        skipframe = true;
        return;
      }
      OPCMessageHeader h;
      if (ReadMessageHeader(client, h) == -1) {
        Serial.println("error reading message header");
        client.stop();
        skipframe = true;
        return;
      }

      if (client.readBytes(pixeldata, 450) != 450) {
        Serial.println("exited due to timeout");
        client.stop();
        skipframe = true;
        return;
      }

      // if (client.readBytes(rgbw, 3) != 3) {
      //   Serial.println("exited due to timeout");
      //   client.stop();
      //   skipframe = true;
      //   return;
      // }

#ifdef DEBUG
      Serial.print("Channel: ");
      Serial.println(h.channel);
      Serial.print("Command: ");
      Serial.println(h.command);
      Serial.print("Length: ");
      Serial.println(h.length);
#endif

      pixels = h.length / 3;
    }

    if (index >= pixels) {
      return;
    }

    // if (client.readBytes(rgbw, 3) != 3) {
    // Serial.println("exited due to timeout");
    //   return;
    // }

    rgbw[0] = pixeldata[index * 3 + 0];
    rgbw[1] = pixeldata[index * 3 + 1];
    rgbw[2] = pixeldata[index * 3 + 2];

    /* rgbw[0] = readByte(client); */
    /* rgbw[1] = readByte(client); */
    /* rgbw[2] = readByte(client); */

/*     int res = client.read(rgbw, 3); */
#ifdef DEBUG
    //Serial.println(res);
    Serial.print(rgbw[0]);
    Serial.print(rgbw[1]);
    Serial.println(rgbw[2]);
#endif
  });

  if (skipframe) {
    return;
  }
  }
}
