from pdf2image import convert_from_path
import pandas as pd
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pickle


# Einlesen und in Graustufenbild umwandeln
pdf_path = "LLW Manual.pdf"
dpi = 600
contiScale = np.array(convert_from_path(pdf_path, dpi=dpi)[1])
gray_contiScale = cv2.cvtColor(contiScale, cv2.COLOR_BGR2GRAY)

def cm_to_pixels(cm, dpi):
    return int(cm * (dpi / 2.54))  # 1 Inch = 2.54 cm


# Funktion zum Extrahieren von ROIs und zum Berechnen des mittleren Pixelwerts
def extract_rois_and_calculate_means(gray_contiScale, dpi, rois_cm):
    means = []
    for roi in rois_cm:
        x = cm_to_pixels(roi["x"], dpi)
        y = cm_to_pixels(roi["y"], dpi)
        width = cm_to_pixels(roi["width"], dpi)
        height = cm_to_pixels(roi["height"], dpi)

        # ROI
        roi_image = gray_contiScale[y:y + height, x:x + width]

        # Mittlerer Pixelwert
        mean_values = cv2.mean(roi_image)[0] # Kanal
        means.append({
            "density": roi["name"],
            "mean pixel value": mean_values
        })

    return means

plt.figure(facecolor='lightpink')
plt.imshow(gray_contiScale, cmap="gray")
plt.title('Graustufenbild ROI')
plt.axis('off')
plt.show()

# Zentimeter-Angaben der ROIs (x, y, Breite, Höhe in cm)
rois_cm = [
    {"name": "1.5", "x": 1, "y": 10.4, "width": 3, "height": 1},
    {"name": "1.3", "x": 1, "y": 12.2, "width": 3, "height": 1},
    {"name": "1.1", "x": 1, "y": 13.8, "width": 3, "height": 1},
    {"name": "0.9", "x": 1, "y": 15.6, "width": 3, "height": 1},
    {"name": "0.7", "x": 1, "y": 17.4, "width": 3, "height": 1},
    {"name": "0.5", "x": 1, "y": 19.1, "width": 3, "height": 1},
    {"name": "0.3", "x": 1, "y": 20.8, "width": 3, "height": 1},
    {"name": "0.1", "x": 1, "y": 22.3, "width": 3, "height": 1},
]

# Berechnung der Mittelwerte der ROIs
roi_means_LLW = extract_rois_and_calculate_means(gray_contiScale, dpi, rois_cm)
print(str(pdf_path))
for roi_mean in roi_means_LLW:
    print(roi_mean)

# Plot der ROIs
fig, axes = plt.subplots(1, len(rois_cm), figsize=(15, 5))
fig.suptitle("Standard color sample continuous - ROIs", fontsize=16)

for i, roi in enumerate(rois_cm):
    x = cm_to_pixels(roi["x"], dpi)
    y = cm_to_pixels(roi["y"], dpi)
    width = cm_to_pixels(roi["width"], dpi)
    height = cm_to_pixels(roi["height"], dpi)

    # ROI ausschneiden
    roi_image = contiScale[y:y + height, x:x + width]

    # ROI in Subplot anzeigen
    axes[i].imshow(roi_image)
    axes[i].set_title(f"ROI: {roi['name']}")
    axes[i].axis("off")

plt.tight_layout()
plt.show()


pdf_path = "LW Manual.pdf"
dpi = 600
contiScale = np.array(convert_from_path(pdf_path, dpi=dpi)[0])
gray_contiScale = cv2.cvtColor(contiScale, cv2.COLOR_BGR2GRAY)

def cm_to_pixels(cm, dpi):
    return int(cm * (dpi / 2.54))  # 1 Inch = 2.54 cm


