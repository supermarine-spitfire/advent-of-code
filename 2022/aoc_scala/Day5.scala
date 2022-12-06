import scala.io.Source
import scala.collection.mutable.{HashMap, Stack, StringBuilder}

def copyStackMap(stackMap: HashMap[String, Stack[String]]) =
    // Implements a deep copy function for the stack maps.
    val stackMapCopy = HashMap.empty[String, Stack[String]]
    for (label, stack) <- stackMap
    do
        // Use a stack to preserve order of items in stack when transferring them.
        val buffer = Stack[String]()
        while (!stack.isEmpty) {
            buffer.push(stack.pop())
        }
        while (!buffer.isEmpty) {
            val itemToCopy = buffer.pop()
            stack.push(itemToCopy)
            stackMapCopy.getOrElseUpdate(label, Stack[String]()).push(itemToCopy)
        }

    stackMapCopy

def getTopCrates(stackMap: HashMap[String, Stack[String]]) =
    // Returns a string representation of all crates at the top of the stacks.
    val topCrates = new StringBuilder()
    for stack <- stackMap.values
    do
        topCrates.append(stack.pop())

    topCrates.result()

@main def dayFive() =
    println("Advent of Code 2022 Day 5")
    println("-------------------------")
    val fileContents = Source.fromFile("input/day-5-input.txt").getLines().toList
    val dividerIndex = fileContents.indexOf("") // Where initial conditions end and instructions begin.
    var (initialConditions, instructions) = fileContents.splitAt(dividerIndex)
    instructions = instructions.tail    // Strip off empty element.

    // Construct stacks and their initial contents.
    val maxLength = initialConditions.head.length()                 // Guaranteed all lines in section are same length.
    val stackLabels = initialConditions.last.split(" ")
                                            .map(_.trim())
                                            .filter(_.nonEmpty)   // At bottom of section.
    val stackContents = initialConditions.init
    val stackPattern = """\[(\w)\]""".r

    val stacksForSingleMoveCrane = HashMap.empty[String, Stack[String]]
    stackLabels.foreach{ label =>
            stacksForSingleMoveCrane += (label -> Stack[String]())
    }

    for level <- stackContents.reverse
    do
        // Sweep a window of size three across level; this captures the crate if present.
        var curLevelIndex = 0
        var curStackIndex = 0
        while (curLevelIndex <= level.length() - 3) {
            val curStackContents = level.substring(curLevelIndex, curLevelIndex + 3)
            curStackContents match
                case stackPattern(crateLabel) =>    // Crate found; push it onto the current stack.
                    stacksForSingleMoveCrane(stackLabels(curStackIndex)).push(crateLabel)
                case _ => ()                        // No crate found; advance to next stack.

            curStackIndex += 1
            curLevelIndex += 4  // Skip over the space separating each stack.
        }

    val stacksForMultiMoveCrane = copyStackMap(stacksForSingleMoveCrane)

    // Now parse the instructions.
    for instruction <- instructions
    do
        val instructionList = instruction.split(" ")    // All instructions will have 6 elements when split.
        val numCrates = instructionList(1).toInt
        val sourceStack = instructionList(3)
        val targetStack = instructionList(5)

        // Move crates according to instructions.
        for _ <- 0 until numCrates
        do
            stacksForSingleMoveCrane(targetStack).push(
                stacksForSingleMoveCrane(sourceStack).pop()
            )

    println("PART 1")
    println("======")
    println(f"Crates on top: ${getTopCrates(stacksForSingleMoveCrane)}")
    println("======")

    // Parse the instructions assuming crane preserves order of removed crates.
    for instruction <- instructions
    do
        val instructionList = instruction.split(" ")    // All instructions will have 6 elements when split.
        val numCrates = instructionList(1).toInt
        val sourceStack = instructionList(3)
        val targetStack = instructionList(5)

        // Move crates according to instructions.
        // Moving multiple crates whilst preserving order can be modelled by pushing the crates onto
        // a "buffer stack" and then emptying the buffer stack onto the target stack.
        val bufferStack = Stack[String]()
        for _ <- 0 until numCrates
        do
            bufferStack.push(
                stacksForMultiMoveCrane(sourceStack).pop()
            )

        while (!bufferStack.isEmpty) {
            stacksForMultiMoveCrane(targetStack).push(
                bufferStack.pop()
            )
        }

    println("PART 2")
    println("======")
    println(f"Crates on top: ${getTopCrates(stacksForMultiMoveCrane)}")
