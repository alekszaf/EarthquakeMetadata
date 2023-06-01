import os
import pandas as pd
import PIL.Image
import PIL.ExifTags
from tkinter import filedialog

#path = './test'

def get_metadata(path, out_path, output_name):
    
    # Initialize empty dataframe
    df = pd.DataFrame()
    meta_err = pd.DataFrame()

    for i in os.listdir(path):
        image_path = os.path.join(path, i)
        img = PIL.Image.open(image_path)
        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
            }

        # Access the XMP metadata
        xmp = img.getxmp().items()
        for k, v in xmp:
            xmp = v

        try:
            
            # Access earthquake metadata
            emeta = xmp['RDF']['Description']['subject']['Bag']['li']
            emeta = [i.split(':', 1) for i in emeta]
            
            # Convert earthquake tags into dictionary
            emeta_dict = dict(emeta)

            # Get date
            try:    
                date = img._getexif()[36867]
            except Exception:
                date = 'NA'

            # Get GPS metadata
            gps={}
            for k, v in exif['GPSInfo'].items():
                geo_tag = PIL.ExifTags.GPSTAGS.get(k)
                gps[geo_tag]=v

            if gps['GPSStatus']=='V':
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

            meta = {
                'File name': i,
                'Date of creation': date,
                'Latitude': lat,
                'Longitude': long,
            } | emeta_dict

            df_meta = pd.DataFrame(meta, index=[0])
            df = pd.concat([df, df_meta], ignore_index=True)
        
        # If error in metadata, skip the file and record it in a dataframe    
        except Exception:
            print(f"Error in metadata for image {i}")
            err_files = {'filename' : i}
            df_meta = pd.DataFrame(err_files, index=[0])
            meta_err = pd.concat([meta_err, df_meta])

    # Save the metadata to a CSV
    df.to_csv(os.path.join(out_path, output_name + '.csv'), index=False)
    
    # Save the list of files with metadata errors to a CSV
    meta_err.to_csv(os.path.join(out_path, output_name + '_errors.csv'), index=False)


if __name__=="__main__":
    
    print("Select the image directory")
    path = filedialog.askdirectory()
    print("Input path: " + path)
    
    print("Select the output directory")
    out_path = filedialog.askdirectory()
    print("Output path: " + out_path)
    
    output_name = input('Output file name: ')
    
    get_metadata(path, out_path, output_name)
    print("Done! Metadata is ready")