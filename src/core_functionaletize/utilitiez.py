"""
A collection of usuful Functions
"""
import math

def on_object(object_x, object_y, object_width, object_height, object_to_check_x, object_to_check_y, object_to_check_width, object_to_check_height) -> bool:
    """
    Returns True if object is on object to check else return False
    """
    if (object_to_check_y <= object_y <= object_to_check_y + object_to_check_height or (object_y <= object_to_check_y <= object_y + object_height)) \
            and ((object_to_check_x <= object_x <= object_to_check_x + object_to_check_width) or (object_x <= object_to_check_x <= object_x + object_width)):
        return True
    return False


def get_angle(x,y,target_x,target_y) -> float:
    """
    Returns the angle between the current point to target
    """
    red = math.atan2(-target_y + y,target_x - x) # Angle in radians
    return math.degrees(red)


def calculat_new_xy(speed,angle_in_degrees):
    """
    Returns the velocity of a moving object with an angle
    """
    velocity_x = math.cos(math.radians(angle_in_degrees)) * speed
    velocity_y = math.sin(math.radians(-angle_in_degrees)) * speed
    return velocity_x, velocity_y


