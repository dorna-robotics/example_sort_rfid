### RF_ID location ###
rf_id_bins = [[[280, 30, 105, -90, -175], 88], [[280, -30, 105, -90, -185], 10]]

### RF_ID, green and red bins location ###
rf_id_reader = [400, 0, 105, -90, -180]
green_bin = [280, 125, 132, -90, -155]
red_bin = [280, -125, 132, -90, -205]


### z min and max ###
bin_z_max = 110
bin_z_min = 80

### home position ###
home = [255, 0, 150, -90, -180]

### vacuum suction IO index ###
output_index = 0

### kinematics ###
toollength = 0

# camera to lens distance = 70 mm 
pass_hsv = {
	"low": (48, 104, 27),
	"high": (74, 255, 141)
}


fail_hsv = {
	"low": (48, 104, 27),
	"high": (74, 255, 141)
}

wait_time = 5
positive_count=10
negative_frame = 10

# camera index
camera_index = 0

window_name = "test"

# pass and fail rectangular 
rect_ratio = 0.55 # width / height ratio
error_thr = 0.15 # maximum divergent from the ratio

# robot IP address
robot_ip = "localhost"

# rf_id thickness
rf_id_thickness = 0.3


### motion parameter ###
# corner radius
corner_radius = 50

# midpoint height
midpoint_height = 80

# jmove: vel, accel, jerk
jmove_fast=[100, 300, 2000]
