from skimage.feature import greycomatrix, greycoprops
from skimage import io, color, img_as_ubyte



img = io.imread('fire_0004_01_01.png')

gray = color.rgb2gray(img)
image = img_as_ubyte(gray)
#io.imshow(image)

bins = np.array([0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 255]) #16-bit
inds = np.digitize(image, bins)

max_value = inds.max()+1
matrix_coocurrence = greycomatrix(inds, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4], levels=max_value, normed=False, symmetric=False)


# GLCM properties
def contrast_feature(matrix_coocurrence):
    contrast = greycoprops(matrix_coocurrence, 'contrast')
    return "Contrast = ", contrast

def dissimilarity_feature(matrix_coocurrence):
    dissimilarity = greycoprops(matrix_coocurrence, 'dissimilarity')
    return "Dissimilarity = ", dissimilarity

def homogeneity_feature(matrix_coocurrence):
    homogeneity = greycoprops(matrix_coocurrence, 'homogeneity')
    return "Homogeneity = ", homogeneity

def energy_feature(matrix_coocurrence):
    energy = greycoprops(matrix_coocurrence, 'energy')
    return "Energy = ", energy

def correlation_feature(matrix_coocurrence):
    correlation = greycoprops(matrix_coocurrence, 'correlation')
    return "Correlation = ", correlation

print("Contraste de la imagen" + str(energy_feature(matrix_coocurrence)))