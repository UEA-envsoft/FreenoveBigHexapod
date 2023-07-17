from PIL import Image
from PIL import ImageDraw
import freenove16x8matrix


class Expression:
    def __init__(self):
        self.display = freenove16x8matrix.freenove16x8matrix(address=0x71)
        self.display.begin()

        # Clear the display buffer.
        self.display.clear()
        #create images
        self.smile = Image.new('1', (16, 8))
        self.open_smile = Image.new('1', (16, 8))
        self.fang_smile = Image.new('1', (16, 8))
        self.smile2 = Image.new('1', (16, 8))
        self.oh = Image.new('1', (16, 8))
        self.grump = Image.new('1', (16, 8))
        self.lips = Image.new('1', (16, 8))
        self.make_images()
        self.grin()

    def make_images(self):
        # make expression images# create 2 16x8 1 bit color images
        #smille
        #create a draw instance.
        draw = ImageDraw.Draw(self.smile)

        # Draw smile
        draw.line((0,6,5,2), fill=255)
        draw.line((0,7,5,1), fill=255)
        draw.line((6,2,9,2), fill=255)
        draw.line((6,1,9,1), fill=255)
        draw.line((15,6,10,2), fill=255)
        draw.line((15,7,10,1), fill=255)

        #open_smile 
        draw = ImageDraw.Draw(self.open_smile)
        # Draw open smile
        draw.line((0,7,0,5), fill=255)
        draw.line((15,7,15,5), fill=255)
        draw.line((1,7,5,3), fill=255)
        draw.line((1,4,5,0), fill=255)
        draw.line((6,3,9,3), fill=255)
        draw.line((6,0,9,0), fill=255)
        draw.line((14,7,10,3), fill=255)
        draw.line((14,4,10,0), fill=255)

        #fang_smile 
        draw = ImageDraw.Draw(self.fang_smile)
        # Draw open smile
        draw.line((0,7,0,3), fill=255)
        draw.line((15,7,15,3), fill=255)
        draw.line((1,7,3,5), fill=255)
        draw.line((1,2,3,0), fill=255)
        draw.line((3,4,3,3), fill=255)
        draw.line((4,2,5,3), fill=255)
        draw.line((4,5,5,4), fill=255)
        draw.line((6,4,9,4), fill=255)
        draw.line((4,0,11,0), fill=255)
        draw.line((10,4,11,5), fill=255)
        draw.line((10,3,11,2), fill=255)
        draw.line((12,4,12,3), fill=255)
        draw.line((14,7,12,5), fill=255)
        draw.line((14,2,12,0), fill=255)

        #smile2 
        draw = ImageDraw.Draw(self.smile2)
        draw.line((0,7,3,4), fill=255)
        draw.line((0,6,3,3), fill=255)
        draw.line((0,5,3,2), fill=255)
        draw.line((4,3,11,3), fill=255)
        draw.line((4,2,11,2), fill=255)
        draw.line((15,7,12,4), fill=255)
        draw.line((15,6,12,3), fill=255)
        draw.line((15,5,12,2), fill=255)

        #oh 
        draw = ImageDraw.Draw(self.oh)
        draw.line((6,7,9,7), fill=255)
        draw.line((3,4,5,6), fill=255)
        draw.line((5,3,5,4), fill=255)
        draw.line((3,3,5,1), fill=255)
        draw.line((6,5,9,5), fill=255)
        draw.line((6,2,9,2), fill=255)
        draw.line((6,0,9,0), fill=255)
        draw.line((10,3,10,4), fill=255)
        draw.line((12,4,10,6), fill=255)
        draw.line((12,3,10,1), fill=255)

        #grump 
        draw = ImageDraw.Draw(self.grump)
        draw.line((0,0,3,3), fill=255)
        draw.line((4,3,11,3), fill=255)
        draw.line((12,3,15,0), fill=255)

        #lips
        draw = ImageDraw.Draw(self.lips)
        draw.line((4,7,6,7), fill=255)
        draw.line((9,7,11,7), fill=255)
        draw.line((7,6,8,6), fill=255)
        draw.line((1,4,3,6), fill=255)
        draw.line((14,4,12,6), fill=255)
        draw.line((2,4,13,4), fill=255)
        draw.line((2,3,4,1), fill=255)
        draw.line((13,3,11,1), fill=255)
        draw.line((5,1,10,1), fill=255)
        

    def grin(self):
        self.display.set_image(self.smile)
        self.display.write_display()
    def open_grin(self):
        self.display.set_image(self.open_smile)
        self.display.write_display()
    def fangs(self):
        self.display.set_image(self.fang_smile)
        self.display.write_display()
    def grin2(self):
        self.display.set_image(self.smile2)
        self.display.write_display()
    def suprise(self):
        self.display.set_image(self.oh )
        self.display.write_display()
    def hump(self):
        self.display.set_image(self.grump)
        self.display.write_display()
    def pout(self):
        self.display.set_image(self.lips)
        self.display.write_display()


# Main program logic follows:
if __name__ == '__main__':
    E = Expression()
    E.suprise()