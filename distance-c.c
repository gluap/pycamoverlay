// code based on
// http://stackoverflow.com/questions/22580242/raspberrypi-g-ultrasonic-sensor-not-working
#include<iostream>
#include<wiringPi.h>
#include<errno.h>
#include<string.h>
#include<stdio.h>
#include<stdint.h>       //for uint32_t
using namespace std;
uint32_t time1=0,time2=0;
uint32_t time_diff=0;
float Range_cm=0;
volatile int flag=0;
void show_distance(void);

void myInterrupt(void)
 {
 	uint32_t timeTemp=micros();
    if(flag==0)
      {
            time1=timeTemp;
            flag=1;

      }
    else
      {
            time2=timeTemp;
            flag=0;
            time_diff=time2-time1;
            Range_cm=time_diff/58.;
       }
  }
void show_distance()
  {
	fwrite(&Range_cm,sizeof(float),1,stdout);
    cout.flush();
  }

int main(void)
  {
    if(wiringPiSetup()<0)
     {
       cout<<"wiringPiSetup failed !!\n";
     }
    pinMode(4,OUTPUT);
    pinMode(5,INPUT);
    pullUpDnControl(5,PUD_DOWN);
    if(wiringPiISR(5,INT_EDGE_BOTH,&myInterrupt) < 0)
            {
            cerr<<"interrupt error ["<<strerror (errno)<< "]:"<<errno<<endl;
            return 1;
            }

    while(1)
    {
    	time1=0;
    	time2=0;
    	flag=0;
	    digitalWrite(4,0);
	    delayMicroseconds(1);
	    digitalWrite(4,1);
	    delayMicroseconds(10);
	    digitalWrite(4,0);
		delayMicroseconds(25000);
		show_distance();
    }
    return 0;
 }
