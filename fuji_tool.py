from pdf2image import convert_from_path
import pandas as pd
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.widgets import EllipseSelector
from matplotlib.widgets import RectangleSelector
import matplotlib.patches as patches
import os
import pickle
import tkinter as tk
from tkinter import filedialog


# =========================
# PDF auswählen und einlesen / Select and read PDF
# =========================

def get_pdf_path():
    root = tk.Tk()
    root.withdraw()
        
    return filedialog.askopenfilename(
        title="PDF-Datei auswählen",
        filetypes=[("PDF-Dateien", "*.pdf")]
    )

pdf_path = get_pdf_path()
pdf_name = os.path.basename(pdf_path)
image = np.array(convert_from_path(pdf_path, dpi=600)[0]) # konvertieren und für Pixelverarbeitung numpy benutzen
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# =========================
# Auswertungsbereich (ROI) / Region of interest (ROI)
# =========================

dpi = 600
x_start = 0 * (dpi / 2.54)
y_start = 0 * (dpi / 2.54)

#roi_width = 14 * (dpi / 2.54)
#roi_height = 26 * (dpi / 2.54)

roi_height, roi_width = image.shape[:2]

# ROI aus Bild extrahieren
roi_gray = gray_image[int(y_start):int(y_start + roi_height), int(x_start):int(x_start + roi_width)]
roi_gray = np.clip(roi_gray, 0, 255).astype(np.uint8)
height, width = roi_gray.shape


# =========================
# Korrektur auf Basis eigener experimenteller Daten / Correction based on own experimental data
# =========================
Grauwert_LLW = np.array([251.3456579, 246.4634221, 239.1434627, 221.2427764,	198.5403707, 178.777219, 159.6124428, 148.0192441, 148.1838775	])
Druck_LLW = np.array([0.262, 0.495, 	0.750, 	1.000, 	1.499, 	1.979, 	2.236, 	2.485, 2.758])
Grauwert_LW = np.array([241.726431, 234.565818, 233.509683, 232.030294, 229.510452, 222.148043, 209.576974, 204.439670, 182.864279])
Druck_LW = np.array([2.240, 2.484, 	2.707, 	2.987, 	3.216, 	3.446, 	3.953, 	4.462, 	5.426])

# =========================
# Kalibrierung anhand der Herstellerangaben für LLW und LW / Calibration based on the manufacturer's specifications for LLW and LW
# =========================
with open("grau_druck_LLW_A.pkl", "rb") as f:
    grau_druck_LLW_A = pickle.load(f)
with open("grau_druck_LLW_B.pkl", "rb") as f:
    grau_druck_LLW_B = pickle.load(f)
with open("grau_druck_LLW_C.pkl", "rb") as f:
    grau_druck_LLW_C = pickle.load(f)
with open("grau_druck_LLW_D.pkl", "rb") as f:
    grau_druck_LLW_D = pickle.load(f)

with open("grau_druck_LW_A.pkl", "rb") as f:
    grau_druck_LW_A = pickle.load(f)
with open("grau_druck_LW_B.pkl", "rb") as f:
    grau_druck_LW_B = pickle.load(f)
with open("grau_druck_LW_C.pkl", "rb") as f:
    grau_druck_LW_C = pickle.load(f)
with open("grau_druck_LW_D.pkl", "rb") as f:
    grau_druck_LW_D = pickle.load(f)


