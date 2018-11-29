#
#  A module for loading PPM files into Python and Displaying them using
#  QuickDraw
#
#  Functions for use outside of this module:
#    loadPPM(fname) -- returns an image
#    displayImage(x,y,image) -- returns nothing
#
#  Created by Ben Stephenson
#  October 6, 2008
#  Updated June 8, 2009
#
import sys

#
#  Create a new Python class so that we can throw exceptions that contain
#  meaningful error messages
#
class PPM_Exception(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

#
#  partition: This function duplicates the functionality of the partition
#  method available on strings in Python 2.5.1.
#
#  Parameters:
#    s:  The string to partition
#    ch: The character to use as the split point
#
#  Returns:
#    A triple with all characters before the split character, the split
#    character (if present) and all of the characters after the split
#    character (if any)
#
def partition(s,ch):
  if (ch in s):
    i = s.index(ch)
    return (s[0:i],s[i],s[i+1:])
  else:
    return (s,None,None)

#
#  strip_comments: A function that removes any comments present on the line in
#                  the .ppm file.  Any white space at the end is also removed,
#                  including the newline character.
#
#  Parameters:
#    s:  a string, which may include a comment denonted by the # character
#
#  Returns:
#    A string, with all characters after the comment character removed.
#    Also removes any trailing whitespace (including the newline).
#
def strip_comments(s):
  #
  #  Works in 2.5.1, but not in older versions 
  #
  #  (rval, junk1, junk2) = s.partition("#")
  (rval,junk1,junk2) = partition(s,"#")
  return rval.rstrip(" \t\n")

#
#  loadPPM: A function that loads the named image file from disk, and stores
#           the image data as a list of columns, where each column is a list
#           of color components.
#
#  Parameters:
#    fname: the name of the file to load
#
#  Returns:
#    The image stored in the file specified
#
#  ASCII PPM files have a reasonably simple structure.  They begin with a
#  magic number (P3) that marks the file as an ASCII PPM file.  This is 
#  followed by the image dimensions, and the maximum intensity level for the
#  image (normally 255).  This is followed by the pixel data, with each
#  pixel being represented by three numbers between 0 and 255 (the red, green
#  and blue intensities respectively).
#
def load_ppm(fname):
  return loadPPM(fname);

def loadPPM(fname):

  #
  # Open the input file
  #
  inf = open(fname,"r")

  #
  # Read the magic number out of the top of the file and verify that we are
  # reading from an ASCII PPM file (denoted by P3)
  #
  magic = strip_comments(inf.readline())
  if (magic != "P3"):
    raise PPM_Exception('The file being loaded does not appear to be a valid ASCII PPM file')

  #
  # Get the image dimensions
  #
  dimensions = strip_comments(inf.readline())
  #(width, sep, height) = dimensions.partition(" ")
  (width, sep, height) = partition(dimensions," ")
  print(width)
  #width = int(width)
  #height = int(height)
  if (width <= 0) or (height <= 0):
    raise PPM_Exception("The file being loaded does not appear to have valid dimensions (" + str(width) + " x " + str(height) + ")")

  #
  # Get the maximum value -- this should always be 255 
  #
  max = inf.readline()
  max = int(strip_comments(max))
  if (max != 255):
    sys.stderr.write("Warning: PPM file does not have a maximum value of 255.  Image may not be handled correctly.")

  #
  # Create a list of the individual color components, loaded from the file
  #
  color_list = []
  for line in inf:
    line = strip_comments(line)
    color_list += line.split(" ")

  inf.close()  # We are done with the file -- be nice and close it 

  #
  # Now that we have a one dimensional list of all of the color components,
  # we need to arrage those color components into a three dimensional list
  # of lists of lists structured so that the outer list is a list of columns,
  # and each column is a list of color components in the order red, then green
  # then blue.  Note that the original image data is assumed to have its 
  # color components stored in this order.
  #
  image = []
  for x in range(0,width):
    image.append([])
    for y in range(0,height):
      image[x].append([int(color_list[(y * width + x) * 3]), \
	               int(color_list[(y * width + x) * 3 + 1]),
		       int(color_list[(y * width + x) * 3 + 2])])

  return image

#
#  limit: A function that ensures a value is limited to the valid range.
#         Limit raises an exception if the value is not legal.
#
#  Parameters:
#    high:  The highest value that is permitted
#    low:   The lowest value that is permitted
#    value: The value being tested to ensure it is within the correct range
#
def limit(high, low, value):
  if (value < low) or (value > high):
    raise PPM_Exception(str(value) + " is outside of the range " + str(high) + " to " + str(low))

#
#  displayImage: A function that displays an image using QuickDraw
#
#  Parameters:
#    x:   The x location within the QuickDraw window where the image will be
#         displayed
#    y:   The y location within the QuickDraw window where the image will be 
#         displayed
#    img: The list of lists of lists that contains the image data
#
#  Returns:  Nothing
#
def displayImage(x, y, img, outf=sys.stdout):
  #
  #  QuickDraw includes a primitive that allows use to dump all of the pixel
  #  data at once.  This is *much* faster than drawing it a pixel at a time.
  #  The pixelsx primitive expects the pixel data in left to right, top to 
  #  bottom order.  Color data is formatted using hexadecimal to reduce the
  #  total number of characters that must be sent.
  #
  outf.write("pixelsx " + str(x) + " " + str(y) + " " + str(len(img)) + " " + str(len(img[0])))
  for j in range(0, len(img[0])):
    for i in range(0, len(img)):
      limit(255.9,-0.9,img[i][j][0])
      limit(255.9,-0.9,img[i][j][1])
      limit(255.9,-0.9,img[i][j][2])
      outf.write(" %02x%02x%02x" % (int(img[i][j][0]),int(img[i][j][1]),int(img[i][j][2])))
  outf.write("\n") # newline to mark the end of the QuickDraw command
  outf.flush()

def createImage(x, y):
  retval = []
  for i in range(0, x):
    retval.append([])
    for j in range(0, y):
      retval[i].append([0,0,0])

  return retval

def width(image):
  return len(image)

def height(image):
  return len(image[0])

