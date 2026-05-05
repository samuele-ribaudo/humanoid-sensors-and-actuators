#include <atmega32/io.h>
#include <avr/interrupt.h>

// Interrupt Service Routine for TIMER0 Overflow (Start of the PWM period)
ISR(TIMER0_OVF_vect)
{
    PORTC |= (1 << PC0);  // Set PC0 HIGH
}

// Interrupt Service Routine for TIMER0 Compare Match (End of the HIGH time)
ISR(TIMER0_COMP_vect)
{
    PORTC &= ~(1 << PC0); // Set PC0 LOW
}

int main(void)
{        
    // 1. Disable interrupts during setup
    cli();

    // 2. Set PC0 as output
    DDRC |= (1 << PC0);
    PORTC &= ~(1 << PC0); // Start low

    // 3. Set TIMER0 clock prescaler to 1024
    // CS02 = 1, CS01 = 0, CS00 = 1
    TCCR0 |= (1 << CS02) | (1 << CS00);
    TCCR0 &= ~(1 << CS01);

    // 4. Enable Overflow and Compare Match interrupts for TIMER0
    TIMSK |= (1 << TOIE0) | (1 << OCIE0);

    // 5. Set the Compare Register to a fixed duty cycle 
    // 127 out of 255 gives approximately a 50% duty cycle
    OCR0 = 127;

    // 6. Enable global interrupts
    sei();

    // Dummy infinite loop
    while(1)
    {
    }
    
    return 0;
}
