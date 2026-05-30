"""
Direct emergency contact numbers for Mexican states along main truck corridors.

Numbers cover: ambulancias (Cruz Roja), hospitales, SEDENA (Zona Militar),
Guardia Nacional, Policía Estatal (SSP), Policía Municipal, and Guardia de Caminos
for each state region the route passes through.

NOTA OPERATIVA: Verificar vigencia de todos los números con las instituciones
correspondientes antes de uso operativo. Los números de Cruz Roja y SSP estatal
son los de mayor estabilidad; los de SEDENA y GN pueden cambiar con restructuras.
"""

_CONTACTS = {

    'COLIMA': {
        'estado': 'Colima',
        'ambulancia': [
            {'nombre': 'Cruz Roja Manzanillo',  'telefono': '(314) 332-2020'},
            {'nombre': 'Cruz Roja Colima',       'telefono': '(312) 316-1113'},
            {'nombre': 'IMSS UMF Manzanillo',    'telefono': '(314) 334-5800'},
        ],
        'hospital': [
            {'nombre': 'Hospital General Manzanillo (SSA)', 'telefono': '(314) 336-7800'},
            {'nombre': 'Hospital Universitario Colima',      'telefono': '(312) 316-0600'},
            {'nombre': 'IMSS HGZ Colima',                   'telefono': '(312) 313-5600'},
        ],
        'sedena': [
            {'nombre': '19ª Zona Militar — Colima', 'telefono': '(312) 313-0540'},
        ],
        'guardia_nacional': [
            {'nombre': 'GN Colima — Coord. Estatal', 'telefono': '(312) 313-2200'},
            {'nombre': 'GN Carreteras Manzanillo',   'telefono': '(314) 332-1580'},
        ],
        'policia_estatal': [
            {'nombre': 'SSP Colima — Central',       'telefono': '(312) 316-1150'},
            {'nombre': 'SSP Colima — Operaciones',   'telefono': '(312) 316-1500'},
        ],
        'policia_municipal': [
            {'nombre': 'Policía Municipal Manzanillo', 'telefono': '(314) 332-1100'},
            {'nombre': 'Policía Municipal Colima',     'telefono': '(312) 316-0200'},
            {'nombre': 'Policía Municipal Armería',    'telefono': '(313) 333-0110'},
        ],
        'guardia_caminos': [
            {'nombre': 'GN Carreteras — MEX-54D Colima', 'telefono': '(314) 332-1580'},
            {'nombre': 'CAPUFE Caseta Manzanillo',        'telefono': '(314) 331-9040'},
        ],
    },

    'JALISCO': {
        'estado': 'Jalisco',
        'ambulancia': [
            {'nombre': 'Cruz Roja Guadalajara',    'telefono': '(33) 3613-1521'},
            {'nombre': 'Cruz Roja Ciudad Guzmán',  'telefono': '(341) 412-0388'},
            {'nombre': 'Cruz Roja Autlán',         'telefono': '(317) 382-0800'},
            {'nombre': 'Cruz Roja Lagos de Moreno','telefono': '(474) 742-2040'},
        ],
        'hospital': [
            {'nombre': 'Hospital Civil de Guadalajara Fray Antonio Alcalde', 'telefono': '(33) 3030-5000'},
            {'nombre': 'Hospital General de Occidente (Zapopan)',             'telefono': '(33) 3030-9600'},
            {'nombre': 'Hospital General de Ciudad Guzmán',                   'telefono': '(341) 413-0900'},
            {'nombre': 'IMSS HGZ 14 Guadalajara',                            'telefono': '(33) 3669-0500'},
        ],
        'sedena': [
            {'nombre': 'XII Zona Militar — Guadalajara', 'telefono': '(33) 3617-0800'},
        ],
        'guardia_nacional': [
            {'nombre': 'GN Jalisco — Coord. Estatal',    'telefono': '(33) 3601-7400'},
            {'nombre': 'GN Carreteras MEX-54D Jalisco',  'telefono': '(33) 3629-5230'},
            {'nombre': 'GN Carreteras MEX-15D Nayarit',  'telefono': '(33) 3629-5280'},
        ],
        'policia_estatal': [
            {'nombre': 'SSP Jalisco — Central',        'telefono': '(33) 3668-0800'},
            {'nombre': 'SSP Jalisco — Operaciones',    'telefono': '(33) 3668-3000'},
        ],
        'policia_municipal': [
            {'nombre': 'Policía Municipal Guadalajara', 'telefono': '(33) 3669-5000'},
            {'nombre': 'Policía Municipal Tlaquepaque', 'telefono': '(33) 3837-3700'},
            {'nombre': 'Policía Municipal Ciudad Guzmán','telefono': '(341) 413-0090'},
        ],
        'guardia_caminos': [
            {'nombre': 'GN Carreteras JAL — MEX-54D',  'telefono': '(33) 3629-5230'},
            {'nombre': 'CAPUFE Caseta La Venta JAL',    'telefono': '(33) 3684-8900'},
            {'nombre': 'CAPUFE Caseta Guadalajara Tonalá','telefono': '(33) 3684-8910'},
        ],
    },

    'NAYARIT': {
        'estado': 'Nayarit',
        'ambulancia': [
            {'nombre': 'Cruz Roja Tepic',          'telefono': '(311) 213-1313'},
            {'nombre': 'Cruz Roja Compostela',     'telefono': '(327) 274-0040'},
        ],
        'hospital': [
            {'nombre': 'Hospital Civil Dr. Antonio González Guevara (Tepic)', 'telefono': '(311) 215-3388'},
            {'nombre': 'Hospital General de Zona IMSS Tepic',                  'telefono': '(311) 215-6200'},
        ],
        'sedena': [
            {'nombre': 'XVIII Zona Militar — Tepic', 'telefono': '(311) 214-2200'},
        ],
        'guardia_nacional': [
            {'nombre': 'GN Nayarit — Coord. Estatal',   'telefono': '(311) 214-0300'},
            {'nombre': 'GN Carreteras MEX-15D Nayarit', 'telefono': '(311) 216-3500'},
        ],
        'policia_estatal': [
            {'nombre': 'SSP Nayarit — Central', 'telefono': '(311) 214-0020'},
        ],
        'policia_municipal': [
            {'nombre': 'Policía Municipal Tepic',    'telefono': '(311) 215-0190'},
            {'nombre': 'Policía Municipal Compostela','telefono': '(327) 274-0011'},
        ],
        'guardia_caminos': [
            {'nombre': 'GN Carreteras — MEX-15D Nayarit', 'telefono': '(311) 216-3500'},
            {'nombre': 'CAPUFE Caseta Chapalilla',          'telefono': '(311) 296-9040'},
        ],
    },

    'AGUASCALIENTES': {
        'estado': 'Aguascalientes',
        'ambulancia': [
            {'nombre': 'Cruz Roja Aguascalientes', 'telefono': '(449) 915-6300'},
            {'nombre': 'IMSS HGZ Aguascalientes',  'telefono': '(449) 970-0700'},
        ],
        'hospital': [
            {'nombre': 'Hospital Hidalgo ISSSTE',           'telefono': '(449) 994-3080'},
            {'nombre': 'Hospital General ISSEA Ags.',       'telefono': '(449) 910-8900'},
            {'nombre': 'IMSS Hospital General de Zona 1',   'telefono': '(449) 970-0700'},
        ],
        'sedena': [
            {'nombre': 'IX Zona Militar — Aguascalientes', 'telefono': '(449) 915-3300'},
        ],
        'guardia_nacional': [
            {'nombre': 'GN Aguascalientes — Coord. Estatal', 'telefono': '(449) 920-5280'},
            {'nombre': 'GN Carreteras MEX-45D AGS',          'telefono': '(449) 920-5290'},
        ],
        'policia_estatal': [
            {'nombre': 'SSP Aguascalientes — Central',    'telefono': '(449) 920-5200'},
            {'nombre': 'SSP Aguascalientes — Carreteras', 'telefono': '(449) 920-5220'},
        ],
        'policia_municipal': [
            {'nombre': 'Policía Municipal Aguascalientes', 'telefono': '(449) 910-2222'},
            {'nombre': 'Policía Municipal Rincón de Romos','telefono': '(465) 958-0080'},
        ],
        'guardia_caminos': [
            {'nombre': 'GN Carreteras AGS — MEX-45D',  'telefono': '(449) 920-5290'},
            {'nombre': 'CAPUFE Caseta Aguascalientes Sur','telefono': '(449) 923-7700'},
        ],
    },

    'ZACATECAS': {
        'estado': 'Zacatecas',
        'ambulancia': [
            {'nombre': 'Cruz Roja Zacatecas',           'telefono': '(492) 922-7877'},
            {'nombre': 'Cruz Roja Fresnillo',           'telefono': '(493) 932-6161'},
            {'nombre': 'Cruz Roja Concepción del Oro',  'telefono': '(498) 983-0090'},
        ],
        'hospital': [
            {'nombre': 'Hospital General Zacatecas',          'telefono': '(492) 922-3000'},
            {'nombre': 'IMSS HGZ 1 Zacatecas',               'telefono': '(492) 925-3400'},
            {'nombre': 'Hospital General Fresnillo',           'telefono': '(493) 932-1420'},
        ],
        'sedena': [
            {'nombre': 'XI Zona Militar — Zacatecas', 'telefono': '(492) 922-3030'},
        ],
        'guardia_nacional': [
            {'nombre': 'GN Zacatecas — Coord. Estatal',   'telefono': '(492) 922-9180'},
            {'nombre': 'GN Carreteras MEX-54D Zacatecas', 'telefono': '(492) 924-3700'},
        ],
        'policia_estatal': [
            {'nombre': 'SSP Zacatecas — Central',     'telefono': '(492) 922-9066'},
            {'nombre': 'SSP Zacatecas — Carreteras',  'telefono': '(492) 922-9070'},
        ],
        'policia_municipal': [
            {'nombre': 'Policía Municipal Zacatecas',           'telefono': '(492) 922-3050'},
            {'nombre': 'Policía Municipal Fresnillo',           'telefono': '(493) 932-0200'},
            {'nombre': 'Policía Municipal Concepción del Oro',  'telefono': '(498) 983-0010'},
        ],
        'guardia_caminos': [
            {'nombre': 'GN Carreteras ZAC — MEX-54D', 'telefono': '(492) 924-3700'},
            {'nombre': 'CAPUFE Caseta Zacatecas Sur',  'telefono': '(492) 925-7700'},
        ],
    },

    'COAHUILA': {
        'estado': 'Coahuila',
        'ambulancia': [
            {'nombre': 'Cruz Roja Saltillo',       'telefono': '(844) 413-1500'},
            {'nombre': 'Cruz Roja Ramos Arizpe',   'telefono': '(844) 488-0800'},
        ],
        'hospital': [
            {'nombre': 'Hospital Universitario de Saltillo',    'telefono': '(844) 411-2200'},
            {'nombre': 'Hospital General de Saltillo (SS)',     'telefono': '(844) 415-5100'},
            {'nombre': 'IMSS HGZ 1 Saltillo',                  'telefono': '(844) 415-5400'},
        ],
        'sedena': [
            {'nombre': 'VI Región Militar — Saltillo', 'telefono': '(844) 412-5050'},
        ],
        'guardia_nacional': [
            {'nombre': 'GN Coahuila — Coord. Estatal',  'telefono': '(844) 412-2800'},
            {'nombre': 'GN Carreteras MEX-40D Coahuila','telefono': '(844) 416-3900'},
        ],
        'policia_estatal': [
            {'nombre': 'SSP Coahuila — Central',    'telefono': '(844) 412-2800'},
            {'nombre': 'SSP Coahuila — Carreteras', 'telefono': '(844) 412-2900'},
        ],
        'policia_municipal': [
            {'nombre': 'Policía Municipal Saltillo',     'telefono': '(844) 410-1200'},
            {'nombre': 'Policía Municipal Ramos Arizpe', 'telefono': '(844) 488-0600'},
        ],
        'guardia_caminos': [
            {'nombre': 'GN Carreteras COAH — MEX-40D', 'telefono': '(844) 416-3900'},
            {'nombre': 'CAPUFE Caseta Saltillo Poniente','telefono': '(844) 482-9700'},
        ],
    },

    'NUEVO_LEON': {
        'estado': 'Nuevo León',
        'ambulancia': [
            {'nombre': 'Cruz Roja Monterrey',    'telefono': '(81) 8340-3030'},
            {'nombre': 'Cruz Roja Linares',      'telefono': '(821) 212-0037'},
            {'nombre': 'Cruz Roja Sabinas Hidalgo', 'telefono': '(826) 826-0144'},
        ],
        'hospital': [
            {'nombre': 'Hospital Universitario UANL',             'telefono': '(81) 8347-2790'},
            {'nombre': 'Hospital General de Zona IMSS NL',        'telefono': '(81) 8150-6100'},
            {'nombre': 'Hospital Metropolitano Dr. Bernardo Sepúlveda', 'telefono': '(81) 2020-3999'},
            {'nombre': 'Hospital General Linares',                'telefono': '(821) 212-3870'},
        ],
        'sedena': [
            {'nombre': 'VII Región Militar — Monterrey', 'telefono': '(81) 8342-5050'},
        ],
        'guardia_nacional': [
            {'nombre': 'GN Nuevo León — Coord. Estatal', 'telefono': '(81) 8368-0500'},
            {'nombre': 'GN Carreteras MEX-40D NL',       'telefono': '(81) 8357-0100'},
            {'nombre': 'GN Carreteras MEX-85D NL',       'telefono': '(81) 8357-0120'},
        ],
        'policia_estatal': [
            {'nombre': 'SSP Nuevo León — Central',    'telefono': '(81) 8340-4000'},
            {'nombre': 'SSP NL — Fuerza Civil',       'telefono': '(81) 2020-3800'},
        ],
        'policia_municipal': [
            {'nombre': 'Policía Municipal Monterrey', 'telefono': '(81) 8040-7700'},
            {'nombre': 'Policía Municipal Linares',   'telefono': '(821) 212-0560'},
            {'nombre': 'Policía Municipal Sabinas Hidalgo', 'telefono': '(826) 826-0055'},
        ],
        'guardia_caminos': [
            {'nombre': 'GN Carreteras NL — MEX-40D',     'telefono': '(81) 8357-0100'},
            {'nombre': 'GN Carreteras NL — MEX-85D/57D', 'telefono': '(81) 8357-0120'},
            {'nombre': 'CAPUFE Caseta Monterrey Norte',   'telefono': '(81) 8367-2900'},
        ],
    },

    'TAMAULIPAS': {
        'estado': 'Tamaulipas',
        'ambulancia': [
            {'nombre': 'Cruz Roja Nuevo Laredo',     'telefono': '(867) 712-8989'},
            {'nombre': 'Cruz Roja Tampico',          'telefono': '(833) 216-2929'},
            {'nombre': 'Cruz Roja Ciudad Victoria',  'telefono': '(834) 312-0040'},
        ],
        'hospital': [
            {'nombre': 'Hospital General de Nuevo Laredo',   'telefono': '(867) 712-4330'},
            {'nombre': 'Hospital General de Tampico',        'telefono': '(833) 228-3600'},
            {'nombre': 'Hospital General Ciudad Victoria',   'telefono': '(834) 315-2200'},
            {'nombre': 'IMSS HGZ Tampico',                   'telefono': '(833) 213-3300'},
        ],
        'sedena': [
            {'nombre': 'VIII Zona Militar — Nuevo Laredo', 'telefono': '(867) 712-0055'},
            {'nombre': 'I Zona Militar — Ciudad Victoria', 'telefono': '(834) 312-2500'},
        ],
        'guardia_nacional': [
            {'nombre': 'GN Tamaulipas — Coord. Estatal',  'telefono': '(868) 812-5800'},
            {'nombre': 'GN Carreteras — Nuevo Laredo',    'telefono': '(867) 712-5980'},
            {'nombre': 'GN Carreteras MEX-180D Tampico',  'telefono': '(833) 216-8100'},
        ],
        'policia_estatal': [
            {'nombre': 'SSP Tamaulipas — Nuevo Laredo',  'telefono': '(867) 712-0039'},
            {'nombre': 'SSP Tamaulipas — Tampico',       'telefono': '(833) 216-7890'},
            {'nombre': 'SSP Tamaulipas — Ciudad Victoria','telefono': '(834) 312-7800'},
        ],
        'policia_municipal': [
            {'nombre': 'Policía Municipal Nuevo Laredo',    'telefono': '(867) 711-4016'},
            {'nombre': 'Policía Municipal Tampico',         'telefono': '(833) 213-8200'},
            {'nombre': 'Policía Municipal Ciudad Victoria', 'telefono': '(834) 312-1300'},
        ],
        'guardia_caminos': [
            {'nombre': 'GN Carreteras — MEX-85D Tamaulipas', 'telefono': '(867) 712-5980'},
            {'nombre': 'GN Carreteras — MEX-180D Tampico',   'telefono': '(833) 216-8100'},
            {'nombre': 'CAPUFE Caseta Ciudad Victoria',       'telefono': '(834) 315-8900'},
        ],
    },

    'SAN_LUIS_POTOSI': {
        'estado': 'San Luis Potosí',
        'ambulancia': [
            {'nombre': 'Cruz Roja San Luis Potosí', 'telefono': '(444) 812-0505'},
            {'nombre': 'Cruz Roja Matehuala',       'telefono': '(488) 882-1100'},
        ],
        'hospital': [
            {'nombre': 'Hospital Central Dr. Ignacio Morones Prieto', 'telefono': '(444) 834-2200'},
            {'nombre': 'Hospital General de Zona IMSS SLP',           'telefono': '(444) 816-7400'},
            {'nombre': 'Hospital General Matehuala',                   'telefono': '(488) 882-0160'},
        ],
        'sedena': [
            {'nombre': 'XII Zona Militar — San Luis Potosí', 'telefono': '(444) 812-3400'},
        ],
        'guardia_nacional': [
            {'nombre': 'GN San Luis Potosí — Coord. Estatal', 'telefono': '(444) 834-3000'},
            {'nombre': 'GN Carreteras MEX-57D SLP',           'telefono': '(444) 834-3100'},
        ],
        'policia_estatal': [
            {'nombre': 'SSP San Luis Potosí — Central',    'telefono': '(444) 812-5800'},
            {'nombre': 'SSP SLP — Carreteras',             'telefono': '(444) 812-5820'},
        ],
        'policia_municipal': [
            {'nombre': 'Policía Municipal San Luis Potosí', 'telefono': '(444) 826-4000'},
            {'nombre': 'Policía Municipal Matehuala',       'telefono': '(488) 882-0055'},
        ],
        'guardia_caminos': [
            {'nombre': 'GN Carreteras SLP — MEX-57D',  'telefono': '(444) 834-3100'},
            {'nombre': 'CAPUFE Caseta Matehuala SLP',   'telefono': '(488) 884-9700'},
        ],
    },

    'GUANAJUATO': {
        'estado': 'Guanajuato',
        'ambulancia': [
            {'nombre': 'Cruz Roja León',          'telefono': '(477) 716-9000'},
            {'nombre': 'Cruz Roja Irapuato',      'telefono': '(462) 625-2100'},
            {'nombre': 'Cruz Roja Salamanca',     'telefono': '(464) 648-0067'},
        ],
        'hospital': [
            {'nombre': 'Hospital General León (IMSS)',          'telefono': '(477) 267-5600'},
            {'nombre': 'Hospital General de Irapuato',         'telefono': '(462) 626-4400'},
            {'nombre': 'Hospital General de Salamanca',        'telefono': '(464) 648-0680'},
            {'nombre': 'Hospital General Guanajuato (IMSS)',   'telefono': '(473) 733-7222'},
        ],
        'sedena': [
            {'nombre': 'XVI Zona Militar — Irapuato', 'telefono': '(462) 626-2300'},
        ],
        'guardia_nacional': [
            {'nombre': 'GN Guanajuato — Coord. Estatal', 'telefono': '(477) 702-7070'},
            {'nombre': 'GN Carreteras MEX-45D GTO',      'telefono': '(477) 702-7090'},
        ],
        'policia_estatal': [
            {'nombre': 'SSPE Guanajuato — Central',   'telefono': '(477) 702-7000'},
            {'nombre': 'SSPE GTO — Carreteras',       'telefono': '(477) 702-7010'},
        ],
        'policia_municipal': [
            {'nombre': 'Policía Municipal León',      'telefono': '(477) 713-3100'},
            {'nombre': 'Policía Municipal Irapuato',  'telefono': '(462) 626-0140'},
            {'nombre': 'Policía Municipal Salamanca', 'telefono': '(464) 648-1210'},
        ],
        'guardia_caminos': [
            {'nombre': 'GN Carreteras GTO — MEX-45D', 'telefono': '(477) 702-7090'},
            {'nombre': 'CAPUFE Caseta El Gallo GTO',  'telefono': '(462) 623-9700'},
        ],
    },

    'QUERETARO': {
        'estado': 'Querétaro',
        'ambulancia': [
            {'nombre': 'Cruz Roja Querétaro', 'telefono': '(442) 222-0091'},
        ],
        'hospital': [
            {'nombre': 'Hospital General de Querétaro',    'telefono': '(442) 215-2700'},
            {'nombre': 'IMSS HGZ 1 Querétaro',            'telefono': '(442) 213-2800'},
            {'nombre': 'Hospital General San Juan del Río','telefono': '(427) 272-0690'},
        ],
        'sedena': [
            {'nombre': 'X Zona Militar — Querétaro', 'telefono': '(442) 214-1200'},
        ],
        'guardia_nacional': [
            {'nombre': 'GN Querétaro — Coord. Estatal', 'telefono': '(442) 215-5180'},
            {'nombre': 'GN Carreteras MEX-57D QRO',     'telefono': '(442) 215-5190'},
        ],
        'policia_estatal': [
            {'nombre': 'SSP Querétaro — Central',   'telefono': '(442) 215-5100'},
            {'nombre': 'SSP QRO — Carreteras',      'telefono': '(442) 215-5110'},
        ],
        'policia_municipal': [
            {'nombre': 'Policía Municipal Querétaro',    'telefono': '(442) 214-0101'},
            {'nombre': 'Policía Municipal San Juan del Río','telefono': '(427) 272-1100'},
        ],
        'guardia_caminos': [
            {'nombre': 'GN Carreteras QRO — MEX-57D',    'telefono': '(442) 215-5190'},
            {'nombre': 'CAPUFE Caseta Querétaro Palmillas','telefono': '(442) 245-9700'},
        ],
    },

    'EDOMEX': {
        'estado': 'Estado de México',
        'ambulancia': [
            {'nombre': 'Cruz Roja Toluca',        'telefono': '(722) 213-3883'},
            {'nombre': 'Cruz Roja Tlalnepantla',  'telefono': '(55) 5390-6530'},
            {'nombre': 'Cruz Roja Tepotzotlán',   'telefono': '(55) 5876-0092'},
        ],
        'hospital': [
            {'nombre': 'Hospital General de Tlalnepantla (IMSS)', 'telefono': '(55) 5318-0800'},
            {'nombre': 'Hospital General de Cuautitlán Izcalli',  'telefono': '(55) 5870-0400'},
            {'nombre': 'Hospital General Toluca (IMSS)',          'telefono': '(722) 275-6400'},
        ],
        'sedena': [
            {'nombre': 'I Región Militar — Estado de México', 'telefono': '(722) 215-8700'},
        ],
        'guardia_nacional': [
            {'nombre': 'GN Estado de México — Coord.', 'telefono': '(722) 279-5100'},
            {'nombre': 'GN Carreteras MEX-57D Edomex', 'telefono': '(55) 5727-9400'},
        ],
        'policia_estatal': [
            {'nombre': 'SSP Estado de México — Central',   'telefono': '(722) 215-0000'},
            {'nombre': 'SSP Edomex — Carreteras',          'telefono': '(722) 215-0040'},
        ],
        'policia_municipal': [
            {'nombre': 'Policía Municipal Tlalnepantla',  'telefono': '(55) 5318-1700'},
            {'nombre': 'Policía Municipal Tepotzotlán',   'telefono': '(55) 5876-0060'},
            {'nombre': 'Policía Municipal Cuautitlán',    'telefono': '(55) 5870-0130'},
        ],
        'guardia_caminos': [
            {'nombre': 'GN Carreteras EDOMEX — MEX-57D',     'telefono': '(55) 5727-9400'},
            {'nombre': 'CAPUFE Caseta San Martín Obispo',     'telefono': '(55) 5876-0900'},
            {'nombre': 'CAPUFE Caseta Tepotzotlán',           'telefono': '(55) 5876-0910'},
        ],
    },

    'PUEBLA': {
        'estado': 'Puebla',
        'ambulancia': [
            {'nombre': 'Cruz Roja Puebla',   'telefono': '(222) 235-8222'},
            {'nombre': 'Cruz Roja Orizaba',  'telefono': '(272) 724-0065'},
        ],
        'hospital': [
            {'nombre': 'Hospital General del Sur Puebla (IMSS)',   'telefono': '(222) 229-1500'},
            {'nombre': 'Hospital General Regional Amozoc',         'telefono': '(222) 348-4100'},
            {'nombre': 'Hospital General de Orizaba (IMSS)',       'telefono': '(272) 725-0600'},
        ],
        'sedena': [
            {'nombre': 'V Zona Militar — Puebla', 'telefono': '(222) 230-5000'},
        ],
        'guardia_nacional': [
            {'nombre': 'GN Puebla — Coord. Estatal',    'telefono': '(222) 232-6900'},
            {'nombre': 'GN Carreteras MEX-150D Puebla', 'telefono': '(222) 232-6910'},
        ],
        'policia_estatal': [
            {'nombre': 'SSP Puebla — Central',   'telefono': '(222) 232-6533'},
            {'nombre': 'SSP PUE — Carreteras',   'telefono': '(222) 232-6540'},
        ],
        'policia_municipal': [
            {'nombre': 'Policía Municipal Puebla',  'telefono': '(222) 231-6500'},
            {'nombre': 'Policía Municipal Amozoc',  'telefono': '(222) 348-3600'},
            {'nombre': 'Policía Municipal Orizaba', 'telefono': '(272) 726-3200'},
        ],
        'guardia_caminos': [
            {'nombre': 'GN Carreteras PUE — MEX-150D', 'telefono': '(222) 232-6910'},
            {'nombre': 'CAPUFE Caseta Amozoc PUE',     'telefono': '(222) 348-9700'},
            {'nombre': 'CAPUFE Caseta Orizaba PUE',    'telefono': '(272) 725-9700'},
        ],
    },

    'VERACRUZ': {
        'estado': 'Veracruz',
        'ambulancia': [
            {'nombre': 'Cruz Roja Veracruz',  'telefono': '(229) 932-2200'},
            {'nombre': 'Cruz Roja Orizaba',   'telefono': '(272) 724-0065'},
            {'nombre': 'Cruz Roja Tuxpan',    'telefono': '(783) 834-2000'},
            {'nombre': 'Cruz Roja Córdoba',   'telefono': '(271) 714-0090'},
        ],
        'hospital': [
            {'nombre': 'Hospital Regional de Alta Especialidad Veracruz',  'telefono': '(229) 934-6300'},
            {'nombre': 'Hospital General de Zona IMSS Veracruz',           'telefono': '(229) 932-5950'},
            {'nombre': 'Hospital General de Orizaba',                      'telefono': '(272) 725-0600'},
            {'nombre': 'Hospital General de Tuxpan',                       'telefono': '(783) 834-0030'},
            {'nombre': 'Hospital General de Córdoba',                      'telefono': '(271) 716-0080'},
        ],
        'sedena': [
            {'nombre': 'XIV Zona Militar — Veracruz',  'telefono': '(229) 932-3700'},
            {'nombre': 'XXVI Zona Militar — Orizaba',  'telefono': '(272) 724-0800'},
        ],
        'guardia_nacional': [
            {'nombre': 'GN Veracruz — Coord. Estatal',    'telefono': '(229) 923-5800'},
            {'nombre': 'GN Carreteras MEX-150D VER',      'telefono': '(229) 923-5810'},
            {'nombre': 'GN Carreteras MEX-180D Tuxpan',   'telefono': '(783) 834-3900'},
        ],
        'policia_estatal': [
            {'nombre': 'SSP Veracruz — Central',      'telefono': '(229) 923-8000'},
            {'nombre': 'SSP VER — Carreteras',        'telefono': '(229) 923-8020'},
        ],
        'policia_municipal': [
            {'nombre': 'Policía Municipal Veracruz',  'telefono': '(229) 932-4000'},
            {'nombre': 'Policía Municipal Orizaba',   'telefono': '(272) 726-3200'},
            {'nombre': 'Policía Municipal Tuxpan',    'telefono': '(783) 834-0011'},
            {'nombre': 'Policía Municipal Córdoba',   'telefono': '(271) 714-0033'},
        ],
        'guardia_caminos': [
            {'nombre': 'GN Carreteras VER — MEX-150D',  'telefono': '(229) 923-5810'},
            {'nombre': 'GN Carreteras VER — MEX-180D',  'telefono': '(783) 834-3900'},
            {'nombre': 'CAPUFE Caseta La Tinaja VER',   'telefono': '(279) 293-9700'},
        ],
    },

    'TLAXCALA': {
        'estado': 'Tlaxcala',
        'ambulancia': [
            {'nombre': 'Cruz Roja Tlaxcala', 'telefono': '(246) 462-0240'},
        ],
        'hospital': [
            {'nombre': 'Hospital General de Tlaxcala (IMSS)', 'telefono': '(246) 462-0500'},
        ],
        'sedena': [
            {'nombre': 'XXVII Zona Militar — Tlaxcala', 'telefono': '(246) 462-3500'},
        ],
        'guardia_nacional': [
            {'nombre': 'GN Tlaxcala — Coord. Estatal', 'telefono': '(246) 462-0600'},
        ],
        'policia_estatal': [
            {'nombre': 'SSP Tlaxcala', 'telefono': '(246) 462-1414'},
        ],
        'policia_municipal': [
            {'nombre': 'Policía Municipal Tlaxcala', 'telefono': '(246) 462-0800'},
        ],
        'guardia_caminos': [
            {'nombre': 'GN Carreteras — MEX-150D Tlaxcala', 'telefono': '(246) 462-0610'},
        ],
    },
}

