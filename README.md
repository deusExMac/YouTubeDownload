# About YouTubeDownload
 Downloads YouTube video and/or audio to a local file, given an YouTube video url using Python's pytube module. 
 This script has been created to experiment with the pytube module. 
 
 The code has been developement and tested in IDLE. 


# Acknowledgements
Based on an idea and corrected/improved first version found here https://www.facebook.com/pythonclcoding/photos/a.2065043456959379/2638731779590541/

# Before you execute YouTubeDownload (aka required versions and modules)
  - **Python version >= 3.5** . 
      Due to the use of methods from the Path module. If you replace these methods (namely *.mkdir()* and *.is_file()* earlier versions can be used as well.
  - [pytube](https://pytube.io/en/latest/)
  - [validators](https://validators.readthedocs.io/en/latest/)
  - [pathlib](https://docs.python.org/3/library/pathlib.html)
  - [clrprint](https://pypi.org/project/clrprint/)

# How to use

Supported arguments via the command line or customized execution via the IDE:

``youtubeDownload.py [-f urlFile] [-o output directory] [-A] [-P] [-S] [-F] [url]``

Arguments:

``[-f urlFile]``: Path to file containing urls to YouTube videos to be batch downloaded. Inside the file, each url should be in a separate line. See file [testUrls.txt](https://github.com/deusExMac/YouTubeDownload/blob/main/testUrls.txt) for an example.

``[-o output directory]``: path to local directory where the downloaded YouTube videos/audio files should be stored. If path does not exist, it is (recursively) created. If creation fails, the script terminates. Downloaded files become the name of the YouTube video title. If file already exists, it is overwritten. Default output directory (if no -o option is given) is the current working directory (./). Videos are currently able to be downloaded and stored only in mp4 format.


``[-P]``: Displays progress. During download, displays the percentage of file already downloaded.

``[-A]``: Download only audio track of video(s). Default format is mp4.

``[-S]``: Displays only available streams of YouTube video identified by url. Does not download the video. For each avialble stream, format, resolution and size in MB is displayed. Available streams are ordered by resolution (default). Other ordering attribute are supported (see -F option)

``[-F]``: Order available streams by filesize. Option [-F] only valid when -S option is specified. Otherwise it is ignored.

``[url]``: Url to download video (or show supported streams). If -f option is present, [url] is ignored.

If no arguments are given, the program asks the user for a an YouTube url that is downloaded to the current local directory.


# Limitations

All publicly available videos should be able to be downloaded. 
The current version does not support downloading:

  - private videos 
  - videos requiring authentication
  - age restricted public videos. Downloading such videos will result in exception. See: https://github.com/pytube/pytube/issues/743




# Troubleshooting

## macOS

On macOS, you may encounter the following error when downloading YouTube video or audio:  

   ``<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1129)>``

To fix such error, you may try these steps:

1) Open terminal

2) Go to Python 3.X installation folder in Applications.

3) Execute as administyrator the "Install\ Certificates.command":

   ``$open Install\ Certificates.command``

4) Execute again YouTubeDownload. Ths issue should now be fixed and the above error should not reappear. 

For more info on this see:
- https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
 
