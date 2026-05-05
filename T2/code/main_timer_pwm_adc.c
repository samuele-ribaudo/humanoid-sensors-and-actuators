#include <atmega32/io.h>
#include <avr/interrupt.h>

// Global variable to hold the latest 8-bit ADC reading
volatile uint8_t adc_duty_cycle = 127;

// ADC Conversion Complete ISR
ISR(ADC_vect)
{
    // Read the 8-bit value from the high register (since ADLAR is set)
    adc_duty_cycle = ADCH; 
}

// TIMER0 Overflow ISR (Start of PWM cycle)
ISR(TIMER0_OVF_vect)
{
    PORTC |= (1 << PC0);        // Set PC0 HIGH
    OCR0 = adc_duty_cycle;      // Safely update the duty cycle for this period

    // Start the next ADC conversion
    ADCSRA |= (1 << ADSC);
}

// TIMER0 Compare Match ISR (End of HIGH time)
ISR(TIMER0_COMP_vect)
{
    PORTC &= ~(1 << PC0);       // Set PC0 LOW
}

int main(void)
{        
    cli();

    // Set PC0 as output
    DDRC |= (1 << PC0);

    // --- TIMER0 SETUP ---
    // Prescaler 1024
    TCCR0 |= (1 << CS02) | (1 << CS00);
    TCCR0 &= ~(1 << CS01);
    // Enable OVF and COMP interrupts
    TIMSK |= (1 << TOIE0) | (1 << OCIE0);

    // --- ADC SETUP ---
    // Select AVCC as reference (REFS0=1) and Left Adjust for 8-bit mode (ADLAR=1)
    // MUX3..0 = 0000 (defaults to ADC0)
    ADMUX = (1 << REFS0) | (1 << ADLAR);

    // Enable ADC (ADEN), Enable Interrupt (ADIE), and set Prescaler to 128 (ADPS2..0 = 1)
    ADCSRA = (1 << ADEN) | (1 << ADIE) | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);

    sei();

    // Kick off the very first ADC conversion to get things started
    ADCSRA |= (1 << ADSC);

    while(1)
    {
    }
    
    return 0;
}
