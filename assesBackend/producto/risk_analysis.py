"""
Structured 6-section risk analysis for Mexican highway tramos.
Vehicle: double-trailer truck (camión de doble remolque).
Load states: Carga Completa (departure → first delivery)
             Media Carga   (after first delivery → final destination)
"""

FULL_LOAD = 'Carga Completa'
HALF_LOAD = 'Media Carga'


def _risk(name, desc, mag):
    return {'riesgo': name, 'descripcion': desc, 'magnitud': mag}


def _impact(dimension, descripcion):
    return {'dimension': dimension, 'descripcion': descripcion}


def _detect(indicador, herramienta):
    return {'indicador': indicador, 'herramienta': herramienta}


def _has(referencias, keyword):
    return any(keyword.lower() in r.lower() for r in referencias)


# ── Recta ──────────────────────────────────────────────────────────────────────

def _recta(load_state, has_rampa, has_caseta, dist_km):
    is_full = load_state == FULL_LOAD
    long_seg = dist_km > 100
    vel_max = '85 km/h' if is_full else '90 km/h'

    return {
        'objetivos_vulnerabilidades': {
            'objetivos': [
                'Integridad física del conductor y tripulación',
                'Carga transportada: ' + ('totalidad del cargamento (doble remolque al 100 %)' if is_full else 'carga residual (50 % del cargamento original; un remolque entregado)'),
                'Unidad de doble remolque — motor, transmisión, neumáticos, frenos',
                'Infraestructura vial y terceros usuarios de la carretera',
            ],
            'vulnerabilidades': [
                'Fatiga y microsueño por monotonía del trazo recto' + (' en tramo largo (> 100 km)' if long_seg else ''),
                'Exceso de velocidad facilitado por visibilidad y trazo despejado',
                ('Alta inercia de frenado con doble remolque al máximo peso: distancias de parada muy superiores a un vehículo convencional' if is_full
                 else 'Distribución asimétrica de peso entre remolques tras primera entrega: comportamiento diferente al esperado en frenadas'),
                'Reventón de neumático por temperatura acumulada en pavimento caliente',
                'Vehículos lentos o con avería sin señalización adecuada en vía rápida',
            ],
        },
        'identificacion_riesgos': [
            _risk('Fatiga / microsueño', 'Monotonía del trazo recto favorece la somnolencia, especialmente en conducción nocturna o en tramos superiores a 100 km sin parada', 'Alto' if long_seg else 'Medio'),
            _risk('Exceso de velocidad', 'El trazo recto y ' + ('la alta inercia con carga completa pueden dar falsa sensación de seguridad' if is_full else 'la reducción de peso tras la primera entrega pueden llevar al conductor a acelerar por encima del límite seguro'), 'Medio'),
            _risk('Reventón de llanta', 'El peso ' + ('máximo del convoy' if is_full else 'residual combinado con distribución asimétrica') + ' genera tensión acumulada en neumáticos; pavimento caliente agrava el riesgo', 'Alto' if is_full else 'Medio'),
            _risk('Colisión por alcance', 'Distancia de frenado extendida por masa del convoy; riesgo ante vehículo detenido o de baja velocidad', 'Alto' if is_full else 'Medio'),
            _risk('Maniobra incorrecta de cambio de carril', 'La longitud del doble remolque dificulta evaluar espacios seguros; punto ciego extendido', 'Medio'),
        ],
        'perspectiva_impacto': [
            _impact('Humano', 'Lesiones o fatalidades del conductor y terceros ante colisión o salida de vía'),
            _impact('Económico', 'Pérdida o daño de ' + ('la totalidad de la carga' if is_full else 'la carga residual') + '; daño a la unidad y costos de rescate, grúa y reparación vial'),
            _impact('Operacional', 'Retraso de entrega, activación de protocolos de emergencia, posible pérdida comercial con el cliente'),
            _impact('Reputacional', 'Accidentes de camión en carretera federal tienen alta cobertura mediática; afectación a la imagen de la empresa operadora'),
            _impact('Ambiental', 'Derrame de mercancía o combustible puede contaminar cunetas, arroyos o acuíferos cercanos al tramo'),
        ],
        'escenarios_ocurrencia': [
            'Conductor somnoliento en tramo nocturno abandona el carril; el segundo remolque impacta el guardarrail y vuelca',
            'Reventón de llanta trasera del primer remolque provoca derrape y pérdida de control del convoy a alta velocidad',
            'Vehículo averiado sin triángulos reflectores en carretera sin iluminación; choque por alcance del camión',
            'Conductor ' + ('con carga completa subestima la distancia de frenado y colisiona con vehículo que frena de emergencia' if is_full else 'acelera tras la primera entrega confiando en el menor peso; supera el límite seguro y no puede detenerse a tiempo'),
            'Lluvia repentina reduce el coeficiente de fricción; distancia de frenado se duplica con el peso del convoy',
        ],
        'elementos_deteccion': [
            _detect('Velocidad del convoy', 'Telemática GPS en tiempo real; alertas automáticas al superar umbral de ' + vel_max),
            _detect('Horas de conducción acumuladas', 'Sistema ELD / registrador de jornada; alerta a operador de flota al aproximarse al límite'),
            _detect('Presión y temperatura de neumáticos', 'Sensor TPMS con alarma en cabina; revisión visual en paradas programadas'),
            _detect('Distancia de seguimiento', 'Radar de proximidad frontal (si equipado) o protocolo de mínimo 4 segundos de distancia'),
            _detect('Condición climatológica', 'App meteorológica integrada o reporte de central de operaciones cada 2 horas'),
        ],
        'previsiones_proteccion': [
            'Límite operacional de velocidad: ' + vel_max + ' en recta (respetar señalización oficial)',
            ('Descanso obligatorio de 30 min en paradero cada 4 h de conducción continua' + (' — paradero disponible en este tramo' if has_caseta else ' — planificar parada en el siguiente punto de servicio')) ,
            'Revisión pre-tramo: presión de neumáticos, nivel de frenos, luces y cinturón de seguridad',
            'Protocolo de cambio de carril: señal mínima 5 s antes, verificar punto ciego de ambos remolques por espejo convexo',
            'En caso de avería: encender luces de emergencia, colocar triángulos a 50 m y 100 m, notificar a base operativa de inmediato',
            'Número de emergencia SCT / Policía Federal y de la empresa en tablero o dispositivo del conductor',
        ],
    }


