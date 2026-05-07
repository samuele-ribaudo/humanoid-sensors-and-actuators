#include <atmega32/io.h>
#include <atmega32/uart.h>
#include <util/delay.h>

void adc_read10Blocking(uint16_t* b);
void adc_init();

int main (void)
{            
    uart_setBaudrateReg(CALC_BAUD_VAL(62500));
    uart_setFormat();
    uart_enable();

    adc_init();

    uint16_t val;

    while(1)
    {
        _delay_ms(10);

        adc_read10Blocking(&val);
        
        uart_writeByteBlocking((uint8_t)(val >> 8)); // Send the High Byte first (bits 9 and 8)
        uart_writeByteBlocking((uint8_t)(val & 0xFF)); // Send the Low Byte second (bits 7 through 0)
    }

    return 0;
}

void adc_init(){
    ADMUX |= (1 << REFS0); // pag. 214 - AVCC with external capacitor at AREF pin
    ADCSRA |= (1 << ADPS0)|(1 << ADPS1); // pag. 216 - 8 prescaler
    ADCSRA |= (1 << ADATE); // pag. 218 - If ADATE is cleared, the ADTS2:0 settings will have no effect. 
    SFIOR &= ~((1 << ADTS0)|(1 << ADTS1)|(1 << ADTS2)); // pag. 218 - Free Running mode
    ADMUX &= ~(1 << ADLAR); // pag. 214 and 217 - 10 bit
    ADCSRA |= (1 << ADEN); // pag. 216 - ADC enable
    ADCSRA |= (1 << ADSC); // pag. 204 - The first conversion must be started by writing a logical one to the ADSC bit in ADCSRA. 
    ADMUX &= 0xE0; // pag. 215 - clear MUX4:0 bits to select channel 0 by default
}

void adc_read10Blocking(uint16_t* b){
    *b = 0x0000;

    while(!(ADCSRA & (1 << ADIF))); // pag. 216 - wait for conversion to complete
    ADCSRA |= (1 << ADIF); // pag. 216 - ADIF is cleared by writing a logical one to the flag

    *b = ADC; // Read the 10-bit result from ADC
}