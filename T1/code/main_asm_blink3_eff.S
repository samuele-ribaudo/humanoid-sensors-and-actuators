#include <atmega32/asm/io.h>

.global main

main:
    in r18, DDRC
    ori r18, 0x07
    out DDRC, r18

loop:
    in r18, PORTC
    andi r18, 0xF8
    ori r18, 0x01
    out PORTC, r18
    rcall delay

    in r18, PORTC
    andi r18, 0xF8
    ori r18, 0x02
    out PORTC, r18
    rcall delay

    in r18, PORTC
    andi r18, 0xF8
    ori r18, 0x04
    out PORTC, r18
    rcall delay

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