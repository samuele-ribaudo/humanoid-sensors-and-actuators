#include <atmega32/asm/io.h>

.global main

main:
    in r19, DDRC
    ori r19, 0x08
    andi r19, 0xEF
    out DDRC, r19

loop:
    ; read on pin 4
    in r19, PINC
    andi r19, 0x10
    lsr r19
    
    ; delay
    rcall delay

    ; mirror on pin 3
    in r18, PORTC
    andi r18, 0xF7
    or r18, r19
    out PORTC, r18
    
    rjmp loop

    ret                         ; exit, should never be reached

delay:
    ldi r18, 0x3F
    ldi r24, 0x0D
    ldi r25, 0x03
1:  subi r18, 0x01
    sbci r24, 0x00
    sbci r25, 0x00
    brne 1b ; local label backward
    rjmp 1f ; local label forward
1:  nop
    ret

.end