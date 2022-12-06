import scala.collection.Set
import scala.io.Source
import scala.util.control.Breaks._

def findUniqueSubstringStartingIndex(str: String, substringLength: Int): Int = 
    var startingIndex = substringLength
    breakable {
        while (startingIndex < str.length()) {
            if (str.substring(startingIndex - substringLength, startingIndex).toSet.knownSize == substringLength) {
                // Found start-of-substring marker (since sets do not hold duplicates).
                break
            } else {
                startingIndex += 1
            }
        }
    }

    startingIndex

@main def daySix() =
    println("Advent of Code 2022 Day 6")
    println("-------------------------")
    val signalInput = Source.fromFile("input/day-6-input.txt").mkString
    // println(s"signalInput: $signalInput")

    // Sweep a window of size 4 across signal_input, looking for a substring of 4 unique characters.
    val startOfPacketIndex = findUniqueSubstringStartingIndex(signalInput, 4)

    println("PART 1")
    println("======")
    println(s"First marker index: $startOfPacketIndex")
    println("======")


    // Sweep a window of size 14 across signal_input, looking for a substring of 14 unique characters.
    val startOfMessageIndex = findUniqueSubstringStartingIndex(signalInput, 14)

    println("PART 2")
    println("======")
    println(s"First marker index: $startOfMessageIndex")
