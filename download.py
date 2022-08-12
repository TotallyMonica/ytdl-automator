import youtube_dl
import sys

version = "0.1"
help = "Usage: " + sys.argv[0] +  " <filename>"

def download(link):
    ydl_opts = {
        'format': 'mp4'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as yt_dl:
        yt_dl.download([link])

if __name__ == "__main__":
    # Check if there is an argument provided
    if len(sys.argv) != 1:
        # There are, so determine if the argument is not a file name
        if '-h' in sys.argv:
            print(help)
            sys.exit(0)
        elif '--help' in sys.argv:
            print(help)
            sys.exit(0)
        elif '-v' in sys.argv:
            print(f"Youtube DL Automator v{version}")
            sys.exit(0)
        else:
            filename = sys.argv[1]

    else:
        # There isn't an argument, so default to VideoList.txt
        filename = "VideoList.txt"
    
    try:
        # Open the file and download each video in the file
        with open(filename, 'r') as filp:
            for line in filp:
                download(line)
    except FileNotFoundError:
        # The file doesn't exist, print an error message, potential solutions, and exit.
        print(f"The file {filename} does not exist. Please create it and try again.")
        print(f"If this file does exist, check the following:")
        print(f"\tMake sure to match capitalization and spacing.")
        print(f"\tMake sure you have the correct permissions.")
        if sys.platform == "win32":
            print(f"\tThis may happen if you are only using one backslash (\\) in your path.")
            print(f"\tTry using forward slashes (/) or double backslashes (\\\\) instead.")
        sys.exit(1)