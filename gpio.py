import RPi.GPIO as GPIO
import time
class gpio:
    def __init__(self, channel=21, up=True):
        self.channel =channel
        self.up = up

        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(channel, GPIO.OUT)
        GPIO.output(self.channel, GPIO.HIGH)

    def upin(self):

        try:
            print("LOW")        
            GPIO.output(self.channel, GPIO.LOW)# Turn off
            time.sleep(5)
            print("HIGH")   
            GPIO.output(self.channel, GPIO.HIGH)# Turn on
            #time.sleep(5)
            #GPIO.output(self.channel, GPIO.LOW)# Turn off
        except:
            print ("error")
        finally:
            print("ok")
            #GPIO.cleanup()
#if __name__=='__main__':
#    g = gpio(21, True)
#    g.upin()