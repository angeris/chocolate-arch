int incomingByte = 0;   // for incoming serial data

int hiloPin = 12;

int dataPins[] = {2, 3, 4, 5, 6, 7, 8, 9};
unsigned char data[256];
void setup() {
  for(int i = 0; i<256; i++){
    data[i] = 0;
  }
  Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(hiloPin, INPUT);
}

bool getHilo(){
  return digitalRead(hiloPin);
}
void loop() {
  
  if(getHilo()){
    unsigned char addr = 0;
    for(int i = 7; i>=0; i--){
      pinMode(dataPins[i], INPUT);
    }

    for(int i = 7; i>=0; i--){
      addr |= digitalRead(dataPins[i]) << i;
    }

    while(getHilo()){};

    for(int i = 7; i>=0; i--){
      pinMode(dataPins[i], OUTPUT);
    }

    unsigned char val = data[addr];
    for(int i = 7; i>=0; i--){
      digitalWrite(dataPins[i], val & (1 << i));
    }
    
  }
  
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();
    if (incomingByte == 0) {

      // Read in metadata
      unsigned char addr;
      while(Serial.available() == 0){}
      addr = Serial.read();
      
      unsigned char num_bytes;
      while(Serial.available() == 0){}
      num_bytes = Serial.read();
      
      unsigned char counter;
      while(num_bytes > 0){
        while(Serial.available() == 0){}
        data[addr+counter] = Serial.read();
        counter += 1;
        num_bytes -= 1;
      }
      
    }

    if (incomingByte == 1) {
      unsigned char addr;
      while(Serial.available() == 0){};
      addr = Serial.read();
      unsigned char num_bytes;
      while(Serial.available() == 0){};
      num_bytes = Serial.read();
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
