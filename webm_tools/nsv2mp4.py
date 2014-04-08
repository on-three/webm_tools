#!/usr/bin/env python 
# vim: set ts=2 expandtab:
'''
Module: msv2mp4.py
Desc: convert .nsv file to .mp4 (h264/aac)
Author: on_three
Email: on.three.email@gmail.com
DATE: Monday, April 7th 2014

  
'''
import os
import argparse
from subprocess import call

def convert(infile, outfile):
  '''Convert infile (usually .nsv)
  
  '''
  #just run a system call to avconv
  command = ['avconv', 
    '-i', '{infile}'.format(infile=infile),
    '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental',
    '{outfile}'.format(outfile=outfile),
  ]
  
  call(command)

def get_ext(filename):
  '''Get extension to normal file
  '''
  f, e = os.path.splitext(filename)
  return e

def main():
  parser = argparse.ArgumentParser(description='Convert .nsv video to (h264/aac)mp4')
  parser.add_argument('infile', help='Input filename (usually .nsv video)', type=str)
  parser.add_argument('-o', '--outfile', help='Output filename. mp4 extension will be added if absent)', type=str, default=None)
  args = parser.parse_args()

  infile = args.infile
  outfile = '{infile}.mp4'.format(infile=infile)
  if args.outfile:
    #check to see if user specified output filename has .mp4 extention
    outfile = args.outfile
    if get_ext(outfile).lower() != '.mp4':
      outfile = '{outfile}.mp4'.format(outfile=outfile)

  convert(infile, outfile)
        

if __name__ == "__main__":
  main()
