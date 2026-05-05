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

    uint8_t val;
    uint8_t samples[1024];

    adc_init();

    uint8_t ch = 0;

    ADMUX &= 0xE0; // pag. 215 - clear MUX4:0 bits
    ADMUX |= (ch & 0x1F); // pag. 215 - MUX4:0 bits

    while(1){
        _delay_ms(10);

        PORTC |= (1 << PC1); // charge the capacitor

        for(int i = 0; i < 1024; i++) {
            while(!(ADCSRA & (1 << ADIF))); // pag. 216 - wait for conversion to complete
            ADCSRA |= (1 << ADIF); // pag. 216 - ADIF is cleared by writing a logical one to the flag
            samples[i] = ADCH;              // Store 8-bit result
        }

        uart_writeBlocking (samples, 1024); // send to the uart

        _delay_ms(10);

        PORTC &= ~(1 << PC1); // discharge the capacitor

        for(int i = 0; i < 1024; i++) {
            while(!(ADCSRA & (1 << ADIF))); // pag. 216 - wait for conversion to complete
            ADCSRA |= (1 << ADIF); // pag. 216 - ADIF is cleared by writing a logical one to the flag
            samples[i] = ADCH;              // Store 8-bit result
        }

        uart_writeBlocking (samples, 1024);
    }

    return 0;
}


void adc_init(){
    ADMUX |= (1 << REFS0); // pag. 214 - AVCC with external capacitor at AREF pin
    ADCSRA |= (1 << ADPS0); // pag. 216 - ADC Prescaler Select Bits
    ADCSRA |= (1 << ADATE); // pag. 218 - If ADATE is cleared, the ADTS2:0 settings will have no effect. 
    SFIOR &= ~((1 << ADTS0)|(1 << ADTS1)|(1 << ADTS2)); // pag. 218 - Free Running mode
    ADMUX |= (1 << ADLAR); // pag. 214 and 217 - access conversion in ADCH
    ADCSRA |= (1 << ADEN); // pag. 216 - ADC enable
    ADCSRA |= (1 << ADSC); // pag. 204 - The first conversion must be started by writing a logical one to the ADSC bit in ADCSRA. 
}
