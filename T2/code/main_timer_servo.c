#include <atmega32/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

// 1MHz clock -> 1 tick = 1us
#define SERVO_MIN    450   // 450us (Full Left)
#define SERVO_MID    1450  // 1450us (Center)
#define SERVO_MAX    2450  // 2450us (Full Right)

void T1_init(){

    // Fast PWM Mode 14 - table 47 pag 109
    TCCR1A |= (1 << WGM11);
    TCCR1B |= (1 << WGM13)|(1 << WGM12);
    TCCR1A |= (1 << COM1A1); // Clear OC1A/OC1B on compare match (Setoutput to low level) - table 44 pag 107
    TCCR1B |= (1 << CS10); // Prescaler = 1

    ICR1 = 20000; // 20ms period -> ICR1 defines the TOP value for Fast PWM mode 14
    OCR1A = SERVO_MID; // Start at the middle position -> OCR1A defines the duty cycle
}

int main (void)
{        
    DDRD |= (1 << PD5); // Set PD5 (OC1A) as output
    T1_init();

    while(1){

        OCR1A = SERVO_MIN;
        _delay_ms(1000);

        OCR1A = SERVO_MID;
        _delay_ms(1000);

        OCR1A = SERVO_MAX;
        _delay_ms(1000);
    }
    
    // Should never be reached    
    return 0;
}