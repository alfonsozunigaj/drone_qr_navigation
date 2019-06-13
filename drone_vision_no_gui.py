from pyparrot.Minidrone import Mambo
from pyparrot.DroneVision import DroneVision
import cv2

import QRManager.qr_reader as qr_manager
import InputFileManager.file_parser as file_manager


def has_content(something):
    return something is not None


class UserVision:
    def __init__(self, vision, instructions, drone):
        self.index = 0
        self.vision = vision
        self.instructions = instructions
        self.drone = drone

    def save_pictures(self, img):
        if has_content(img):
            self.user_code_after_vision_opened(img)
            filename = "images/test_image_%06d.png" % self.index
            print("[SAVE] saving image: ", filename)
            cv2.imwrite(filename, img)
            self.index += 1

    def user_code_after_vision_opened(self, args):
        img = self.vision.get_latest_valid_picture()
        if has_content(img):
            instruction = qr_manager.read_qr_code(img)
            if instruction:
                self.save_pictures(img)
            self.perform_instruction(instruction)

    def perform_instruction(self, instruction):
        print("[PERFORM] instruction:", instruction)
        if not has_content(instruction):
            return
        if instruction == "take_off":
            self.drone.safe_takeoff(1)

        elif instruction == "land":
            self.perform_landing()

        elif instruction in self.instructions:
            self.follow_instructions(instruction)

    def follow_instructions(self, instruction):
        for movement in self.instructions[instruction]:
            self.drone.fly_direct(roll=movement['roll'],
                                  pitch=movement['pitch'],
                                  yaw=movement['yaw'],
                                  vertical_movement=movement['v_move'],
                                  duration=movement['duration'])

    def perform_landing(self):
        self.drone.safe_land(5)
        self.vision.close_video()
        self.drone.disconnect()


if __name__ == '__main__':

    INSTRUCTIONS = file_manager.get_navigation_instructions_from_json()
    print ("[INSTRUCTION] Dictionary created")
    MAMBO_ADDRESS = "d0:3a:4d:78:e6:36"

    mambo = Mambo(MAMBO_ADDRESS, use_wifi=True)
    mambo_connected = mambo.connect(num_retries=20)
    print("[MAMBO]connected: %s" % mambo_connected)
    mambo.smart_sleep(1)

    if mambo_connected:
        vision = DroneVision(mambo, is_bebop=False, buffer_size=30)
        userVision = UserVision(vision, INSTRUCTIONS, mambo)

        vision.set_user_callback_function(
            userVision.user_code_after_vision_opened,
            user_callback_args=None)
        success = vision.open_video()
        print("[VISION] Success in opening vision is %s" % success)
        mambo.smart_sleep(3)

    else:
        print("[VISION]Error connecting to bebop.  Retry")
