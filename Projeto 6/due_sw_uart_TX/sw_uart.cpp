//Inclui um arquivo no codigo
#include "sw_uart.h"
#pragma GCC optimize ("-O3")

void sw_uart_setup(due_sw_uart *uart, int tx) {
	
	uart->pin_tx     = tx;

  pinMode(tx, OUTPUT);
  digitalWrite(tx,HIGH);
  
}



int sw_uart_send_byte(due_sw_uart *uart) {
  digitalWrite(3,LOW);
  _sw_uart_wait_T(uart);

  char letter[9] = {'1','0','0','0','0','1','1','0'};

  for (int i = 0; letter[i] != '\0'; i++)
  {
    if (letter[i] == '1')
    {
      digitalWrite(uart->pin_tx,HIGH);
    }
    else
    {
      digitalWrite(uart->pin_tx,LOW);
    }
    
    _sw_uart_wait_T(uart);
  }

  digitalWrite(uart->pin_tx,HIGH);
  _sw_uart_wait_T(uart);

  digitalWrite(uart->pin_tx,HIGH);
  _sw_uart_wait_T(uart);

}


// MCK 21MHz
void _sw_uart_wait_half_T(due_sw_uart *uart) {
  for(int i = 0; i < 1093; i++)
    asm("NOP");
}

void _sw_uart_wait_T(due_sw_uart *uart) {
  _sw_uart_wait_half_T(uart);
  _sw_uart_wait_half_T(uart);
}
