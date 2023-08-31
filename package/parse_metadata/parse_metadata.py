import os
import pandas as pd
import PIL.Image
import PIL.ExifTags
from tkinter import filedialog

#path = './test'


def get_metadata(path, out_path, output_name):

    def get_tags(img):
        try:
            # Access the XMP metadata
            xmp = img.getxmp().items()
            for k, v in xmp:
                xmp = v

            # Access earthquake metadata
            emeta = xmp['RDF']['Description']['subject']['Bag']['li']
            emeta = [i.split(':', 1) for i in emeta]
            print(emeta)

            # Convert earthquake tags into dictionary
            emeta_dict = dict(emeta)

        except Exception:
            print('No valid metadata')
            emeta_dict = {'Earthquake': 'NA',
                        'Country' : 'NA',
                        'Date and time of earthquake' : 'NA',
                        'Magnitude of earthquake' : 'NA',
                        'Photo taken by' : 'NA',
                        'Building name' : 'NA',
                        'Building address' : 'NA',
                        'Building occupancy' : 'NA',
                        'Structure category' : 'NA',
                        'Number of storeys' : 'NA',
                        'Main material' : 'NA',
                        'Primary structural system' : 'NA',
                        'Damage grade' : 'NA',
                        'Building age' : 'NA',
                        'Regular/Irregular' : 'NA',
                        'Site' : 'NA'}
        return emeta_dict

    def get_gps(exif):
        # Get GPS metadata
        try:
            gps={}
            for k, v in exif['GPSInfo'].items():
                geo_tag = PIL.ExifTags.GPSTAGS.get(k)
                gps[geo_tag]=v

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

        except Exception:
            lat = 'NA'
            long = 'NA'
            print(f"Invalid GPS for image {i}")

        return lat, long

    def get_date(i, img):
            try:
                date = img._getexif()[36867]
            except Exception:
                 print(f"Invalid date for image {i}")
                 date = 'NA'
            return date



    # Initialize empty dataframe
    df = pd.DataFrame()
    meta_err = pd.DataFrame()

    ext = ('.png', '.jpg', '.jpeg', '.JPG')

    for i in os.listdir(path):
        if i.endswith(ext):
            image_path = os.path.join(path, i)
            img = PIL.Image.open(image_path)
            exif = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in img._getexif().items()
                if k in PIL.ExifTags.TAGS
                }

            date = get_date(i, img)
            lat, long = get_gps(exif)
            emeta_dict = get_tags(img)

            meta = {
                'File name': i,
                'Date of creation': date,
                'Latitude': lat,
                'Longitude': long,
            } | emeta_dict

            df_meta = pd.DataFrame(meta, index=[0])
            df = pd.concat([df, df_meta], ignore_index=True)
            print(f"Metadata of image {i} saved")

        #If error in metadata, skip the file and record it in a dataframe
        # except Exception:
        #     print(f"Error in metadata for image {i}")
        #     err_files = {'filename' : i}
        #     df_meta_err = pd.DataFrame(err_files, index=[0])
        #     meta_err = pd.concat([meta_err, df_meta_err])


    # # Save the metadata to a CSV
    df.to_csv(os.path.join(out_path, output_name + '.csv'), index=False)

    # # Save the list of files with metadata errors to a CSV
    # meta_err.to_csv(os.path.join(out_path, output_name + '_errors.csv'), index=False)


if __name__=="__main__":

    print("Select the image directory")
    path = filedialog.askdirectory()
    print("Input path: " + path)

    print("Select the output directory")
    #out_path = filedialog.askdirectory()
    out_path = './Outputs'
    print("Output path: " + out_path)

    output_name = input('Output file name: ')

    get_metadata(path, out_path, output_name)
    print("Done! Metadata is ready")