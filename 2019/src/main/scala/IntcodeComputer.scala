import scala.collection.mutable
import scala.io.Source
import scala.io.StdIn

class IntcodeComputer(val buffer: mutable.Queue[Int] = mutable.Queue[Int]()) {
  private var param1Mode = -1
  private var param2Mode = -1
  private var param3Mode = -1

  private var program = ""

  private def evalOpcode(tape: Array[Int], lIndex: Int, rIndex: Int, opcode: Int): Int = {
    val lVal = if (param1Mode == 0) tape(lIndex) else lIndex
    val rVal = if (param2Mode == 0) tape(rIndex) else rIndex
    val result = opcode match {
      case 1 => lVal + rVal
      case 2 => lVal * rVal
      case _ => Int.MinValue
    }
    result
  }

  private def parseOpcode(instruction: Int): Int = {
    if (instruction == 99) return instruction
    val instructionStr = instruction.toString
    instructionStr.length match {
      case 1 =>
        param1Mode = 0 // Hundreds digit, implicit 0.
        param2Mode = 0 // Thousands digit, implicit 0.
        param3Mode = 0 // Ten-thousands digit, implicit 0.
        instruction
      case 2 =>
        param1Mode = 0 // Hundreds digit, implicit 0.
        param2Mode = 0 // Thousands digit, implicit 0.
        param3Mode = 0 // Ten-thousands digit, implicit 0.
        instruction
      case 3 =>
        param1Mode = instruction % 1000 / 100 // Hundreds digit.
        param2Mode = 0 // Thousands digit, implicit 0.
        param3Mode = 0 // Ten-thousands digit, implicit 0.
        instructionStr.substring(2).toInt
      case 4 =>
        param1Mode = instruction % 1000 / 100   // Hundreds digit.
        param2Mode = instruction % 10000 / 1000 // Thousands digit.
        param3Mode = 0 // Ten-thousands digit, implicit 0.
        instructionStr.substring(3).toInt
      case 5 =>
        param1Mode = instruction % 1000 / 100     // Hundreds digit.
        param2Mode = instruction % 10000 / 1000   // Thousands digit.
        param3Mode = instruction % 100000 / 10000 // Ten-thousands digit.
        instructionStr.substring(4).toInt
    }
  }

  def loadProgram(program: String): Unit = {
    this.program = program
  }

  def run(interactiveMode: Boolean = true): String = {
    val machineTape = program.split(",").map(s => s.toInt)

    var i = 0
    while (i < machineTape.length) {
      val opcode = parseOpcode(machineTape(i))
      opcode match {
        case 1 =>
          // Addition.
          val lIndex = machineTape(i + 1)
          val rIndex = machineTape(i + 2)
          val resIndex = machineTape(i + 3)
          val lVal = if (param1Mode == 0) machineTape(lIndex) else lIndex
          val rVal = if (param2Mode == 0) machineTape(rIndex) else rIndex
          machineTape(resIndex) = lVal + rVal
          i += 4
        case 2 =>
          // Multiplication.
          val lIndex = machineTape(i + 1)
          val rIndex = machineTape(i + 2)
          val resIndex = machineTape(i + 3)
          val lVal = if (param1Mode == 0) machineTape(lIndex) else lIndex
          val rVal = if (param2Mode == 0) machineTape(rIndex) else rIndex
          machineTape(resIndex) = lVal * rVal
          i += 4
        case 3 =>
          // Get input.
          val address = machineTape(i + 1)
          val input = if (interactiveMode)
            StdIn.readLine("Enter integer: ").toInt
          else
            buffer.dequeue()
          machineTape(address) = input
          i += 2
        case 4 =>
          // Print output.
          val address = machineTape(i + 1)
          val output = machineTape(address)
          if (interactiveMode) {
            println(s"Output: $output")
          } else {
            buffer.enqueue(output)
          }
          i += 2
        case 5 =>
          // Jump-if-true.
          val lIndex = machineTape(i + 1)
          val rIndex = machineTape(i + 2)
          val lVal = if (param1Mode == 0) machineTape(lIndex) else lIndex
          val rVal = if (param2Mode == 0) machineTape(rIndex) else rIndex
          if (lVal != 0) {
            // Jump to address.
            i = rVal
          } else {
            // Advance to next instruction.
            i += 3
          }
        case 6 =>
          // Jump-if-false.
          val lIndex = machineTape(i + 1)
          val rIndex = machineTape(i + 2)
          val lVal = if (param1Mode == 0) machineTape(lIndex) else lIndex
          val rVal = if (param2Mode == 0) machineTape(rIndex) else rIndex
          if (lVal == 0) {
            // Jump to address.
            i = rVal
          } else {
            // Advance to next instruction.
            i += 3
          }
        case 7 =>
          // Less than.
          val lIndex = machineTape(i + 1)
          val rIndex = machineTape(i + 2)
          val resIndex = machineTape(i + 3)
          val lVal = if (param1Mode == 0) machineTape(lIndex) else lIndex
          val rVal = if (param2Mode == 0) machineTape(rIndex) else rIndex
          machineTape(resIndex) = if (lVal < rVal) 1 else 0
          i += 4
        case 8 =>
          // Equals.
          val lIndex = machineTape(i + 1)
          val rIndex = machineTape(i + 2)
          val resIndex = machineTape(i + 3)
          val lVal = if (param1Mode == 0) machineTape(lIndex) else lIndex
          val rVal = if (param2Mode == 0) machineTape(rIndex) else rIndex
          machineTape(resIndex) = if (lVal == rVal) 1 else 0
          i += 4
        case 99 =>
          // Halt.
          i = machineTape.length + 1
      }
    }
    machineTape.mkString(",")
  }

