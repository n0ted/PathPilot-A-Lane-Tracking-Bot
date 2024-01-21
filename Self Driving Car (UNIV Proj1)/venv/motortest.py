import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class motor_control:
    def __init__(self, enable_a, in1_a, in2_a, enable_b, in1_b, in2_b):
        self.enable_a = enable_a
        self.in1_a = in1_a
        self.in2_a = in2_a
        self.enable_b = enable_b
        self.in1_b = in1_b
        self.in2_b = in2_b

        GPIO.setup(self.enable_a, GPIO.OUT)
        GPIO.setup(self.in1_a, GPIO.OUT)
        GPIO.setup(self.in2_a, GPIO.OUT)
        GPIO.setup(self.enable_b, GPIO.OUT)
        GPIO.setup(self.in1_b, GPIO.OUT)
        GPIO.setup(self.in2_b, GPIO.OUT)

        self.pwm_a = GPIO.PWM(self.enable_a, 100)
        self.pwm_b = GPIO.PWM(self.enable_b, 100)
        self.pwm_a.start(0)
        self.pwm_b.start(0)
        self.current_speed = 0

    def move(self, speed=0.5, turn=0, duration=0):
        speed *= 100
        turn *= 70
        left_speed = speed - turn
        right_speed = speed + turn

        left_speed = min(100, max(-100, left_speed))
        right_speed = min(100, max(-100, right_speed))

        self.pwm_a.ChangeDutyCycle(abs(left_speed))
        self.pwm_b.ChangeDutyCycle(abs(right_speed))

        GPIO.output(self.in1_a, GPIO.HIGH if left_speed > 0 else GPIO.LOW)
        GPIO.output(self.in2_a, GPIO.LOW if left_speed > 0 else GPIO.HIGH)
        GPIO.output(self.in1_b, GPIO.HIGH if right_speed > 0 else GPIO.LOW)
        GPIO.output(self.in2_b, GPIO.LOW if right_speed > 0 else GPIO.HIGH)

        sleep(duration)

    def stop(self, duration=0):
        self.pwm_a.ChangeDutyCycle(0)
        self.pwm_b.ChangeDutyCycle(0)
        self.current_speed = 0
        sleep(duration)

def main():
    motor_control.move(0.5, 0, 2)
    motor_control.stop(2)
    motor_control.move(-0.5, 0, 2)
    motor_control.stop(2)
    motor_control.move(0, 0.5, 2)
    motor_control.stop(2)
    motor_control.move(0, -0.5, 2)
    motor_control.stop(2)

if __name__ == '__main__':
    motor_control = MotorControl(2, 3, 4, 17, 22, 27)
    main()
