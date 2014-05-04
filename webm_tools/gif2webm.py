#!/usr/bin/env python 
# vim: set ts=2 expandtab:
'''
Module: gif2webm.py
Desc: convert a gif to a webm that plays N times
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

def convert(infile, outfile, loops, working_dir):
  '''Convert a gif to a webm
  '''
  tmp_filenames =  os.path.join(working_dir, 'tmp%05d.jpg')
  tmp_outfile = os.path.join(working_dir, 'tmp.avi')

  #1. get duration (and looping?) info on all gif frames
  image = Image.open(infile)
  duration_ms = image.info['duration']#duration in milliseconds to seconds
  duration_s = float(duration_ms)/1000.0
  
  print(str(duration_s))
  #for conversion we need 'frames per second'
  fps = 7
  if duration_s > 0:
    fps = int(1.0/duration_s)
  print(str(fps))

  #2. Clear current temp_dir of images
  clean_working_dir(working_dir, 'jpg')
  clean_working_dir(working_dir, 'avi')
  
  #3. Split current gif into a series of images
  system_call('convert', '-coalesce', infile, tmp_filenames)

  #4. Use avconv (or ffmpeg) to turn image series into a high quality .avi
  system_call('avconv','-y', '-r', str(fps), '-i', tmp_filenames, '-r', str(fps), '-an', tmp_outfile)
  #do simple concatenation of input file to 'loop' it N times
  #avconv is pure shit, so looping requires a lot of intermediate files and concatenation
  tmp_infile = os.path.join(working_dir, 'tmp_infile.avi')
  infile_copy = os.path.join(working_dir, 'tmp_infile_copy.avi')
  shutil.copy(tmp_outfile, infile_copy)
  for loop in range(0, loops-1):
    shutil.copy(tmp_outfile, tmp_infile)
    system_call('avconv', '-y', '-i', 'concat:{f1}|{f2}'.format(f1=tmp_infile,f2=infile_copy), '-c', 'copy', '-r', str(fps), '-an', tmp_outfile)

  #5 convert the whole thing to webm
  system_call('avconv', '-i',tmp_outfile, '-c:v', 'libvpx', '-qmin' ,'50', '-qmax', '50', '-crf', '10', outfile)

def get_ext(filename):
  '''Get extension to normal file
  '''
  f, e = os.path.splitext(filename)
  return e

def main():
  parser = argparse.ArgumentParser(description='Convert a gif to a webm that plays the gif N times')
  parser.add_argument('infile', help='Input filename (.gif)', type=str)
  parser.add_argument('-o', '--outfile', help='Output filename (.webm extension will be added if absent)', type=str, default=None)
  parser.add_argument('-l', '--loops', help='Number of times to loop the input .gif in the output file.', type=int, default=1)
  parser.add_argument('-w', '--working_dir', help='Working directory for temp files. default is /tmp/.', type=str, default='/tmp/')
  args = parser.parse_args()

  infile = os.path.abspath(args.infile)
  loops = args.loops
  working_dir = args.working_dir

  outfile = '{infile}.webm'.format(infile=infile)
  if args.outfile:
    #check to see if user specified output filename has .webm extention
    outfile = args.outfile
    if get_ext(outfile).lower() != '.webm':
      outfile = '{outfile}.webm'.format(outfile=outfile)
  outfile=os.path.abspath(outfile)

  convert(infile, outfile, loops, working_dir)
        

if __name__ == "__main__":
  main()
