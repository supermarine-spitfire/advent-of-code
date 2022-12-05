import scala.collection.Map
import scala.io.Source

@main def dayFour() =
    println("Advent of Code 2022 Day 4")
    println("-------------------------")
    val sectionAssignmentPairs = Source.fromFile("input/day-4-input.txt")
                                       .getLines()
                                       .toList
                                       .map(_.split(","))                   // Get each section assignment.

    var numFullyContainedPairs = 0
    var numOverlappingPairs = 0
    for sectionPair <- sectionAssignmentPairs
    do
        // Get lower and upper limits of each section assignment.
        val section1Limits = sectionPair(0).split("-").map(_.toInt)
        val section2Limits = sectionPair(1).split("-").map(_.toInt)

        val section1LowerLimit = section1Limits(0)
        val section1UpperLimit = section1Limits(1)
        val section2LowerLimit = section2Limits(0)
        val section2UpperLimit = section2Limits(1)

        // Find section assignment ranges that completely overlap each other.
        // Case 1: Section 1 fully encloses Section 2.
        // Case 2: Section 2 fully encloses Section 1.
        // Case 3: Section 1 and Section 2 share same start but Section 1 ends before Section 2.
        // Case 4: Section 1 and Section 2 share same start but Section 2 ends before Section 1.
        // Case 5: Section 1 and Section 2 share same end but Section 1 starts before Section 2.
        // Case 6: Section 1 and Section 2 share same end but Section 2 starts before Section 1.
        // Case 7: Section 1 and Section 2 are identical ranges.
        if (
               (section1LowerLimit < section2LowerLimit && section1UpperLimit > section2UpperLimit)
            || (section2LowerLimit < section1LowerLimit && section2UpperLimit > section1UpperLimit)
            || (section2LowerLimit == section1LowerLimit && section1UpperLimit < section2UpperLimit)
            || (section2LowerLimit == section1LowerLimit && section2UpperLimit < section1UpperLimit)
            || (section2LowerLimit > section1LowerLimit && section2UpperLimit == section1UpperLimit)
            || (section2LowerLimit < section1LowerLimit && section2UpperLimit == section1UpperLimit)
            || (section2LowerLimit == section1LowerLimit && section2UpperLimit == section1UpperLimit)
        ) {
            numFullyContainedPairs += 1
        }
            // Find section assignment ranges that overlap in some way.
            // Case 1: Section 1 and Section 2 are identical ranges.
            // Case 2: Section 1 fully encloses Section 2.
            // Case 3: Section 2 fully encloses Section 1.
            // Case 4: Section 1 and Section 2 share same start.
            // Case 5: Section 1 and Section 2 share same end.
            // Case 6: Section 1 starts inside Section 2.
            // Case 7: Section 2 starts inside Section 1.
            // Case 8: Section 1 ends inside Section 2.
            // Case 9: Section 2 ends inside Section 1.
        if(
               (section2LowerLimit == section1LowerLimit && section2UpperLimit == section1UpperLimit)
            || (section1LowerLimit < section2LowerLimit && section1UpperLimit > section2UpperLimit)
            || (section2LowerLimit < section1LowerLimit && section2UpperLimit > section1UpperLimit)
            || (section1LowerLimit == section2LowerLimit)
            || (section1UpperLimit == section2UpperLimit)
            || (section1LowerLimit >= section2LowerLimit && section1LowerLimit <= section2UpperLimit)
            || (section2LowerLimit >= section1LowerLimit && section2LowerLimit <= section1UpperLimit)
            || (section1UpperLimit >= section2LowerLimit && section1UpperLimit <= section2UpperLimit)
            || (section2UpperLimit >= section1LowerLimit && section2UpperLimit <= section1UpperLimit)
        ) {
            numOverlappingPairs += 1
        }

    println("PART 1")
    println("======")
    println(s"Number of fully contained range assignment pairs: $numFullyContainedPairs")
    println("======")


    println("PART 2")
    println("======")
    println(s"Number of overlapping range assignment pairs: $numOverlappingPairs")
