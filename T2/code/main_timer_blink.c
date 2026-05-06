#include <atmega32/io.h>
#include <avr/interrupt.h>

volatile uint8_t count = 0;

void T2_init(){
    cli(); // disable interrupts
    TCCR2 &= ~((1 << CS22)|(1 << CS21)|(1 << CS20)); // clear prescaler bits
    TCCR2 |= (1 << CS22); // table 54 pag 127
    TIMSK |= (1 << TOIE2); // pag 130
    TCNT2 = 0; // reset the counter
    sei(); // enable interrupts
}

ISR(TIMER2_OVF_vect){
    count++;
    if(count >= 61){ // see explaination in the report
        PORTC ^= (1 << PC0); // Toggle the LED
        count = 0;       // Reset the counter
    }
}

int main (void)
{        
    DDRC |= (1 << PC0); // set PC0 as output
    T2_init();

    while(1);


    // Should never be reached    
    return 0;
}