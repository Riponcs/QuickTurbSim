import numpy as np
import cv2

def create_and_blend_blurred_versions(image, noise_map, max_sigma=11, num_levels=11):
    # Create blurred versions of the image
    blurred_images = [image]
    for i in range(1, num_levels):
        sigma = i**0.5 * max_sigma / num_levels
        blurred_image = cv2.GaussianBlur(blurred_images[-1], (0, 0), sigma)
        blurred_images.append(blurred_image)

    # Normalize noise map to range [0, 1] and then scale to indices
    normalized_noise_map = (noise_map - noise_map.min()) / (noise_map.max() - noise_map.min())
    indices = (normalized_noise_map * (len(blurred_images) - 1)).astype(int)

    # Stack all blurred images along a new dimension
    stacked_images = np.stack(blurred_images, axis=-1)

    # Create meshgrid for x and y coordinates
    x_coords, y_coords = np.meshgrid(np.arange(noise_map.shape[1]), np.arange(noise_map.shape[0]))

    # Use advanced indexing to select the correct blur level for each pixel
    final_image = stacked_images[y_coords, x_coords, :, indices[y_coords, x_coords]]

    return final_image