//#include <SD.h>
//#include <SPI.h>
//File myFile;
const int OhmMeter = 0;
const int R3 = 6;
const int R2 = 5;
const int R1 = 4;
float R = 0.00;
void calculate_resistor() {
    float v_ref = 4.94;
    float r1 = 0.00;
    float r_ref1 = 1000.00;
    float adc_value1 = 0.00;
    float voltage1 = 0.00;
    float r2 = 0.00;
    float r_ref2 = 10000.00;
    float adc_value2 = 0.00;
    float voltage2 = 0.00;
    float r3 = 0.00;
    float r_ref3 = 100000.00;
    float adc_value3 = 0.00;
    float voltage3 = 0.00;
    pinMode(R1, OUTPUT);
    pinMode(R2, INPUT);
    pinMode(R3, INPUT);
    digitalWrite(R1, HIGH);
    for (int i = 0; i < 20; i++) {
        adc_value1 = adc_value1 + analogRead(OhmMeter);
        delay(3);
    }

    adc_value1 = adc_value1 / 20;

    if (adc_value1 < 1022.90) {
        voltage1 = ((adc_value1 * v_ref) / 1024);
        r1 = (voltage1 * r_ref1) / (v_ref - voltage1);
    }
    pinMode(R1, INPUT);
    pinMode(R2, OUTPUT);
    pinMode(R3, INPUT);
    digitalWrite(R2, HIGH);
    for (int i = 0; i < 20; i++) {
        adc_value2 = adc_value2 + analogRead(OhmMeter);
        delay(3);
    }
    adc_value2 = adc_value2 / 20;
    if (adc_value2 < 1022.90) {
        voltage2 = ((adc_value2 * v_ref) / 1024);

        r2 = (voltage2 * r_ref2) / (v_ref - voltage2);
    }
    pinMode(R1, INPUT);
    pinMode(R2, INPUT);
    pinMode(R3, OUTPUT);
    digitalWrite(R3, HIGH);
    for (int i = 0; i < 20; i++) {
        adc_value3 = adc_value3 + analogRead(OhmMeter);
        delay(3);
    }
    adc_value3 = adc_value3 / 20;
    if (adc_value3 < 1022.90) {
        voltage3 = ((adc_value3 * v_ref) / 1024);
        r3 = (voltage3 * r_ref3) / (v_ref - voltage2);
    }
    r1 = r1 / 1000;

    r2 = r2 / 1000;

    r3 = r3 / 1000;
    if (r1 < 2 && r2 < 101 && r3 < 1001)
        R = r1 * 1000;
    else if (r1 > 2 && r2 < 101 && r3 < 1001)
        R = r2;
    else if (r1 > 2 && r2 > 101 && r3 < 2000)
        R = r3;
    else
        R = -1.00;
    Serial.print("R = ");

    Serial.println(R, 2);
}
void setup() {
    Serial.begin(9600);
    while (!Serial) {
        ;
    }
    if (!SD.begin(10)) {
        while (1)
            ;
    }
    // We don't need the sd card anymore
//    myFile = SD.open("test.csv", FILE_WRITE);
//    if (myFile) {
//        Serial.println("working");
//    } else {
//        Serial.println("SD Card failure");
//    }
}
int iter = 0;
void loop() {
    calculate_resistor();
//    myFile = SD.open("test.csv", FILE_WRITE);
    Serial.println("_________________________________________");
//    myFile.println(String(iter) + "," + String(R));
//    myFile.close();
    iter++;

    delay(500);
}
/*
 * Notes: 10,000 Ohms displayed as roughly 100 (97.53). This could just be due to manufacturing proccess of resistor and slight inaccuracy.
 * 78 sheets 7/12/21l
 */
