import scala.io.Source
import scala.io.StdIn

class IntcodeComputer(val program: String) {
  private var param1Mode = -1;
  private var param2Mode = -1;
  private var param3Mode = -1;

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

  private def parseOpcode(opcode: Int) = {
    val opcodeStr = opcode.toString
    opcodeStr.length match {
      case 1 => opcode
      case 2 => opcode
      case 4 =>
        param1Mode = opcodeStr.charAt(1).toInt // Hundreds digit.
        param2Mode = opcodeStr.charAt(0).toInt // Thousands digit.
        param3Mode = 0 // Ten-thousands digit, implicit 0.
        println(s"param1Mode: $param1Mode")
        println(s"param2Mode: $param2Mode")
        println(s"param3Mode: $param3Mode")
        opcodeStr.substring(2).toInt
      case 5 =>
        param1Mode = opcodeStr.charAt(2).toInt // Hundreds digit.
        param2Mode = opcodeStr.charAt(1).toInt // Thousands digit.
        param3Mode = opcodeStr.charAt(0).toInt // Ten-thousands digit.
        println(s"param1Mode: $param1Mode")
        println(s"param2Mode: $param2Mode")
        println(s"param3Mode: $param3Mode")
        opcodeStr.substring(3).toInt
    }
  }

  def run(): String = {
    val machineTape = program.split(",").map(s => s.toInt)

    var i = 0
    while (i < machineTape.length) {
      val opcode = parseOpcode(machineTape(i))
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
        println(output)
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
    if (args.length > 0) {
//      val pgmStr = Source.fromFile(args(0)).getLines.mkString
//      println(s"pgmStr: $pgmStr")
//      val computer = new IntcodeComputer(pgmStr)
//      println("Part 1 Output")
//      val result = computer.run()
//      println(result)
//      println("Part 2 Output")
//      val (noun, verb) = computer.findInputs("19690720", 0, 99)
//      println(s"noun: $noun")
//      println(s"verb: $verb")
//      println(s"100 * $noun + $verb = ${100 * noun + verb}")
      var pgm = "3,0,4,0,99"
      var computer = new IntcodeComputer(pgm)
      var result = computer.run()
      println(result)
    } else {
      Console.err.println("Please enter filename.")
    }
  }
}