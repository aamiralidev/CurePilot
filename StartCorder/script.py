import cv2
import numpy as np
import sys
import os
from tqdm import tqdm

def mse(imageA, imageB):
    # Mean Squared Error between the two images
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def find_matching_frames(video_path, screenshots_dir, chunk_size=500):
    # Check if CUDA is available
    if cv2.cuda.getCudaEnabledDeviceCount() == 0:
        print("CUDA not available, defaulting to CPU. Performance may be degraded.")
        return

    # List all images in the screenshots directory
    screenshot_paths = [os.path.join(screenshots_dir, f) for f in os.listdir(screenshots_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not screenshot_paths:
        print(f"No image files found in {screenshots_dir}")
        return

    # Load screenshots to GPU
    screenshots = [cv2.cuda_GpuMat(cv2.imread(path)) for path in screenshot_paths if cv2.imread(path) is not None]

    if len(screenshots) == 0:
        print(f"Error reading screenshot files in {screenshots_dir}")
        return

    video = cv2.VideoCapture(video_path)
    print(screenshots)
    if not video.isOpened():
        print(f"Error opening video file: {video_path}")
        return

    frame_rate = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    best_matches = [None] * len(screenshots)
    best_frame_numbers = [-1] * len(screenshots)
    min_mses = [float('inf')] * len(screenshots)

    pbar = tqdm(total=total_frames, desc="Processing Video", unit="frame")

    for start_frame in range(0, total_frames, chunk_size):
        video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        for frame_idx in range(chunk_size):
            ret, frame = video.read()
            if not ret:
                break

            frame_gpu = cv2.cuda_GpuMat()
            frame_gpu.upload(frame)

            for i, screenshot_gpu in enumerate(screenshots):
                # Resize frame to match screenshot size
                frame_resized_gpu = cv2.cuda.resize(frame_gpu, (screenshot_gpu.cols, screenshot_gpu.rows))

                # Download frame from GPU for MSE calculation
                frame_resized = frame_resized_gpu.download()
                screenshot = screenshot_gpu.download()

                error = mse(screenshot, frame_resized)
                if error < min_mses[i]:
                    min_mses[i] = error
                    best_matches[i] = frame
                    best_frame_numbers[i] = start_frame + frame_idx

            pbar.update(1)

    pbar.close()
    video.release()
    
    timecodes = [num / frame_rate for num in best_frame_numbers]
    return best_matches, best_frame_numbers, timecodes, screenshot_paths

def format_time(seconds):
    # Calculate hours, minutes, and remaining seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Calculate milliseconds
    milliseconds = int((seconds - int(seconds)) * 1000)
    
    # Format the time as hh:mm:ss:ms
    formatted_time = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}:{milliseconds:03d}"
    
    return formatted_time

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <video_path> <screenshots_directory>")
        sys.exit(1)

    video_path = sys.argv[1]
    screenshots_dir = sys.argv[2]

    result = find_matching_frames(video_path, screenshots_dir)
    if result is None:
        print("An error occurred during processing.")
        sys.exit(1)

    best_matches, best_frame_numbers, timecodes, screenshot_paths = result

    for screenshot_path, best_frame_number, timecode in zip(screenshot_paths, best_frame_numbers, timecodes):
        if best_frame_number != -1:
            # Format the timecode in hh:mm:ss:ms
            formatted_timecode = format_time(timecode)
            print(f"Best match for {os.path.basename(screenshot_path)} found at frame number: {best_frame_number} with timecode: {formatted_timecode}")
        else:
            print(f"No matching frame found for {os.path.basename(screenshot_path)}.")

if __name__ == "__main__":
    main()

