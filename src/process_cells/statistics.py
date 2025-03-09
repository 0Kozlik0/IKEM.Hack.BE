def create_statistics(scoring):

    ratio = round(scoring["percent_pos"] / scoring["num_total"] * 100, 2)
    print("ratio: ", ratio)

    # Calculate grading
    if ratio <= 3:
        grading = "Grade 1"
    elif ratio > 3 and ratio <= 20:
        grading = "Grade 2"
    elif ratio > 20:
        grading = "Grade 3"
    else:
        grading = "Non representative area"

    return {
        "positive_cells": scoring["num_pos"],
        "negative_cells": scoring["num_neg"],
        "total_cells": scoring["num_total"],
        "percentage": scoring["percent_pos"],
        "grading": grading
    }