# ── Recta Ascendente ───────────────────────────────────────────────────────────

def _recta_ascendente(load_state, has_rampa, has_caseta, dist_km):
    is_full = load_state == FULL_LOAD
    vel_asc = '40–50 km/h' if is_full else '50–60 km/h'

    return {
        'objetivos_vulnerabilidades': {
            'objetivos': [
                'Motor, transmisión y sistema de enfriamiento del tracto bajo carga sostenida en rampa',
                'Seguridad del conductor y convoy ante posible parada en pleno ascenso',
                'Carga: ' + ('doble remolque al máximo; peso empuja hacia atrás en ascenso' if is_full else 'remolque único con carga residual; distribución de peso alterada'),
                'Vehículos que circulan detrás del convoy y pueden ser sorprendidos por su lentitud',
            ],
            'vulnerabilidades': [
                'Sobrecarga térmica del motor bajo ' + ('peso máximo del convoy en ascenso prolongado' if is_full else 'peso reducido pero ascenso continuo; riesgo menor pero presente'),
                'El convoy reduce drásticamente su velocidad, exponiendo a colisiones por alcance desde atrás',
                'Selección incorrecta de marcha puede provocar calado o pérdida de impulso en pleno ascenso',
                'Mayor consumo de combustible en ascenso; riesgo de quedar sin diesel si el nivel es marginal',
                'Fatiga muscular del conductor por manejo constante de marchas y tensión en volante durante el ascenso',
            ],
        },
        'identificacion_riesgos': [
            _risk('Sobrecalentamiento del motor', 'El ascenso continuo con ' + ('carga máxima' if is_full else 'media carga') + ' eleva la temperatura del motor por encima del rango seguro', 'Alto' if is_full else 'Medio'),
            _risk('Calado / pérdida de marcha en ascenso', 'Error de selección de engranaje detiene el convoy en pleno ascenso, creando obstáculo peligroso para el tráfico', 'Alto' if is_full else 'Medio'),
            _risk('Colisión por alcance desde atrás', 'El convoy reduce su velocidad significativamente; vehículo rápido desde atrás puede no anticiparlo', 'Alto'),
            _risk('Avería mecánica en ascenso', 'Fallo de correa, turbo o bomba de agua en rampa sin espacio lateral de detención seguro', 'Crítico' if is_full else 'Alto'),
            _risk('Agotamiento de combustible', 'El ascenso bajo ' + ('carga completa' if is_full else 'media carga') + ' acelera el consumo; riesgo de quedar varado sin diesel', 'Medio'),
        ],
        'perspectiva_impacto': [
            _impact('Humano', 'Conductor varado en carretera de ascenso con espacio reducido; riesgo de impacto por tráfico descendente o ascendente'),
            _impact('Económico', 'Avería en ascenso implica grúa pesada especializada, daño al motor, pérdida de tiempo de ' + ('totalidad' if is_full else 'media') + ' de la carga'),
            _impact('Operacional', 'Bloqueo parcial o total de carril en tramo de ascenso; afectación al tráfico regional hasta despeje'),
            _impact('Reputacional', 'Avería visible en carretera federal refuerza percepción negativa sobre el estado de mantenimiento de la flota'),
            _impact('Ambiental', 'Fuga de refrigerante o aceite en carretera de montaña; riesgo de escorrentía hacia barrancas'),
        ],
        'escenarios_ocurrencia': [
            'Motor se sobrecalienta a mitad del ascenso bajo ' + ('carga completa y temperatura ambiente > 35 °C' if is_full else 'media carga en condiciones de verano') + '; conductor debe detener en hombro angosto',
            'Conductor selecciona marcha incorrecta; el convoy cala y queda perpendicular al carril de ascenso',
            'Vehículo que sigue al convoy choca por alcance al no anticipar la reducción de velocidad del camión en la rampa',
            'Turbocompresor falla en ascenso; camión pierde potencia progresivamente y queda varado en zona sin salida',
            'Nivel de combustible insuficiente no detectado antes del ascenso; convoy se detiene en plena rampa',
        ],
        'elementos_deteccion': [
            _detect('Temperatura del motor', 'Indicador de temperatura en tablero; alarma sonora/visual si supera umbral crítico (generalmente > 110 °C)'),
            _detect('Presión de aceite', 'Sensor de presión de aceite; descenso anormal indica desgaste o fuga inminente'),
            _detect('Relación RPM / velocidad', 'Tacómetro y velocímetro: relación anormal indica marcha incorrecta o pérdida de potencia'),
            _detect('Nivel de combustible', 'Indicador de combustible; verificar en la gasolinera del tramo anterior antes del ascenso'),
            _detect('Temperatura ambiente', 'Sensor ambiental del vehículo; a > 35 °C el riesgo de sobrecalentamiento es mayor'),
        ],
        'previsiones_proteccion': [
            'Verificar refrigerante, aceite y combustible en gasolinera previa al ascenso' + (' — gasolinera disponible en tramo anterior' if has_caseta else ''),
            'Seleccionar la marcha correcta ANTES de iniciar el ascenso; no intentar cambiar de marcha en plena rampa',
            'Si el motor comienza a sobrecalentar: reducir velocidad, activar calefacción al máximo para disipar calor, detenerse en el primer punto seguro',
            'Si el convoy se detiene: freno de estacionamiento, calzar ruedas, luces de emergencia, llamar a base inmediatamente',
            'Velocidad de ascenso recomendada: ' + vel_asc + ' (ajustar según señalización oficial)',
            'Activar luces de advertencia si la velocidad cae por debajo del flujo normal para alertar al tráfico detrás',
        ],
    }


