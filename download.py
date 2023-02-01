#!/usr/bin/env python3

import os
import yt_dlp
import sys

VERSION = "0.1"

def download(link, output, cookies=None):
    # Options for youtube_dl
    ydl_opts = {
        "format": "mp4",
        "continue": True,
    }

    # Format the output file
    if not output['is_dir']:
        ydl_opts['outtmpl'] = output['path']
    elif output['path'][-1] == "/" or output['path'][-1] == "\\":
        ydl_opts['outtmpl'] = output['path'].replace("\\", "/") + "%(title)s - s%(episode)se%(episode_number)02d.%(ext)s"
    else:
        ydl_opts['outtmpl'] = output['path'].replace("\\", "/") + "/%(title)s - s%(episode)se%(episode_number)02d.%(ext)s"
    
    if cookies:
        ydl_opts['cookiefile'] = cookies

    # Ensure the link is a list
    if not type(link) == list:
        link = (link)

    # Download and let it rip.
    with yt_dlp.YoutubeDL(ydl_opts) as yt_dl:
        yt_dl.download(link)

def auto(filename, output, cookies):
    # Open the file and download each video in the file

    # Don't allow downloading if the output argument hasn't been specified
    # TODO: Change from Exception to something more specific
    if not output:
        raise Exception("Output directory not specified")
    
    # Don't allow downloading if the output argument is a file
    # TODO: Change from Exception to something more specific
    elif not output['is_dir']:
        raise Exception("File specified, output should be a directory")
    
    videos = []

    with open(filename, "r") as filp:
        for line in filp:
            videos.append(line)
    
    for i in range(len(videos)):
        videos[i] = problematic_url(videos[i])
    
    download(videos, output, cookies)

def problematic_url(url):
    WEBSITES = {
        'historyvault': {
            'domains': ["https://www.historyvault.com", "https://watch.historyvault.com", "https://historyvault.com"],
            'fix':     "{}/full-special"
        }
    }
    match = ""

    for site in WEBSITES:
        if not match:
            for domain in WEBSITES[site]['domains']:
                    if url.startswith(domain):
                        match = site
                        break

        else:
            break
    
    if match:
        if url.endswith(WEBSITES[match]['fix']):
            return url
        else:
            return WEBSITES[match]['fix'].replace("{}", url)
    else:
        return url

