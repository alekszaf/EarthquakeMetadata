import os
import pandas as pd
import PIL.Image
import PIL.ExifTags
from tkinter import filedialog

#path = './test'

def get_metadata(path):
    
    # Initialize empty dataframe
    df = pd.DataFrame()

    for i in os.listdir(path):
        image_path = os.path.join(path, i)
        img = PIL.Image.open(image_path)
        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
            }

        # Check exif metadata
        #print(exif)

        # Check xmp metadata
        #print(img.getxmp())

        # Access the XMP metadata
        xmp = img.getxmp().items()
        for k, v in xmp:
            xmp = v

        # Access earthquake metadata
        emeta = xmp['RDF']['Description']['subject']['Bag']['li']
        print(emeta)

        emeta = [i.split(':', 1) for i in emeta]

        # THIS IS TEMPORARY SOLUTION - skip the images with "Building address" entry
        if ['Building address', ' N/A'] in emeta:
            emeta_dict = dict(emeta)
            print(emeta_dict)

            # Get date
            date = img._getexif()[36867]
            print(date)

            # Get GPS metadata
            gps={}
            for k, v in exif['GPSInfo'].items():
                geo_tag = PIL.ExifTags.GPSTAGS.get(k)
                gps[geo_tag]=v
            print(i)
            print(gps)

            if gps['GPSImgDirectionRef']=='M':
                lat = 'NA'
                long = 'NA'
            else:
                # Get Latitude and Longitude
                lat = gps['GPSLatitude']
                long = gps['GPSLongitude']

                # Convert to degrees
                lat = float(lat[0]+(lat[1]/60)+(lat[2]/(3600*100)))
                long = float(long[0]+(long[1]/60)+(long[2]/(3600*100)))

                # Negative if LatitudeRef:S or LongitudeRef:W
                if gps['GPSLatitudeRef']=='S':
                    lat = -lat
                if gps['GPSLongitudeRef']=='W':
                    long = -long

            print(lat, long)

            meta = {
                'filename': i,
                'date': date,
                'latitude': lat,
                'longitude': long,
            } | emeta_dict
        df_loc = pd.DataFrame(meta, index=[0])
        df = pd.concat([df, df_loc], ignore_index=True)

    df.to_csv('photo_location_data.csv', index=False)

if __name__=="__main__":
    print("Select the image directory")
    path = filedialog.askdirectory()
    get_metadata(path)
    print("Done!")