# ── Recta Descendente ──────────────────────────────────────────────────────────

def _recta_descendente(load_state, has_rampa, has_caseta, dist_km):
    is_full = load_state == FULL_LOAD
    vel_desc = '40 km/h' if is_full else '50 km/h'

    return {
        'objetivos_vulnerabilidades': {
            'objetivos': [
                'Sistema de frenos del tracto y ambos remolques (máxima demanda en descenso)',
                'Control de velocidad del convoy ante la fuerza gravitacional acumulada',
                'Estabilidad de la carga: ' + ('peso máximo que genera mayor inercia hacia adelante en frenadas' if is_full else 'carga asimétrica entre remolques tras primera entrega; comportamiento impredecible en frenadas bruscas'),
                'Usuarios en la vía por debajo (incorporaciones, cruces, paraderos)',
            ],
            'vulnerabilidades': [
                'Sobrecalentamiento de frenos (fading) bajo ' + ('carga completa: peso máximo en descenso prolongado comprometiendo la capacidad de frenado' if is_full else 'media carga: frenos menos solicitados pero asimetría entre ejes puede provocar frenada irregular'),
                'Desplazamiento de carga hacia el frente del remolque durante frenadas en descenso',
                'Temperatura de neumáticos elevada por fricción continua en descenso; riesgo de reventón',
                'Rampa de emergencia ' + ('disponible en este tramo' if has_rampa else 'no identificada en este tramo: el frenado correcto es la única salvaguarda'),
                'Visibilidad reducida ante curvas al final del descenso recto',
            ],
        },
        'identificacion_riesgos': [
            _risk('Fallo de frenos (fading)', 'Calentamiento excesivo de frenos en descenso prolongado con ' + ('carga completa: máxima solicitación del sistema de frenado' if is_full else 'media carga asimétrica: posible sobrecarga de los frenos de un eje'), 'Crítico' if is_full else 'Alto'),
            _risk('Camión desbocado (runaway)', 'Pérdida total de frenado; el convoy acelera sin control hasta el final del descenso o la primera curva', 'Crítico'),
            _risk('Desplazamiento de carga', 'Frenadas bruscas desplazan la carga hacia el frente; inestabilidad del segundo remolque ' + ('con carga asimétrica' if not is_full else 'bajo máximo peso'), 'Alto'),
            _risk('Vuelco por velocidad excesiva', 'El convoy alcanza velocidad crítica en el descenso; vuelco ante cualquier irregularidad del pavimento o curva', 'Crítico' if is_full else 'Alto'),
            _risk('Reventón de llanta en descenso', 'Temperatura de neumáticos elevada por fricción continua; un reventón a alta velocidad en descenso es altamente desestabilizador', 'Alto'),
        ],
        'perspectiva_impacto': [
            _impact('Humano', 'Camión desbocado puede causar víctimas múltiples en incorporaciones, casetas o zonas urbanas al pie del descenso; el conductor puede quedar atrapado'),
            _impact('Económico', 'Destrucción total de la unidad y ' + ('la totalidad de la carga' if is_full else 'la carga residual') + '; responsabilidad civil por daños a infraestructura; costos de limpieza de vía'),
            _impact('Operacional', 'Cierre de vía por horas o días; desvío de tránsito regional; pérdida total del viaje y la carga'),
            _impact('Reputacional', 'Accidente de camión desbocado: el evento de mayor visibilidad mediática en transporte de carga; consecuencias legales y regulatorias graves'),
            _impact('Ambiental', 'Derrame de combustible, aceite y mercancía; riesgo de incendio; daño al ecosistema de ladera o barranca'),
        ],
        'escenarios_ocurrencia': [
            'Frenos sobrecalentados tras descenso previo no detectados; conductor entra al tramo con frenos comprometidos y los pierde a mitad del descenso',
            'Conductor no activa el freno motor/retarder; depende exclusivamente de frenos de servicio que se fatigan en 5–8 km',
            'Reventón de llanta trasera del primer remolque en pleno descenso desestabiliza el segundo remolque que gira lateralmente',
            'Rampa de emergencia no identificada por el conductor; el convoy la sobrepasa a alta velocidad sin poder usarla',
            'Lluvia inesperada reduce la adherencia al pavimento en el descenso; la distancia de frenado se duplica o triplica',
        ],
        'elementos_deteccion': [
            _detect('Temperatura de frenos', 'Sensor térmico de frenos (si equipado); indicios visuales: humo en ruedas, olor a quemado'),
            _detect('Velocidad del convoy en descenso', 'Telemática GPS; alerta crítica si supera ' + vel_desc + ' en este tipo de tramo'),
            _detect('Señalización y ubicación de rampas', 'Conocer la posición exacta de la rampa ANTES de iniciar el descenso' + (' — rampa identificada en este tramo' if has_rampa else ' — sin rampa en este tramo: velocidad es la única salvaguarda')),
            _detect('Comportamiento del segundo remolque', 'Espejo retrovisor convexo y cámara trasera (si disponible); cualquier oscilación lateral es alarma inmediata'),
            _detect('Presión del sistema de frenos de aire', 'Manómetro de presión de aire; caída por debajo del umbral mínimo indica fuga o fallo'),
        ],
        'previsiones_proteccion': [
            'OBLIGATORIO: Activar freno motor/retarder ANTES de iniciar el descenso; no esperar a que el convoy gane velocidad',
            'Velocidad máxima en descenso: ' + vel_desc + ' (respetar señalización); usar reloj de tablero para confirmar velocidad constante',
            'Verificar temperatura de frenos y presión de llantas en paradero o caseta antes del descenso' + (' — punto disponible en este tramo' if has_caseta else ' — detención preventiva antes del descenso si hay duda'),
            'Memorizar la ubicación exacta de la rampa de emergencia antes de iniciar' + (' — rampa identificada en este tramo' if has_rampa else ' — solicitar información a central de operaciones sobre rampas en tramos vecinos'),
            'PROHIBIDO rebasar en el descenso; mantener carril derecho en todo momento',
            'En caso de pérdida de frenos: usar rampa de emergencia; si no está disponible, fricción guiada contra guardarrail lado montaña como último recurso',
            'Verificar y tensar la sujeción de la carga antes del inicio del descenso para evitar desplazamiento en frenadas',
            'Comunicar inicio y fin del descenso a la base; si no hay reporte en tiempo estimado, activar protocolo de búsqueda',
        ],
    }


