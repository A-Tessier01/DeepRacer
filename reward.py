

# import math
# def quadratic_bezier(P0, P1, P2, t):
#     x = (1-t)**2 * P0[0] + 2*(1-t)*t * P1[0] + t**2 * P2[0]
#     y = (1-t)**2 * P0[1] + 2*(1-t)*t * P1[1] + t**2 * P2[1]
#     return (x, y)
    
# def calculate_heading_cartesian(x1, y1, x2, y2):
#     # Calculate the differences
#     delta_x = x2 - x1
#     delta_y = y2 - y1
#     # Calculate the angle in radians
#     angle_radians = math.atan2(delta_y, delta_x)
#     # Convert the angle from radians to degrees
#     angle_degrees = math.degrees(angle_radians)
#     # Normalize the angle to 0-360 degrees
#     compass_heading = (angle_degrees + 360) % 360
#     return compass_heading


# # pos_target = quadratic_bezier(target_min, target_control, target_max, .5)
# # heading_target = calculate_heading_cartesian(params['x'], params['y'], pos_target[0], pos_target[1])

# pos = quadratic_bezier((3,5), (7,15), (14,3), .5)
# print(pos)
# tar = calculate_heading_cartesian(2,3,pos[0], pos[1])
# print(tar)

# heading_delta = math.abs(params['heading']-tar)
def reward_function(params):
    import math

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

    pos_target = quadratic_bezier(target_min, target_control, target_max, .5)
    heading_target = calculate_heading_cartesian(params['x'], params['y'], pos_target[0], pos_target[1])
   
   
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
   
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
   
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track
   
    return float(reward)


params = {
    "x":10,
    "y":15,
    "heading":47.2,
    "waypoints":[(43.13, 12.21),(36.85, 20.61),(31.94, 42.07),(8.62, 16.71),(3.98, 46.45),(42.22, 35.33),(31.49, 20.87),(32.45, 14.88),(20.52, 47.52),(25.58, 41.12)],
    "closest_waypoints": [7,8],
    "track_width": 20,
    "distance_from_center": 3
}

print(reward_function(params))