# Funktion zum Extrahieren von ROIs und zum Berechnen des mittleren Pixelwerts
def extract_rois_and_calculate_means1(gray_contiScale, dpi, rois_cm):
    means1 = []
    for roi in rois_cm:
        x = cm_to_pixels(roi["x"], dpi)
        y = cm_to_pixels(roi["y"], dpi)
        width = cm_to_pixels(roi["width"], dpi)
        height = cm_to_pixels(roi["height"], dpi)

        # ROI
        roi_image = gray_contiScale[y:y + height, x:x + width]

        # Mittlerer Pixelwert
        mean_values = cv2.mean(roi_image)[0] # Kanal
        means1.append({
            "density": roi["name"],
            "mean pixel value": mean_values
        })

    return means1

plt.figure(facecolor='lightpink')
plt.imshow(gray_contiScale, cmap="gray")
plt.title('Graustufenbild ROI')
plt.axis('off')
plt.show()

# Zentimeter-Angaben der ROIs (x, y, Breite, Höhe in cm)
rois_cm = [
    {"name": "1.5", "x": 1, "y": 10.4, "width": 3, "height": 1},
    {"name": "1.3", "x": 1, "y": 12.2, "width": 3, "height": 1},
    {"name": "1.1", "x": 1, "y": 13.8, "width": 3, "height": 1},
    {"name": "0.9", "x": 1, "y": 15.6, "width": 3, "height": 1},
    {"name": "0.7", "x": 1, "y": 17.4, "width": 3, "height": 1},
    {"name": "0.5", "x": 1, "y": 19.1, "width": 3, "height": 1},
    {"name": "0.3", "x": 1, "y": 20.8, "width": 3, "height": 1},
    {"name": "0.1", "x": 1, "y": 22.3, "width": 3, "height": 1},
]

# Berechnung der Mittelwerte der ROIs
roi_means_LW = extract_rois_and_calculate_means(gray_contiScale, dpi, rois_cm)
print(str(pdf_path))
for roi_mean in roi_means_LW:
    print(roi_mean)

# Plot der ROIs
fig, axes = plt.subplots(1, len(rois_cm), figsize=(15, 5))
fig.suptitle("Standard color sample continuous - ROIs", fontsize=16)

for i, roi in enumerate(rois_cm):
    x = cm_to_pixels(roi["x"], dpi)
    y = cm_to_pixels(roi["y"], dpi)
    width = cm_to_pixels(roi["width"], dpi)
    height = cm_to_pixels(roi["height"], dpi)

    # ROI ausschneiden
    roi_image = contiScale[y:y + height, x:x + width]

    # ROI in Subplot anzeigen
    axes[i].imshow(roi_image)
    axes[i].set_title(f"ROI: {roi['name']}")
    axes[i].axis("off")

plt.tight_layout()
plt.show()



def plot_density_vs_mean_with_fit(roi_means_LLW):
    densities_LLW = [float(item["density"]) for item in roi_means_LLW]
    mean_pixel_values_LLW = [item["mean pixel value"] for item in roi_means_LLW]

    densities_LW = [float(item["density"]) for item in roi_means_LW]
    mean_pixel_values_LW = [item["mean pixel value"] for item in roi_means_LW]

    poly_coeffs_LW = np.polyfit(densities_LW, mean_pixel_values_LW, deg=3)
    fit_curve_LW = np.polyval(poly_coeffs_LW, densities_LW)


    poly_coeffs_LLW = np.polyfit(densities_LLW, mean_pixel_values_LLW, deg=3)
    fit_curve_LLW = np.polyval(poly_coeffs_LLW, densities_LLW)

    
    return densities_LW, mean_pixel_values_LW, densities_LLW, mean_pixel_values_LLW

densities_LW, mean_pixel_values_LW, densities_LLW, mean_pixel_values_LLW = plot_density_vs_mean_with_fit(roi_means_LLW)

density_to_gray_LLW = np.polyfit(densities_LLW, mean_pixel_values_LLW, deg=3)
density_to_gray_LW = np.polyfit(densities_LW, mean_pixel_values_LW, deg=3)


filename = "LLW_ABCD.xlsx"
data = pd.read_excel(filename,decimal=",", sheet_name=0, skiprows=0)
columns = data.columns

x_LLW = data.iloc[:, 0]
y_LLW_A= data.iloc[:, 1]
y_LLW_B= data.iloc[:, 2]
y_LLW_C= data.iloc[:, 3]
y_LLW_D= data.iloc[:, 4]


