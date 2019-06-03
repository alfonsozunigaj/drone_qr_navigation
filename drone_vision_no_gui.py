from pyparrot.Bebop import Bebop
from pyparrot.DroneVision import DroneVision

import QRManager.qr_reader as qr_manager
import InputFileManager.file_parser as file_manager


def has_content(something):
    return something is not None


class UserVision:
    def __init__(self, vision, instructions, bebop):
        self.index = 0
        self.vision = vision
        self.instructions = instructions
        self.bebop = bebop

    def user_code_after_vision_opened(self):
        img = self.vision.get_latest_valid_picture()
        if has_content(img):
            instruction = qr_manager.read_qr_code(img)
            self.translate_instruction(instruction)

    def translate_instruction(self, instruction):
        if has_content(instruction):
            return
        # print(instruction)
        if instruction in self.instructions:
            values = self.instructions[instruction]
            bebop.move_relative(values[0], values[1], values[2], values[3])
        elif instruction == "take_off":
            bebop.safe_takeoff(1)
        elif instruction == "land":
            bebop.safe_land(5)
            self.vision.close_video()
            bebop.disconnect()


if __name__ == '__main__':

    bebop = Bebop(drone_type="Bebop")

    SUCCESS = bebop.connect(5)
    INSTRUCTIONS = file_manager.get_navigation_instructions()
    print (INSTRUCTIONS)

    if SUCCESS:
        bebopVision = DroneVision(bebop, is_bebop=True)
        userVision = UserVision(bebopVision, INSTRUCTIONS, bebop)
        bebopVision.set_user_callback_function(
            userVision.user_code_after_vision_opened,
            user_callback_args=None)
        bebopVision.open_video()
    else:
        print("Error connecting to bebop.  Retry")