# ── Curva Ascendente ───────────────────────────────────────────────────────────

def _curva_ascendente(load_state, has_rampa, has_caseta, dist_km):
    is_full = load_state == FULL_LOAD
    vel_curva = '35–45 km/h' if is_full else '45–55 km/h'

    return {
        'objetivos_vulnerabilidades': {
            'objetivos': [
                'Estabilidad lateral del convoy: centro de gravedad elevado por doble remolque cargado en curva + gradiente',
                'Tracción de los ejes motrices sobre superficie inclinada y curva simultáneamente',
                'Carga: ' + ('peso máximo con alto centro de gravedad; amplifica el momento volcador' if is_full else 'media carga con posible distribución desigual entre remolques; comportamiento asimétrico en curva'),
                'Vehículos en sentido contrario y terceros en el área de la curva',
            ],
            'vulnerabilidades': [
                'Centro de gravedad elevado con ' + ('carga completa' if is_full else 'carga asimétrica en media carga') + ' amplifica el riesgo de vuelco lateral en curva',
                'Fuerza centrífuga y gradiente de ascenso actúan simultáneamente sobre el convoy en la misma dirección de desequilibrio',
                'Visibilidad reducida en curva cerrada; conductor no anticipa obstáculos en el carril contrario',
                'El radio de giro del doble remolque es notablemente mayor que el del tracto: el segundo remolque puede invadir el carril contrario',
                'Superficie húmeda, gravilla o pavimento deteriorado reduce la adherencia en curva + gradiente',
            ],
        },
        'identificacion_riesgos': [
            _risk('Vuelco lateral en curva ascendente', 'Combinación de fuerza centrífuga + gradiente bajo ' + ('carga completa' if is_full else 'media carga asimétrica') + ' puede superar el umbral de vuelco a velocidades relativamente bajas', 'Crítico' if is_full else 'Alto'),
            _risk('Pérdida de tracción en curva', 'Los ejes motrices pierden adherencia en la curva + gradiente, especialmente con superficie húmeda o suelta; el convoy puede deslizarse', 'Alto'),
            _risk('Invasión del carril contrario', 'El radio de giro extendido del doble remolque lleva al segundo remolque a cruzar la línea central en curvas cerradas', 'Alto'),
            _risk('Colisión frontal con vehículo en sentido contrario', 'Visibilidad reducida en curva cerrada; un vehículo en sentido contrario que también ocupa el centro puede provocar colisión frontal', 'Crítico'),
            _risk('Calado del motor en curva ascendente', 'Si el conductor intenta cambiar de marcha dentro de la curva para mantener impulso, el convoy puede calarse y quedar varado en posición oblicua', 'Medio'),
        ],
        'perspectiva_impacto': [
            _impact('Humano', 'Vuelco lateral en zona de curva puede atrapar al conductor y a pasajeros de vehículos en sentido contrario; evacuación difícil en zona de montaña'),
            _impact('Económico', 'Volcadura destruye unidad y ' + ('totalidad de la carga' if is_full else 'carga residual') + '; daño a infraestructura de la curva (guardarrail, señalización, talud)'),
            _impact('Operacional', 'Cierre de carretera en zona de curva con acceso difícil para equipos de rescate; restablecimiento muy lento'),
            _impact('Reputacional', 'Volcadura de camión de doble remolque en carretera federal o de montaña: máxima exposición mediática; investigación de la SCT'),
            _impact('Ambiental', 'Derrame de carga o combustible en zona de curva con posible escorrentía hacia alcantarillas o zonas naturales en ladera'),
        ],
        'escenarios_ocurrencia': [
            'Conductor entra a la curva ascendente sin reducir la velocidad suficientemente con ' + ('doble remolque al máximo' if is_full else 'media carga y remolque posterior desbalanceado') + '; el segundo remolque vuelca lateralmente',
            'Superficie con lluvia reciente; los neumáticos pierden adherencia en la curva ascendente; el tracto subvira y sale del carril',
            'Conductor intenta mantener impulso cambiando de marcha dentro de la curva; el convoy cala y queda perpendicular al carril bloqueando la vía',
            'Vehículo en sentido contrario invade el carril por error propio; colisión frontal en curva sin visibilidad anticipada',
            'Grava o arena en el asfalto de la curva exterior; llanta trasera del primer remolque pierde tracción y el convoy se desplaza al carril contrario',
        ],
        'elementos_deteccion': [
            _detect('Señalización de curva y velocidad recomendada', 'Señales viales de chevrones y velocidad máxima en curva; comunicar al conductor antes del tramo'),
            _detect('Sistema de alerta de vuelco / RSS', 'Sistema electrónico de estabilidad del vehículo (RSS/ESC, si equipado); alerta antes de alcanzar el umbral de vuelco'),
            _detect('Velocidad de entrada a la curva', 'Telemática GPS; comparar velocidad real vs velocidad recomendada de la curva; alerta si la supera'),
            _detect('Condición de la superficie', 'Reporte climatológico previo; observación visual del pavimento antes de la curva; reporte de central de operaciones'),
            _detect('Ángulo de articulación del segundo remolque', 'Cámara trasera o sensor de articulación (si disponible); cualquier ángulo anómalo es señal de alarma'),
        ],
        'previsiones_proteccion': [
            'ANTES de la curva: reducir velocidad a ' + vel_curva + '; seleccionar la marcha correcta; NO cambiar de marcha dentro de la curva',
            'Mantener el carril derecho con margen adicional al centro de la vía para compensar el radio de giro extendido del segundo remolque',
            'Activar luces de advertencia si la velocidad cae drásticamente en la entrada de la curva para alertar al tráfico detrás',
            'Revisar presión y estado de neumáticos antes de tramos con curvas en ascenso' + (' — paradero disponible' if has_caseta else ''),
            'Conocer el radio de giro del doble remolque: anticipar la ocupación de carril y verificar con espejo retrovisor',
            'Contactar a la base al inicio de cada tramo de curvas; reportar condiciones de superficie',
        ],
    }