filename = "LW_ABCD.xlsx"
data = pd.read_excel(filename,decimal=",", sheet_name=0, skiprows=0)
columns = data.columns
x_LW = data.iloc[:, 0]
y_LW_A= data.iloc[:, 1]
y_LW_B= data.iloc[:, 2]
y_LW_C= data.iloc[:, 3]
y_LW_D = data.iloc[:, 4]
X_G = np.arange(70, 245, 0.1)


y_G_LLW_A= np.polyval(density_to_gray_LLW, y_LLW_A)
y_G_LLW_B= np.polyval(density_to_gray_LLW, y_LLW_B)
y_G_LLW_C= np.polyval(density_to_gray_LLW, y_LLW_C)
y_G_LLW_D= np.polyval(density_to_gray_LLW, y_LLW_D)

y_G_LW_A= np.polyval(density_to_gray_LW, y_LW_A)
y_G_LW_B= np.polyval(density_to_gray_LW, y_LW_B)
y_G_LW_C= np.polyval(density_to_gray_LW, y_LW_C)
y_G_LW_D= np.polyval(density_to_gray_LW, y_LW_D)


grau_druck_LLW_A = np.polyfit(y_G_LLW_A, x_LLW, deg=3)
grau_druck_LLW_B = np.polyfit(y_G_LLW_B, x_LLW, deg=3)
grau_druck_LLW_C = np.polyfit(y_G_LLW_C, x_LLW, deg=3)
grau_druck_LLW_D = np.polyfit(y_G_LLW_D, x_LLW, deg=3)



grau_druck_LW_A = np.polyfit(y_G_LW_A, x_LW, deg=3)
grau_druck_LW_B = np.polyfit(y_G_LW_B, x_LW, deg=3)
grau_druck_LW_C = np.polyfit(y_G_LW_C, x_LW, deg=3)
grau_druck_LW_D = np.polyfit(y_G_LW_D, x_LW, deg=3)




plt.plot(X_G, np.polyval(grau_druck_LW_A,X_G),label='A')
plt.plot(X_G, np.polyval(grau_druck_LW_B,X_G),label='B')
plt.plot(X_G, np.polyval(grau_druck_LW_C,X_G),label='C')
plt.plot(X_G, np.polyval(grau_druck_LW_D,X_G),label='D')
plt.xlabel('Pixel')
plt.ylabel('Druck [MPa]')
plt.title('LW')
plt.legend()
plt.show()

plt.plot(X_G, np.polyval(grau_druck_LLW_A,X_G),label='A')
plt.plot(X_G, np.polyval(grau_druck_LLW_B,X_G),label='B')
plt.plot(X_G, np.polyval(grau_druck_LLW_C,X_G),label='C')
plt.plot(X_G, np.polyval(grau_druck_LLW_D,X_G),label='D')
plt.xlabel('Pixel')
plt.ylabel('Druck [MPa]')
plt.title('LLW')
plt.legend()
plt.show()

with open("grau_druck_LLW_A.pkl", "wb") as f:
    pickle.dump(grau_druck_LLW_A, f)
with open("grau_druck_LLW_B.pkl", "wb") as f:
    pickle.dump(grau_druck_LLW_B, f)  
with open("grau_druck_LLW_C.pkl", "wb") as f:
    pickle.dump(grau_druck_LLW_C, f)  
with open("grau_druck_LLW_D.pkl", "wb") as f:
    pickle.dump(grau_druck_LLW_D, f) 

with open("grau_druck_LW_A.pkl", "wb") as f:
    pickle.dump(grau_druck_LW_A, f)
with open("grau_druck_LW_B.pkl", "wb") as f:
    pickle.dump(grau_druck_LW_B, f)  
with open("grau_druck_LW_C.pkl", "wb") as f:
    pickle.dump(grau_druck_LW_C, f)  
with open("grau_druck_LW_D.pkl", "wb") as f:
    pickle.dump(grau_druck_LW_D, f) 
