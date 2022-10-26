import PIL.Image
import glob
import os

if not "Data\AllData-jpgs" in 'Data':
    os.mkdir("Data\AllData-jpgs")

lst_imgs = [i for i in glob.glob('Data\AllData-pngs\*.png')]
print(lst_imgs)
for i in lst_imgs:
    img = PIL.Image.open(i)
    #resize images?
    #img.thumbnail((1024, 1024), Image.ANTIALIAS)
    img = img.convert('RGB')
    j = i.split('.')
    j = j[0].split('\\')
    img.save('Data\AllData-jpgs\\'+j[2] + ".jpg")


print("Done.")
os.startfile("Data\AllData-jpgs")