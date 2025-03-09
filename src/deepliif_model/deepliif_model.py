import os
import json
import base64
from io import BytesIO

import requests
from PIL import Image


def b64_to_pil(b):
    return Image.open(BytesIO(base64.b64decode(b.encode())))


def predict_deepliif(img_dir, filename):
    images_dir = img_dir

    res = requests.post(
        url='https://deepliif.org/api/infer',
        files={
            'img': open(f'{images_dir}/{filename}', 'rb')
        },
        # optional param that can be 10x, 20x (default) or 40x
        params={
            'resolution': '20x'
        }
    )

    data = res.json()

    segmentation_mask_path = None
    
    for name, img in data['images'].items():
        output_filepath = f'{images_dir}/{os.path.splitext(filename)[0]}_{name}.png'
        with open(output_filepath, 'wb') as f:
            b64_to_pil(img).save(f, format='PNG')
        
        # Store the path to the segmentation mask
        if name == 'SegOverlaid':
            segmentation_mask_path = output_filepath

    print(json.dumps(data['scoring'], indent=2))
    
    return segmentation_mask_path, data['scoring']