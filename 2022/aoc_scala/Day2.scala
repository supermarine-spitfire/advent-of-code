import scala.collection.Map
import scala.io.Source

@main def dayTwo() =
    println("Advent of Code Day 2")
    println("--------------------")
    val strategyGuide = Source.fromFile("input/day-2-input.txt").getLines().map((s: String) => s.split(" "))

    // Read sums as outcome score plus shape score.
    val perfectDecisionMatrix = Map[String, Map[String, Int]](  // Start looking up by opponent, then by player.
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
    for (opponentMove, playerMove) <- strategyGuide do println(s"$opponentMove: $playerMove")
