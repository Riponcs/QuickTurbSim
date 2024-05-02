# Atmospheric Turbulence Image Generation README

## Overview
This code simulates atmospheric turbulence effects on images. It utilizes Perlin noise for creating turbulence and Gaussian blur to mimic atmospheric disturbance. This README file details the configuration parameters and how to tune them for different effects.

## Configuration Parameters

### General Configuration (Ideal for 512x512 Images)
- `TurbulenceStrength`: Controls the intensity of the turbulence. Higher values result in more significant image distortion. Recommended range: 1-10.
- `sigma`: Determines the amount of blur applied after tilt. It controls the intensity of the blur effect. Ideally, it should be between 5 to 20 for the best results. Usually, `sigma` value is close to `TurbulenceStrength` value.
- `TurbScale`: Turbulence scale relative to the image size. Smaller values create larger, more noticeable turbulence patterns. Recommended range: 1/128 to 1/32.
- `temp_Scale`: Temporal scale, affecting the variation over time (for videos). Setting this to 0 results in no changes to frames in tilt, while a lower number like 1 simulates a fast frame rate camera effect. Recommended range: 0-30. Don't worry about it when generating images/not videos `('num_frames_in_video': 1)`.
- `input_img`: Path to the input image. Ensure this is set to the correct image file path.
- `SaveDir`: Directory where the output images/videos will be saved. Ensure the directory exists or that the code can create it.
- `doResize`: Set to `True` to resize the input image to the specified dimensions. Set to `False` to use the original image size.
- `height`, `width`: Desired height and width of the output images if `doResize` is `True`. We may need to tune those parameter for different input sizes.
- `num_frames_in_video`: Number of frames per video. Higher numbers result in longer videos. Recommended for single images: 1.
- `num_videos`: Number of different turbulence simulations to generate. This can be unlimited, but keep in mind the computational resources required.

### Advanced Configuration (No Tuning Required)
- `levels`: Number of levels in Perlin noise generation. Higher levels result in more detailed turbulence patterns. Recommended range: 6-10.

## Usage Instructions
1. Set the `input_img` to the path of your desired input image.
2. Adjust the general configuration parameters according to the desired output.
3. For advanced users, tweak the advanced configuration parameters to fine-tune the simulation.
4. Run the script to generate the turbulence-affected images or videos.
5. Check the `SaveDir` directory for the output. Images will be saved as frame_videoNumber_frameNumber.png

## Examples

- **Mild Turbulence**: Slightly turbulent image (`TurbulenceStrength`=3, `sigma`=5, `TurbScale`=1/64, `num_frames_in_video`=1).
- **High-Speed Camera Effect**: Fast-moving turbulence, like high-speed camera footage (`TurbulenceStrength`=7, `sigma`=10, `TurbScale`=1/128, `temp_Scale`=1, `num_frames_in_video`=10).
- **Intense Atmospheric Disturbance**: Strong atmospheric turbulence for extreme weather simulation (`TurbulenceStrength`=10, `sigma`=15, `TurbScale`=1/50, `temp_Scale`=20, `num_frames_in_video`=20).
