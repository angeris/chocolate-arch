int CLOCK_PIN = 13;

int dataPins[] = {2, 3, 4, 5, 6, 7, 8, 9};
void setup() {
  Serial.begin(9600);
  pinMode(CLOCK_PIN, OUTPUT);

  for(int i = 7; i>=0; i--){
      pinMode(dataPins[i], INPUT);
  }
    
}

void loop() {
  if (Serial.available() > 0) {
    unsigned char info = Serial.read();

    // Read Program Counter From Digital Bus
    if(info == 48){
      Serial.print("Printing program counter: ");
      digitalWrite(CLOCK_PIN, HIGH);
      digitalWrite(CLOCK_PIN, LOW);
      unsigned char pc = 0;
      for(int i = 7; i>=0; i--){
         pc |= (digitalRead(dataPins[i]) << i);
      }
      Serial.println(pc);
    }
    if(info == 49){
      Serial.print("Printing Registers...");
      for(int i = 7; i>=0; i--){
          pinMode(dataPins[i], OUTPUT);
      }

      for (int k = 0; k < 4; k++) {  // Do this for 4 registers.
        unsigned char instr = 50 + k;
        for(int i = 7; i>=0; i--){
           digitalWrite(dataPins[i], instr & (1 << i));
        }

        for(int i = 7; i>=0; i--){
           pinMode(dataPins[i], OUTPUT);
        }
        unsigned char reg = 0;
        for(int i = 7; i>=0; i--){
          reg |= (digitalRead(dataPins[i]) << i);
        }
        Serial.print("r");
        Serial.print(k);
        Serial.print(": ");
        Serial.println(reg);
      }
      
    }
    
    
    
  }

}
