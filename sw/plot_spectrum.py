import seabreeze.spectrometers as sb
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

plt.ion() 
devices = sb.list_devices()
print devices
spec = sb.Spectrometer(devices[0])
spec2 = sb.Spectrometer(devices[1])
spec.integration_time_micros(100000)
spec2.integration_time_micros(100000)
wl =  spec.wavelengths()

print spec.serial_number
print spec.model
print spec.pixels

print spec2.serial_number
print spec.model
print spec2.pixels

print len(wl)
array =  np.array(wl)


try:
    while True:
        inten = spec.intensities(correct_dark_counts=False, correct_nonlinearity=False)
        inten2 = spec2.intensities(correct_dark_counts=False, correct_nonlinearity=False)
        plt.clf()
        plt.ylim(500,1500)
        plt.plot(wl, inten)
        plt.show()
        plt.pause(0.0001)
        print inten
        print inten2
        
        array = np.vstack([array, inten])
        print array.shape

        hdu = fits.PrimaryHDU(array)


except Exception as e:
    print e
    print "Ukladam"

finally:
    hdu.writeto('new.fits', overwrite=True)