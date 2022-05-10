# custom vars
width = 750
height = 750
margin_abs = 130
margin_abs_half = margin_abs // 2
visual_set = 0
fps_max = 24
set_player_minutes = 45

# calculated vars
top_left_corner = (margin_abs_half, margin_abs_half)     # 50, 50
bot_right_corner = (width-margin_abs, width-margin_abs)  # 650, 650
top_right_corner = (width-margin_abs, margin_abs_half)   # 650, 50
bot_left_corner = (margin_abs_half, width-margin_abs)    # 50, 650
scalex_size = (width - margin_abs) / 8
scaley_size = (height - margin_abs) / 8
player_time = 60*set_player_minutes
