from pyparrot.Minidrone import Mambo
from pyparrot.DroneVision import DroneVision
import QRManager.qr_reader as qr_manager
import InputFileManager.file_parser as file_manager


def has_content(something):
    return something is not None


class UserVision:
    def __init__(self, vision, drone):
        self.vision = vision
        self.drone = drone

    def user_code_after_vision_opened(self, args):
        img = self.vision.get_latest_valid_picture()
        if has_content(img):
            instruction = qr_manager.read_qr_code(img)
            if instruction:
                print(instruction)
                self.drone.ask_for_state_update()
                if instruction == "take_off":
                    while self.drone.sensors.flying_state == "landed":
                        self.drone.safe_takeoff(1)
                        self.drone.ask_for_state_update()
                    self.drone.smart_sleep(1)
                elif instruction == "land":
                    while self.drone.sensors.flying_state != "landed":
                        self.drone.safe_land(5)
                        self.drone.ask_for_state_update()
                    self.vision.close_video()
                    self.drone.disconnect()
                elif instruction == "A":
                    print("Time to turn!")
                    self.drone.turn_degrees(90)
                    self.drone.smart_sleep(1)
                    self.drone.turn_degrees(-90)
                    self.drone.smart_sleep(1)
                    self.drone.fly_direct(0, 20, 0, 0, 1)
                    self.drone.smart_sleep(3)
                    self.drone.turn_degrees(180)
                    self.drone.smart_sleep(3)
                    self.drone.fly_direct(0, 40, 0, 0, 1)
                    self.drone.smart_sleep(3)
                    self.drone.turn_degrees(-180)
                    self.drone.smart_sleep(1)
        


if __name__ == '__main__':
    MAMBO_ADDRESS = "d0:3a:4d:78:e6:36"
    mambo = Mambo(MAMBO_ADDRESS, use_wifi=True)
    mambo_connected = mambo.connect(num_retries=2)
    mambo.smart_sleep(1)
    if mambo_connected:
        vision = DroneVision(mambo, is_bebop=False, buffer_size=30)
        userVision = UserVision(vision, mambo)
        vision.set_user_callback_function(
            userVision.user_code_after_vision_opened,
            user_callback_args=None)
        success = vision.open_video()
    else:
        print("[VISION]Error connecting to bebop.  Retry")
