#! /usr/bin/env python2

from __future__ import print_function
import liboCams
import cv2
import time
import sys
import os

from optparse import OptionParser

class ImageCapture():
    def __init__(self, dir, textfile_name, annotate, format_num):

        # Find oCam to initialize
        devpath = liboCams.FindCamera('oCam')
        if devpath is None:
            print("oCam not Found")
            exit()

        # Initialize camera
        print("Initializing Camera")
        self.camera = liboCams.oCams(devpath, verbose=0)

        # Create image directory if needed or find the next image index
        self.dir = dir
        self.count = 0
        self.annotate = bool(annotate)
        textfile = textfile_name + ".dat"

        print("Saving images to directory: " + dir +"/")
        print("Using info file: " + textfile)

        fmtlist = self.camera.GetFormatList()

        if format_num < 0:
            print('Format List')

            for i, fmt in enumerate(fmtlist):
              print('\t', i, " ", fmt)

            selected_fmt = int(raw_input("Enter a number from the list above: "))

        else:
            selected_fmt = format_num

        self.camera.Set(fmtlist[selected_fmt])

        if not os.path.exists(dir): # check this is a new directory
            if os.path.exists(textfile): # check if the info file exists
                print("Error: New Directory being used with a pre-existing info file.")
                exit()
            else:
                # create directory and info file
                os.makedirs(dir)
                self.info_file = open(textfile, "a")

        else:
            if os.path.exists(textfile): # check if the info file exists
                #open file and get the next index to label new pics
                self.info_file = open(textfile, "a")
                self.count = len(next(os.walk(dir))[2])
                print("Found", self.count, "existing images in the directory.")

            else:
                print("Error: Existing Directory being used with a new info file.")
                exit()

        self.cv_saved_image = None
        self.fully_annotated = False

        self.startx = 0
        self.starty = 0

        self.endx = 0
        self.endy = 0

        self.camera.Start()


    def mouseCB(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if not self.fully_annotated:
                self.startx, self.starty = x, y
                print("Down:", x,y)
        if event == cv2.EVENT_LBUTTONUP:
            if not self.fully_annotated:
                self.endx, self.endy = x,y
                print("Up: ", x,y)
                self.fully_annotated = True


    def shutdown(self):
        print("Turning off camera.")
        self.camera.Close()
        self.info_file.close()
        cv2.destroyAllWindows()
        print("Program ended.")

    def annotate_saved_image(self, image_path, image_name):
        # open saved image

        print("\n"+ image_path)

        img_og = cv2.imread(filename=image_path)
        img_mod = img_og.copy()
        cv2.imshow("Annotate", img_mod)
        cv2.setMouseCallback('Annotate', self.mouseCB)

        while True:
            key = cv2.waitKey(1)

            if self.fully_annotated:

                cv2.rectangle(img_mod, (self.startx, self.starty), (self.endx, self.endy), (0,0,255))

                print("Press y if the bounding box looks good. ")

                cv2.imshow("Annotate", img_mod)
                okay = cv2.waitKey(0)

                if okay == ord('y'):

                    leftx, lefty = min(self.startx, self.endx), min(self.starty, self.endy)
                    width = max(self.startx, self.endx) - leftx
                    height = max(self.starty, self.endy) - lefty

                    line = image_name + " " + str(leftx) + " " + str(lefty) + " " + str(width) + " " + str(height) + "\n"

                    print(line)

                    self.info_file.write(line)
                    break

                else:
                    self.fully_annotated = False
                    self.startx = 0
                    self.starty = 0
                    self.endx = 0
                    self.endy = 0
                    img_mod = img_og.copy()
                    cv2.imshow("Annotate", img_mod)
                    okay = cv2.waitKey(1)

            elif key == 27:
                os.remove(image_path)
                print("Annotation Aborted and Image Deleted")
                self.count -= 1
                break

        self.fully_annotated = False
        self.startx = 0
        self.starty = 0
        self.endx = 0
        self.endy = 0
        cv2.destroyAllWindows()

    def stream_image(self):

        while True:
            frame = self.camera.GetFrame()
            rgb = cv2.cvtColor(frame, cv2.COLOR_BAYER_GB2BGR)
            cv2.imshow("Live Image", rgb)
            key = cv2.waitKey(1)

            if key == ord('s'):
                # save image
                image_path = self.dir + '/' + self.dir + str(self.count) + ".jpg"
                image_name = self.dir + str(self.count) + ".jpg"

                cv2.imwrite(filename=image_path, img=rgb)

                self.count += 1

                # close streaming window
                cv2.destroyAllWindows()
                # call annotation function
                if self.annotate:
                    self.annotate_saved_image(image_path, image_name)

            elif key == ord('q'):
                self.shutdown()
                break

            elif key == 27: #esc key
                self.shutdown()
                break

def main():
    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="dir", default="img", type="string",
                      help="directory to store the images")
    parser.add_option("-t", "--textfile", dest="info_file", default = "info", type="string",
                      help="info file to train opencv cascade classifier")
    parser.add_option("-a", "--annotation", dest="annotate", default = "1", type="int",
                      help="Set to 0 if you only want to save an image and skip the annotation")

    parser.add_option("-f", "--format", dest="format", default = "-1", type="int",
                      help="Set the format of the camera")

    (options, args) = parser.parse_args()

    oCam_capture = ImageCapture(options.dir, options.info_file, options.annotate, options.format)

    oCam_capture.stream_image()

if __name__ == '__main__':
    main()
