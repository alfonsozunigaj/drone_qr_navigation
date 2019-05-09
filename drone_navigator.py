from pyparrot.Bebop import Bebop
from pyparrot.DroneVisionGUI import DroneVisionGUI
import QRManager.qr_reader as qr_manager


def demo_user_code_after_vision_opened(bebop_vision, args):
    bebop = args[0]
    bebop.smart_sleep(1)
    while bebop_vision.vision_running:
        img = bebop_vision.get_latest_valid_picture()
        if img is not None:
            instruction = qr_manager.read_qr_code(img)
            if instruction is not None:
                if instruction == "take_off":
                    bebop.safe_takeoff(5)
                    bebop.smart_sleep(5)
                elif instruction == "landing":
                    bebop.safe_land(5)
                    bebop_vision.close_video()
    bebop.disconnect()

if __name__ == "__main__":
    BEBOP = Bebop(drone_type="Bebop")
    SUCCESS = BEBOP.connect(20)
    if SUCCESS:
        BEBOP_VISION = DroneVisionGUI(BEBOP,
                                      is_bebop=True,
                                      user_code_to_run=demo_user_code_after_vision_opened,
                                      user_args=(BEBOP, ))
        BEBOP_VISION.open_video()

    else:
        print("Error connecting to bebop. Retry")
