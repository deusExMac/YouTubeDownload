import os
import sys
import time


import argparse
import validators
from pathlib import Path

from pytube import YouTube

import clrprint



# The following two classes are used to parse
# arguments on the shell 'scommand line.
#
# These specialize ArgumentOarser of argparse module by
# throwing an exception if arguments are not correct.
class ArgumentParserError(Exception): pass
  
class ThrowingArgumentParser(argparse.ArgumentParser):
      def error(self, message):
          raise ArgumentParserError(message)




def percent( tem, total):
        perc = (float(tem) / float(total)) * float(100)
        return perc


def progress_function( stream,  _chunk, bytes_remaining):

    # Other approach below...
    size = stream.filesize
    p = percent( (size-bytes_remaining), size)
    print('[', '{:.2f}'.format(p)+'%]', sep='', end='')
    
    

    
def getAvailableStreams(yturl, sortBy='resolution'):

    try:
       print('\tAvailable STREAMS for [', yturl, '] (sorting by ', sortBy, '):', sep=''  )   
       yt = YouTube( yturl )
    except Exception as iEx:
         print('Error:', str(iEx)) 
         return(-9) 
          
    for stream in yt.streams.order_by(sortBy).desc():  
        print('\t\t* ', stream.mime_type, '   (', stream.resolution, ", ", '{:.2f}'.format(stream.filesize/(1024*1024)), "MB)", sep='')  

    return(0) 


# Downloads video given an url
# yturl: A YouTube video url
# Returns: status and the local filename the video was saved to
def downloadVideo( yturl, destination='.', showProgress=False ):
   try:      
      yt = YouTube( yturl )
      if showProgress:
         yt.register_on_progress_callback(progress_function)
      
      videoStreamLink = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
      print('(', '{:.2f}'.format(videoStreamLink.filesize / (1024*1024)), ' MB) ', sep='', end='')
      
      localFile = videoStreamLink.download(output_path = destination)
      
      return(0, localFile)
   except Exception as dVEx:
          clrprint.clrprint('Error:', str(dVEx), clr='red')
          return(-2, '')



# Downloads ONLY audio track of YouTube video given an url
# yturl: A YouTube video url
# Returns: status and the local filename the video was saved to
def downloadAudio( yturl, destination='.', showProgress=False ):
  try:
    yt = YouTube( yturl )
    if showProgress:
         yt.register_on_progress_callback(progress_function)
             
    audioStreamLink = yt.streams.filter(only_audio=True).first()
    print('(', '{:.2f}'.format(audioStreamLink.filesize / (1024*1024)), ' MB) ', sep='', end='')
    
    localFile = audioStreamLink.download( output_path = destination )
    
    return(0, localFile)
  except Exception as dAEx:
         clrprint.clrprint('Error:', str(dAEx), clr='red')
         return(-3, '')





def processUrlFile(urlFile, destination='.', audioOnly=False, showProgress=False, streamsOnly=False):

    nDone = 0
    nDownloaded = 0
    nFailed = 0
    
    for readLine in open(urlFile, 'r', encoding='UTF-8'):
       
       u = readLine.strip()
       if u == '':
          # Empty line. Skip it   
          continue

       # That's a comment. Skip it
       if u.startswith('#'):
          continue
             
       nDone += 1

       clrprint.clrprint(nDone,') Downloading [',  u, '] ', clr='green', sep='', end='')
       
       if not validators.url(u):
          nFailed += 1
          clrprint.clrprint('Invalid Url.', clr='red')
          continue
             
       start = time.perf_counter()

       if streamsOnly:
          err = getAvailableStreams(u)
       else:      
           if audioOnly:
              clrprint.clrprint(' (AUDIO).......', clr='green', sep='', end='')   
              err, localF = downloadAudio(u, destination, showProgress)
           else:              
              clrprint.clrprint(' (VIDEO).......', clr='green', sep='', end='') 
              err, localF  = downloadVideo(u, destination, showProgress)
           
           clrprint.clrprint(' done (in ',  '{:.2f}'.format(time.perf_counter() - start), 's)', clr='green', sep='' )
           
       
       if err < 0:
           nFailed += 1
       else:
           nDownloaded += 1
           if not streamsOnly:
              clrprint.clrprint('\tSaved to file [', localF, ']', clr='yellow')   
           
       
    return( nDone, nDownloaded, nFailed )       








