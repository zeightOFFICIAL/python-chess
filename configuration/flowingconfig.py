# ver 904
# flowingconfig.py
# python libraries =====================================================================================================
from screeninfo import get_monitors

# defaults -------------------------------------------------------------------------------------------------------------
# rate of screen update [should not be changed]
# 60 - default
fps_max = 60
# window width and height [changeable]
# 600 - default
# if auto-detection works - its height=width is equal to display height
try:
    for display in get_monitors():
        if display.is_primary:
            width = display.height
            print("log (flowingconfig.py:width): Detected screen height:", width)
            width -= 90
except:
    print("log (flowingconfig.py:width): Screen's height auto-detection failed. Applying default.")
    width = 600
# game mode [changeable]
# 0 - PvP
# 1 - PvE
game_mode = 0
# if game mode is 1, then difficulty determines algorithms complexity [changeable]
# 0 - random
# 1 - evaluation
# 2 - minimax (released in build 800)
# 3 - advanced minimax (released in build 800)
difficulty = 0
# padding size, distance between board and the window border [should not be changed]
padding_absolute = 130
# visual set (released in build 800) [changeable]
visual_set = 0
# timer for each person (in minutes) [changeable]
time_restriction = 15
# time before game starts [not recommended to change]
freeze_time = 3

# reading from file ----------------------------------------------------------------------------------------------------
try:
    f = open("config.txt")
    lines = f.readlines()
    for line in lines:
        name = str(line.split("=")[0])
        var = int(line.split("=")[1])
        locals()[name] = var
        print("log (flowingconfig.py:reading): Parametr:", name, "~ Value:", var)
except (FileExistsError, AttributeError, ValueError) as e:
    print("log (flowingconfig.py:reading): Config file is corrupted, does not exist or is unreadable, possibly parsing error.\nNot parsed values are set to default.")

# static and calculated values -----------------------------------------------------------------------------------------
time_restriction = 15 if time_restriction > 60 * 1000 else time_restriction
height = width
padding_abs_half = padding_absolute // 2
top_left_corner = (padding_abs_half, padding_abs_half)
bottom_right_corner = (width - padding_absolute, width - padding_absolute)
top_right_corner = (width - padding_absolute, padding_abs_half)
bottom_left_corner = (padding_abs_half, width - padding_absolute)
cell_size_x = (width - padding_absolute) / 8
cell_size_y = (height - padding_absolute) / 8
time_restriction_seconds = 60 * time_restriction
pop_increasing_size = 0.086 * width
