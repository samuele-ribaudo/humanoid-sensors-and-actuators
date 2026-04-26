// Get register definitions with auto complete
#include <atmega32/io.h>

// For delay functions: F_CPU has to be defined
#include <util/delay.h>
#define F_CPU 1000000UL


void USART_Init(unsigned int baud){
    DDRD &= ~(1 << PD0);     // Set D0 (RXD) as input
    DDRD |= (1 << PD1);      // Set D1 (TXD) as output

    unsigned int val = F_CPU / (16UL * baud) - 1; // page 143 - table 60 -> asynchronous normal mode

    UBRRH = (unsigned char) val >> 8;
    UBRRL = (unsigned char) val;
    
    // Enable receiver and transmitter
    UCSRB |= (1 << RXEN)|(1 << TXEN);
    
    // Page 163 - asynchronous (UMSEL=0), no parity (UPM1:0=0), 1 stop bit (USBS=0), 8-bit (UCSZ1:0=3)
    UCSRC = (1 << URSEL)|(3 << UCSZ0); // UCSRC = 0b10000110; 
}


void USART_Transmit(unsigned char data){
    // Wait for empty transmit buffer
    while (!(UCSRA & (1 << UDRE))); // page 159 and 160
    // Put data into buffer, sends the data
    UDR = data;
}


void USART_SendMessage(char* message){
    int i = 0;
    while(message[i] != '\0'){
        USART_Transmit(message[i]);
        i++;
    }
}


int main (void){

    USART_Init(62500);
    // USART_SendMessage("Hello World!\n");
    while(1){
        USART_SendMessage("Hello World!\n");
        _delay_ms(1000);
    }
    // Should never be reached
    return 0;
}
