import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from spectral import *
import seaborn as sns


hyperimg = np.load(r"/Users/simenkrogstie/Documents/Programming/Høst 2024/INF250/Mandatory Exercise 3/sandvika.npy")



wavelengths = envi.read_envi_header('Visnir.hdr')['wavelength']
wavelengths = [float(i) for i in wavelengths]                   

def fetch_band_num(list):
    target_wavelengths = {
        "blue" : 440,
        "green" : 535,
        "red" : 645,
        "NIR" : 800
    }

    w_array = np.array(list)    
    band_num = {}
    for key, value in target_wavelengths.items():
        band_number = int(np.argmin(np.abs(w_array - value)))
        band_num[key] = band_number
    
    return band_num



band_numbers = fetch_band_num(wavelengths)


red_band = band_numbers['red']
green_band = band_numbers['green']
blue_band = band_numbers['blue']
nir_band = band_numbers['NIR']

imshow(hyperimg, (red_band, green_band, blue_band), stretch=((0.02,0.98),(0.02,0.98),(0.02,0.98)))



def ndvi_index(red, nir):
    ndvi = (nir-red)/(nir+red)
    return ndvi

red = hyperimg[:,:,red_band]
nir = hyperimg[:,:,nir_band]
green = hyperimg[:,:,green_band]
blue = hyperimg[:,:,blue_band]

ndvi_image = ndvi_index(red, nir)
plt.imshow(ndvi_image, cmap='Spectral')
plt.title('NDVI Image')
plt.colorbar(label='NDVI Value')
plt.axis('off')




vegetation = np.array(hyperimg[280,330,:].reshape(-1, 1))
roof = np.array(hyperimg[150,210,:].reshape(-1, 1))
asphalt =  np.array(hyperimg[90,170,:].reshape(-1, 1))

plt.figure(figsize=(10, 6))
plt.plot(vegetation, label='Vegetation', linestyle='dashed', color='green')
plt.plot(roof, label='Roof', linestyle='dashed', color='red')
plt.plot(asphalt, label='Asphalt', linestyle='dashed', color='blue')
plt.xlabel('Wavelenghts (nm)')
plt.ylabel('Reflectance')
plt.title('Spectral Signatures')
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.6)




ndvi_flattened = ndvi_image.flatten()

plt.figure(figsize=(10, 6))
sns.histplot(ndvi_flattened, bins=50, kde=True, color='green')
plt.title('NDVI value distribution')
plt.xlabel('NDVI')
plt.ylabel('Frequency')
plt.grid(True, linestyle='--')
plt.show()

modified_ndvi = np.copy(ndvi_image)
modified_ndvi[modified_ndvi > 0.6] = np.nan

plt.imshow(modified_ndvi, cmap='Spectral')
plt.title('Thresholded NDVI Image')
plt.colorbar(label='NDVI Value')
plt.axis('off')


pc = principal_components(hyperimg)
# plt.figure()
# plt.plot(pc.eigenvalues[0:10])
pc_0999 = pc.reduce(fraction=0.999)

# Scores
img_pc = pc_0999.transform(hyperimg)
plt.figure(figsize=(4,4))
plt.title('Score 1')
plt.imshow(img_pc[:,:,0], vmin=0.1, vmax=0.15)
plt.figure(figsize=(4,4))
plt.title('Score 2')
plt.imshow(img_pc[:,:,1], vmin=0.1, vmax=0.15)
plt.figure(figsize=(4,4))
plt.title('Score 3')
plt.imshow(img_pc[:,:,2], vmin=0.1, vmax=0.15)

loadings = pc_0999.eigenvectors
plt.figure(figsize=(4,4))
plt.title('Loading 1')
plt.xlabel('Wavenelengt (nm)')
plt.ylabel('Weigth')
plt.plot(loadings[:,[0]])

plt.figure(figsize=(4,4))
plt.title('Loading 2')
plt.xlabel('Wavenelengt (nm)')
plt.ylabel('Weigth')
plt.plot(loadings[:,[1]])

plt.figure(figsize=(4,4))
plt.title('Loading 3')
plt.xlabel('Wavenelengt (nm)')
plt.ylabel('Weigth')
plt.plot(loadings[:,[2]])