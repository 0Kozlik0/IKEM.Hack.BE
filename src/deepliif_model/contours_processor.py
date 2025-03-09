import cv2
import numpy as np

def extract_contours(path):
    # image_path = "test/im2_SegOverlaid.png"  # Update with your actual path
    img = cv2.imread(path)

    # Convert from BGR to RGB (OpenCV loads as BGR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Create masks for red and blue colors
    # Define color ranges (you may need to adjust these based on your specific image)
    lower_red = np.array([180, 0, 0])
    upper_red = np.array([255, 100, 100])

    lower_blue = np.array([0, 0, 180])
    upper_blue = np.array([100, 100, 255])

    # Create masks
    red_mask = cv2.inRange(img_rgb, lower_red, upper_red)
    blue_mask = cv2.inRange(img_rgb, lower_blue, upper_blue)

    # Create blank images for the contours
    red_contours = np.zeros_like(img_rgb)
    blue_contours = np.zeros_like(img_rgb)

    # Apply the masks to get only the contours
    red_contours[red_mask > 0] = [255, 0, 0]  # Red color
    blue_contours[blue_mask > 0] = [0, 0, 255]  # Blue color

    return red_contours, blue_contours


def create_mask(contours_image, color):
    gray = cv2.cvtColor(contours_image, cv2.COLOR_BGR2GRAY)

    # Find contours
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a blank image to draw filled contours
    filled_contours = np.zeros_like(contours_image)

    # Set minimum contour area threshold (adjust as needed)
    min_contour_area = 70  # Filter out contours smaller than this area

    # Fill and filter contours
    filtered_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area >= min_contour_area:
            filtered_contours.append(contour)
            cv2.drawContours(filled_contours, [contour], -1, color, -1)  # -1 thickness means fill

    num_contours = len(filtered_contours)

    return filled_contours, num_contours


def merge_pred_masks(negative_mask, positive_mask):
    # Create a blank binary mask with zeros (background)
    binary_mask = np.zeros((negative_mask.shape[0], negative_mask.shape[1]), dtype=np.uint8)
    
    # Set positive cells to 1
    # Extract red channel from positive_mask and create binary mask
    positive_binary = (positive_mask[:,:,0] > 0).astype(np.uint8)
    binary_mask[positive_binary > 0] = 1
    
    # Set negative cells to 2
    # Extract blue channel from negative_mask and create binary mask
    negative_binary = (negative_mask[:,:,2] > 0).astype(np.uint8)
    binary_mask[negative_binary > 0] = 2
    
    return binary_mask
