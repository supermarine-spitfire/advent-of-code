import scala.io.Source

class DayOne {
  def calcFuelForModule(moduleMass: Int): Int = {
    math.floor(moduleMass / 3).asInstanceOf[Int] - 2
  }

  def calcFuelForFuel(fuelMass: Int): Int = {
    @scala.annotation.tailrec
    def loop(acc: Int, mass: Int): Int = {
      Console.out.println(s"acc: ${acc}")
      Console.out.println(s"mass: ${mass}")
      val reqFuel = calcFuelForModule(mass)
      if (reqFuel <= 0 ) {
        acc
      } else {
        Console.out.println(s"reqFuel: ${reqFuel}")
        loop(acc + reqFuel, reqFuel)
      }
    }

    loop(0, fuelMass)
  }
}

object DayOne {
  def main(args: Array[String]): Unit = {
    if (args.length > 0) {
      var totalFuel = 0
      val fuelCalculator = new DayOne()
      for (mass <- Source.fromFile(args(0)).getLines()) {
        Console.out.println(s"Mass of current module: ${mass}")
        var moduleFuel = fuelCalculator.calcFuelForModule(mass.toInt)
        Console.out.println(s"Fuel required for module: ${moduleFuel}")
        var fuelFuel = fuelCalculator.calcFuelForFuel(moduleFuel)
        Console.out.println(s"Fuel required for fuel: ${fuelFuel}")
        totalFuel += moduleFuel
        totalFuel += fuelFuel
        Console.out.println(s"Current value of totalFuel: ${totalFuel}")
      }
      Console.out.println(s"Total required fuel: ${totalFuel}")
    } else{
      Console.err.println("Please enter filename.")
    }
  }
}