#include <Arduino.h>

// Пин для потенциометра
#define POT_PIN 34 // GPIO34 - пин потенциометра
#define SPEAKER_PIN 26

// Настройка звука
#define BASE_SAMPLE_RATE 12000
#define MAX_SAMPLE_RATE 20000
#define MIN_VOLUME 50
#define MAX_VOLUME 255

// Аудиоданные из `idle.h`
extern const unsigned char idle_data[];
extern const int idle_len;

// Аудиоданные из `start.h`
extern const unsigned char start_data[];
extern const int start_len;

volatile uint16_t sampleIndex = 0;
volatile uint32_t sampleRate = BASE_SAMPLE_RATE;
volatile uint8_t volume = MIN_VOLUME;
volatile const unsigned char* currentSampleData = start_data;
volatile int currentSampleLen = start_len;

hw_timer_t* timer = nullptr;
bool isStartPlayed = false;

void IRAM_ATTR playNextSample();
void updateEngineSound();

void setup() {
  Serial.begin(115200); // Инициализация Serial Monitor
  pinMode(POT_PIN, INPUT); // Настройка пина для потенциометра
  pinMode(SPEAKER_PIN, OUTPUT);

  // Настройка PWM
  ledcSetup(0, BASE_SAMPLE_RATE, 8);
  ledcAttachPin(SPEAKER_PIN, 0);

  // Настройка таймера
  timer = timerBegin(0, 80, true);
  timerAttachInterrupt(timer, &playNextSample, true);
  timerAlarmWrite(timer, 1000000 / BASE_SAMPLE_RATE, true);
  timerAlarmEnable(timer);

  Serial.println("Воспроизведение start.raw...");
}

void loop() {
  updateEngineSound();

  if (isStartPlayed && currentSampleData != idle_data) {
    currentSampleData = idle_data;
    currentSampleLen = idle_len;
    sampleIndex = 0;
    Serial.println("Воспроизведение idle.raw...");
  }
}

// Прерывание для воспроизведения следующего сэмпла
void IRAM_ATTR playNextSample() {
  if (sampleIndex < currentSampleLen) {
    uint8_t sample = currentSampleData[sampleIndex++];
    sample = (sample * volume) / 255;
    ledcWrite(0, sample);
  } else {
    if (currentSampleData == start_data) {
      isStartPlayed = true;
    }
    sampleIndex = 0;
  }
}

// Обновление звука двигателя
void updateEngineSound() {
  int potValue = analogRead(POT_PIN); // Считываем значение потенциометра

  // Отладка
  Serial.print("Значение потенциометра: ");
  Serial.println(potValue);

  sampleRate = map(potValue, 0, 4095, BASE_SAMPLE_RATE, MAX_SAMPLE_RATE);
  volume = map(potValue, 0, 4095, MIN_VOLUME, MAX_VOLUME);
  timerAlarmWrite(timer, 1000000 / sampleRate, true);
}
