stackWidth :: [Int] -> Double
stackWidth [v, h] = sqrt (fromIntegral v / fromIntegral h)

santaFits :: [Int] -> Bool
santaFits [v, h, d] = stackWidth [v, h] > fromIntegral d

main = do
    input <- getLine
    let numbers = map (read :: String -> Int) (words input)
    if santaFits numbers
        then putStrLn "Es gibt Geschenke"
        else putStrLn "Weihnachten faellt ins Wasser"
