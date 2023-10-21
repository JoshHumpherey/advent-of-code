BLACK = 0
WHITE = 1
TRANSPARENT = 2
UNDEFINED = -1
    
class Image:

    def __init__(self, width: int, length: int, input, debug: bool):
        self.debug = debug
        self.width = width
        self.length = length
        self.area = width * length
        self.layers = []

        for ptr in range(0, len(input), self.area):
            l = [[0 for _ in range(self.width)] for _ in range(self.length)]
            for r in range(0, self.length):
                for c in range(0, self.width):
                    l[r][c] = input[ptr]
                    ptr += 1
            self.layers.append(l)
        
        if debug:
            print(f"Area: {self.area}, Layers: {len(self.layers)}")

    def get_layer_counts(self, layer_idx: int) -> dict:
        """ Fetches the count of each int for a given layer """
        layer = self.layers[layer_idx]
        counts = {0:0}
        for r in range(0, len(layer)):
            for c in range(0, len(layer[0])):
                if layer[r][c] not in counts:
                    counts[layer[r][c]] = 1
                else:
                    counts[layer[r][c]] += 1
        return counts

    def render(self):
        """ Renders the final image by stacking all layers together and resolving """
        canvas = [[UNDEFINED for _ in range(self.width)] for _ in range(self.length)]

        for l in self.layers:
            for r in range(0, len(l)):
                for c in range(0, len(l[0])):
                    if canvas[r][c] == UNDEFINED and l[r][c] in [BLACK, WHITE]:
                        canvas[r][c] = l[r][c]
        
        for r in range(0, len(canvas)):
            line = ""
            for c in range(0, len(canvas[0])):
                if canvas[r][c] == 0:
                    line += str('.')
                else:
                    line += str('1')
            print(line)

def get_input():
    input = []
    with open('input.txt') as f:
        lines = f.readlines()
        for c in lines[0]:
            input.append(int(c))
    return input

def main():
    DEBUG = True
    input = get_input()
    img = Image(width=25, length=6, input=input, debug=DEBUG)

    # lowest_zeros, low_counts = float('inf'), {}
    # for idx in range(len(img.layers)):
    #     c = img.get_layer_counts(layer_idx=idx)
    #     if c[0] < lowest_zeros:
    #         lowest_zeros = c[0]
    #         low_counts = c
    
    img.render()
    


main()