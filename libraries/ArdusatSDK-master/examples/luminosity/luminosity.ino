/*
 * =====================================================================================
 *
 *       Filename:  indoor_luminosity.ino
 *
 *    Description:  Outputs the luminosity sensor readings in a JSON format that
 *                  can be read by the Ardusat Experiment Platform
 *                  (http://experiments.ardusat.com).
 *
 *                  This example uses many third-party libraries available from
 *                  Adafruit (https://github.com/adafruit). These libraries are
 *                  mostly under an Apache License, Version 2.0.
 *
 *                  http://www.apache.org/licenses/LICENSE-2.0
 *
 *        Version:  1.0
 *        Created:  10/29/2014
 *       Revision:  none
 *       Compiler:  Arduino
 *
 *         Author:  Ben Peters (ben@ardusat.com)
 *   Organization:  Ardusat
 *         Edited:  8/25/2015
 *      Edited By:  Sam Olds (sam@ardusat.com)
 *
 * =====================================================================================
 */

/*-----------------------------------------------------------------------------
 *  Includes
 *-----------------------------------------------------------------------------*/
#include <Arduino.h>
#include <Wire.h>
#include <ArdusatSDK.h>

/*-----------------------------------------------------------------------------
 *  Setup Software Serial to allow for both RF communication and USB communication
 *    RX is digital pin 8 (connect to TX/DOUT of RF Device)
 *    TX is digital pin 9 (connect to RX/DIN of RF Device)
 *-----------------------------------------------------------------------------*/
ArdusatSerial serialConnection(SERIAL_MODE_HARDWARE_AND_SOFTWARE, 8, 9);

/*-----------------------------------------------------------------------------
 *  Constant Definitions
 *-----------------------------------------------------------------------------*/
/* Default Sensor Configurations - To use different configuration, place a
                                   "//" at the beginning of the next line and
                                   remove the "//" at the beginning of the
                                   configuration you want to use */
Luminosity lum; // => TCS34725_INTEGRATIONTIME_24MS, TCS34725_GAIN_16X

/* Useful outside or in very bright room */
//Luminosity lum(TCS34725_INTEGRATIONTIME_24MS, TCS34725_GAIN_1X);

/* Useful at night or in dark room */
//Luminosity lum(TCS34725_INTEGRATIONTIME_154MS, TSL2561_GAIN_60X);


/*
 * ===  FUNCTION  ======================================================================
 *         Name:  setup
 *  Description:  This function runs when the Arduino first turns on/resets. This is
 *                our chance to take care of all one-time configuration tasks to get
 *                the program ready to begin logging data.
 * =====================================================================================
 */
void setup(void)
{
  serialConnection.begin(9600);

  lum.begin();

  /* We're ready to go! */
  serialConnection.println("");
}

/*
 * ===  FUNCTION  ======================================================================
 *         Name:  loop
 *  Description:  After setup runs, this loop function runs until the Arduino loses
 *                power or resets. We go through and update each of the attached
 *                sensors, write out the updated values in JSON format, then delay
 *                before repeating the loop again.
 * =====================================================================================
 */
void loop(void)
{
  serialConnection.println(lum.readToJSON("lum"));

  delay(1000);
}
