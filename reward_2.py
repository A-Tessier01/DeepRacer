import math

#Props
consideration_window = 18
t_steering = 2/consideration_window
t_heading = 1/consideration_window
heading_deviation = 10
steering_deviation = 10
speed_deviation = .25
curvature_prediction_waypoints = (5,10)
max_speed = 4
min_speed = 1.5
speed_falloff = 8
relative_action_reward_weights = [.3333, .3333, .3333] # Heading, Steering, Speed


def reward(params):
    
    waypoints = params['waypoints']
    waypoints = waypoints[:-1]
    current_pos = (params['x'],params['y'])

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
        lst = [current_pos]
        lst.extend(waypoints)
        return lst
    
    def calc_targets(points):
        #bezier stuff - dynamic calc params
        start_pt = points[0]
        cp_1 = len(int(points/3))
        cp_2 = len(2*int(points/3))
        end_pt = points[-1]
        #end bezier stuff
        steering_target_pt = cubic_bezier(start_pt, cp_1, cp_2, end_pt, t_steering)
        heading_target_pt = cubic_bezier(start_pt, cp_1, cp_2, end_pt, t_heading)
        speed_target = calc_target_speed([start_pt, end_pt])
        steering_target = calculate_heading_cartesian(current_pos, steering_target_pt)
        heading_target = calculate_heading_cartesian(current_pos, heading_target_pt)
        return (heading_target, steering_target, speed_target)

    def calc_track_curvature(points):
        init_pt = points[0]
        end_pt = points[1]
        return calc_angle_delta(init_pt, end_pt)

    def calculate_heading_cartesian(p1, p2):
        # Calculate the differences
        delta_x = p2[0] - p1[0]
        delta_y = p2[1] - p1[1]
        # Calculate the angle in radians
        angle_radians = math.atan2(delta_y, delta_x)
        # Convert the angle from radians to degrees
        angle_degrees = math.degrees(angle_radians)
        return angle_degrees

    def calc_angle_delta(heading_1, heading_2):
        delta = heading_1 - heading_2
        if delta > 180:
            delta -= 360
        elif delta < -180:
            delta += 360
        return delta

    def calc_anlge_delta_2(heading_1, heading_2):
        def normalize(a):
            return a+360 if a < 0 else a
        abs_degree_diff = abs(normalize(heading_1)-normalize(heading_2))
        return min([abs_degree_diff, 360-abs_degree_diff])
    
    def calc_target_speed(points):
        crv = calc_track_curvature(points)
        target_speed = -(crv/speed_falloff)+max_speed
        return target_speed

    def calc_heading_reward(current_heading, target_heading, deviation):
        angle_diff = calc_angle_delta(current_heading, target_heading)
        return 1 if angle_diff < deviation else 1e-3
        
    def calc_steering_reward(current_heading, current_steering_angle, target_steering_angle, deviation):
        absolute_steering_angle = current_heading+current_steering_angle
        steering_diff = calc_angle_delta(absolute_steering_angle, target_steering_angle)
        return 1 if steering_diff < deviation else 1e-3

    def calc_speed_reward(current_speed, target_speed, speed_deviation):
        speed_diff = abs(current_speed - target_speed)
        return 1 if speed_diff < speed_deviation else 1e-3
    
    def get_reward_aggragate(targets):
        heading_reward = calc_heading_reward(params['heading'], targets[0], heading_deviation)
        steering_reward = calc_steering_reward(params['heading'], params['steering_angle'], targets[1], steering_deviation)
        speed_reward = calc_speed_reward(params['speed'], targets[2], speed_deviation)
        total_reward = 0
        for weight, reward in zip(relative_action_reward_weights, [heading_reward, steering_reward, speed_reward]):
            total_reward += reward*weight
        return total_reward

    all_rel_pts = get_car_and_window_points(get_next_n_waypoints(current_waypoint, consideration_window, waypoints))
    targets = calc_targets(all_rel_pts)
    reward = get_reward_aggragate(targets)
    return reward


def test1():
    params = {
        "x":10,
        "y":15,
        "heading":47.2,
        "waypoints":[(43.13, 12.21),(36.85, 20.61),(31.94, 42.07),(8.62, 16.71),(3.98, 46.45),(42.22, 35.33),(31.49, 20.87),(32.45, 14.88),(20.52, 47.52),(25.58, 41.12)],
        "closest_waypoints": [7,8],
        "track_width": 20,
        "distance_from_center": 3,
        "steering_angle": -15,
        "all_wheels_on_track": True,
        "speed": 3.21
    }


params = {
    "x":10,
    "y":15,
    "heading":47.2,
    "waypoints":[(43.13, 12.21),(36.85, 20.61),(31.94, 42.07),(8.62, 16.71),(3.98, 46.45),(42.22, 35.33),(31.49, 20.87),(32.45, 14.88),(20.52, 47.52),(25.58, 41.12)],
    "closest_waypoints": [7,8],
    "track_width": 20,
    "distance_from_center": 3,
    "steering_angle": -15,
    "all_wheels_on_track": True,
    "speed": 3.21
}
