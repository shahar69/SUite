import RPi.GPIO as GPIO
import smbus
import time


def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  # X-axis servo (left-right)
GPIO.setup(17, GPIO.OUT)  # Y-axis servo (up-down)

pwm_x = GPIO.PWM(18, 50)
pwm_y = GPIO.PWM(17, 50)

bus = smbus.SMBus(1)
address = 0x48


def read_adc(channel):
    for _ in range(5):
        try:
            bus.write_byte_data(address, 0x40 | ((channel & 0x03) << 4), 0x00)
            bus.read_byte(address)
            value = bus.read_byte(address)
            return value
        except OSError:
            time.sleep(0.1)
    print("Failed to read ADC after 5 retries. Trying again...")
    return None


def set_servo_angle(servo, angle):
    duty_cycle = 2.5 + (angle / 18)
    servo.ChangeDutyCycle(duty_cycle)


pwm_x.start(0)
pwm_y.start(0)

try:
    while True:
        x = read_adc(0)  # X-axis value from joystick
        y = read_adc(1)  # Y-axis value from joystick

        if x is not None and y is not None:
            angle_x = map_value(x, 0, 255, 0, 180)
            angle_y = map_value(y, 0, 255, 0, 180)

            set_servo_angle(pwm_x, angle_x)  # Control X-axis servo
            set_servo_angle(pwm_y, angle_y)  # Control Y-axis servo

        time.sleep(0.2)

except KeyboardInterrupt:
    print('Program terminated.')

pwm_x.stop()
pwm_y.stop()
GPIO.cleanup()
