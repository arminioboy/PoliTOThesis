import csv
import xml.etree.ElementTree as ET

def normalize_num(s):
    """Normalizza numero: virgola → punto + trim"""
    return f"{float(s.replace(',', '.')):.6g}"

def indent(elem, level=0):
    i = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        for child in elem:
            indent(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def generate_plecs_xml_2D(csv_file, output_file):
    data_eon = {}
    data_eoff = {}

    vds_set = set()
    ids_set = set()

    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f, delimiter=';')
        reader.fieldnames = [h.strip() for h in reader.fieldnames]

        for row in reader:
            vds = normalize_num(row["vds"])
            ids = normalize_num(row["ids"])
            eon = normalize_num(row["eon"])
            eoff = normalize_num(row["eoff"])

            vds_set.add(vds)
            ids_set.add(ids)

            if vds not in data_eon:
                data_eon[vds] = {}
                data_eoff[vds] = {}

            data_eon[vds][ids] = eon
            data_eoff[vds][ids] = eoff

    # ordinamento numerico ma mantenendo stringhe
    vds_values = sorted(vds_set, key=lambda x: float(x))
    ids_values = sorted(ids_set, key=lambda x: float(x))

    root = ET.Element("Root")

    def build_block(tag, data):
        block = ET.SubElement(root, tag)

        ET.SubElement(block, "ComputationMethod").text = "Table only"
        ET.SubElement(block, "CurrentAxis").text = " ".join(ids_values)
        ET.SubElement(block, "VoltageAxis").text = " ".join(vds_values)
        ET.SubElement(block, "TemperatureAxis").text = "25"

        energy = ET.SubElement(block, "Energy")
        temp = ET.SubElement(energy, "Temperature")

        for vds in vds_values:
            row_vals = []
            for ids in ids_values:
                if ids in data[vds]:
                    row_vals.append(data[vds][ids])
                else:
                    # ⚠️ punto mancante → fallback
                    row_vals.append("0")

            volt = ET.SubElement(temp, "Voltage")
            volt.text = " ".join(row_vals) + "\n"

    build_block("TurnOnLoss", data_eon)
    build_block("TurnOffLoss", data_eoff)

    indent(root)

    ET.ElementTree(root).write(output_file, encoding="utf-8", xml_declaration=True)

    print("XML generato correttamente")

generate_plecs_xml_2D("eon_eoff_GaN_125.csv","PLECS_thermals_125.xml")
