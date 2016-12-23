#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Asus
#
# Created:     14/10/2016
# Copyright:   (c) Asus 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import serial
from ConfigParser import ConfigParser
import msvcrt

class lp_com(object):

    def __init__(self):
        try:
            self.read_config_file()
            self.setup_serial_port()


        except Exception as e:
            print "Exception in UART_com.init(): " + repr(e)
            raise e

    def read_config_file(self):
        """read parameters from the config file"""
        try:
            print "reading config file..."

            self.config_file_name = "settings.cfg"
            self.c_file = open(self.config_file_name, 'r')
            self.config_file = ConfigParser()
            self.config_file.readfp(self.c_file)

            self.port_num = int(self.config_file.get('COM Port','port number'))
            self.response_timeout_sec = int(self.config_file.get('Execution','response timeout seconds'))

            print "done reading config file"

        except Exception as e:
            print "Exception in read_config_file(): " + repr(e)
            raise e

    def setup_serial_port(self):
        """setup serial port that the MSP430 is connected to"""
        try:
            print "setting up serial port..."

            self.MSP430 = serial.Serial(self.port_num-1)
            self.MSP430.timeout = self.response_timeout_sec

            print "serial port opened: ",self.MSP430

        except Exception as e:
            print "Exception in UART_com.setup_serial_port(): " + repr(e)
            raise e

    def send_and_read(self,c):
        """send a character and read data"""
        try:

            self.MSP430.write(c)
            for line in self.MSP430.readlines():
                print line,

        except Exception as e:
            print "Exception in send_and_read(): " + repr(e)
            raise e
def main():

    try:
        launchpad = lp_com()
        launchpad.send_and_read("?")

        print "\nEnter character to send(q to quit): ",
        s = msvcrt.getch()
        print "%s\twaiting for response..."%(s),
        while(s != 'q'):

            launchpad.send_and_read(s)
            print "\nEnter character to send(q to quit): ",
            s=msvcrt.getch()
            print "%s\twaiting for response..."%(s),


    except Exception as e:
        print "Exception in main(): " + repr(e)
        raise e


if __name__ == '__main__':
    main()
