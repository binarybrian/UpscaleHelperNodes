import base64
import io
import os
import torch
from PIL import Image
import numpy as np

class ImageExport:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "output_directory": ("STRING", {"default": ""}),
                "filename": ("STRING", {"default": "encoded_image.txt"}),
            }
        }

    FUNCTION = "encode_image"
    CATEGORY = "Upscale Nodes/utility"

    def encode_image(self, image: torch.Tensor, output_directory: str, filename: str):
        pil_image = self.tensor_to_pil(image)

        # Convert image to bytes
        buffered = io.BytesIO()
        pil_image.save(buffered, format=pil_image.format)
        image_bytes = buffered.getvalue()

        # Encode bytes to base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        os.makedirs(output_directory, exist_ok=True)
        filepath = os.path.join(output_directory, filename)

        # Ensure the filename ends with .csv
        if not filepath.lower().endswith('.txt'):
            filepath += '.txt'

        # Write base64 string to file
        try:
            with open(filepath, 'wb') as file:
                file.write(image_base64)
            print(f"Encoded image saved to {filepath}")
        except Exception as e:
            print(f"Error saving encoded image file: {str(e)}")

        return ()

    @classmethod
    def IS_CHANGED(cls, image, output_directory, filename):
        return float("NaN")

    def tensor_to_pil(self, img_tensor, batch_index=0):
        # Takes an image in a batch in the form of a tensor of shape [batch_size, channels, height, width]
        # and returns an PIL Image with the corresponding mode deduced by the number of channels

        # Take the image in the batch given by batch_index
        img_tensor = img_tensor[batch_index].unsqueeze(0)
        i = 255. * img_tensor.cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8).squeeze())
        return img