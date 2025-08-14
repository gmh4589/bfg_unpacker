import os
from PIL import Image
from source.reaper import Reaper, file_reaper
from source.ui import localize


class ImageConverter(Reaper):
    out_format = 'png'

    @file_reaper
    def run(self):
        # Full support:
        # BLP, BMP, DDS, DIB, EPS, GIF, ICNS, ICO, IM, JPEG, JP2, JPX, MSP, PCX, PFM, PNG, APNG,
        # PPM, SGI, SPI, TGA, TIFF, WEBP, XBM
        # Read only:
        # CUR, DCX, FITS, FLI, FLC, FPX, FTEX, GBR, GD, IMT, IPTC, NAA, MCIDAS, MIC, MPO, PCD,
        # PIXAR, PSD, QOI, SUN, WAL, WMF, EMF, XPM
        # Write only:
        # PALM, PDF, XV

        with open(self.file_name, "rb") as im_file:
            ext = self.file_name.split('.')[-1]
            file_name = os.path.basename(self.file_name).replace(ext, self.out_format)

            try:
                image = Image.open(im_file)

                if image.mode != 'RGBA':
                    image = image.convert('RGBA')

                if self.out_format in ("jpeg", "j", "jfif", "jpe", "jpg"):
                    image = image.convert('YCbCr')
                elif self.out_format == 'pcx':
                    image = image.convert('RGB')
                elif self.out_format == 'xbm':
                    image = image.convert('1')

                image.save(f"{self.output_folder}\\{file_name}")
            except Image.DecompressionBombError:
                print(localize.big_image_error)

            self.update_pb(1, 1, file_name)
