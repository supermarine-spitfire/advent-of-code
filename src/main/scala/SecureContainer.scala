import scala.collection.mutable.ListBuffer

class SecureContainer(val numDigits: Int) {
  def extractDigits(m: Int, n: Int): (Int, Int) = {
    val left = m % math.pow(10, n).toInt / math.pow(10, n - 1).toInt
    val right = m % math.pow(10, n - 1).toInt / math.pow(10, n - 2).toInt
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
      Console.out.println(s"$m fails condition 1.")
      return false
    }
    for (n <- numDigits until 1 by -1) {
      val (left, right) = extractDigits(m, n)
      if (left == right) {
        // Passes condition 2.
        hasDuplicateDigits = true
      }

      if (left > right) {
        // Fails condition 3.
        Console.out.println(s"$m fails condition 3.")
        return false
      }
    }
    hasDuplicateDigits
  }
}

object SecureContainer {
  def main(args: Array[String]): Unit = {
    checkPassword(111111) // Valid
    checkPassword(122345) // Valid
    checkPassword(111123) // Valid
    checkPassword(135679) // Valid
    checkPassword(223450) // Invalid
    checkPassword(123789) // Invalid

    val input = "156218-652527"
    val range = input.split("-")
    val lowerLimit = range(0).toInt
    val upperLimit = range(1).toInt

    val (passwords, numPasswords) = findPasswords(lowerLimit, upperLimit)
    println(s"Number of valid passwords: $numPasswords")
  }

  def checkPassword(password: Int) = {
    val sc = new SecureContainer(6)
    if (sc.checkNumber(password)) {
      println(s"$password is valid.")
    } else {
      println(s"$password is invalid.")
    }
  }

  def findPasswords(lowerLimit: Int, upperLimit: Int) = {
    val sc = new SecureContainer(6)
    val passwords = ListBuffer[Int]()
    for (password <- lowerLimit to upperLimit) {
      if (sc.checkNumber(password)) {
        passwords += password
      }
    }
    (passwords.toList, passwords.length)
  }
}