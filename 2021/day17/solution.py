def get_target():
    with open('day17/input.txt') as f:
        raw_input = f.readlines()[0].strip()
        splits = raw_input.split(' ')
        raw_x, raw_y = splits[2], splits[3]
        x_vals, y_vals = raw_x.split('=')[1], raw_y.split('=')[1]
        x_vals = x_vals[:len(x_vals)-1]
        x1, x2 = x_vals.split('..')
        y1, y2 = y_vals.split('..')
        x1, x2 = min(int(x1), int(x2)), max(int(x1), int(x2))
        y1, y2 = min(int(y1), int(y2)), max(int(y1), int(y2))
        print([x1, x2], [y1, y2])
        return [x1, x2], [y1, y2]
        
def overshot_target(x_pair, y_pair, x, y, xvel, yvel) -> bool:
    if x < x_pair[0] and xvel <= 0:
        return True
    elif x > x_pair[1] and xvel >= 0:
        return True
    elif y < y_pair[0] and yvel < 0:
        return True
    else:
        return False

def in_target(x_pair, y_pair, x, y) -> bool:
    if x_pair[0] <= x <= x_pair[1] and y_pair[0] <= y <= y_pair[1]:
        return True
    return False

def iterate(x, y, xvel, yvel):
    x += xvel
    y += yvel

    if xvel > 0:
        xvel -= 1
    if xvel < 0:
        xvel += 1
    yvel -= 1
    return x,y,xvel,yvel

def shoot_probe(x_pair, y_pair, xvel, yvel) -> int:
    x,y = 0,0
    startx, starty = xvel, yvel
    y_max = float('-inf')
    
    while True:
        x,y,xv,yv = iterate(x,y,xvel,yvel)
        y_max = max(y, y_max)
        
        if in_target(x_pair, y_pair, x, y):
            print(f"Hit target: {[startx, starty], [y_pair[0], y, y_pair[1]], yvel}")
            return y_max
        elif overshot_target(x_pair, y_pair, x, y, xvel, yvel):
            # print(f"Overshot: {[startx, starty]}")
            return float('-inf')
        xvel, yvel = xv, yv

# max_yv = abs(target[1][0])
def part1() -> int:
    x_pair, y_pair = get_target()
    combos = 0
    
    for xvel in range(1, x_pair[1]+1):
        y_max = float('-inf')
        for yvel in range(y_pair[0]-1, 400):
            res = shoot_probe(x_pair, y_pair, xvel, yvel)
            if res != float('-inf'):
                y_max = max(res, y_max)
                combos += 1
            
    return combos
            
    
    
        
        