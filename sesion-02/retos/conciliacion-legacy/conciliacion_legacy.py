# conciliacion_legacy.py — script heredado (2017). Sin tests. Sin documentación.
# Concilia los movimientos del extracto del banco corresponsal contra el libro
# interno y reporta diferencias. Se ejecuta cada noche.
#
# Reto sugerido: modernizar este script con el ciclo AI SDLC (ver sesion-02/RETOS_SUGERIDOS.md).
# Todos los datos son sintéticos.

import csv, datetime

def proc(f1, f2, tol=0.01):
    a = {}
    b = {}
    r = []
    for x in csv.reader(open(f1)):
        if x[0] == 'ref': continue
        a[x[0]] = [float(x[1]), x[2], x[3]]
    for x in csv.reader(open(f2)):
        if x[0] == 'ref': continue
        b[x[0]] = [float(x[1]), x[2], x[3]]
    for k in a:
        if k in b:
            if abs(a[k][0] - b[k][0]) > tol:
                r.append([k, 'DIF_MONTO', a[k][0], b[k][0]])
            elif a[k][1] != b[k][1]:
                d1 = datetime.datetime.strptime(a[k][1], '%Y-%m-%d')
                d2 = datetime.datetime.strptime(b[k][1], '%d/%m/%Y')
                if abs((d1 - d2).days) > 1:
                    r.append([k, 'DIF_FECHA', a[k][1], b[k][1]])
        else:
            r.append([k, 'NO_EN_LIBRO', a[k][0], None])
    for k in b:
        if not k in a:
            r.append([k, 'NO_EN_EXTRACTO', None, b[k][0]])
    t = 0
    for i in r:
        if i[1] == 'DIF_MONTO':
            t = t + (i[2] - i[3])
    w = csv.writer(open('reporte_' + str(datetime.date.today()) + '.csv', 'w'))
    for i in r:
        w.writerow(i)
    print('diferencias:', len(r), 'neto:', t)
    return r

if __name__ == '__main__':
    proc('extracto.csv', 'libro.csv')
