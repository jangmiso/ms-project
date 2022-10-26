import time

def check_fps(prev_time):
    current = time.time()
    one_loop = current - prev_time
    prev_time = current
    fps = 1/one_loop
    return prev_time, fps
