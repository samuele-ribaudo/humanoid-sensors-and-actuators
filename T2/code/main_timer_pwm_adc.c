#include <atmega32/io.h>
#include <avr/interrupt.h>

volatile uint8_t duty_cycle = 0;

ISR(ADC_vect){
    duty_cycle = ADCH; // Read the ADC value and store it in duty_cycle
}

ISR(TIMER0_OVF_vect){ 
    // Only turn the LED ON if the duty cycle is not 0
    if (duty_cycle > 3) {
        PORTC |= (1 << PC0); 
    } else {
        PORTC &= ~(1 << PC0); // Force it OFF just in case
    }
    
    OCR0 = duty_cycle; // Safely update the duty cycle for this period
    ADCSRA |= (1 << ADSC); // Start the next ADC conversion
}

ISR(TIMER0_COMP_vect){ 
    // Only turn the LED OFF if the duty cycle is not at absolute maximum
    if (OCR0 < 252) {
        PORTC &= ~(1 << PC0); 
    }
}

void ADC_init(){
    ADMUX |= (1 << REFS0); // pag. 214 - AVCC with external capacitor at AREF pin
    ADMUX |= (1 << ADLAR); // pag. 214 and 217 - access conversion in ADCH
    ADCSRA |= (1 << ADPS0)|(1 << ADPS1)|(1 << ADPS2); // pag. 216 - ADC Prescaler Select Bits
    ADCSRA |= (1 << ADIE); // pag. 216 - ADC Interrupt Enable
    ADCSRA |= (1 << ADEN); // pag. 216 - ADC Enable
}

void T0_init(){
    TCCR0 &= ~((1 << CS02)|(1 << CS01)|(1 << CS00)); // clear prescaler bits
    TCCR0 |= (1 << CS02)|(1 << CS00); // table 42 pag 82
    TIMSK |= (1 << TOIE0)|(1 << OCIE0); // pag 83
    TCNT0 = 0; // reset the counter
}

int main (void)
{        
    cli(); // disable interrupts

    DDRC |= (1 << PC0); // set PC0 as output
    ADC_init();
    T0_init();

    sei(); // enable interrupts

    ADCSRA |= (1 << ADSC); // Start the first conversion

    while(1);
    
    // Should never be reached    
    return 0;
}
