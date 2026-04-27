#include <atmega32/asm/io.h>

.global add512

add512:

// ptr to a is in R23:R22
// ptr to b is in R21:R20
// ptr to c is in R25:R24

        push r28        ; L1 slide 43 call saved rgister
        push r29

        movw r26, r22   ; move a into X -> r26:r27
        movw r28, r20   ; move b into Y -> r28:r29
        movw r30, r24   ; move c into Z -> r30:r31

        clc             ; set carry to 0
        ldi r18, 64     ; counter value (512bit / 8bit)

loop:   ld r19, X+
        ld r20, Y+
        adc r19, r20
        st Z+, r19

        dec r18         ; affects only Z,N,V and not C
        brne loop
    
        pop r29
        pop r28

        ret

.end