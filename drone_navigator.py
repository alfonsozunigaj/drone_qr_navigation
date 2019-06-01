from pyparrot.Bebop import Bebop
from pyparrot.DroneVisionGUI import DroneVisionGUI
import QRManager.qr_reader as qr_manager
import InputFileManager.file_parser as file_manager


def demo_user_code_after_vision_opened(bebop_vision, args):
    bebop = args[0]
    instructions = args[1]
    bebop.smart_sleep(1)
    while bebop_vision.vision_running:
        img = bebop_vision.get_latest_valid_picture()
        if img is not None:
            instruction = qr_manager.read_qr_code(img)
            if instruction is not None:
                if instruction == "take_off":
                    bebop.safe_takeoff(5)
                elif instruction == "land":
                    bebop.safe_land(5)
                    bebop_vision.close_video()
                elif instruction in instructions:
                    values = instructions[instruction]
                    bebop.move_relative(values[0], values[1], values[2], values[3])
    bebop.disconnect()


if __name__ == "__main__":
    BEBOP = Bebop(drone_type="Bebop")
    SUCCESS = BEBOP.connect(20)
    INSTRUCTIONS = file_manager.get_navigation_instructions()
    if SUCCESS:
        BEBOP_VISION = DroneVisionGUI(BEBOP,
                                      is_bebop=True,
                                      user_code_to_run=demo_user_code_after_vision_opened,
                                      user_args=(BEBOP, INSTRUCTIONS))
        BEBOP_VISION.open_video()
    else:
        print("Error connecting to bebop. Retry")