def main():

    #
    # Parse command line arguments, if any
    #
    cmdLineArgs = ThrowingArgumentParser()    
    cmdLineArgs.add_argument('-f', '--urlfile', type=str, nargs='?', default='' )
    cmdLineArgs.add_argument('-o', '--outputpath', type=str, nargs='?', default='.' )
    cmdLineArgs.add_argument('-A', '--audioonly', action='store_true' )
    cmdLineArgs.add_argument('-P', '--showprogress', action='store_true' )
    cmdLineArgs.add_argument('-S', '--liststreams', action='store_true' )
    cmdLineArgs.add_argument('-F', '--byfilesize', action='store_true' )    
    cmdLineArgs.add_argument('url',   nargs=argparse.REMAINDER, default=[] )

    arguments = vars( cmdLineArgs.parse_args() )
    
    print('Executing with arguments:')
    if arguments['urlfile'] == '':
       print('\tFile input: False')
    else:
       print('\tFile input:', arguments['urlfile'])
       
    print('\tOutput path:', arguments['outputpath'])
    print('\tAudio only:', arguments['audioonly'])
    print('\tShow progress:', arguments['showprogress'])
    print('\tSTREAMS only:', arguments['liststreams'])    
    print()


    #
    # If arguments specified output directory for downloaded videos/audio
    # create recursively directories if these do not exist.
    # If creation of directories fails, process terminates.
    # 
    if arguments['outputpath'] != '':
       try:   
          Path(arguments['outputpath']).mkdir(parents=True, exist_ok=True)
       except Exception as oPathVer:
          print('Error verifying output directory(-ies)', arguments['outputpath'], '. Terminating.')
          sys.exit(-5)



    # Are urls in a file?
    # Start processing all urls in file and quit.
    if arguments['urlfile'] != '':

       uFile = Path( arguments['urlfile'] )
       if not uFile.is_file():
          print(arguments['urlfile'], 'is not a valid file.\nMake sure -f argument references an existing file containing a list of YouTube urls.')
          sys.exit(-6)
          
       nD, nS, nF = processUrlFile( urlFile=arguments['urlfile'], destination=arguments['outputpath'], audioOnly=arguments['audioonly'], showProgress=arguments['showprogress'], streamsOnly=arguments['liststreams'] )
       print('\nTotal of', nD, 'urls processed. Downloaded:', nS, 'failed:', nF)
       sys.exit(0)
       

    #
    # No file containing urls given. Check if a single url is given in the argument list. If not
    # ask one from user.
    #
    
    targetUrl = ''
    if arguments['url']:   
       targetUrl = arguments['url'][0]
    else:
         while True:
             if arguments['liststreams']:
                targetUrl = input("Enter YouTube url to list STREAMS >>")
             else:   
                targetUrl = input("Enter YouTube url to download >>")
                
             if len(targetUrl.strip()) > 0:
                 break  

    # Is it a proper url? 
    if not validators.url(targetUrl):
       print('Invalid url', targetUrl)
       sys.exit(-1)

    #
    # Should we only list the available streams?
    #
    if arguments['liststreams']:
       getAvailableStreams( targetUrl, 'filesize' if arguments['byfilesize'] else 'resolution')
       sys.exit(0)


    #   
    # We want to download the video/audio
    #
    err = -9
    start = time.perf_counter()
    if arguments['audioonly']:
       clrprint.clrprint('\tDownloading AUDIO [', targetUrl, '].......', clr='green', sep='', end='')    
       err, localF = downloadAudio( targetUrl, destination=arguments['outputpath'], showProgress=arguments['showprogress'])
       print(' done (in ', '{:.2f}'.format(time.perf_counter() - start), 's)' , sep='')
    else:
       clrprint.clrprint('\tDownloading VIDEO [', targetUrl, '].......', clr='green', sep='', end='')       
       err, localF = downloadVideo( targetUrl, destination=arguments['outputpath'], showProgress=arguments['showprogress'])
       print(' done (in ', '{:.2f}'.format(time.perf_counter() - start), 's)' , sep='')

    if err == 0:
       clrprint.clrprint('\t\tSaved to file [', localF, ']', clr='yellow')
    
    



if __name__ == '__main__':
   main() 






