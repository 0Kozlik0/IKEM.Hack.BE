def create_statistics(scoring, num_positive_contours, num_negative_contours):

    ratio = round(num_positive_contours / num_negative_contours * 100, 2)
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
        "positive_cells": num_positive_contours,
        "negative_cells": num_negative_contours,
        "total_cells": num_positive_contours + num_negative_contours,
        "percentage": ratio,
        "grading": grading
    }
