from PIL import Image

def scale_image(file):
    file_height = 500
    img = Image.open(file)
    iwidth = img.size[0]
    iheight = img.size[1]
    # clean up the file name to take off extension
    if (iheight > iwidth):
        img.thumbnail((2000, file_height))
        img.save(file)
    else:
        img.thumbnail((2000, file_height))
        img.save(file)
    

