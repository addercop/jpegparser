#!/usr/bin/python
#Simple script to parse jpegs from beginning to end--0xFFD8 to 0XFFD9.
#No care is taken against false positives.
import sys
import os
import mmap

JPEG_BEGIN = '\xff\xd8'
JPEG_END = '\xff\xd9'
OUTPUT_DIRECTORY = "./output/"
OUTPUT_EXTENSION = ".jpg"
OUTPUT_FILENUMBER = 1
KILOBYTE = 2**10

def write_out(blob):
	global OUTPUT_FILENUMBER
	if len(blob) < KILOBYTE:
		return
	handle = open(OUTPUT_DIRECTORY + ("%08d" % OUTPUT_FILENUMBER) + OUTPUT_EXTENSION, "w")
	OUTPUT_FILENUMBER += 1
	handle.write(blob)
	handle.close()

def parse(blob,offset):
	startflag = offset
	endflag = blob.find(JPEG_END,startflag)
	write_out(blob[startflag:endflag+2])
	return endflag

def scan(memory):
	offset = 0
	while offset != -1:
		offset += len(JPEG_END)
		offset = memory.find(JPEG_BEGIN, offset)
		offset = parse(memory,offset)
		

def main():
	global OUTPUT_DIRECTORY
	if len(sys.argv) < 2:
		print "Usage:",sys.argv[0]," binaryblob"
		return
	handle = open(sys.argv[1],"r")
	mapfile = mmap.mmap(handle.fileno(),0,mmap.MAP_SHARED,mmap.PROT_READ)
	os.mkdir(OUTPUT_DIRECTORY)
	scan(mapfile)

if __name__ == '__main__':
	main()