def main():
    output = {}
    run = True
    url = None
    cookies = None

    # Information related to script
    run_info = {
        'version': VERSION,
        'help': "Usage: " + sys.argv[0] +  " <filename>",
        'args': {
            'help': {
                'shorthand': "-h",
                'longhand': ["--help"],
                'desc': "Prints the help for the script"
            },
            'version': {
                'longhand': ["--version", "--ver"],
                'desc': "Prints the version for the script"
            },
            'auto': {
                'shorthand': "-a",
                'longhand': ["--auto", "--urls"],
                'desc': "Downlaod videos from a file"
            },
            'cookies': {
                'shorthand': "-c",
                'longhand': ["--cookies"],
                'desc': "Downlaod videos from a file"
            },
            'output': {
                'shorthand': "-o",
                'longhand': ["--output"],
                'desc': "Specify the output"
            }
        },
        'defaults': {
            'AutoFile': "VideoList.txt"
        }
    }

    # Check if there is an argument provided
    if len(sys.argv) != 1:

        # There are, so determine if the argument is not a file name
        if "-h" or "--help" in sys.argv:
            print(run_info["version"])
            print("Arguments:")
            for arg in run_info["args"]:
                print()
            sys.exit(0)
        
        if "-v" or "--version" in sys.argv:
            print(f"Youtube DL v{run_info['version']}")
            sys.exit(0)
        
        if "-o" or "--output" in sys.argv:
            try:
                arg = sys.argv.index("-o")
            except IndexError:
                arg = sys.argv.index("--output")
            
            try:
                outfile = sys.argv[arg + 1]
            except IndexError:
                raise ValueError("No output file specified")

            output = {
                'path': outfile,
                'is_dir': os.path.isdir(outfile),
                'exists': os.path.exists(outfile)
            }
        
        if "-a" or "--auto" or "--urls" in sys.argv:
            try:
                arg = sys.argv.index("-a")
            except IndexError:
                try:
                    arg = sys.argv.index("--urls")
                except IndexError:
                    arg = sys.argv.index("--auto")
            
            filename = run_info['defaults']["AutoFile"]

            # There isn't an argument, so default to VideoList.txt
            try:
                filename = sys.argv[arg + 1]
            except IndexError:
                print(f"No file supplied, using default filename {filename}")    

            if os.path.exists(filename) and not output['is_dir']:
                auto(filename)
                sys.exit(0)
            elif not os.path.exists(filename):
                print("This file does not exist. Please create it and try again.")
                sys.exit(0)
            elif not os.path.output['is_dir']:
                print("Directories cannot be used for automated downloads.")
                sys.exit(0)

            else:
                # The file doesn"t exist, print an error message, potential solutions, and exit.
                error_string = f"The file {filename} does not exist. Please create it and try again."
                error_string += f"\nIf this file does exist, check the following:"
                error_string += f"\n\tMake sure to match capitalization and spacing."
                error_string += f"\n\tMake sure you have the correct permissions."

                if sys.platform == "win32":
                    error_string += f"\n\nThis may happen if you are only using one backslash (\\) in your path."
                    error_string += f"\nTry using forward slashes (/) or double backslashes (\\\\) instead."

                raise ValueError(error_string)
    
    # Run the main script
    while run:

        # Print the headers
        print(f"Youtube DL Frontend v{run_info['version']}")
        print(f"Output file:\t{output['path'] if output else None}")
        print(f"Video Link: \t{url if url else None}")
        print(f"Cookies     \t{cookies}")
        print("\n")

        # Options
        print("What would you like to do?")
        print("1.\tSet the output file")
        print("2.\tSpecify a URL")
        print("3.\tSpecify cookies")
        print("4.\tDownload")
        print("0.\tExit")

        # Get selection
        choice = input()
        print("\n")

        # Determine the selection
        if choice == "0":
            print("Exiting...")
            run = False
        
        # Change the directory
        elif choice == "1":
            print(f"Current path: {output['path'] if output and 'path' in output and output['path'] else os.getcwd()}")
            print("Enter the path of the file")
            outfile = input()

            # Set the output dict to reflect these changes
            output = {
                'path': outfile,
                'is_dir': os.path.isdir(outfile),
                'exists': os.path.exists(outfile)
            }
        
        # Specify the URL
        elif choice == "2":
            print(f"Current URL: {url}")
            print("Enter the new URL")
            url = input()

        elif choice == "3":
            print(f"Current cookies file: {cookies}")
            print("Enter a new cookies file.")
            cookies = input()

            if not os.path.exists(cookies):
                print("The file doesn't exist. Would you like to create it? ('y/N')")
                choice = input()

                if cookies.lower() == 'y':
                    parent = cookies[:cookies.rfind('/')]
                    os.makedirs(cookies, exist_ok=True)

        elif choice == "4":
            # Validate the path
            if '\\' in output['path'] and sys.platform == "win32":
                output['delimited'] = output['path'].split("\\")
            else:
                output['delimited'] = output['path'].split("/")
            
            parent = ""
            for i in range(len(output['delimited'])):
                if i < len(output['delimited']) - 1:
                    parent += '/' + output['delimited'][i]
            
            # Confirm the parent path exists
            if not os.path.exists(parent):
                print("The parent folder does not exist. Would you like to create it? (y/N)")
                choice = input()

                if choice.lower() == 'y':
                    os.makedirs(parent, exist_ok=True)
                
                else:
                    raise FileNotFoundError("The parent path does not exist.")
            
            # Confirm if the file should be overwritten if and only if the destination is a file 
            elif output['is_dir'] and output['exists']:
                print("The specified file exists. Would you like to overwrite it? (y/N)")
                choice = input()

                if choice.lower() == 'y':
                    pass
                else:
                    raise FileExistsError("Output file exists.")
            
            # Check the link in the problematic URLs
            url = problematic_url(url)
            
            print(f"Downloading...")
            download([url], output, cookies)

if __name__ == "__main__":
    main()