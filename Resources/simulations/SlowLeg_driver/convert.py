import re

# Inserisci qui il percorso del tuo file se diverso
input_file = 'Eon_Eoff_circuit.log'
output_file = 'forward_circuit_125.csv'

targets = ['vds', 'ids', 'eon', 'eoff', 'vdsreal', 'idsreal', 'rdson']
data = {t: {} for t in targets}

with open(input_file, 'r') as f:
    current_meas = None
    for line in f:
        line = line.strip()
        # Identifica la misura
        m = re.match(r'^Measurement:\s+(\w+)', line)
        if m:
            current_meas = m.group(1).lower()
            continue
        
        # Estrae i dati (Step e Valore)
        if current_meas in targets:
            parts = line.split()
            if len(parts) >= 2 and parts[0].isdigit():
                step = int(parts[0])
                # Valore assoluto come richiesto
                val = abs(float(parts[1]))
                data[current_meas][step] = val

# Trova tutti gli step unici
all_steps = sorted(list(set().union(*(d.keys() for d in data.values()))))


# Costruisci tutte le righe
rows = []
for step in all_steps:
    row = {}
    for t in targets:
        val = data[t].get(step, 0.0)
        
        #inverti solo vds
        if t == 'vds':
            val = val
        
        if t == 'ids':
            val = val
        
        row[t] = val
        
    rows.append(row)

# Ordina per vds crescente
rows.sort(key=lambda x: x['vds'])

# Scrittura CSV
with open(output_file, 'w') as out:
    out.write(";".join(targets) + "\n")
    
    for row in rows:
        formatted = []
        for t in targets:
            val_str = f"{row[t]:g}".replace('.', ',')
            formatted.append(val_str)
        out.write(";".join(formatted) + "\n")

print(f"File '{output_file}' generato con successo!")
