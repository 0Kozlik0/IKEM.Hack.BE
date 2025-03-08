import torch
import cv2
import numpy as np
from torchvision import transforms
from model.model import DeepLabV3  # Ensure this matches the training model definition

# Load Trained Model
def load_model(model_path, device):
    model = DeepLabV3(num_classes=4).to(device)  # Changed to 3 classes
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    return model

# Preprocess Image
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (256, 256))
    transform = transforms.ToTensor()
    image = transform(image).unsqueeze(0)  # Add batch dimension
    return image

# Perform Inference
def infer_image(model, image_tensor, device):
    image_tensor = image_tensor.to(device)
    with torch.no_grad():
        output = model(image_tensor)
    
    # For multi-class segmentation, get the class with highest probability
    output = torch.argmax(output, dim=1).cpu().squeeze().numpy()
    
    # Convert to visualization format (optional)
    # Create a colored mask where different colors represent different classes
    colored_mask = np.zeros((output.shape[0], output.shape[1], 3), dtype=np.uint8)
    # Background (class 0) - black
    # Positive cells (class 1) - green
    colored_mask[output == 1] = [0, 255, 0]
    # Negative cells (class 2) - red
    colored_mask[output == 2] = [0, 0, 255]
    
    return output, colored_mask

# Save Output Mask
def save_mask(mask, output_path, colored_mask=None, colored_output_path=None):
    # Save class index mask (0, 1, 2)
    cv2.imwrite(output_path, mask.astype(np.uint8))
    
    # Save colored visualization if provided
    if colored_mask is not None and colored_output_path is not None:
        cv2.imwrite(colored_output_path, colored_mask)

# Main Execution
def predict_patch_file(image_path, model_path, output_path, colored_output_path=None):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = load_model(model_path, device)
    image_tensor = preprocess_image(image_path)
    mask, colored_mask = infer_image(model, image_tensor, device)
    
    if colored_output_path:
        save_mask(mask, output_path, colored_mask, colored_output_path)
        print(f"Segmentation mask saved at {output_path}")
        print(f"Colored visualization saved at {colored_output_path}")
    else:
        save_mask(mask, output_path)
        print(f"Segmentation mask saved at {output_path}")

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (256, 256))
    transform = transforms.ToTensor()
    image = transform(image).unsqueeze(0)  # Add batch dimension
    return image

def preprocess_npy(npy_array):
    # Resize the numpy array to match model input size
    resized_array = cv2.resize(npy_array, (256, 256))
    
    # Convert to tensor and add batch dimension
    transform = transforms.ToTensor()
    tensor = transform(resized_array).unsqueeze(0)
    
    return tensor

def predict_patch_npy(npy_image):
    
    model_path = "best_model.pth"
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = preprocess_npy(model_path, device)
    image_tensor = preprocess_image(npy_image)
    mask = infer_image(model, image_tensor, device)

    return mask

def process_npy_images(npy_images):

    masks = np.array([])
    for npy_image in npy_images:
        mask = predict_patch_npy(npy_image)
        masks = np.append(masks, mask)

    return masks
