import scala.io.Source
import scala.io.StdIn

class IntcodeComputer() {
  private var param1Mode = -1;
  private var param2Mode = -1;
  private var param3Mode = -1;

  private var program = "";

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

  private def parseOpcode(opcode: Int): Int = {
    if (opcode == 99) return opcode
    val opcodeStr = opcode.toString
    println(s"opcodeStr: $opcodeStr")
    opcodeStr.length match {
      case 1 =>
        param1Mode = 0 // Hundreds digit, implicit 0.
        param2Mode = 0 // Thousands digit, implicit 0.
        param3Mode = 0 // Ten-thousands digit, implicit 0.
        opcode
      case 2 =>
        param1Mode = 0 // Hundreds digit, implicit 0.
        param2Mode = 0 // Thousands digit, implicit 0.
        param3Mode = 0 // Ten-thousands digit, implicit 0.
        opcodeStr.substring(1).toInt
      case 3 =>
        param1Mode = opcodeStr.charAt(1).toInt // Hundreds digit.
        param2Mode = 0 // Thousands digit, implicit 0.
        param3Mode = 0 // Ten-thousands digit, implicit 0.
        opcodeStr.substring(2).toInt
      case 4 =>
        param1Mode = opcodeStr.charAt(1).toInt // Hundreds digit.
        param2Mode = opcodeStr.charAt(0).toInt // Thousands digit.
        param3Mode = 0 // Ten-thousands digit, implicit 0.
        println(s"param1Mode: $param1Mode")
        println(s"param2Mode: $param2Mode")
        println(s"param3Mode: $param3Mode")
        opcodeStr.substring(3).toInt
      case 5 =>
        param1Mode = opcodeStr.charAt(2).toInt // Hundreds digit.
        param2Mode = opcodeStr.charAt(1).toInt // Thousands digit.
        param3Mode = opcodeStr.charAt(0).toInt // Ten-thousands digit.
        println(s"param1Mode: $param1Mode")
        println(s"param2Mode: $param2Mode")
        println(s"param3Mode: $param3Mode")
        opcodeStr.substring(4).toInt
    }
  }

  def loadProgram(program: String): Unit = {
    this.program = program
  }

  def run(): String = {
    val machineTape = program.split(",").map(s => s.toInt)

    var i = 0
    while (i < machineTape.length) {
      val opcode = parseOpcode(machineTape(i))
      println(s"opcode: $opcode")
      if (opcode == 99) {
        // Halt.
        i = machineTape.length + 1
      } else if (opcode == 3) {
        // Get input.
        val address = machineTape(i + 1)
        val input = StdIn.readLine("Enter integer: ").toInt
        machineTape(address) = input
        i += 2
      } else if (opcode == 4) {
        // Print output.
        val output = machineTape(i + 2)
        println(s"Output: $output")
        i += 2
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
        i += 4
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
    // Test
    var pgm = "3,0,4,0,99"
    runProgram(pgm)

    // Part 1
    pgm = Source.fromFile(filename).getLines.mkString
    runProgram(pgm)
  }

  def runProgram(program: String) = {
    println(s"Program tape: $program")
    val computer = new IntcodeComputer()
    computer.loadProgram(program)
    val result = computer.run()
    println(s"Machine tape: $result")
  }
}