# =========================
# Folientyp und Kalibrierungsmethode auswählen / Select film type and calibration method
# =========================
while True:
    film_type = selection = input(
    "[EN] Please select the desired film type: 1 = LW, 2 = LLW\n\n"
    "[DE] Bitte wählen Sie den gewünschten Folientyp aus: 1 = LW, 2 = LLW\n\n"
    "Selection / Auswahl: ").strip().upper()
    print("\n" + "-" * 60 + "\n")

    if film_type in ["1","LW"]:
        Dmax= 10
        Dmin= 2.5
        while True:
            data_type = input("[EN] Please select the calibration method: ""1 = manufacturer calibration, 2 = correction based on experimental data\n\n"
                              "[DE] Bitte wählen Sie die Kalibrierungsmethode aus: " "1 = Herstellerkalibrierung, 2 = Korrektur auf Basis experimenteller Daten\n\n"
                              "Selection / Auswahl: ").strip()
            print("\n" + "-" * 60 + "\n")

            if data_type == "2":
                coeffs = np.polyfit(Grauwert_LW, Druck_LW, 3)  
                break
            elif data_type == "1":
                while True:
                            Bedigung_type = input("[EN] Please select the measurement condition according to the manufacturer's specifications: ""A, B, C, or D\n\n"
                                                  "[DE] Bitte wählen Sie die Messbedingung gemäß den Herstellerangaben aus: ""A, B, C oder D\n\n"
                                                  "Selection / Auswahl: ").strip()
                            print("\n" + "-" * 60 + "\n")

                            if Bedigung_type in ["a","A"]:
                                coeffs = grau_druck_LW_A
                                break
                            elif Bedigung_type in ["b","B"]:
                                coeffs = grau_druck_LW_B
                                break
                            elif Bedigung_type in ["c","C"]:
                                coeffs = grau_druck_LW_C
                                break
                            elif Bedigung_type in ["d","D"]:
                                coeffs = grau_druck_LW_D
                                break
                            else:
                                print("Ungültige Eingabe, bitte erneut eingeben!")
                                continue                                                                 
                break
        break
    elif film_type in ["2","LLW"]:
        Dmax= 2.5
        Dmin= 0.5
        while True:
            data_type = input("[EN] Please select the calibration method: ""1 = manufacturer calibration, 2 = correction based on experimental data\n\n"
                              "[DE] Bitte wählen Sie die Kalibrierungsmethode aus: " "1 = Herstellerkalibrierung, 2 = Korrektur auf Basis experimenteller Daten\n\n"
                              "Selection / Auswahl:").strip()
            print("\n" + "-" * 60 + "\n")

            if data_type == "2":
                coeffs = np.polyfit(Grauwert_LW, Druck_LW, 3)  
                break
            elif data_type == "1":
                while True:
                            Bedigung_type = input("[EN] Please select the measurement condition according to the manufacturer's specifications: ""A, B, C, or D\n\n"
                                                  "[DE] Bitte wählen Sie die Messbedingung gemäß den Herstellerangaben aus: ""A, B, C oder D\n\n"
                                                  "Selection / Auswahl:").strip().upper()
                            print("\n" + "-" * 60 + "\n")
                            if Bedigung_type in ["a","A"]:
                                coeffs = grau_druck_LLW_A
                                break
                            elif Bedigung_type in ["b","B"]:
                                coeffs = grau_druck_LLW_B
                                break
                            elif Bedigung_type in ["c","C"]:
                                coeffs = grau_druck_LLW_C
                                break
                            elif Bedigung_type in ["d","D"]:
                                coeffs = grau_druck_LLW_D
                                break
                            else:
                                print("Ungültige Eingabe, bitte erneut eingeben!")
                                continue                                                                 
                break
        break
    else:
        print("[EN] Invalid input. Please try again!\n\n"
            "[DE] Ungültige Eingabe. Bitte versuchen Sie es erneut!")
        

# =========================
# Umrechnung von Grauwerten in Druckwerte / Conversion of grayscale values into pressure values
# =========================

pressure_matrix = np.polyval(coeffs, roi_gray)

plt.figure()
plt.imshow(pressure_matrix, cmap='jet', vmax=Dmax)
plt.colorbar(label="Pressure [MPa]")
plt.title(f"Pressure Matrix,{pdf_path}")
plt.axis('off')
manager = plt.get_current_fig_manager()
manager.window.state('zoomed')
plt.show()

# =========================
# Auswahl zwischen kreisförmigem und rechteckigem ROI-Werkzeug / Choose between the circular and rectangular ROI selection tools
# =========================

rec_coords = {}
circle_coords = {}

