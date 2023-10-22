from lib.parse import parse_string_lists


class ArithmeticLogicUnit:

    def __init__(self) -> None:
        self.vars = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0,
        }
        self.input = "inp"
        self.add = "add"
        self.mul = "mul"
        self.div = "div"
        self.mod = "mod"
        self.eql = "eql"
    
    def well_formed(self, inp: str):
        for char in inp:
            if char == "0":
                return False
        return len(inp) == 14

    def find_largest_possible_model_number(self) -> str:
        for i in range(99999999999999, 10000000000000, -1):
            inp = str(i)
            print(inp)
            if self.well_formed(inp) and self.is_valid_model_number(inp):
                return inp
        return "-1"
                    

    def is_valid_model_number(self, inp: str) -> bool:
        instructions = parse_string_lists("2021/day24/input.txt")
        input_array = list(inp)

        for ins in instructions:
            root = ins[0]
            var1 = ins[1]
            val2 = 0
            if len(ins) > 2:
                if ins[2].isnumeric() or ins[2][0] == "-":
                    val2 = int(ins[2])
                else:
                    val2 = int(self.vars[ins[2]])

            if root == self.input:
                self.vars[var1] = int(input_array.pop(0))
            elif root == self.add:
                self.vars[var1] += val2
            elif root == self.div:
                val1 = self.vars[var1]
                self.vars[var1] = (val1 // val2)
            elif root == self.mod:
                val1 = self.vars[var1]
                self.vars[var1] = (val1 % val2)
            elif root == self.mul:
                self.vars[var1] *= val2
            else:
                val1 = self.vars[var1]
                self.vars[var1] = 1 if val1 == val2 else 0
        
        return self.vars["z"] == 0






alu = ArithmeticLogicUnit()
# alu.is_valid_model_number("99999999999999")
print(alu.find_largest_possible_model_number())