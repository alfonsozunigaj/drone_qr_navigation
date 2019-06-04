from pyparrot.Minidrone import Mambo
from pyparrot.DroneVision import DroneVision
import cv2

import QRManager.qr_reader as qr_manager
import InputFileManager.file_parser as file_manager


def has_content(something):
    return something is not None


def translate_move(values_list):
    return {'roll': 0,
            'pitch': 0,
            'yaw': 0,
            'vertical_movement': 0,
            "duration": 0}


class UserVision:
    def __init__(self, vision, instructions, drone):
        self.index = 0
        self.vision = vision
        self.instructions = instructions
        self.drone = drone

    def save_pictures(self, args):

        img = self.vision.get_latest_valid_picture()

        if has_content(img):
            self.user_code_after_vision_opened(img)
            filename = "images/test_image_%06d.png" % self.index
            cv2.imwrite(filename, img)
            self.index += 1
            # print(self.index)

    def user_code_after_vision_opened(self, args):
        img = self.vision.get_latest_valid_picture()
        # self.save_pictures(img)

        if has_content(img):
            instruction = qr_manager.read_qr_code(img)
            print(instruction)
            self.translate_instruction(instruction)

    def translate_instruction(self, instruction):
        if not has_content(instruction):
            return
        """
        if instruction in self.instructions:
            values = self.instructions[instruction]
            m = translate_move(values)

            self.drone.fly_direct(roll=m['roll'],
                                  pitch=m['pitch'],
                                  yaw=m['yaw'],
                                  vertical_movement=m['vertical_movement'],
                                  duration=m['duration'])
                                  """
        if instruction == "A": # adelante
            self.drone.fly_direct(roll=0, pitch=30, yaw=0, vertical_movement=0,
                                  duration=2)
        elif instruction == "B": # girar
            self.drone.fly_direct(roll=50, pitch=0, yaw=0, vertical_movement=0,
                                  duration=1)
        elif instruction == "take_off":

            self.drone.safe_takeoff(1)
        elif instruction == "land":
            self.drone.safe_land(5)
            self.vision.close_video()
            self.drone.disconnect()


if __name__ == '__main__':

    mamboAddr = "d0:3a:4d:78:e6:36"

    mambo = Mambo(mamboAddr, use_wifi=True)
    print("trying to connect to mambo now")
    SUCCESS = mambo.connect(num_retries=20)
    print("connected: %s" % SUCCESS)
    mambo.smart_sleep(1)
    mambo.ask_for_state_update()
    mambo.smart_sleep(1)
    # bebop = Bebop(drone_type="Bebop")

    # SUCCESS = bebop.connect(5)
    INSTRUCTIONS = file_manager.get_navigation_instructions()
    print (INSTRUCTIONS)

    if SUCCESS:
        vision = DroneVision(mambo, is_bebop=False, buffer_size=30)
        userVision = UserVision(vision, INSTRUCTIONS, mambo)

        vision.set_user_callback_function(
            userVision.user_code_after_vision_opened,
            user_callback_args=None)
        success = vision.open_video()
        print("Success in opening vision is %s" % success)
        mambo.smart_sleep(3)

    else:
        print("Error connecting to bebop.  Retry")
