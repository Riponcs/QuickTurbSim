import numpy as np
import cv2
from noise import snoise3
from einops import rearrange
import os
from tqdm import tqdm
from tiltblur import create_and_blend_blurred_versions
import time

# Configuration Parameters
config = {
    'TurbulenceStrength': 10,   # Turbulence Strength
    'sigma': 12,                # Maximum blur strength
    'TurbScale': 1 / 64,        # Turbulence Scale compared to image size
    'temp_Scale': 2,            # Temporal Changes
    'input_img': 'input/stripe.jpg',
    'SaveDir': 'Simulated_Images/',
    'doResize': True,
    'height': 512,
    'width': 512,
    'num_frames_in_video': 10,  # Number of frames (depth) for simulation
    'num_videos': 1,            # Number of videos to generate
    'make_fast': True,          # If True, will use a faster but less accurate method
}

if __name__ == "__main__":
    start = time.time()
    for i in range(config['num_videos']):
        imgPath = config['input_img']  # Replace with your image path
        output_dir = config['SaveDir']
        os.makedirs(output_dir, exist_ok=True)

        # Read image and resize to desired dimensions
        img = cv2.imread(imgPath)[..., ::-1]

        if config['doResize'] and (img.shape[0] != config['height'] or img.shape[1] != config['width']):
            img = cv2.resize(img, (config['height'], config['width']))

        # Turbulence Simulation Parameters
        levels = 8
        width, height = img.shape[0], img.shape[1]
        depth = config['num_frames_in_video']
        base_frequency = config['TurbScale']
        temporal_varStrength = config['temp_Scale']
        displacement_factor = config['TurbulenceStrength']

        # Generate Turbulence
        x_coords, y_coords, z_coords = np.meshgrid(np.arange(width), np.arange(height), np.arange(depth), indexing='ij')
        x_normalized, y_normalized, z_normalized = x_coords * base_frequency, y_coords * base_frequency, z_coords * base_frequency * temporal_varStrength

        # We create Seperate 3D Perlin Noise Maps for x and y displacement and Blur, It's possible to combine them into one map to make it about faster
        if config['make_fast']:
            x1, x2, y1, y2 = np.random.randint(0, 500000), np.random.randint(0, 500000), np.random.randint(0, 500000), np.random.randint(0, 500000)

            noise_volume_x = np.vectorize(snoise3)(x_normalized + x1, y_normalized + y1, z_normalized, octaves=levels)
            noise_volume_y = np.flip(noise_volume_x, (0,2))
            blur_volume_xy = (noise_volume_x+noise_volume_y)/2
        else:
            x1, x2, y1, y2 = np.random.randint(0, 500000), np.random.randint(0, 500000), np.random.randint(0, 500000), np.random.randint(0, 500000)
            noise_volume_x = np.vectorize(snoise3)(x_normalized + x1, y_normalized + y1, z_normalized, octaves=levels)
            
            x1, x2, y1, y2 = np.random.randint(0, 500000), np.random.randint(0, 500000), np.random.randint(0, 500000), np.random.randint(0, 500000)
            noise_volume_y = np.vectorize(snoise3)(x_normalized + x2, y_normalized + y2, z_normalized, octaves=levels)

            
            x1, x2, y1, y2 = np.random.randint(0, 500000), np.random.randint(0, 500000), np.random.randint(0, 500000), np.random.randint(0, 500000)
            blur_volume_xy = np.vectorize(snoise3)(x_normalized + x2, y_normalized + y2, z_normalized, octaves=levels)

        # Apply displacement to image
        ImageVolume = np.zeros((height, width, 3, depth))
        for z in tqdm(range(depth)):
            displacement_x = noise_volume_x[:, :, z] * displacement_factor
            displacement_y = noise_volume_y[:, :, z] * displacement_factor

            distorted_x = np.clip(np.arange(width) + displacement_x, 0, width - 1).astype(int)
            distorted_y = np.clip(np.arange(height)[:, None] + displacement_y, 0, height - 1).astype(int)

            ImageVolume[:,:,:,z] = img[distorted_y, distorted_x]

        # Apply Gaussian Adaptive Blur based on Perlin Noise
        BlurredImageVolume = np.zeros((height, width, 3, depth))
        for z in tqdm(range(depth)):
            frame = ImageVolume[:,:,:,z]
            Noise2D = blur_volume_xy[:,:,z]
            final_image = create_and_blend_blurred_versions(frame, Noise2D, max_sigma=config['sigma'], num_levels=20)
            BlurredImageVolume[:,:,:,z] = final_image
        
        # Iterate through the depth dimension of BlurredImageVolume to save each frame
        for z in tqdm(range(BlurredImageVolume.shape[3])):
            frame = BlurredImageVolume[:, :, :, z]
            frame_bgr = cv2.cvtColor(frame.astype('float32'), cv2.COLOR_RGB2BGR)
            filename = f'{output_dir}/frame_{str(i).zfill(5)}_{str(z).zfill(4)}.png'
            cv2.imwrite(filename, frame_bgr)
        
    print(f'Took {time.time()-start:.2f}s to generate {config["num_videos"]} videos with {config["num_frames_in_video"]} frames each. Resolution {config["height"]}x{config["width"]}')
