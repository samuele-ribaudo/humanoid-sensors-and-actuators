#include <atmega32/io.h>
#include <avr/interrupt.h>

void T0_init(){
    cli(); // disable interrupts
    TCCR0 &= ~((1 << CS02)|(1 << CS01)|(1 << CS00)); // clear prescaler bits
    TCCR0 |= (1 << CS02)|(1 << CS00); // table 42 pag 82
    TIMSK |= (1 << TOIE0)|(1 << OCIE0); // pag 83
    TCNT0 = 0; // reset the counter
    OCR0 = 127; // 50% duty cycle of 255
    sei(); // enable interrupts
}

ISR(TIMER0_OVF_vect){ // This ISR is called when the timer overflows
    PORTC |= (1 << PC0); // Set the LED
}

ISR(TIMER0_COMP_vect){ // This ISR is called when the timer reaches the value in OCR0
    PORTC &= ~(1 << PC0); // Clear the LED
}

int main (void)
{       
    DDRC |= (1 << PC0); // set PC0 as output
    T0_init(); 

    while(1);

    // Should never be reached    
    return 0;
}
