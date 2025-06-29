import pandas as pd
import re
import os
import glob
import pdfplumber
from datetime import datetime
def llegir_ticket(ruta):
    dades = []
    data = None
    total = None

    with pdfplumber.open(ruta) as pdf:
        for pag in pdf.pages:
            text = pag.extract_text()
            if text:
                for linia in text.split('\n'):
                    if not data:
                        d = re.search(r'(\d{2}/\d{2}/\d{4})', linia)
                        if d:
                            try:
                                data = datetime.strptime(d.group(1), '%d/%m/%Y').strftime('%Y-%m-%d')
                            except:
                                pass

                    p1 = re.match(r'^(\d+)\s+([A-ZÀ-ÿ\s\.\-]+)\s+(\d+,\d+)\s*(\d+,\d+)?$', linia)
                    if p1:
                        q, nom, pu, pt = p1.groups()
                        if not pt:
                            pt = pu
                        dades.append([data, nom.strip(), int(q), float(pu.replace(',', '.')), float(pt.replace(',', '.'))])
                        continue

                    p2 = re.match(r'^([A-ZÀ-ÿ\s\.\-]+)\s+(\d+,\d+) kg\s+(\d+,\d+) €/kg\s+(\d+,\d+)$', linia)
                    if p2:
                        nom, pes, preu_kg, pt = p2.groups()
                        dades.append([data, nom.strip(), float(pes.replace(',', '.')), float(preu_kg.replace(',', '.')), float(pt.replace(',', '.'))])
                        continue

                    if not total:
                        t1 = re.search(r'TOTAL \(€\)\s+(\d+,\d+)', linia)
                        if t1:
                            total = float(t1.group(1).replace(',', '.'))
                        else:
                            t2 = re.search(r'TARGETA BANCÀRIA\s+(\d+,\d+)', linia)
                            if t2:
                                total = float(t2.group(1).replace(',', '.'))

    df = pd.DataFrame(dades, columns=["Fecha", "Producto", "Cantidad/Peso", "Precio Unidad", "Total"])
    df['Importe Total Ticket'] = total if total else None
    return df


carpeta = r"C:\Users\crist\OneDrive\Documents\GitHub\Analisi-de-dades-mitjansant-Business-Intelligence-Un-estudi-de-casos-practics\codi\Mercadona"
sortida = "ticket_dataset.csv"

existeix = os.path.exists(sortida)
llista = glob.glob(os.path.join(carpeta, "*.pdf"))

for arxiu in llista:
    try:
        df = llegir_ticket(arxiu)
        df.to_csv(sortida, mode='a', index=False, header=not existeix)
        existeix = True
    except Exception as e:
        print(e)