while True:
    selection_mode = input("[EN] Please select the ROI shape: rectangle (R) or circle (C)\n\n"
    "[DE] Bitte wählen Sie die ROI-Form aus: Rechteck (R) oder Kreis (K)\n\n"
    "Selection / Auswahl: ").strip().upper()
    

    if selection_mode == "R":
        print("[EN] Rectangle selected. Drag the mouse to select the ROI. "
                "Then press Enter to confirm.\n\n"
                "[DE] Rechteck ausgewählt. Ziehen Sie mit der Maus, um den ROI auszuwählen. "
                "Drücken Sie anschließend die Eingabetaste zur Bestätigung.")
        def draw_rectangle(eclick, erelease):

            x1, y1 = int(eclick.xdata), int(eclick.ydata)
            x2, y2 = int(erelease.xdata), int(erelease.ydata)
            rec_coords['x_start'], rec_coords['x_end'] = sorted([x1, x2])
            rec_coords['y_start'], rec_coords['y_end'] = sorted([y1, y2])

            #rect_size_px = 2.2 *600 /2.54
            #rec_coords['x_start'] = x1
            #rec_coords['y_start'] = y1
            #rec_coords['x_end'] = x1 + int(rect_size_px)
            #rec_coords['y_end'] = y1 + int(rect_size_px)
            
            rect_width = abs(x2 - x1)
            rect_height = abs(y2 - y1)

            while len(ax.patches) > 0:
                ax.patches[0].remove()

            rect = patches.Rectangle(
                (x1 , y1),
                abs(x2 - x1),
                abs(y2 - y1),
                #rect_size_px,
                #rect_size_px,

                linewidth=2,
                edgecolor='r',
                facecolor='none'
            )

            ax.add_patch(rect)
            plt.draw()


        def on_key(event):
            if event.key == 'enter':
                plt.close()

        fig, ax = plt.subplots()
        ax.imshow(roi_gray, cmap='gray')

        toggle_selector = RectangleSelector(ax, draw_rectangle,
                                            useblit=True,
                                            button=[1],
                                            minspanx=5, minspany=5,
                                            spancoords='pixels',
                                            interactive=True)
        
        fig.canvas.mpl_connect('key_press_event', on_key)
        manager = plt.get_current_fig_manager()
        manager.window.state('zoomed')
        plt.show()

        if not rec_coords:
            print("[EN] No ROI selected. Please select an area again.\n\n"
                "[DE] Kein ROI ausgewählt. Bitte wählen Sie erneut einen Bereich aus.")
            continue

        original_backend = mpl.get_backend()
        mask = np.zeros_like(roi_gray, dtype=np.uint8)

        cv2.rectangle(
            mask,
            (rec_coords['x_start'], rec_coords['y_start']),   
            (rec_coords['x_end'], rec_coords['y_end']),      
            255,
            -1
        )

        mask_bool = mask > 0
        break
    elif selection_mode in ["K","C"]:
        print("[EN] Circle selected. Drag the mouse to select the circular ROI. "
                "Then press Enter to confirm.\n\n"
                "[DE] Kreis ausgewählt. Ziehen Sie mit der Maus, um den kreisförmigen ROI auszuwählen. "
                "Drücken Sie anschließend die Eingabetaste zur Bestätigung.")

        def on_select(eclick, erelease):
            if eclick.xdata is None or eclick.ydata is None:
                return
            if erelease.xdata is None or erelease.ydata is None:
                return

            x1, y1 = eclick.xdata, eclick.ydata
            x2, y2 = erelease.xdata, erelease.ydata

            xc = (x1 + x2) / 2
            yc = (y1 + y2) / 2

            # radius = 23.55 * (dpi / 25.4) / 2
            radius = min(abs(x2 - x1), abs(y2 - y1)) / 2
            circle_coords["x_center"] = int(xc)
            circle_coords["y_center"] = int(yc)
            circle_coords["radius"] = int(radius)

            while len(ax.patches) > 0:
                ax.patches[0].remove()

            circle = patches.Circle(
                (xc, yc),
                radius,
                linewidth=2,
                edgecolor='r',
                facecolor='none'
            )
            ax.add_patch(circle)
            plt.draw()

        def on_key(event):
            if event.key == "enter":
                if circle_coords:
                    plt.close(event.canvas.figure)
            elif event.key == "escape":
                circle_coords.clear()
                while len(ax.patches) > 0:
                    ax.patches[0].remove()
                plt.draw()
                print("Zurückgesetzt")


        fig, ax = plt.subplots()
        ax.imshow(roi_gray, cmap="gray")


        selector = EllipseSelector(
            ax,
            on_select,
            useblit=True,
            button=[1],
            minspanx=5,
            minspany=5,
            spancoords="pixels",
            interactive=True,
            drag_from_anywhere=True
        )

        fig.canvas.mpl_connect('key_press_event', on_key)

        manager = plt.get_current_fig_manager()
        manager.window.state('zoomed')

        plt.show()

        if not circle_coords:
            print("[EN] No ROI selected. Please select an area again.\n\n"
                "[DE] Kein ROI ausgewählt. Bitte wählen Sie erneut einen Bereich aus.")
            continue


        original_backend = mpl.get_backend()
        mask = np.zeros_like(roi_gray, dtype=np.uint8)

        cv2.circle(
            mask,
            (circle_coords['x_center'], circle_coords['y_center']),
            circle_coords['radius'],
            255,
            -1
        )

        mask_bool = mask > 0
        break
    else:
        print( "[EN] Invalid selection. Please enter only 'R' or 'K'.\n\n"
                "[DE] Ungültige Auswahl. Bitte geben Sie nur 'R' oder 'K' ein.")

