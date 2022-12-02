import scala.collection.mutable.ArrayBuffer
import scala.io.Source

// Old approach for invoking a method from the command line.
/*
 * object Day1 {
 *     def main(args: Array[String]): Unit = {
 *         Method body goes here...
 *     }
 * }
 */

// Current approach for invoking a method from the command line.
@main def dayOne() =
    println("Advent of Code 2022 Day 1")
    println("-------------------------")
    // Load calorie counts.
    val calorieLogFile = "input/day-1-input.txt"
    val calorieCounts = Source.fromFile(calorieLogFile).getLines()

    // Get total calories carried by each elf.
    var totalCalories = new ArrayBuffer[Int]()
    var calorieSum = 0
    for calorieCount <- calorieCounts
    do
        if calorieCount != "" then
            calorieSum += calorieCount.toInt
        else
            totalCalories.append(calorieSum)
            calorieSum = 0

    // Get highest calorie count.
    totalCalories = totalCalories.sortWith(_ > _)
    // totalCalories = totalCalories.sorted
    println("PART 1")
    println("======")
    println(s"Highest calorie count: ${totalCalories.head}")

    // Get sum of top three calorie counts.
    println("PART 2")
    println("======")
    // val topThreeCalorieSum = totalCalories.slice(totalCalories.length - 3, totalCalories.length).sum
    val topThreeCalorieSum = totalCalories.slice(0, 3).sum
    println(s"Top three calorie sum: $topThreeCalorieSum")
