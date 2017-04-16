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
    if(info == 48){
      
      digitalWrite(CLOCK_PIN, HIGH);
      digitalWrite(CLOCK_PIN, LOW);
      unsigned char pc = 0;
      for(int i = 7; i>=0; i--){
         pc |= (digitalRead(dataPins[i]) << i)
      }
      Serial.println(pc);
    }
    
  }

}
