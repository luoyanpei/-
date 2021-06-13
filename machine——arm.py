import sensor, image, time, math
import lcd
from pyb import UART

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(30)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()
uart_B = UART(3, 115200)
lcd.init()

while(True):
    clock.tick()
    img = sensor.snapshot()
    apriltag_1= img.find_apriltags()
    if apriltag_1 is not None:
        for tag in apriltag_1:
            img.draw_rectangle(tag.rect(),color=(255,0,0))
            img.draw_cross(tag.cx(),tag.cy(),color=(0,255,0))
            print_args=(tag.id(),tag.cx(),tag.cy())
            if(len(apriltag_1)==2):
                c0_x=apriltag_1[0].cx()
                c0_y=apriltag_1[0].cy()
                c1_x=apriltag_1[1].cx()
                c1_y=apriltag_1[1].cy()
                if c1_x in range(c0_x-10,c0_x+10):
                    print("continue")
                    continue
                if (c1_x> c0_x+10):
                    #angle=int(math.atan((c2_y-c0_y)/(c0_x-c2_x)))
                    uart_B.write('l')
                    time.sleep_ms(100)
                    print("l")
                    #print(angle)
                if (c1_x < c0_x-10):
                    uart_B.write('r')
                    time.sleep_ms(100)
                    print("r")
    lcd.display(img)