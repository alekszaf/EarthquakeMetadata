import os
import pandas as pd
import PIL.Image
import PIL.ExifTags
from tkinter import filedialog
#import exiftool

#path = './test'

path = filedialog.askdirectory()
print(path)

df = pd.DataFrame()

for i in os.listdir(path):
    image_path = os.path.join(path, i)
    img = PIL.Image.open(image_path)
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in PIL.ExifTags.TAGS
        }
    
    #Check exif metadata
    #print(exif)
    
    #Check xmp metadata
    print(img.getxmp())
    
    #Get GPS metadata
    gps={}
    for k, v in exif['GPSInfo'].items():
        geo_tag = PIL.ExifTags.GPSTAGS.get(k)
        gps[geo_tag]=v
        
    if gps == {}:
        pass
 
    #Get Latitude and Longitude
    lat = gps['GPSLatitude']
    long = gps['GPSLongitude']
    
    #Convert to degrees
    lat = float(lat[0]+(lat[1]/60)+(lat[2]/(3600*100)))
    long = float(long[0]+(long[1]/60)+(long[2]/(3600*100)))
    
    #Negative if LatitudeRef:S or LongitudeRef:W
    if gps['GPSLatitudeRef']=='S':
        lat = -lat
    if gps['GPSLongitudeRef']=='W':
        long = -long
    
    print(lat, long)
    coords = {'filename': i,'latitude': lat, 'longitude': long}
    
    df_loc = pd.DataFrame(coords, index=[0])
    df = pd.concat([df, df_loc], ignore_index=True)


df.to_csv('photo_location_data.csv', index=False)