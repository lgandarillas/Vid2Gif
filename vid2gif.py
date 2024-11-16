import os
import sys
import ffmpeg

def validate_inputs(file_path):
    """Validates the video file."""
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)

def trim_video(file_path, start_time=0, end_time=0):
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
    """Converts a video to GIF."""
    output_path = os.path.splitext(video_path)[0] + ".gif"
    
    try:
        ffmpeg.input(video_path).output(output_path, vf="fps=24", loop=0).run(overwrite_output=True)
        print(f"GIF saved as '{output_path}'.")
        return output_path

    except ffmpeg.Error as e:
        print("Error during GIF conversion:", e)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: python vid2gif.py <video_path> [<start_seconds> <end_seconds>]")
        sys.exit(1)

    video_path = sys.argv[1]
    start_seconds = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    end_seconds = int(sys.argv[3]) if len(sys.argv) > 3 else 0

    # Validate video file
    validate_inputs(video_path)

    if start_seconds > 0 or end_seconds > 0:
        # Trim video if times are provided
        trimmed_video = trim_video(video_path, start_seconds, end_seconds)
    else:
        # Use the original video if no times are provided
        trimmed_video = video_path

    # Convert to GIF
    convert_to_gif(trimmed_video)

