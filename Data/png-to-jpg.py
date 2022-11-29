import PIL.Image
import glob
import os

#if not "Data\AllData-jpgs" in 'Data':
#    os.mkdir("Data\AllData-jpgs")

lst_imgs = [i for i in glob.glob('*.png')]
print(lst_imgs)
for i in lst_imgs:
    img = PIL.Image.open(i)
    #resize images?
    #img.thumbnail((1024, 1024), Image.ANTIALIAS)
    img = img.convert('RGB')
    j = i.split('.')
    j = j[0].split('\\')
    img.save(j[0] + ".jpg")


print("Done.")
