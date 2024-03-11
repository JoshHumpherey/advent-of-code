def part1() -> int:
    with open('day3/input.txt') as f:
        lines = f.readlines()
        lim = len(lines) / 2
        digits = [0] * 12
        for bstr in lines:
            bstr = bstr.strip()
            for i in range(len(bstr)):
                digits[i] += int(bstr[i])

        gamma, epsilon = "", ""
        
        for i in range(len(digits)):
            if digits[i] > lim:
                gamma += '1'
                epsilon += '0'
            else:
                gamma += '0'
                epsilon += '1'

        print(f"Gamma {gamma}, Epsilon {epsilon}")
        return int(gamma,2) * int(epsilon, 2)

def part2() -> int:
    with open('day3/input.txt') as f:
        lines = f.readlines()
        
        oxygen, co2 = [], []
        for bstr in lines:
            bstr = bstr.strip()
            oxygen.append(bstr)
            co2.append(bstr)
            
        
        for i in range(0, 12):
            o_plus, o_min, c_plus, c_min = 0,0,0,0
            for bstr_o in oxygen:
                val = int(bstr_o[i])
                if val == 1:
                    o_plus += 1
                else:
                    o_min += 1
            for bstr_c in co2:
                val = int(bstr_c[i])
                if val == 1:
                    c_plus += 1
                else:
                    c_min += 1

            o_sig, c_sig = '0', '0'
            if o_plus >= o_min:
                o_sig = '1'
            
            if c_plus < c_min:
                c_sig = '1'
            

            new_oxygen, new_co2 = [], []
            for candidate in oxygen:
                if len(oxygen) == 1:
                    new_oxygen.append(candidate)
                    continue
                elif candidate[i] == o_sig:
                    new_oxygen.append(candidate)

            for candidate in co2:
                if len(co2) == 1:
                    new_co2.append(candidate)
                    continue
                elif candidate[i] == c_sig:
                    new_co2.append(candidate)

            oxygen, co2 = new_oxygen, new_co2

        print([oxygen, co2])
        return int(oxygen[0],2) * int(co2[0], 2)
                    
                
                
            
            

        
        
            
            
        