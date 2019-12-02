// FOR DAY 1
def calcFuelForModule(moduleMass: Int): Int = {
  math.floor(moduleMass / 3).asInstanceOf[Int] - 2
}

def calcFuelForFuel(fuelMass: Int) = {
  def loop(acc: Int, mass: Int): Int = {
    Console.out.println(s"acc: ${acc}")
//    Console.out.println(s"mass: ${mass}")
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

def calcTotalFuel(mass: Int) = {
  val moduleFuel = calcFuelForModule(mass)
  val fuelFuel = calcFuelForFuel(moduleFuel)
  println(s"moduleFuel: ${moduleFuel}")
  println(s"fuelFuel: ${fuelFuel}")
  println(s"Total fuel: ${moduleFuel + fuelFuel}")
}

calcTotalFuel(14)
calcTotalFuel(1969)
calcTotalFuel(100756)