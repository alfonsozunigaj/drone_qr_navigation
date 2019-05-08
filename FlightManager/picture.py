import cv2
from pyparrot.Bebop import Bebop
from pyparrot.DroneVisionGUI import DroneVisionGUI


IS_ALIVE = False


class UserVision:
    def __init__(self, vision):
        self.index = 0
        self.vision = vision

    def save_pictures(self):
        #print("saving picture")
        img = self.vision.get_latest_valid_picture()
        if img:
            filename = "test_image_%06d.png" % self.index
            cv2.imwrite(filename, img)
            self.index += 1


def demo_user_code_after_vision_opened(bebop_vision, args):
    bebop = args[0]

    print("Vision successfully started!")
    #removed the user call to this function (it now happens in open_video())
    #bebop_vision.start_video_buffering()

    # takeoff
    # bebop.safe_takeoff(5)

    # skipping actually flying for safety purposes indoors - if you want
    # different pictures, move the bebop around by hand
    print("Fly me around by hand!")
    bebop.smart_sleep(10)

    if bebop_vision.vision_running:
        #print("Moving the camera using velocity")
        #bebop.pan_tilt_camera_velocity(pan_velocity=0, tilt_velocity=-2, duration=4)
        #bebop.smart_sleep(5)

        # land
        #bebop.safe_land(5)

        print("Finishing demo and stopping vision")
        bebop_vision.close_video()

    # disconnect nicely so we don't need a reboot
    print("disconnecting")
    bebop.disconnect()

if __name__ == "__main__":
    BEBOP = Bebop(drone_type="Bebop")
    SUCCESS = BEBOP.connect(20)
    if SUCCESS:
        BEBOP_VISION = DroneVisionGUI(BEBOP,
                                      is_bebop=True,
                                      user_code_to_run=demo_user_code_after_vision_opened,
                                      user_args=(BEBOP, ))
        USER_VISION = UserVision(BEBOP_VISION)
        BEBOP_VISION.set_user_callback_function(USER_VISION.save_pictures, user_callback_args=None)
        BEBOP_VISION.open_video()

    else:
        print("Error connecting to bebop. Retry")
