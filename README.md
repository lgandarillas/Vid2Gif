# Vid2Gif

Vid2Gif is a command-line tool designed to convert video files into GIFs, offering a lightweight and efficient solution for creating animations.

## Installation

1. Clone this repository
   ```bash
   git clone https://github.com/yourusername/Vid2Gif.git
   cd Vid2Gif
    ```
2. Create a virtual environment and activate it
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/MacOS
    venv\Scripts\activate     # Windows
    ```
3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

## Usage
Run the script with the following syntax:
    ```bash
    python vid2gif.py <video_path> [<start_seconds> <end_seconds>]
    ```
- `<video_path>`: Path to the video file (supports common formats like MP4, MKV, AVI, etc.).
- `<start_seconds>`: (Optional) Number of seconds to trim from the start of the video.
- `<end_seconds>`: (Optional) Number of seconds to trim from the end of the video.
<br><br>

### Examples
1. Convert a video to a GIF without trimming:
```bash
python vid2gif.py myvideo.mp4
```
2. Convert a video to a GIF, trimming 5 seconds from the start and 10 seconds from the end:
```bash
python vid2gif.py myvideo.mp4 5 10
```

## Output
- A trimmed video is saved in the same directory as the original video, with `_trimmed` appended to the filename. Example: `myvideo_trimmed.mp4`
- A high-quality GIF is generated from the trimmed video. Example: `myvideo_trimmed.gif`

### Requirements
Python 3.7 or higher
ffmpeg installed on your system
