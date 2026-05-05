#include <atmega32/io.h>
#include <avr/interrupt.h> // Required for ISR, cli(), and sei()

// Global variable to keep track of the number of timer overflows (T.7.2)
// 'volatile' ensures the compiler knows it changes inside an ISR.
volatile uint8_t overflow_count = 0;

// Interrupt Service Routine catching the TIMER2 overflow vector (T.7.2)
ISR(TIMER2_OVF_vect)
{
    overflow_count++;
    
    // Toggle the LED state after 61 overflows (~1 second)
    if (overflow_count >= 61) 
    {
        PORTC ^= (1 << PC0); // Toggle the PC0 pin
        overflow_count = 0;  // Reset the overflow counter
    }
}

int main (void)
{        
    // 1. Disable interrupts during configuration (T.7.1)
    cli();

    // 2. Set C0 as the desired output pin and initialize it low (T.7.1)
    DDRC |= (1 << PC0);
    PORTC &= ~(1 << PC0);

    // 3. Initialize the TIMER2 Counter Register to 0 (T.7.1)
    TCNT2 = 0;

    // 4. Initialize the TIMER2 clock prescaler to 64 (T.7.1)
    TCCR2 |= (1 << CS22);
    TCCR2 &= ~((1 << CS21) | (1 << CS20)); 

    // 5. Set TIMER2 to issue an interrupt when an overflow event is detected (T.7.1)
    TIMSK |= (1 << TOIE2);

    // 6. Re-enable global interrupts (T.7.1)
    sei();

    // 7. Define a dummy infinite loop to maintain microcontroller activity (T.7.1)
    while(1)
    {
        // The CPU sits here while the ISR toggles the LED in the background!
    }

    // Should never be reached    
    return 0;
}
