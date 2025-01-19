module Main where

import Data.List (sort)

hasDuplicates :: [String] -> Bool
hasDuplicates [] = False
hasDuplicates (x:xs) = x `elem` xs || hasDuplicates xs

hasAnagram :: [String] -> Bool
hasAnagram [] = False
hasAnagram xs = hasDuplicates sortedInp == False
    where sortedInp = [sort(x) | x <- xs]

part1 :: [String] -> Int
part1 xs = length [x | x <- xs, hasDuplicates (words x) == False]

part2 :: [String] -> Int
part2 xs = length [x | x <- xs, hasAnagram (words x) == True]

main :: IO ()
main = do
    rawInput <- readFile "input.txt"
    let input = lines rawInput
    print (part1 input)
    print (part2 input)