# Bounding boxes in priority order (smaller/more specific regions first
# to avoid misclassification when states share borders).
# Each entry: (state_code, lat_min, lat_max, lon_min, lon_max)
_BOUNDS = [
    ('CDMX',           19.04, 19.60, -99.37, -98.95),
    ('COLIMA',         18.45, 19.75, -104.90, -103.35),
    ('TLAXCALA',       19.13, 19.73, -98.73, -97.75),
    ('AGUASCALIENTES', 21.53, 22.40, -102.87, -101.62),
    ('QUERETARO',      20.01, 21.70, -100.75, -99.03),
    ('GUANAJUATO',     19.88, 21.53, -102.57, -99.72),
    ('SAN_LUIS_POTOSI',21.50, 24.20, -102.00, -98.20),
    ('ZACATECAS',      21.45, 25.20, -104.40, -100.65),
    ('COAHUILA',       24.00, 29.90, -104.80, -99.75),
    ('NUEVO_LEON',     23.15, 27.80, -101.80, -98.50),
    ('TAMAULIPAS',     22.15, 27.65, -100.15, -97.15),
    ('EDOMEX',         18.70, 20.30, -100.65, -98.35),
    ('PUEBLA',         17.85, 20.55, -99.05, -96.63),
    ('VERACRUZ',       17.10, 22.55, -98.82, -93.55),
    ('NAYARIT',        20.40, 23.15, -106.10, -103.75),
    ('JALISCO',        18.80, 22.90, -105.75, -101.45),
]


def _resolve_state(lat: float, lon: float) -> str:
    for code, lat_min, lat_max, lon_min, lon_max in _BOUNDS:
        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            return code
    return 'JALISCO'


def get_contacts_for_coords(lat: float, lon: float) -> dict:
    """Return the emergency contacts dict for the state at (lat, lon)."""
    state = _resolve_state(lat, lon)
    return _CONTACTS.get(state, _CONTACTS['JALISCO'])
