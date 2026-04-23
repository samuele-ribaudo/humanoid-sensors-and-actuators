// Get register definitions with auto complete
#include <atmega32/io.h>

// For delay functions: F_CPU has to be defined
#include <util/delay.h>

#define F_CPU 1000000UL


int main (void)
{
    DDRD &= ~(1 << D0);     // Set D0 as input
    DDRD |= (1 << D1);      // Set D1 as output

    UBBR = 0x00;



    // Should never be reached
    return 0;
}
