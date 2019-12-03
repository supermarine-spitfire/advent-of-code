import scala.io.Source

class IntcodeComputer(val program: String) {
  private def evalOpcode(tape: Array[Int], lIndex: Int, rIndex: Int, opcode: Int): Int = {
    val lVal = tape(lIndex)
    val rVal = tape(rIndex)
    val result = opcode match {
      case 1 => lVal + rVal
      case 2 => lVal * rVal
      case _ => Int.MinValue
    }
    result
  }

  def run(): String = {
    val machineTape = program.split(",").map(s => s.toInt)

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
    machineTape.mkString(",")
  }

  override def toString: String = program
}

object IntcodeComputer {
  def main(args: Array[String]): Unit = {
    if (args.length > 0) {
      val pgmStr = Source.fromFile(args(0)).getLines.mkString
      println(s"pgmStr: $pgmStr")
      val computer = new IntcodeComputer(pgmStr)
      val result = computer.run()
      println(result)
    } else {
      Console.err.println("Please enter filename.")
    }
  }
}