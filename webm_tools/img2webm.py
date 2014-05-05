#!/usr/bin/env python 
# vim: set ts=2 expandtab:
'''
Module: img2webm.py
Desc: convert an img to a webm that plays for N seconds
Author: on_three
Email: on.three.email@gmail.com
DATE: Sunday May the 5th 2014

  
'''
import os
import argparse
from subprocess import call
from PIL import Image
import shutil
import glob

def system_call(*args):
  print(str(args))
  call(list(args))

def clean_working_dir(working_dir, filetype):
  files = os.path.join(working_dir, '*.{ext}'.format(ext=filetype))
  for fl in glob.glob(files):
    os.remove(fl)

def convert(infile, outfile, duration_s):
  '''Convert an image to a webm
  '''
  duration = '00:00:{duration_s:02d}'.format(duration_s=duration_s)
  #-t duration (output)
  #convert the whole thing to webm
  system_call('avconv', '-loop', '1','-i', infile, '-c:v', 'libvpx', '-qmin' , '50', '-qmax', '50', '-c:an', '-crf', '-t', duration ,outfile)

def get_ext(filename):
  '''Get extension to normal file
  '''
  f, e = os.path.splitext(filename)
  return e

def main():
  parser = argparse.ArgumentParser(description='Convert a gif to a webm that plays the gif N times')
  parser.add_argument('infile', help='Input image name', type=str)
  parser.add_argument('-o', '--outfile', help='Output filename (.webm extension will be added if absent)', type=str, default=None)
  parser.add_argument('-s', '--seconds', help='Time in seconds to show the image.', type=int, default=1)
  #parser.add_argument('-w', '--working_dir', help='Working directory for temp files. default is /tmp/.', type=str, default='/tmp/')
  args = parser.parse_args()

  infile = os.path.abspath(args.infile)
  duration_s = args.seconds

  outfile = '{infile}.webm'.format(infile=infile)
  if args.outfile:
    #check to see if user specified output filename has .webm extention
    outfile = args.outfile
    if get_ext(outfile).lower() != '.webm':
      outfile = '{outfile}.webm'.format(outfile=outfile)
  outfile=os.path.abspath(outfile)

  convert(infile, outfile, duration_s)
        

if __name__ == "__main__":
  main()
