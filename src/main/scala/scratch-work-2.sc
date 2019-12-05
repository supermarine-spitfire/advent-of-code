import scala.collection.mutable.ListBuffer

// FOR DAY 4
class SecureContainer(val numDigits: Int) {
  def extractDigits(m: Int, n: Int): (Int, Int) = {
    val left = m % math.pow(10, n).toInt / math.pow(10, n - 1).toInt
    println(s"left: $left")
    val right = m % math.pow(10, n - 1).toInt / math.pow(10, n - 2).toInt
    println(s"right: $right")
    (left, right)
  }

  /*
   * Checks if a number satisfies the following conditions:
   * 1. It has the same number of digits as numDigits.
   * 2. A minimum of two contiguous digits are identical.
   * 3. From left to right, the number's digits are monotonically increasing.
   */
  def checkNumber(m: Int): Boolean = {
    var hasDuplicateDigits = false
    if (m.toString.length != numDigits) {
      // Fails condition 1.
      println("Fails condition 1.")
      false
    } else {
      for (n <- numDigits until 1 by -1) {
//        println(s"n: $n")
//        println(s"n - 1: ${n - 1}")
//        println(s"n - 2: ${n - 2}")
        val (left, right) = extractDigits(m, n)
        if (left == right) {
          // Passes condition 2.
          hasDuplicateDigits = true
          Console.out.println("Passes condition 2.")
        }

        if (left > right) {
          // Fails condition 3.
          println("Fails condition 3.")
          return false
        }
      }
      hasDuplicateDigits
    }
  }

  def print() = {
    println("Trying to print from SecureContainer.")
  }
}

def findPasswords(lowerLimit: Int, upperLimit: Int) = {
  val sc = new SecureContainer(6)
  val passwords = ListBuffer[Int]()
  for (password <- lowerLimit to upperLimit) {
    println(s"password: $password")
    if (sc.checkNumber(password)) {
      passwords += password
    } else {
    }
  }
  (passwords.toList, passwords.length)
}

def checkPassword(password: Int) = {
  val sc = new SecureContainer(6)
  if (sc.checkNumber(password)) {
    println(s"$password is valid.")
  } else {
    println(s"$password is invalid.")
  }
}

checkPassword(111111) // Valid
checkPassword(122345) // Valid
checkPassword(111123) // Valid
checkPassword(135679) // Invalid
checkPassword(223450) // Invalid
checkPassword(123789) // Invalid

val input = "156218-652527"
val range = input.split("-")
val lowerLimit = range(0).toInt
val upperLimit = range(1).toInt

//val (passwords, numPasswords) = findPasswords(lowerLimit, upperLimit)
//println(s"Number of valid passwords: $numPasswords")