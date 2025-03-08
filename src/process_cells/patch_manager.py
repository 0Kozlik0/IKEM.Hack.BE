import numpy as np


def cut_image_to_patches(image, parameters, patch_size):
    """
        Cut image to specific same size patches

        :param image: Image of ROI
        :param parameters: Information about RIO (x, y, width, height)
        :param patch_size: Specific size of created patches
        :return: Numpy array of same size patches created from tiff
    """

    # Cut image into the same size patches
    patches = []
    min_y, min_x = 0, 0
    max_y, max_x = patch_size, patch_size

    # Calculate final number of patches
    columns = np.ceil(parameters[3] / patch_size)
    rows = np.ceil(parameters[2] / patch_size)
    n_final_patches = rows * columns

    x_shift = 0
    y_shift = 0
    end_x_shift = 0
    end_y_shift = 0

    for i in range(int(n_final_patches)):

        # Check for last patch in row
        if x_shift == rows-1:
            end_x_shift = patch_size - (parameters[2] - (x_shift*patch_size))

        # Check for last patch in column
        if y_shift == columns-1:
            end_y_shift = patch_size - (parameters[3] - (y_shift*patch_size)) 

        
        y_min_new = int((min_y + (y_shift * patch_size)) - end_y_shift)
        y_max_new = int((max_y + (y_shift * patch_size)) - end_y_shift)
        x_min_new = int((min_x + (x_shift * patch_size)) - end_x_shift)
        x_max_new = int((max_x + (x_shift * patch_size)) - end_x_shift)

        i_patch = image[y_min_new:y_max_new, x_min_new:x_max_new]
        patches.append(i_patch)
        x_shift = x_shift + 1

        # Shift to next row
        if x_shift == rows:
            x_shift = 0
            y_shift = y_shift + 1
            end_x_shift = 0

    return patches


def merge_patches(masks, original_size, patch_size):
    """
        Merge mask patches to one big area mask

        :param masks: .npy array of masks
        :param original_size: (x, y) height and width of final area patch
        :param patch_size: Size of mask patch
        :return: Merged area mask (.npy)
    """
    shift = 0
    new_img = 0
    rows = np.ceil(original_size[0] / patch_size)
    columns = np.ceil(original_size[1] / patch_size)

    for j in range(int(rows)):
        new_line = None

        for i in range(int(columns)):
            # First patch of last row
            if i == 0 and j == rows-1:
                new_line = masks[i + shift]
                x_min_line = int(patch_size - (original_size[0] - j * patch_size))
                print("x_min_line: ", x_min_line)
                print("patch_size: ", patch_size)
                print("new_line ", new_line)
                if isinstance(new_line, tuple):
                    new_line = new_line[0][x_min_line:patch_size, 0:patch_size]
                else:
                    new_line = new_line[x_min_line:patch_size, 0:patch_size]
                continue
            # First patch of row
            if i == 0:
                new_line = masks[i + shift]
                continue
            # End of the column and row
            if i == columns-1 and j == rows-1:
                end_column_patch = masks[i + shift]
                x_min_column = int(patch_size - (original_size[0] - j * patch_size))
                y_min_column = int(patch_size - (original_size[1] - i * patch_size))
                end_column_patch = end_column_patch[x_min_column:patch_size, y_min_column:patch_size]
                new_line = np.hstack((new_line, end_column_patch))
                continue
            # End of the columns
            if j == rows-1:
                end_column_patch = masks[i + shift]
                x_min_column = int(patch_size - (original_size[0] - j * patch_size))
                end_column_patch = end_column_patch[x_min_column:patch_size, 0:patch_size]
                new_line = np.hstack((new_line, end_column_patch))
                continue
            # End of the row
            if i == columns-1:
                end_column_patch = masks[i + shift]
                y_min_column = int(patch_size-(original_size[1]-i*patch_size))
                end_column_patch = end_column_patch[0:patch_size, y_min_column:patch_size]
                new_line = np.hstack((new_line, end_column_patch))
                continue
            new_line = np.hstack((new_line, masks[i + shift]))

        shift = shift + int(columns)
        if j == 0:
            new_img = new_line
        else:
            new_img = np.vstack((new_img, new_line))

    return new_img