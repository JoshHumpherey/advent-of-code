module Main where

import Data.List (elemIndex)

increment :: Int -> [Int] -> [Int]
increment 0 (x:xs) = x+1 : xs
increment n (x:xs) = x : increment (n-1) xs

zero :: Int -> [Int] -> [Int]
zero 0 (x:xs) = 0 : xs
zero n (x:xs) = x : zero (n-1) xs

maxIndex :: [Int] -> Int
maxIndex xs = head [i | (i, x) <- zip [0..] xs, x == maximum xs]

getMemoryBanks :: String -> [Int]
getMemoryBanks inp = map read (words inp)

distribute :: Int -> Int -> [Int] -> [Int]
distribute amt idx xs
    | amt <= 0 = xs
    | idx >= length xs = distribute amt 0 xs
    | otherwise = distribute (amt-1) (idx+1) (increment idx xs)

singleReallocate :: Int -> [Int] -> [Int]
singleReallocate idx xs = distribute (xs !! idx) (idx + 1) zeroedList
    where zeroedList = zero idx xs

fullReallocate :: [Int] -> [[Int]] -> [[Int]]
fullReallocate xs seen
    | isMember == False = fullReallocate nextReallocate nextSeen
    | otherwise = nextSeen
    where
        isMember = xs `elem` seen
        nextSeen = seen ++ [xs]
        nextReallocate = singleReallocate (maxIndex xs) xs

indexOfSublist :: Eq a => [a] -> [[a]] -> Int
indexOfSublist target listOfLists = 
    case [i | (i, sublist) <- zip [0..] listOfLists, sublist == target] of
        [] -> -1
        (i:_) -> i

cycleLength :: [[Int]] -> [Int]-> Int
cycleLength seen target = (length seen - 1) - targetIdx
    where targetIdx = indexOfSublist target seen

main :: IO ()
main = do
    input <- readFile "input.txt"
    let bank = getMemoryBanks input
    let cycles = fullReallocate bank []
    print (length cycles - 1)
    print (cycleLength cycles (last cycles))