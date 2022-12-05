import scala.collection.Map
import scala.io.Source

@main def dayThree() =
    println("Advent of Code 2022 Day 3")
    println("-------------------------")
    val rucksacks = Source.fromFile("input/day-3-input.txt").getLines().toList

    val priorities = (('a' to 'z') ++ ('A' to 'Z')).map(c => c.toString())
                                 .toList
                                 .zip(((1 to 53)).toList)   // Priority scores.
                                 .toMap

    // println(s"priorities: $priorities")
    var totalPriorities = 0
    for (rucksack <- rucksacks)
    do
        val compartment1 = rucksack.substring(0, rucksack.length / 2)
        val compartment2 = rucksack.substring(rucksack.length / 2)
        val commonItems = compartment1.toSet.map(_.toString()) intersect compartment2.toSet.map(_.toString())
        // println(s"commonItems: $commonItems")

        // Calculate total priority of common items.
        totalPriorities += priorities(commonItems.toList.head)

    println("PART 1")
    println("======")
    println(s"Total priorities: $totalPriorities")
    println("======")

    totalPriorities = 0
    var i = 0
    while i < rucksacks.length do
        // Get all items in common between the rucksacks, grouped in threes.
        val commonItems = (
            rucksacks(i).toSet & rucksacks(i + 1).toSet & rucksacks(i + 2).toSet
            ).map(_.toString())

        // Calculate total priority of common items.
        totalPriorities += priorities(commonItems.toList.head)
        i += 3

    println("PART 2")
    println("======")
    println(s"Total priorities: $totalPriorities")
