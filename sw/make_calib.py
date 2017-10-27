
import seabreeze
seabreeze.use("pyseabreeze")
import seabreeze.spectrometers as sb
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

plt.ion() 
print sb.list_devices()
spec = sb.Spectrometer.from_serial_number()
spec.integration_time_micros(10000000)
wl =  spec.wavelengths()

print spec.serial_number
print spec.model
print spec.pixels

print len(wl)
array =  np.array(wl)


try:
    while True:
        inten = spec.intensities(correct_dark_counts=False, correct_nonlinearity=False)
        plt.clf()
        plt.ylim(500,1500)
        plt.plot(wl, inten)
        plt.show()
        plt.pause(0.0001)
        print inten
        array = np.vstack([array, inten])
        print array.shape

        hdu = fits.PrimaryHDU(array)


except Exception as e:
    print e
    print "Ukladam"

finally:
    hdu.writeto('new.fits', overwrite=True)