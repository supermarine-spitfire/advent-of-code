import scala.collection.mutable
import scala.io.Source

object DaySeven {
  def main(args: Array[String]): Unit = {
    val filename = "day-7-input.txt"
    println("PART 1")
    val phaseSettings = generatePhaseSettings(0, 4)

    // Part 1 tests
    var pgm = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
    partOne(pgm, List(Vector(4, 3, 2, 1, 0)))
    pgm = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
    partOne(pgm, List(Vector(0, 1, 2, 3, 4)))
    pgm = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
    partOne(pgm, List(Vector(1, 0, 4, 3, 2)))

    pgm = Source.fromFile(filename).getLines.mkString
    partOne(pgm, phaseSettings)
    // Attempt 1: 2134662412 (too high)
    // Attempt 2: 368584
  }

  def generatePhaseSettings(lowerLimit: Int, upperLimit: Int): Seq[IndexedSeq[Int]] = {
    val phaseSettings = Range(lowerLimit, upperLimit + 1).permutations.toList
    phaseSettings
  }

  def partOne(program: String, phaseSettings: Seq[IndexedSeq[Int]]): Unit = {
    println(s"Program tape: $program")
    val buffer = new mutable.Queue[Int]()

    val computer = new IntcodeComputer(buffer = buffer)
    computer.loadProgram(program)
    var input = 0
    var maxValue = Int.MinValue
    var maxPhaseSetting = mutable.ArrayBuffer[Int]()
    for (phaseSetting <- phaseSettings) {
      for (p <- phaseSetting) {
        buffer.enqueue(p)
        buffer.enqueue(input)
        println(s"buffer (before running): $buffer")
        computer.run(interactiveMode = false)
        println(s"buffer (after running): $buffer")
        input = buffer.dequeue()
        println(s"maxValue: $maxValue")
        println(s"input: $input")
      }
      if (input > maxValue) {
        println("Updating maxValue.")
        maxValue = input
        maxPhaseSetting.clear()
        for (p <- phaseSetting) {
          maxPhaseSetting += p
        }
      } else {
        println("No change to maxValue.")
      }
      buffer.clear()
      input = 0
    }
    println(s"maxValue: $maxValue")
    println(s"maxPhaseSetting: $maxPhaseSetting")
    println()
  }
}
