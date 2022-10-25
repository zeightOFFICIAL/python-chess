# ver 910
# flowingconfig.py

# libraries ============================================================================================================
from screeninfo import get_monitors
import logging

# setting up defaults ==================================================================================================
# debug [should not be turned on by user, and in production by developer] ----------------------------------------------
debug_mode = 0
if debug_mode == 1:
    logging.basicConfig(
        format='log:%(levelname)s:%(filename)s:%(lineno)d - %(message)s', level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.CRITICAL+1)
# rate of screen update [should not be changed] ------------------------------------------------------------------------
fps_max = 36
# window width and height [changeable, adjustible] ---------------------------------------------------------------------
# if auto-detection works - its height=width is equal to display height minus 90
try:
    for display in get_monitors():
        if display.is_primary:
            width = display.height - 90
            logging.debug(
                "Auto-detection of screen height: Detected screen height: %d", width)
except:
    logging.debug(
        "Auto-detection of screen height: Screen's height auto-detection failed. Applying default.")
    width = 600
# game mode [changeable] -----------------------------------------------------------------------------------------------
# 0 - PvP (hotseat)
# 1 - PvE (versus script)
game_mode = 0
# if game mode is 1, then difficulty determines algorithms complexity [changeable] -------------------------------------
# 0 - random choice
# 1 - simple table evaluation 1-turn-deep
# 2 - advanced table evaluation minimax 2-turns-deep (released in build 800, adjusted in 910)
# 3 - advanced table evaluation minimax 3-turns-deep plus alpha-beta cut (released in build 800, adjusted in 910)
difficulty = 0
# padding size, distance between board and the window border [should not be changed] -----------------------------------
padding_absolute = 130
# visual set (released in build 800) [changeable] ----------------------------------------------------------------------
visual_set = 0
# timer for each person (in minutes) [changeable] ----------------------------------------------------------------------
time_restriction = 15
# time before game starts [not recommended to change] ------------------------------------------------------------------
freeze_time = 3

# reading from file ====================================================================================================
try:
    config_file = open("config.txt")
    lines = config_file.readlines()
    for line in lines:
        var_name = str(line.split("=")[0])
        if (var_name in ["game_mode", "difficulty", "visual_set", "freeze_time", "time_restriction"]):
            var_value = int(line.split("=")[1])
            locals()[var_name] = var_value
            logging.debug(
                "Reading config: Assign value %d to parameter %s", var_value, var_name)
except (FileExistsError, AttributeError, ValueError, FileNotFoundError) as e:
    logging.warning(
        "Reading config: Config file is corrupted, does not exist or is unreadable, possibly parsing error.\nNot parsed values are set to default.")

# check values for logical errors ======================================================================================
time_restriction = 15 if (time_restriction > 60000) or (
    time_restriction < 0.5) else time_restriction
game_mode = 0 if (game_mode != 0 and not 1) else game_mode
difficulty = 0 if (difficulty > 3) or (difficulty < 0) else difficulty
freeze_time = 5 if (freeze_time > 10) or (freeze_time < 0) else freeze_time

# static and calculated values =========================================================================================
height = width
padding_half = padding_absolute // 2
top_left_corner = (padding_half, padding_half)
top_right_corner = (width - padding_absolute, padding_half)
bottom_left_corner = (padding_half, width - padding_absolute)
bottom_right_corner = (width - padding_absolute, width - padding_absolute)
cell_size_x = (width - padding_absolute) / 8
cell_size_y = (height - padding_absolute) / 8
time_restriction_seconds = 60 * time_restriction
pop_increasing_size = 0.085 * width
