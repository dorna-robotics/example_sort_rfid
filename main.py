from dorna2 import Dorna
import config as CONFIG
import vision
import time

def main(robot, camera):
    good = 0
    bad = 0
    
    # connecting
    robot.log("connecting to the robot")
    if not robot.connect(CONFIG.robot_ip):
        robot.log("connection failed")
        return 0

    # init robot
    robot.set_toollength(CONFIG.toollength)
    robot.set_motor(1)
    robot.set_output(CONFIG.output_index, 0)

    # go to the home position
    robot.log("go home")
    robot.jmove(rel=0, vel=CONFIG.jmove_fast[0], accel=CONFIG.jmove_fast[1], jerk=CONFIG.jmove_fast[2], z=robot.get_pose(2)+CONFIG.midpoint_height)
    robot.jmove(rel=0, x=CONFIG.home[0], y=CONFIG.home[1], z=CONFIG.home[2], a=CONFIG.home[3], b=CONFIG.home[4])
    
    # loop over rf_id_bins
    for rf_id_bin in CONFIG.rf_id_bins:
        # loop over rf_ids in one bin
        for rf_id_index in range(rf_id_bin[1]):

            ### go above bin ###
            # go above rf_id_bin
            robot.jmove(rel=0, z=robot.get_pose(2)+CONFIG.midpoint_height, cont=1, corner=CONFIG.corner_radius, timeout=0)
            robot.jmove(rel=0, x=rf_id_bin[0][0], y=rf_id_bin[0][1], z=CONFIG.bin_z_max+CONFIG.midpoint_height, a=rf_id_bin[0][3], b=rf_id_bin[0][4], timeout=0)
            robot.jmove(rel=0, z=CONFIG.bin_z_max, cont=0)

            ### pick ###
            # go down for pick, vac on and sleep
            robot.jmove(rel=0, z=CONFIG.bin_z_min + (rf_id_bin[1] - rf_id_index)*CONFIG.rf_id_thickness)
            robot.set_output(CONFIG.output_index, 1)
            robot.sleep(0.5)
            
            ### reader ###
            # go to the reader
            robot.jmove(rel=0, z=CONFIG.bin_z_max+CONFIG.midpoint_height, cont=1, corner=CONFIG.corner_radius, timeout=0)
            robot.jmove(rel=0, x=CONFIG.rf_id_reader[0], y=CONFIG.rf_id_reader[1], z=CONFIG.rf_id_reader[2]+CONFIG.midpoint_height, a=CONFIG.rf_id_reader[3], b=CONFIG.rf_id_reader[4], cont=0, timeout=0)
            robot.jmove(rel=0, z=CONFIG.rf_id_reader[2], cont=0)

            ### wait for camera signal ###
            # wait for the signal
            start = time.time()
            positive_count = 0
            negative_frame = 0 # counter for negative frame
            while all([time.time()-start < CONFIG.wait_time, positive_count < CONFIG.positive_count]):
                # get a frame 
                ret, frame = camera.frame()
                
                # check the camera status
                if not ret:
                    negative_frame += 1
                    if negative_frame > CONFIG.negative_frame:
                        robot.log("camera is not working")
                        return 0
                    continue
                
                # check the frame
                if frame is None:
                    robot.log("camera is not working")
                    return 0

                # detect pass
                thr, result = vision.color_detector(frame, CONFIG.pass_hsv["low"], CONFIG.pass_hsv["high"])
                positive_count += result

                # sleep
                time.sleep(0.01)
            
            # good or bad
            if positive_count >= CONFIG.positive_count:
                drop_bin = CONFIG.green_bin
                good += 1
            else:
                drop_bin = CONFIG.red_bin
                bad += 1
            
            # drop
            robot.jmove(rel=0, z=robot.get_pose(2)+CONFIG.midpoint_height, cont=1, corner=CONFIG.corner_radius, timeout=0)
            robot.jmove(rel=0, x=drop_bin[0], y=drop_bin[1], z=drop_bin[2]+CONFIG.midpoint_height, a=drop_bin[3], b=drop_bin[4], cont=0, timeout=0)
            robot.jmove(rel=0, z=drop_bin[2], cont=0)

            # vac off and sleep 
            robot.set_output(CONFIG.output_index, 0)
            robot.sleep(0.5)
            
            robot.log('#### total picked: %d/%d,    good: %d    bad: %d ####' % (good+bad, sum([x[1] for x in CONFIG.rf_id_bins]), good, bad))
    # go to the home position
    robot.jmove(rel=0, z=robot.get_pose(2)+CONFIG.midpoint_height)
    robot.jmove(x=CONFIG.home[0], y=CONFIG.home[1], z=CONFIG.home[2], a=CONFIG.home[3], b=CONFIG.home[4])

if __name__ == '__main__':
    # create the Dorna object
    robot = Dorna()
    robot.log("create Dorna object")
    
    # create camera object
    camera = vision.camera_2d(CONFIG.camera_index)
    robot.log("create camera object")
    
    # main loop
    main(robot, camera)
    
    # close the camera
    robot.log("closing the camera")
    camera.release()
    
    robot.log("closing the connection")
    robot.set_output(CONFIG.output_index, 0)
    robot.close()
