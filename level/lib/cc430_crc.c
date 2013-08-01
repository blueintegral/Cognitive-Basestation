#include <stdint.h>
#include <stdio.h>
#include <inttypes.h>

#define CRC16_POLY 0x8005 

uint16_t culCalcCRC(uint8_t crcData, uint16_t crcReg) { 
    uint8_t i;
    for (i = 0; i < 8; i++) { 
        if (((crcReg & 0x8000) >> 8) ^ (crcData & 0x80)) 
            crcReg = (crcReg << 1) ^ CRC16_POLY; 
	else 
            crcReg = (crcReg << 1); 
        crcData <<= 1; 
    } 
    return crcReg; 
}// culCalcCRC 

//---------------------------------------------------------------- 

// Example of Usage 

#define CRC_INIT 0xFFFF 

int main(void){
    uint8_t txBuffer[2] = {1, 0}; 
    uint16_t checksum; 
    uint8_t i; 
    checksum = CRC_INIT;   // Init value for CRC calculation 

    for (i = 0; i < sizeof(txBuffer); i++) 
        checksum = culCalcCRC(txBuffer[i], checksum);

    printf("%"PRIu16"\n", checksum);
    return 0;
}
