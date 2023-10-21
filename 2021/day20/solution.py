class Image:

    def __init__(self, raw_algo: str, image_data):
        self.BOARD_SIZE = 500
        self.algo = ''
        self.image = self.board = [ [0]*self.BOARD_SIZE for _ in range(self.BOARD_SIZE) ]
        
        for bit in raw_algo:
            if bit == '#':
                self.algo += '1'
            else:
                self.algo += '0'

        r_start = self.BOARD_SIZE // 2 - len(image_data) // 2
        c_start = self.BOARD_SIZE // 2 - len(image_data[0]) // 2
        norm_r = 0
        for r in range(r_start, r_start + len(image_data)):
            norm_c = 0
            for c in range(c_start, c_start + len(image_data[0])):
                if image_data[norm_r][norm_c] == '#':
                    self.image[r][c] = 1
                norm_c += 1
            norm_r += 1



    def pixels(self) -> int:
        total = 0
        for r in range(len(self.image)):
            for c in range(len(self.image[0])):
                total += self.image[r][c]
        return total









    

    def next_pixel(self, r, c, iteration) -> int:
        raw_key = ''
        for xr in range(r-1, r+2):
            for xc in range(c-1, c+2):
                if xr < 0 or xr >= len(self.image) or xc < 0 or xc >= len(self.image[0]):
                    raw_key += str(iteration % 2)
                else:
                    raw_key += str(self.image[xr][xc])
        key = int(raw_key, 2)
        res = int(self.algo[key])
        return res
    
    def upscale(self, iteration) -> None:
        new_image = []
        for r in range(len(self.image)):
            next_row = []
            for c in range(len(self.image[0])):
                next_row.append(self.next_pixel(r,c, iteration))
            new_image.append(next_row)
        self.image = new_image
                
        

def create_image() -> Image:
    with open('day20/input.txt') as f:
        lines = f.readlines()
        algo = ''
        image_data = []
        for i in range(len(lines)):
            if i == 0:
                algo = lines[i].strip()
            elif i >= 2:
                image_data.append([char for char in lines[i].strip()])
        return Image(raw_algo=algo, image_data=image_data)



def part1() -> int:
    img = create_image()

    for i in range(0, 2):
        print(f"Upscaling: {i+1}")
        img.upscale(iteration=i)
    
    return img.pixels()
                