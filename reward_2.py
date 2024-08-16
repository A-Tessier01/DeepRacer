import math

#Props
consideration_window = 18
t_steering = 2/consideration_window
t_heading = 1/consideration_window
heading_deviation = 10


def reward(params):
    
    waypoints = params['waypoints']
    waypoints = waypoints[:-1]

    current_waypoint = params['closest_waypoints'][1]

    def cubic_bezier(P0, P1, P2, P3, t):
        x = (1-t)**3 * P0[0] + 3*(1-t)**2 * t * P1[0] + 3*(1-t) * t**2 * P2[0] + t**3 * P3[0]
        y = (1-t)**3 * P0[1] + 3*(1-t)**2 * t * P1[1] + 3*(1-t) * t**2 * P2[1] + t**3 * P3[1]
        return (x, y)
    
    def get_next_n_waypoints(s, n, waypoints):
        lst = []
        for waypoint in range(s, s+n):
            lst.append(waypoints[waypoint % len(waypoints)])
        return

    def get_car_and_window_points(waypoints):
        lst = [(params['x'],params['y'])]
        lst.extend(waypoints)
        return lst
    
    def calc_target_points(points):
        #bezier stuff - dynamic calc params
        start_pt = points[0]
        cp_1 = len(int(points/3))
        cp_2 = len(2*int(points/3))
        end_pt = points[-1]
        #end bezier stuff
        steering_target = cubic_bezier(start_pt, cp_1, cp_2, end_pt, t_steering)
        heading_target = cubic_bezier(start_pt, cp_1, cp_2, end_pt, t_heading)

    def calc_track_curvature()

    def calculate_heading_cartesian(p1, p2):
        # Calculate the differences
        delta_x = p2[0] - p1[0]
        delta_y = p2[1] - p1[1]
        # Calculate the angle in radians
        angle_radians = math.atan2(delta_y, delta_x)
        # Convert the angle from radians to degrees
        angle_degrees = math.degrees(angle_radians)
        return angle_degrees

    def normalize_to_360(theta):
        return theta+360 if theta < 0 else theta

    def calc_heading_reward(current_heading, target_heading, deviation):
        
        delta_theta = abs(normalize_to_360(current_heading)-normalize_to_360(target_heading))
        return 1 if delta_theta < deviation else 1e-3
        
    def calc_steering_reward(current_heading, current_steering_angle, target_steering_angle, deviation):
        current_steering_heading
        delta_theta = abs()



    
    all_rel_pts = get_car_and_window_points(get_next_n_waypoints(current_waypoint, consideration_window, waypoints))
    calc_target_points(all_rel_pts)

    

    


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
