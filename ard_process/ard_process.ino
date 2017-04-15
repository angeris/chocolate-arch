int incomingByte = 0;   // for incoming serial data
unsigned char data[256];
void setup() {
  for(int i = 0; i<256; i++){
    data[i] = 0;
  }
  Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {

  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();
    if (incomingByte == 0) {
      //Serial.println("Writing Mem");
      unsigned char addr;
      while(Serial.available() == 0){}
      addr = Serial.read();
      //Serial.print("Writing To: ");
      //Serial.println(addr);
      unsigned char num_bytes;
      while(Serial.available() == 0){}
      num_bytes = Serial.read();
      //Serial.print("Writing # bytes: ");
      //Serial.println(num_bytes);
      unsigned char counter;
      while(num_bytes > 0){
        while(Serial.available() == 0){}
        data[addr+counter] = Serial.read();
        counter += 1;
        num_bytes -= 1;
      }
      digitalWrite(LED_BUILTIN, HIGH);
    }

    if (incomingByte == 1) {
      unsigned char addr;
      digitalWrite(LED_BUILTIN, HIGH);
      //Serial.println("Reading Mem");
      while(Serial.available() == 0){};
      addr = Serial.read();
       //Serial.print("Reading From: ");
       //Serial.println(addr);
      unsigned char num_bytes;
      while(Serial.available() == 0){};
      num_bytes = Serial.read();
      //Serial.print("Reading # bytes: ");
      //Serial.println(num_bytes);
      unsigned char counter = 0;
      while(counter < num_bytes){
        Serial.write(data[addr+counter]);
        counter ++;
      }
    }

    if (incomingByte == 10) {
      for(int i = 0; i<256; i++){
        data[i] = 0;
      }
      
    }
  }
}
