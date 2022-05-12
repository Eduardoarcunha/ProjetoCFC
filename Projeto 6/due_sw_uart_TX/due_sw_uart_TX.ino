#include "sw_uart.h"

due_sw_uart uart;

//0110 0001
//inverso: 1000 0110

void setup() {
  //baudrate = 9600
  Serial.begin(9600);
  sw_uart_setup(&uart, 3);

}


void loop() {
 send_byte();
 delay(5);
 exit(0);
}



void send_byte() {
  sw_uart_send_byte(&uart);
}