# =========================
# Druckwerte aus dem ROI extrahieren / Extract pressure values from the ROI
# =========================
    
act_values = pressure_matrix[mask_bool]
act_matrix_masked = np.where(mask_bool, pressure_matrix, np.nan)



# =========================
# Mittleren Druck sowie den Anteil der Druckwerte im gültigen Messbereich berechnen / Calculate the mean pressure and the proportion of pressure values within the valid measurement range
# =========================

rec_pressure_range = (Dmin, Dmax)

valid_mask = (act_values >= rec_pressure_range[0]) & (act_values <= rec_pressure_range[1])

n_in_range = valid_mask.sum()
n_total = act_values.size
pressure_eff = (n_in_range / n_total) * 100



above_percentage = ((act_values > Dmax).sum() / n_total) * 100
below_percentage = ((act_values < Dmin).sum() / n_total) * 100
avg_pressure_all = np.mean(act_values)



print("[EN] Results\n"
        f"Share of values within the valid pressure range ({Dmin:.2f} - {Dmax:.2f} MPa): {pressure_eff:.2f} %\n"
        f"Share of values >  {Dmax:.2f} MPa: {above_percentage:.2f} %\n"
        f"Share of values < {Dmin:.2f} MPa: {below_percentage:.2f} %\n"
        f"Mean pressure (alle Werte): {avg_pressure_all:.2f} MPa\n\n")



print("[DE] Ergebnisse\n"
        f"Anteil der Werte im gültigen Druckbereich ({Dmin:.2f} - {Dmax:.2f} MPa): {pressure_eff:.2f} %\n"
        f"Prozent der Werte > {Dmax:.2f} MPa: {above_percentage:.2f} %\n"
        f"Prozent der Werte < {Dmin:.2f} MPa: {below_percentage:.2f} %\n"
        f"Durchschnittlicher Druck (alle Werte): {avg_pressure_all:.2f} MPa")


plt.figure()
plt.imshow(act_matrix_masked, cmap="jet",vmax=Dmax)
plt.colorbar(label="Pressure [MPa]")
plt.title(f"Pressure Matrix – Selected Area {pdf_name}")
plt.axis('off')
plt.text(400, 4200, f"Prozent der Werte > {Dmax:.2f} MPa: {above_percentage:.2f} %")
plt.text(400, 4300, f"Prozent der Werte < {Dmin:.2f} MPa: {below_percentage:.2f} %")
plt.text(400, 4000, f"Pressure Efficiency ({Dmin:.2f} - {Dmax:.2f} MPa): {pressure_eff:.2f} %")
plt.text(400, 4100, f"Durchschnittlicher Druck in Active Area (alle Werte): {avg_pressure_all:.2f} MPa")
manager = plt.get_current_fig_manager()
manager.window.state('zoomed')
plt.show()
