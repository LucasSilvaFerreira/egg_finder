__author__ = 'lucas'
from skimage import data, io, transform
from skimage.measure import label, regionprops
from skimage.filters import threshold_otsu
from skimage.feature import canny
from skimage.morphology import square, closing
import numpy as np
from scipy import ndimage as ndi
from skimage.measure import label
import sys
import glob

def main():
    for file_path in glob.glob("/home/lucas/Downloads/Lucas/GSK 10uM/*.JPG"):

        img = data.imread(file_path, as_grey=True)

        img = transform.resize(img, [600, 600])
        img_color = transform.resize(data.imread(file_path), [600, 600])

        img[img >img.mean()-0.1] = 0

        # io.imshow(img)
        # io.show()
        #
        edges = canny(img)
        bordas_fechadas = closing(img > 0.1, square(15)) # fechando gaps
        fill_cells = ndi.binary_fill_holes(bordas_fechadas)
        # io.imshow(fill_cells)
        # io.show()
        img_label = label(fill_cells, background=0)
        n= 0
        for  x in regionprops(img_label):
            if x.area < 2000 and x.area > 300:
                n +=1
                print x.area
                minr, minc, maxr, maxc = x.bbox
                try:
                    out_path_name = file_path.split("/")[-1].rstrip(".JPG")
                    io.imsave("out/cell_{}_pic_{}_area_{}.png".format(n, out_path_name, str(round(x.area))),img_color[minr-3: maxr+3, minc-3: maxc+3])
                    #io.show()
                except:
                    pass

if __name__ == '__main__':
    sys.exit(main())
