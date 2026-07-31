# Python-Tool-for-Fuji-Prescale-LLW-and-LW-Pressure-Film-Analysis
This Python-based tool analyzes pressure distributions from scanned images of FUJIFILM Prescale LLW and LW pressure-sensitive films.

The repository includes two calibration datasets: one based on data provided by the manufacturer and another obtained experimentally under actual laboratory conditions at the institute.

This code was written by Bingzhong Jiang under the supervision of Moritz Stahl as part of a university research project (Studienarbeit) at Technische Universität Braunschweig.

Requirements

This program was developed and tested with Python 3.12.10.

On Windows, Poppler must also be installed. After installation, open Edit the system environment variables in the Windows settings and add the path to the bin folder of the Poppler installation directory to the system Path variable.

Installation
1. Create a virtual environment
python -m venv .venv
2. Activate the virtual environment

Windows:

.venv\Scripts\activate

3. Install the dependencies

pip install -r requirements.txt

4. Run the manufacturer calibration

First, run the following script:

python hersteller_kalibrierung.py

This script generates the calibration coefficients based on the manufacturer’s data. The diagrams displayed during execution are provided for overview purposes only and can be closed afterward.

5. Start the evaluation tool
python fuji_tool.py
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Dieses Python-basierte Tool analysiert Druckverteilungen anhand gescannter Bilder von druckempfindlichen FUJIFILM-Prescale-Folien der Typen LLW und LW.

Das Repository enthält zwei Kalibrierdatensätze: einen auf Grundlage der Herstellerangaben und einen weiteren, der experimentell unter realen Laborbedingungen am Institut ermittelt wurde.

Der Code wurde von Bingzhong Jiang unter der Betreuung von Moritz Stahl im Rahmen einer Studienarbeit an der Technischen Universität Braunschweig entwickelt.

Voraussetzungen：

Dieses Programm wurde mit Python 3.12.10 entwickelt und getestet.

Unter Windows muss zusätzlich Poppler installiert werden. Öffnen Sie anschließend in den Windows-Einstellungen die Option „Systemumgebungsvariablen bearbeiten“ und fügen Sie den Pfad zum bin-Ordner des Poppler-Installationsverzeichnisses zur Systemvariable Path hinzu.

Installation：

1. Virtuelle Umgebung erstellen

python -m venv .venv

3. Virtuelle Umgebung aktivieren

Windows:

.venv\Scripts\activate

3. Abhängigkeiten installieren
   
pip install -r requirements.txt

4. Herstellerkalibrierung durchführen

Führen Sie zunächst das folgende Skript aus:

python hersteller_kalibrierung.py

Dieses Skript erzeugt die Kalibrierkoeffizienten auf Grundlage der Herstellerangaben. Die während der Ausführung angezeigten Diagramme dienen lediglich der Übersicht und können anschließend geschlossen werden.

5. Auswertungstool starten

python fuji_tool.py
