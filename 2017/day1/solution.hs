module Main where

import Data.Char (digitToInt)

createPairs :: String -> [(Char, Char)]
createPairs [] = [] 
createPairs inp = zip inp (tail inp ++ [head inp])

createModPairs :: String -> [(Char, Char)]
createModPairs [] = []
createModPairs inp = zip inp (map (inp !!) indices)
  where
    len = length inp
    halfLen = len `div` 2
    indices = map (\i -> (i + halfLen) `mod` len) [0..len-1]

checksum :: (String -> [(Char, Char)]) -> String -> Int
checksum pairsFunc inp = sum [digitToInt x | (x, y) <- pairsFunc inp, x == y]

part1 :: [String] -> Int
part1 inp = sum [checksum createPairs x | x <- inp]

part2 :: [String] -> Int
part2 inp = sum [checksum createModPairs x | x <- inp]

main :: IO ()
main = do
    rawInput <- readFile "input.txt"
    let input = lines rawInput
    print (part1 input)
    print (part2 input)