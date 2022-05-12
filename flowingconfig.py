# enviroment settings
fps_max = 24
width = 750
height = width
margin_abs = 130
margin_abs_half = margin_abs // 2

# game settings
visual_set = 0
set_player_minutes = 30

# calculated and static vars
top_left_corner = (margin_abs_half, margin_abs_half)     # 50, 50
bot_right_corner = (width-margin_abs, width-margin_abs)  # 650, 650
top_right_corner = (width-margin_abs, margin_abs_half)   # 650, 50
bot_left_corner = (margin_abs_half, width-margin_abs)    # 50, 650
scalex_size = (width - margin_abs) / 8
scaley_size = (height - margin_abs) / 8
player_time = 60 * set_player_minutes
increasing_size = 55

def load_config():
    pass