  def run(noun: Int, verb: Int): String = {
    val machineTape = program.split(",").map(s => s.toInt)
    // Dynamically set inputs to program.
    machineTape(1) = noun
    machineTape(2) = verb

    var i = 0
    while (i < machineTape.length) {
      val opcode = machineTape(i)
      if (opcode == 99) {
        i = machineTape.length + 1
      } else {
        val lIndex = machineTape(i + 1)
        val rIndex = machineTape(i + 2)
        val resIndex = machineTape(i + 3)
        val result = evalOpcode(machineTape, lIndex, rIndex, opcode)
        if (result == Int.MinValue) {
          Console.err.println("UNRECOGNISED OPCODE.")
          return "ERROR"
        } else {
          machineTape(resIndex) = result
        }
      }
      i += 4
    }
    machineTape(0).toString
  }

  def findInputs(outputVal: String, lowerLimit: Int, upperLimit: Int): (Int, Int) = {
    for (i <- lowerLimit to upperLimit) {
      for (j <- lowerLimit to upperLimit) {
        val result = run(i, j)
        if (result.equals(outputVal)) {
          // Return tuple of the form (noun, verb)
          return (i, j)
        }
      }
    }
    (Int.MinValue, Int.MinValue)
  }

  override def toString: String = program
}

object IntcodeComputer {
  def main(args: Array[String]): Unit = {
    val filename = "day-5-input.txt"
    // Part 1 test
    println("PART 1")
    var pgm = "3,0,4,0,99"
    runProgram(pgm)

    // Part 1
    pgm = Source.fromFile(filename).getLines.mkString
    runProgram(pgm)

    // Part 2 tests
    println("PART 2")
    pgm = "3,9,8,9,10,9,4,9,99,-1,8"  // Output "1" if input = 8, "0" otherwise.
    runProgram(pgm)
    pgm = "3,9,7,9,10,9,4,9,99,-1,8"  // Output "1" if input < 8, "0" otherwise.
    runProgram(pgm)
    pgm = "3,3,1108,-1,8,3,4,3,99"  // Output "1" if input = 8, "0" otherwise.
    runProgram(pgm)
    pgm = "3,3,1107,-1,8,3,4,3,99"  // Output "1" if input < 8, "0" otherwise.
    runProgram(pgm)

    // Part 2
    pgm = Source.fromFile(filename).getLines.mkString
    runProgram(pgm)
  }

  def runProgram(program: String): Unit = {
    println(s"Program tape: $program")
    val computer = new IntcodeComputer()
    computer.loadProgram(program)
    val result = computer.run()
    println(s"Machine tape: $result")
  }
}