# ── Curva Descendente ──────────────────────────────────────────────────────────

def _curva_descendente(load_state, has_rampa, has_caseta, dist_km):
    is_full = load_state == FULL_LOAD
    vel_critica = '30–40 km/h' if is_full else '40–50 km/h'

    return {
        'objetivos_vulnerabilidades': {
            'objetivos': [
                'Sistema de frenos bajo la demanda más exigente del viaje: frenado + curva + peso + gradiente simultáneos',
                'Estabilidad del convoy: la combinación de fuerza gravitacional + centrífuga es el escenario mecánico más crítico',
                'Conductor y tripulación; vehículos en sentido contrario; infraestructura del tramo (guardarrail, talud)',
                'Carga: ' + ('peso máximo con máxima inercia en frenada curva-descenso' if is_full else 'carga asimétrica; un remolque más ligero puede bambolear en la curva descendente'),
            ],
            'vulnerabilidades': [
                'Combinación simultánea de fuerza centrífuga, gravedad y ' + ('masa máxima' if is_full else 'masa asimétrica') + ': el escenario mecánico más exigente para el sistema de frenado del convoy',
                'Frenos posiblemente ya comprometidos por descenso anterior si el tramo forma parte de una cadena de curvas-descenso',
                'Temperatura de frenos y neumáticos elevada desde tramos previos',
                'Visibilidad reducida en curva cerrada descendente; conductor ve tarde los obstáculos',
                'Rampa de emergencia ' + ('disponible en este tramo' if has_rampa else 'no identificada en este tramo: máxima restricción de velocidad es la única salvaguarda'),
            ],
        },
        'identificacion_riesgos': [
            _risk('Vuelco en curva descendente', 'El escenario de mayor peligro del viaje: la suma de descenso + curva con ' + ('carga completa' if is_full else 'carga asimétrica') + ' puede producir vuelco a velocidades que parecen moderadas', 'Crítico'),
            _risk('Fallo de frenos en curva', 'Frenos comprometidos por descenso anterior + demanda adicional de la curva; pérdida total de control dentro de la curva', 'Crítico'),
            _risk('Salida de vía por exceso de velocidad', 'El convoy supera la velocidad crítica de la curva y sale de vía; riesgo de caída por talud o impacto contra barrera', 'Crítico' if is_full else 'Alto'),
            _risk('Jackknifing (efecto tijera)', 'El tracto gira más que los remolques durante el frenado en curva; los remolques empujan lateralmente y pueden voltear el tracto o bloquear toda la vía', 'Crítico' if is_full else 'Alto'),
            _risk('Colisión frontal por invasión de carril', 'El segundo remolque invade el carril contrario en la curva descendente; colisión con vehículo en sentido contrario', 'Crítico'),
        ],
        'perspectiva_impacto': [
            _impact('Humano', 'Potencial de fatalidades múltiples: conductor, tripulación y vehículos en sentido contrario; el vuelco de un camión de doble remolque en curva descendente es un evento catastrófico de alta probabilidad de víctimas'),
            _impact('Económico', 'Pérdida total de unidad y carga; daños a infraestructura (guardarrail, señalización, talud, postes); costos de rescate y limpieza que pueden superar el valor de la carga'),
            _impact('Operacional', 'Cierre de vía por horas o días en zona de difícil acceso; desvío de cientos de vehículos; pérdida completa del viaje'),
            _impact('Reputacional', 'Evento de máxima visibilidad mediática; investigación obligatoria de la SCT y posible suspensión de operaciones de la empresa'),
            _impact('Ambiental', 'Derrame de mercancía, combustible y fluidos en zona de ladera; riesgo de incendio; daño grave al ecosistema circundante'),
        ],
        'escenarios_ocurrencia': [
            'Frenos calientes tras descenso previo no detectados; conductor entra a la curva descendente con sistema de frenado comprometido; el convoy alcanza velocidad crítica y vuelca',
            'Conductor no activa freno motor antes de la curva; al frenar bruscamente dentro de ella provoca jackknifing con ' + ('doble remolque cargado' if is_full else 'media carga con distribución desigual entre remolques'),
            'Lluvia inesperada en curva descendente; adherencia reducida al 40 %; el convoy se desliza hacia el exterior de la curva y sale de vía por el talud',
            'Vehículo lento sin señalización en curva descendente; el conductor del camión frena violentamente; el segundo remolque oscila y golpea el guardarrail opuesto',
            'Tramo nocturno sin iluminación; conductor no reduce suficientemente antes de la curva descendente; la velocidad de entrada supera el umbral de vuelco',
        ],
        'elementos_deteccion': [
            _detect('Temperatura de frenos ANTES de la curva', 'Sensor térmico (si equipado) o inspección visual obligatoria (humo, olor) en paradero o punto previo a la curva' + (' — punto disponible en tramo' if has_caseta else '')),
            _detect('Velocidad de entrada a la curva', 'Telemática GPS con alerta crítica si supera ' + vel_critica + '; alerta a conductor Y operador de flota simultáneamente'),
            _detect('Sistema RSS / control de estabilidad', 'Sistema electrónico de estabilidad (RSS/ESC/EBS); alerta inminente antes del umbral de vuelco o jackknife'),
            _detect('Ubicación exacta de la rampa de emergencia', 'Conocer la posición kilométrica ANTES de iniciar el tramo' + (' — rampa identificada en este tramo' if has_rampa else ' — sin rampa identificada: la velocidad reducida es la única salvaguarda; planificar alternativa con central')),
            _detect('Comportamiento del segundo remolque', 'Cámara trasera en tiempo real o espejo convexo; cualquier oscilación lateral es señal de alarma inmediata'),
        ],
        'previsiones_proteccion': [
            'CRÍTICO: Activar freno motor/retarder ANTES de la curva; velocidad máxima de entrada: ' + vel_critica,
            'Verificar temperatura de frenos en punto previo a la curva' + (' — punto disponible en este tramo' if has_caseta else ' — si no hay punto previo, detención cautelar para enfriamiento de 10–15 min antes del tramo'),
            'Memorizar la posición exacta de la rampa de emergencia antes de iniciar' + (' — rampa identificada en este tramo' if has_rampa else ' — sin rampa: la única protección es la velocidad reducida; NO ingresar si los frenos están calientes'),
            'PROHIBIDO rebasar, cambiar de carril o hablar por radio dentro de la curva descendente',
            'Distancia mínima de seguimiento: 6 segundos (máxima para cualquier tramo del viaje)',
            'En caso de pérdida de frenos dentro de la curva: usar rampa; si no está disponible, fricción guiada contra guardarrail lado montaña como último recurso; avisar a base por radio',
            'Verificar y tensar la sujeción de la carga inmediatamente antes del inicio del tramo',
            'Comunicar inicio y fin del tramo a la base; activar protocolo de búsqueda si no hay reporte en el tiempo estimado',
        ],
    }


