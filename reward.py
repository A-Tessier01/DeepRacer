import math
import numpy as np

#Bezier target heuristic based reward function
def reward_function(params):

    current_waypoint = params['closest_waypoints'][1]
   
    waypoints = params['waypoints']
   
    target_waypoint_min = (current_waypoint)%len(waypoints)
    target_waypoint_control = (current_waypoint+2)%len(waypoints)
    target_waypoint_max = (current_waypoint+4)%len(waypoints)
    
    target_min = waypoints[target_waypoint_min]
    target_control = waypoints[target_waypoint_control]
    target_max = waypoints[target_waypoint_max]
   

    import math
    def quadratic_bezier(P0, P1, P2, t):
        x = (1-t)**2 * P0[0] + 2*(1-t)*t * P1[0] + t**2 * P2[0]
        y = (1-t)**2 * P0[1] + 2*(1-t)*t * P1[1] + t**2 * P2[1]
        return (x, y)
        
    def calculate_heading_cartesian(x1, y1, x2, y2):
        # Calculate the differences
        delta_x = x2 - x1
        delta_y = y2 - y1
        # Calculate the angle in radians
        angle_radians = math.atan2(delta_y, delta_x)
        # Convert the angle from radians to degrees
        angle_degrees = math.degrees(angle_radians)
        return angle_degrees

    target_pos_heading = quadratic_bezier(target_min, target_control, target_max, .5)
    target_pos_steering = quadratic_bezier(target_min, target_control, target_max, .8)
    heading_target = calculate_heading_cartesian(params['x'], params['y'], target_pos_heading[0], target_pos_heading[1])
    steering_target = calculate_heading_cartesian(params['x'], params['y'], target_pos_steering[0], target_pos_steering[1])


    heading_error = abs(params['heading']-heading_target)
    steering_error = abs(params['heading']+params['steering_angle']-steering_target)

    heading_error_reward_weight = (360-heading_error)/360
    steering_error_reward_weight = (360-steering_error)/360

   
    if not params['all_wheels_on_track']:
        return 1e-3
    
    reward = 1 * heading_error_reward_weight * steering_error_reward_weight
   
    return float(reward)

#proportional weighting of distance to edge to track curvature for reward 
def reward_function_v2(params):
    import math

    current_waypoint = params['closest_waypoints'][1]
   
    waypoints = params['waypoints']

    waypoints_remaining = len(waypoints)-current_waypoint
   
    considered_waypoints = []
    if waypoints_remaining >= 5:
        if waypoints_remaining == 0:
            considered_waypoints = waypoints[0:5]
        else:
            considered_waypoints.extend(waypoints[current_waypoint+1:])
            considered_waypoints.extend(waypoints[0:5-len(considered_waypoints)])
    else:
        considered_waypoints = waypoints[current_waypoint+1:current_waypoint+6] if waypoints_remaining >= 5 else waypoints[0:5]

    def calculate_heading_cartesian(x1, y1, x2, y2):
        # Calculate the differences
        delta_x = x2 - x1
        delta_y = y2 - y1
        # Calculate the angle in radians
        angle_radians = math.atan2(delta_y, delta_x)
        # Convert the angle from radians to degrees
        angle_degrees = math.degrees(angle_radians)
        return angle_degrees
    
    apply_heading_calculation = lambda a : calculate_heading_cartesian(params['x'], params['y'], a[0], a[1])
    waypoint_headings = list(map(apply_heading_calculation, considered_waypoints))
    # -left +right
    signed_waypoint_variation = min(waypoint_headings)-max(waypoint_headings)







    # target_pos_heading = quadratic_bezier(target_min, target_control, target_max, .5)
    # target_pos_steering = quadratic_bezier(target_min, target_control, target_max, .8)
    # heading_target = calculate_heading_cartesian(params['x'], params['y'], target_pos_heading[0], target_pos_heading[1])
    # steering_target = calculate_heading_cartesian(params['x'], params['y'], target_pos_steering[0], target_pos_steering[1])


    # heading_error = abs(params['heading']-heading_target)
    # steering_error = abs(params['heading']+params['steering_angle']-steering_target)

    # heading_error_reward_weight = (360-heading_error)/360
    # steering_error_reward_weight = (360-steering_error)/360

   
    # if not params['all_wheels_on_track']:
    #     return 1e-3
    
    # reward = 1 * heading_error_reward_weight * steering_error_reward_weight
    reward = -1
   
    return float(reward)

params = {
    "x":10,
    "y":15,
    "heading":47.2,
    "waypoints":[(43.13, 12.21),(36.85, 20.61),(31.94, 42.07),(8.62, 16.71),(3.98, 46.45),(42.22, 35.33),(31.49, 20.87),(32.45, 14.88),(20.52, 47.52),(25.58, 41.12)],
    "closest_waypoints": [7,8],
    "track_width": 20,
    "distance_from_center": 3,
    "steering_angle": -15,
    "all_wheels_on_track": True
}

# print(reward_function_v2(params))

def read_npy_file(path):
    try:
        data = np.