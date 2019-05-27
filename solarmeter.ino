//const double vv = 2.87/1024;
const double vv = 5.0/1023*11989.0/1979;
const double aa = 5.0/1023*10;
const int samples = 50;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  long v = 0;
  long a = 0;
  for(int i = 0; i < samples; ++i)
  {
    v += analogRead(A2);
    a += analogRead(A0);
    delay(2);
  }
  float volts = v/samples; //in Volt
  float amps = a/samples;//in Amp
  //long t = millis()/1000;
  //volts = 0;
  Serial.print(volts);
  Serial.print(" ");
  Serial.println(amps);
  delay(100);
}
