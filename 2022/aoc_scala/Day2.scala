import scala.collection.Map
import scala.io.Source

def arrayToTuple(arr: Array[String]): Tuple2[String, String] =
    // Assumes arr is of length 2.
    (arr(0), arr(1))

@main def dayTwo() =
    println("Advent of Code Day 2")
    println("--------------------")
    val strategyGuide = Source.fromFile("input/day-2-input.txt").getLines().map((s: String) => arrayToTuple(s.split(" "))).toList

    // Read sums as outcome score plus shape score.
    val perfectStrategyLookupTable = Map[String, Map[String, Int]](  // Start looking up by opponent, then by player.
        "A" -> Map[String, Int](    // Rock
            "X" -> (3 + 1),   // Rock: draw
            "Y" -> (6 + 2),   // Paper: win
            "Z" -> (0 + 3)    // Scissors: loss
        ),
        "B" -> Map[String, Int](    // Paper
            "X" -> (0 + 1),   // Rock: loss
            "Y" -> (3 + 2),   // Paper: draw
            "Z" -> (6 + 3)    // Scissors: win
        ),
        "C" -> Map[String, Int](    // Scissors
            "X" -> (6 + 1),   // Rock: win
            "Y" -> (0 + 2),   // Paper: loss
            "Z" -> (3 + 3)    // Scissors: draw
        )
    )

    // Calculate total score, assuming strategy guide is perfect.
    var totalScore = 0
    for (opponentMove, playerMove) <- strategyGuide
    do
        totalScore += perfectStrategyLookupTable(opponentMove)(playerMove)

    println("PART 1")
    println("======")
    println(s"Total score (perfect strategy guide): $totalScore")
    println("======")

    // Read sums as outcome score plus shape score.
    val outcomeLookupTable = Map[String, Map[String, Int]]( // Start looking up by opponent's move, then by expected outcome
        "A" -> Map[String, Int](    // Rock
            "X" -> (0 + 3), // Loss: play scissors.
            "Y" -> (3 + 1), // Draw: play rock.
            "Z" -> (6 + 2)  // Win: play paper.
        ),
        "B" -> Map[String, Int](   // Paper
            "X" -> (0 + 1), // Loss: play rock.
            "Y" -> (3 + 2), // Draw: play paper.
            "Z" -> (6 + 3)  // Win: play scissors.
        ),
        "C" -> Map[String, Int](   // Scissors
            "X" -> (0 + 2), // Loss: play paper.
            "Y" -> (3 + 3), // Draw: play scissors.
            "Z" -> (6 + 1)  // Win: play rock.
        )
    )

    // Calculate total score, assuming strategy guide describes what each match's outcome is.
    totalScore = 0
    for (opponentMove, playerMove) <- strategyGuide
    do
        totalScore += outcomeLookupTable(opponentMove)(playerMove)

    println("PART 2")
    println("======")
    println(s"Total score (outcome strategy guide): $totalScore")
    println("======")
