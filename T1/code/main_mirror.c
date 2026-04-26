// Get register definitions with auto complete
#include <atmega32/io.h>

// For delay functions: F_CPU has to be defined
#include <util/delay.h>
#define F_CPU 1000000UL



int main (void)
{
    DDRC |= (1 << PC3); 
    DDRC &= ~(1 << PC4);

    unsigned char temp;

    while(1){
        temp = (PINC >> PC4) & 1;
        
        _delay_ms(1000);
        if(temp) PORTC |= (1 << PC3);
        else PORTC &= ~(1 << PC3);
    }

    // Should never be reached
    return 0;
}
