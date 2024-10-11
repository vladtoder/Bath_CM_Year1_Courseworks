#include <Servo.h>

Servo servo;

volatile unsigned long lastRedButtonPressTime = 0;
volatile unsigned long lastGreenButtonPressTime = 0;
const long debounceDelay = 200;  // Time in milliseconds

// Assign pins.
const int redLEDs[] = {4, 5, 6};
const int greenLEDs[] = {10, 12, 13};
const int blueRedLED = 8;
const int blueGreenLED = 9;
const int redButton = 2;
const int greenButton = 3;
const int servoPin = 11;
const int potentiometer = A0;

const int buzzer = A1;
bool buzzerON = false;

// Global variables.
int minDelayTime = 500;
int maxDelayTime = 1000;
int redRndNum;
int greenRndNum;
int blueRedLEDState; 
int blueGreenLEDState; 
float difficulty; // Potentiometer value.
volatile int redScore = 0;
volatile int greenScore = 0;

void setup() 
{
    Serial.begin(9600);

    // Set pin modes.
    for (int i=0; i<3; i++)
    {
        pinMode(redLEDs[i], OUTPUT);
        pinMode(greenLEDs[i], OUTPUT);
    }
    pinMode(blueRedLED, OUTPUT);
    pinMode(blueGreenLED, OUTPUT);
    pinMode(buzzer, OUTPUT);
    pinMode(redButton, INPUT);
    pinMode(greenButton, INPUT);
    pinMode(potentiometer, INPUT);

    servo.attach(servoPin);
    servo.write(90);

    // Trigger interrupts when a button is pressed (i.e. the pin goes from LOW to HIGH).
    attachInterrupt(0, redButtonPress, RISING); 
    attachInterrupt(1, greenButtonPress, RISING);
}

//run main program loop
void loop() 
{
    if buzzerON
    {
        tone(buzzer, 1000);
        delay(500);
        noTone(buzzer);
        buzzerON = false;
    }

    if (redScore > greenScore)
    {
       servo.write(135);
    }
    else if (greenScore > redScore)
    {
        servo.write(45);
    }

    difficulty = analogRead(potentiometer);
    if (difficulty != 0)
    {
        difficulty = difficulty / 1023;
    }
    else
    {
        difficulty = 1;
    }

    redRndNum = random(3); 
    greenRndNum = random(3);
    int redDelay = random(minDelayTime, maxDelayTime) * difficulty;
    int greenDelay = random(minDelayTime, maxDelayTime) * difficulty;
    const int redGreenDelay = 1000;

    // Turn on red LED.
    digitalWrite(redLEDs[redRndNum], HIGH);

    delay(redDelay);

    digitalWrite(redLEDs[redRndNum], LOW);
    blueRedLEDState = digitalRead(blueRedLED);

    // Turn off blue LED for the red player if they scored.
    if(blueRedLEDState == HIGH)
    {
        digitalWrite(blueRedLED, LOW);
    }


    delay(redGreenDelay);

    // Turn on green LED.
    digitalWrite(greenLEDs[greenRndNum], HIGH);
    // Turn off red LED.

    delay(greenDelay);

    blueGreenLEDState = digitalRead(blueGreenLED);
    // Turn off green LED.
    digitalWrite(greenLEDs[greenRndNum], LOW);
    // Turn off blue LED for the green player if they scored.
    if(blueGreenLEDState == HIGH)
    {
        digitalWrite(blueGreenLED, LOW);
    }
    delay(redGreenDelay);
}

void redButtonPress() {
    unsigned long currentMillis = millis();
    if (currentMillis - lastRedButtonPressTime > debounceDelay) 
    {
        lastRedButtonPressTime = currentMillis;
    for (int i=0; i<3; i++)
    {
        int redLEDState = digitalRead(redLEDs[i]);
        // If any one of the 3 LDEs is lit up, increment the score and turn on blue LED.
        if (redLEDState == HIGH)
        {
            digitalWrite(blueRedLED, HIGH); 
            redScore++;
            break;
        }
        // If none of the LEDs are lit up, decrement the score.
        else if (i == 2)
        {
           redScore--; 
            buzzerON = true;
        }
    }
    Serial.print("Red: ");
        Serial.println(redScore);
    }
    if (redScore >= 10)
    {
        while (true)
        {
            for (int i=0; i<3; i++)
                digitalWrite(redLEDs[i], HIGH);
            digitalWrite(blueRedLED, HIGH);
        }
    }
}

void greenButtonPress() {
    unsigned long currentMillis = millis();
    if (currentMillis - lastRedButtonPressTime > debounceDelay) 
    {
        lastRedButtonPressTime = currentMillis;
    for (int i=0; i<3; i++)
    {
        int greenLEDState = digitalRead(greenLEDs[i]);
        // If any one of the 3 LDEs is lit up, increment the score and turn on blue LED.
        if (greenLEDState == HIGH)
        {
            digitalWrite(blueGreenLED, HIGH); 
            greenScore++;
            break;
        } 
        // If none of the LEDs are lit up, decrement the score.
        else if (i == 2)
        {
            greenScore--; 
            buzzerON = true;
        }
    }
           Serial.print("Green: ");
            Serial.println(greenScore);
    }
    if (greenScore >= 10)
    {
        while (true)
        {
            for (int i=0; i<3; i++)
                digitalWrite(greenLEDs[i], HIGH);
            digitalWrite(blueGreenLED, HIGH);
        }
    }
}

