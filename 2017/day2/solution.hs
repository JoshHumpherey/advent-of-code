module Main where

parseNumbers :: String -> [Int]
parseNumbers str = map read (words str)

generatePairs :: [Int] -> [(Int, Int)]
generatePairs xs = [(x, y) | (x, i) <- zip xs [0..], (y, j) <- zip xs [0..], i /= j]

rowDiff :: String -> Int
rowDiff inp = maximum parsedInp - minimum parsedInp
    where 
        parsedInp = parseNumbers inp

rowDiv :: String -> Int
rowDiv inp = [fst pair `div` snd pair | pair <- genPairs, fst pair `mod` snd pair == 0] !! 0
    where 
        parsedInp = parseNumbers inp
        genPairs = generatePairs parsedInp

part1 :: [String] -> Int
part1 inp = sum [rowDiff x | x <- inp]

part2 :: [String] -> Int
part2 inp = sum [rowDiv x | x <- inp]

main :: IO ()
main = do
    rawInput <- readFile "input.txt"
    let input = lines rawInput
    print (part1 input)
    print (part2 input)
