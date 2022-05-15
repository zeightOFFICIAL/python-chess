# defaults
# rate of screen update [it is not recommended to change]
fps_max = 24
# window width and height [free change]
width = 750
# game mode (0 - PvP, 1 - PvE) [free change]
game_mode = 0
# if game mode is 1, then difficulty determines algorithms complexity
difficulty = 0
# padding size, distance between board and the window border [it is not recommended to change]
padding_absolute = 130
# visual set (experimental, released in build 800) [free change]
visual_set = 0
# timer for each person (in minutes) [free change]
time_restriction = 30
# size increment [it is not recommended to change]
pop_increasing_size = 55
# time before game starts [it is not recommended to change]
freeze_time = 0

# reading from file

try:
    f = open("config.txt")
    lines = f.readlines()
    for line in lines:
        name = str(line.split("=")[0])
        var = int(line.split("=")[1])
        locals()[name] = var
except:
    print("log: config file is corrupted, does not exist or is unreadable")
    pass

# static and calculated values
height = width
padding_abs_half = padding_absolute // 2
top_left_corner = (padding_abs_half, padding_abs_half)
bottom_right_corner = (width - padding_absolute, width - padding_absolute)
top_right_corner = (width - padding_absolute, padding_abs_half)
bottom_left_corner = (padding_abs_half, width - padding_absolute)
cell_size_x = (width - padding_absolute) / 8
cell_size_y = (height - padding_absolute) / 8
time_restriction_seconds = 60 * time_restriction
