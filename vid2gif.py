import os
import sys
import ffmpeg

def validate_inputs(file_path, start_time, end_time):
    """Validates the input parameters."""
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)

    if not start_time.isdigit() or not end_time.isdigit():
        print("Error: Start time and end time must be positive integers.")
        sys.exit(1)

    start_time = int(start_time)
    end_time = int(end_time)

    if start_time < 0 or end_time < 0:
        print("Error: Times must be non-negative.")
        sys.exit(1)

    return start_time, end_time


def trim_video(file_path, start_time, end_time):
    """Trims the video based on the specified times."""
    output_path = os.path.splitext(file_path)[0] + "_trimmed.mp4"
    
    try:
        # Get the video duration
        probe = ffmpeg.probe(file_path)
        duration = float(probe['format']['duration'])

        # Calculate new duration
        trim_start = start_time
        trim_end = duration - end_time
        if trim_start >= trim_end:
            print("Error: Invalid trim times. Check start and end times.")
            sys.exit(1)

        # Trim the video
        ffmpeg.input(file_path, ss=trim_start, to=trim_end).output(output_path).run(overwrite_output=True)
        print(f"Trimmed video saved as '{output_path}'.")
        return output_path

    except ffmpeg.Error as e:
        print("Error during video trimming:", e)
        sys.exit(1)


def convert_to_gif(video_path):
    """Converts a trimmed video to GIF."""
    output_path = os.path.splitext(video_path)[0] + ".gif"
    
    try:
        ffmpeg.input(video_path).output(output_path, vf="fps=24", loop=0).run(overwrite_output=True)
        print(f"GIF saved as '{output_path}'.")
        return output_path

    except ffmpeg.Error as e:
        print("Error during GIF conversion:", e)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python vid2gif.py <video_path> <start_seconds> <end_seconds>")
        sys.exit(1)

    video_path = sys.argv[1]
    start_seconds = sys.argv[2]
    end_seconds = sys.argv[3]

    # Validate inputs
    start_seconds, end_seconds = validate_inputs(video_path, start_seconds, end_seconds)

    # Trim video
    trimmed_video = trim_video(video_path, start_seconds, end_seconds)

    # Convert to GIF
    convert_to_gif(trimmed_video)
