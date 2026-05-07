#include <atmega32/io.h>
#include <avr/interrupt.h>

#define USE_FLEX_SENSOR // Comment out this line to use the Potentiometer settings

#ifdef USE_FLEX_SENSOR
    #define ADC_MIN 323
    #define ADC_MAX 787
#else
    #define ADC_MIN 0
    #define ADC_MAX 1023
#endif

#define SERVO_MIN 450
#define SERVO_MAX 2450

void adc_init();
void T1_init();


ISR(ADC_vect){ 
    uint16_t adc_val = ADC;

    // Mapping formula: (Value - InMin) * (OutMax - OutMin) / (InMax - InMin) + OutMin
    double mapped_val = (double)(adc_val - ADC_MIN) * (SERVO_MAX - SERVO_MIN) / (ADC_MAX - ADC_MIN) + SERVO_MIN;

    // Safety Constraints
    if (mapped_val < SERVO_MIN) mapped_val = SERVO_MIN;
    if (mapped_val > SERVO_MAX) mapped_val = SERVO_MAX;

    OCR1A = (uint16_t) mapped_val;
}


int main (void)
{            
    cli(); // disable interrupts during setup

    DDRD |= (1 << PD5); // OC1A output
    T1_init();
    adc_init();

    sei(); // enable interrupts after setup

    while(1);

    return 0;
}


void adc_init(){
    ADMUX |= (1 << REFS0); // pag. 214 - AVCC with external capacitor at AREF pin
    ADCSRA |= (1 << ADPS0)|(1 << ADPS1); // pag. 216 - 8 prescaler
    ADCSRA |= (1 << ADATE); // pag. 218 - If ADATE is cleared, the ADTS2:0 settings will have no effect.
    ADCSRA |= (1 << ADIE); // pag. 216 - Enable ADC interrupt
    SFIOR &= ~((1 << ADTS0)|(1 << ADTS1)|(1 << ADTS2)); // pag. 218 - Free Running mode
    ADMUX &= ~(1 << ADLAR); // pag. 214 and 217 - 10 bit
    ADCSRA |= (1 << ADEN); // pag. 216 - ADC enable
    ADCSRA |= (1 << ADSC); // pag. 204 - The first conversion must be started by writing a logical one to the ADSC bit in ADCSRA. 
    ADMUX &= 0xE0; // pag. 215 - clear MUX4:0 bits to select channel 0 by default
}


void T1_init(){
    // Fast PWM Mode 14 - table 47 pag 109
    TCCR1A |= (1 << WGM11);
    TCCR1B |= (1 << WGM13)|(1 << WGM12);
    TCCR1A |= (1 << COM1A1); // Clear OC1A/OC1B on compare match (Setoutput to low level) - table 44 pag 107
    TCCR1B |= (1 << CS10); // Prescaler = 1

    ICR1 = 20000; // 20ms period -> ICR1 defines the TOP value for Fast PWM mode 14
    OCR1A = SERVO_MIN; // Start at min position
}