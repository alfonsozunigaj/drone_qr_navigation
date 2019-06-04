from pyparrot.Minidrone import Mambo

# you will need to change this to the address of YOUR mambo
mamboAddr = "d0:3a:4d:78:e6:36"

# make my mambo object
mambo = Mambo(mamboAddr, use_wifi=True)

print ("trying to connect")
success = mambo.connect(num_retries=20)
print ("connected: %s" % success)

# get the state information
print ("sleeping")
mambo.smart_sleep(2)
mambo.ask_for_state_update()
mambo.smart_sleep(2)

print ("taking off!")
mambo.safe_takeoff(5)
mambo.smart_sleep(2)
print ("Flying direct: going forward (positive pitch), pitch=30, duration=2")
mambo.fly_direct(roll=0, pitch=30, yaw=0, vertical_movement=0, duration=2)
mambo.smart_sleep(2)

print ("Flying direct: going forward (positive pitch), pitch=30, duration=2")
mambo.fly_direct(roll=0, pitch=-30, yaw=0, vertical_movement=0, duration=2)
mambo.smart_sleep(2)

print ("landing")
mambo.safe_land(2)
mambo.smart_sleep(5)

print ("disconnect")
mambo.disconnect()
