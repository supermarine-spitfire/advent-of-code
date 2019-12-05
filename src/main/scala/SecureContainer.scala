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
   * 2. Exactly two contiguous digits are identical.
   * 3. From left to right, the number's digits are monotonically increasing.
   */
  def checkNumber(m: Int): Boolean = {
    if (m.toString.length != numDigits) {
      // Fails condition 1.
      return false
    }

    var previousDigit = m % math.pow(10, numDigits).toInt /
                        math.pow(10, numDigits - 1).toInt
    val flag = Int.MaxValue // Denotes a non-duplicate digit.
    val numOccurrences = collection.mutable.HashMap[Int, Int](
      0 -> 0,
      1 -> 0,
      2 -> 0,
      3 -> 0,
      4 -> 0,
      5 -> 0,
      6 -> 0,
      7 -> 0,
      8 -> 0,
      9 -> 0
    )

    for (n <- numDigits until 1 by -1) {
      val (left, right) = extractDigits(m, n)

      if (left == right) {
        if (n == numDigits) {
          // At the beginning of the number.
          numOccurrences(previousDigit) = 2
        } else if (n == 2) {
          // At the end of the number.
          if (previousDigit == flag) {
            // Encountered two identical digits for the first time.
            numOccurrences(left) = 2
          }
          else if (numOccurrences(previousDigit) == 0) {
            // Encountered two identical digits.
            numOccurrences(previousDigit) = 2
          } else {
            // Encountered three or more identical digits.
            numOccurrences(previousDigit) += 1
          }
        } else if (right == previousDigit) {
          // In the middle of the number.
          // Encountered three or more identical digits.
          numOccurrences(previousDigit) += 1
        } else {
          // In the middle of the number.
          // Encountered two identical digits.
          previousDigit = left
          numOccurrences(previousDigit) = 2
        }
      } else {
        // Ran into a different digit.
        previousDigit = flag
      }

      if (left > right) {
        // Fails condition 3.
        return false
      }
    }

    // Check if condition 2 is satisfied.
    numOccurrences.valuesIterator.contains(2)
  }
}

object SecureContainer {
  def main(args: Array[String]): Unit = {
    checkPassword(122345) // Valid
    checkPassword(112233) // Valid
    checkPassword(111122) // Valid
    checkPassword(123444) // Invalid
    checkPassword(111111) // Invalid
    checkPassword(111123) // Invalid
    checkPassword(223450) // Invalid
    checkPassword(123789) // Invalid

    // All valid
    checkPassword(778888)
    checkPassword(677888)
    checkPassword(567789)
    checkPassword(456778)
    checkPassword(345677)

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
    println()
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