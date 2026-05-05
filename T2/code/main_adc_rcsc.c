#include <atmega32/io.h>

#include <atmega32/uart.h>
#include <atmega32/adc.h>

#include <util/delay.h>

void adc_init();


int main (void)
{            
    DDRC  = 0xFF;

    uart_setBaudrateReg(CALC_BAUD_VAL(62500));
    uart_setFormat();
    uart_enable();

    adc_setStdConfig();
    adc_enable();

    uint8_t samples[1024];


    while(1){
        _delay_ms(10);

        PORTC |= (1 << PC1); // charge the capacitor

        for(int i = 0; i < 1024; i++) {
            adc_readBlocking(&samples[i], 0);
        }

        PORTC &= ~(1 << PC1); // discharge the capacitor

        //uart_writeBlocking(samples, 1024); // send to the uart
        for(int i = 0; i < 1024; i++){
            uart_writeByteBlocking(samples[i]);
        }
    }

    return 0;
}