# ── Dispatch map ───────────────────────────────────────────────────────────────

_BUILDERS = {
    'Recta':             _recta,
    'Recta Ascendente':  _recta_ascendente,
    'Recta Descendente': _recta_descendente,
    'Curva Ascendente':  _curva_ascendente,
    'Curva Descendente': _curva_descendente,
}

# Trazo types where half-load meaningfully changes the risk profile
_HALF_LOAD_FLAG_TRAZOS = {'Recta Descendente', 'Curva Ascendente', 'Curva Descendente'}


def generate_risk_analysis(tramo: dict, load_state: str) -> dict:
    """
    Return a structured 6-section risk analysis for a single tramo.

    tramo      — dict with 'trazo_topografia', 'referencias', 'distancia_km'
    load_state — FULL_LOAD or HALF_LOAD

    Returns:
    {
      'load_state':      str,
      'load_state_flag': bool,   # True when half-load meaningfully shifts the risk profile
      'sections': {
        'objetivos_vulnerabilidades':  { 'objetivos': [...], 'vulnerabilidades': [...] },
        'identificacion_riesgos':      [ { 'riesgo', 'descripcion', 'magnitud' }, ... ],
        'perspectiva_impacto':         [ { 'dimension', 'descripcion' }, ... ],
        'escenarios_ocurrencia':       [ str, ... ],
        'elementos_deteccion':         [ { 'indicador', 'herramienta' }, ... ],
        'previsiones_proteccion':      [ str, ... ],
      }
    }
    """
    trazo     = tramo.get('trazo_topografia', 'Recta')
    refs      = tramo.get('referencias', [])
    dist_km   = tramo.get('distancia_km', 0.0)
    has_rampa  = _has(refs, 'rampa')
    has_caseta = _has(refs, 'caseta') or _has(refs, 'paradero')

    builder  = _BUILDERS.get(trazo, _recta)
    sections = builder(load_state, has_rampa, has_caseta, dist_km)

    load_state_flag = (load_state == HALF_LOAD) and (trazo in _HALF_LOAD_FLAG_TRAZOS)

    return {
        'load_state':      load_state,
        'load_state_flag': load_state_flag,
        'sections':        sections,
    }
