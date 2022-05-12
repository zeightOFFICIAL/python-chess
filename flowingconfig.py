# defaults
fps_max = 24
width = 750
padding_absolute = 130
visual_set = 0
time_restriction = 30
pop_increasing_size = 55

try:
    f = open("config.txt")
    lines = f.readlines()
    for line in lines:
        name = str(line.split("=")[0])
        var = int(line.split("=")[1])
        locals()[name] = var
except FileNotFoundError:
    pass

height = width
padding_abs_half = padding_absolute // 2
top_left_corner = (padding_abs_half, padding_abs_half)
bottom_right_corner = (width - padding_absolute, width - padding_absolute)
top_right_corner = (width - padding_absolute, padding_abs_half)
bottom_left_corner = (padding_abs_half, width - padding_absolute)
cell_size_x = (width - padding_absolute) / 8
cell_size_y = (height - padding_absolute) / 8
time_restriction_seconds = 60 * time_restriction
