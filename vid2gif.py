import os
import sys
import subprocess
from tqdm import tqdm
import ffmpeg

def validate_inputs(file_path):
    """Validates the video file."""
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)

def run_with_progress(cmd, duration, desc):
    """Runs a command with a progress bar."""
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    pbar = tqdm(total=duration, unit='s', desc=desc)

    last_time = 0
    while True:
        line = process.stdout.readline()
        if not line:
            if process.poll() is not None:
                break
            continue
        if 'out_time_ms' in line:
            try:
                time_ms = int(line.strip().split('=')[1])
                current_time = time_ms / 1e6
                pbar.update(current_time - last_time)
                last_time = current_time
            except ValueError:
                # Skip if `out_time_ms` is "N/A"
                continue

    process.wait()
    pbar.close()
    if process.returncode != 0:
        print(f"Error during {desc.lower()}.")
        sys.exit(1)

def trim_video(file_path, start_time=0, end_time=0):
    """Trims the video based on the specified times."""
    output_path = os.path.splitext(file_path)[0] + "_trimmed.mp4"
    
    try:
        probe = ffmpeg.probe(file_path)
        duration = float(probe['format']['duration'])

        trim_start = start_time
        trim_end = duration - end_time
        if trim_start >= trim_end:
            print("Error: Invalid trim times. Check start and end times.")
            sys.exit(1)

        # Build ffmpeg command for trimming
        cmd = [
            'ffmpeg',
            '-i', file_path,
            '-ss', str(trim_start),
            '-to', str(trim_end),
            '-c', 'copy',
            '-y', output_path,
            '-progress', 'pipe:1',
            '-loglevel', 'quiet'
        ]

        # Run with progress bar
        run_with_progress(cmd, trim_end - trim_start, desc='Trimming Video')
        print(f"Trimmed video saved as '{output_path}'")
        return output_path

    except ffmpeg.Error as e:
        print("Error during video trimming:", e)
        sys.exit(1)

def convert_to_gif(video_path):
    """Converts a video to GIF with a progress bar."""
    output_path = os.path.splitext(video_path)[0] + ".gif"
    
    try:
        probe = ffmpeg.probe(video_path)
        duration = float(probe['format']['duration'])

        # Build ffmpeg command for GIF conversion
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', 'fps=24',
            '-loop', '0',
            '-y', output_path,
            '-progress', 'pipe:1',
            '-loglevel', 'quiet'
        ]

        # Run with progress bar
        run_with_progress(cmd, duration, desc='Converting to GIF')
        print(f"GIF saved as '{output_path}'")
        return output_path

    except Exception as e:
        print("Error during GIF conversion:", e)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: python vid2gif.py <video_path> [<start_seconds> <end_seconds>]")
        sys.exit(1)

    video_path = sys.argv[1]
    start_seconds = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    end_seconds = int(sys.argv[3]) if len(sys.argv) > 3 else 0

    validate_inputs(video_path)

    if start_seconds > 0 or end_seconds > 0:
        trimmed_video = trim_video(video_path, start_seconds, end_seconds)
    else:
        trimmed_video = video_path

    convert_to_gif(trimmed_video)

