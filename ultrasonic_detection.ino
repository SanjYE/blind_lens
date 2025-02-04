const int triggerPin = 9;
const int echoPin = 10;
const int ledPin = 13;
const int safetyThreshold = 10;
 
long duration;
int distance;

void setup() {
  pinMode(triggerPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void measureDistance() {
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;
}

void alertUser() {
  if (distance <= safetyThreshold) {
    digitalWrite(ledPin, HIGH);
    Serial.print('1'); 
  } 
  else {
    digitalWrite(ledPin, LOW);
    Serial.print('0'); 
  }
}

void loop() {
  measureDistance();
  alertUser();
  delay(500); 
}
