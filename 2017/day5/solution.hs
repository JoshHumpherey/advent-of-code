module Main where

import qualified Data.Vector.Unboxed as V
import qualified Data.Vector.Unboxed.Mutable as MV
import Control.Monad.ST
import Control.Monad (when)

stringListToIntList :: [String] -> [Int]
stringListToIntList xs = [read x :: Int | x <- xs]

stringListToIntListMutable :: [String] -> V.Vector Int
stringListToIntListMutable xs = V.fromList [read x :: Int | x <- xs]

increment :: Int -> [Int] -> [Int]
increment 0 (x:xs) = x+1 : xs
increment n (x:xs) = x : increment (n-1) xs

decrement :: Int -> [Int] -> [Int]
decrement 0 (x:xs) = x-1 : xs
decrement n (x:xs) = x : decrement (n-1) xs

jump :: Int -> [Int] -> Int -> Bool -> Int
jump idx xs count variableOffset
    | idx < 0 = 0
    | idx >= length xs = count
    | offset >= 3 && variableOffset = jump (idx + offset) (decrement idx xs) (count+1) variableOffset
    | otherwise = jump (idx + offset) (increment idx xs) (count+1) variableOffset
    where offset = xs !! idx

jumpMutable :: V.Vector Int -> Bool -> Int
jumpMutable input variableOffset = runST $ do
    vec <- V.thaw input
    let len = MV.length vec
    let noop = -1
    let loop !idx !count
          | idx < 0 = return noop
          | idx >= len = return count
          | otherwise = do
              offset <- MV.read vec idx
              let !nextIdx = idx + offset
              when (variableOffset && offset >= 3) $ do
                  MV.modify vec (subtract 1) idx
              when (not variableOffset || offset < 3) $ do
                  MV.modify vec (+1) idx
              loop nextIdx (count + 1)
    loop 0 0

main :: IO ()
main = do
    rawInput <- readFile "input.txt"
    print (jumpMutable (stringListToIntListMutable (lines rawInput)) False)
    print (jumpMutable (stringListToIntListMutable (lines rawInput)) True)