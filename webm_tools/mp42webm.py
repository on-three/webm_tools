#!/usr/bin/env python 
# vim: set ts=2 expandtab:
'''
Module: mp42webm.py
Desc: convert section of video file to .webm
Author: on_three
Email: on.three.email@gmail.com
DATE: Monday, April 7th 2014

  
'''
import os
import argparse
from subprocess import call

def convert(infile, outfile, start=None, length=None, qmax=45):
  '''Convert infile (usually .mp4)
  avconv -i infile.mp4 -ss 00:00:00 -t 00:00:10 -codec:v libvpx -an test.webm
  ffmpeg -i video.mp4 -threads 3 -qmin 30 -quality best -c:v libvpx -b:v 3MB -an output.webm 
  '''
  #just run a system call to ffmpeg
  #ffmpeg -i input.flv -vcodec libvpx -acodec libvorbis output.webm
  command = ['avconv', 
    '-i', '{infile}'.format(infile=infile)]
  if start:
    command.extend(['-ss', start,])
  if length:
    command.extend(['-t', length])

  command.extend([
    '-codec:v', 'libvpx', '-qmax', str(qmax), '-fs', '3MB', '-an',
    '{outfile}'.format(outfile=outfile),
  ])
  
  call(command)

def get_ext(filename):
  '''Get extension to normal file
  '''
  f, e = os.path.splitext(filename)
  return e

def main():
  parser = argparse.ArgumentParser(description='Convert video to .webm')
  parser.add_argument('infile', help='Input filename (usually .mp4 video)', type=str)
  parser.add_argument('-o', '--outfile', help='Output filename. mp4 extension will be added if absent)', type=str, default=None)
  parser.add_argument('-s', '--start', help='start time for .webem extraction as "00:00:00".', type=str, default=None)
  parser.add_argument('-l', '--length', help='Length for .webm extraction as "00:00:00"', type=str, default=None)
  parser.add_argument('-q', '--qmax', help='Maximum encoding quantization (1-50). Smaller produces better, larger files.', type=int, default=45)
  args = parser.parse_args()

  infile = args.infile
  start = None
  if args.start:
    start = args.start
    #TODO: make sure start is in form "00:00:00"
  length = None
  if args.length:
    length= args.length
    #TODO: make sure length is in for "00:00:00"

  qmax = args.qmax

  outfile = '{infile}.webm'.format(infile=infile)
  if args.outfile:
    #check to see if user specified output filename has .mp4 extention
    outfile = args.outfile
    if get_ext(outfile).lower() != '.webm':
      outfile = '{outfile}.webm'.format(outfile=outfile)

  convert(infile, outfile, start, length, qmax)
        

if __name__ == "__main__":
  main()
