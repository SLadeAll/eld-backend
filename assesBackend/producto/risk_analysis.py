"""
PROCESO risk analysis — 7-column operational security table for each tramo.
Vehicle: double-trailer truck (camión de doble remolque).
Load states: Carga Completa | Media Carga.

Output per tramo:
  {
    'load_state':   str,
    'load_state_flag': bool,
    'tabla_proceso': [ [#, Area, Dinamica, Amenazas, Vigilancia, Restriccion, Intervencion], ... ],
    'os_profile':   str,
  }
"""

FULL_LOAD = 'Carga Completa'
HALF_LOAD = 'Media Carga'

_HALF_LOAD_FLAG_TRAZOS = {'Recta Descendente', 'Curva Ascendente', 'Curva Descendente'}


def _r(num, area, dinamica, amenazas, vigilancia, restriccion, intervencion):
    return [str(num), area, dinamica, amenazas, vigilancia, restriccion, intervencion]


# ── RECTA ──────────────────────────────────────────────────────────────────────

def _recta(load_state, has_rampa, has_caseta, dist_km):
    is_full = load_state == FULL_LOAD
    vel = '85 km/h' if is_full else '90 km/h'
    carga_nota = 'carga completa al máximo peso' if is_full else 'media carga con distribución asimétrica entre remolques'

    rows = [
        _r(1,
           'Vía de circulación',
           f'Circulación continua a {vel} en carril derecho; tráfico mixto en carril izquierdo; el convoy ({carga_nota}) ocupa una longitud superior a 22 m',
           'Cierre súbito de carril por vehículo adelantador; colisión por alcance desde atrás; vehículo fantasma sin luces en tramo nocturno',
           'Monitorear espejos retrovisores cada 30 s; verificar distancia de seguimiento; identificar vehículos que sigan al convoy a distancia constante inusual',
           f'Mantener distancia mínima de 4 s al vehículo de adelante; señalizar todo cambio de carril con 5 s de anticipación; velocidad máxima operacional {vel}',
           'Si vehículo agresivo detrás: activar luces de advertencia + reducción gradual de velocidad + reporte a base; si persiste: detención en hombro + contacto con Policía Federal',
        ),
        _r(2,
           'Hombro / arcén lateral',
           'Zona de detención de emergencia no planificada; presencia ocasional de vehículos varados y peatones; OS realiza inspección visual del vehículo en paradas',
           'Abordaje no autorizado al convoy detenido; robo de carga en varada provocada; obstáculos en hombro que dañen neumáticos del convoy',
           'Inspeccionar estado del hombro antes de detenerse; identificar visualmente a toda persona que se aproxime al convoy; vigilar perímetro a 20 m de radio',
           'Prohibir acercamiento de personas no identificadas; mantener puertas de cabina cerradas en toda parada no programada; no abrir remolques sin autorización de base',
           'Si acercamiento sospechoso: activar alarma + comunicar a base + arrancar si es seguro; si imposible arrancar: bloquear acceso a remolques y esperar respuesta policial',
        ),
        _r(3,
           'Zona de adelantamiento',
           f'Maniobras de rebase frecuentes; vehículos rápidos superan al convoy con diferencia de velocidad de 40–60 km/h; carril izquierdo activo en tramo recto de {dist_km:.0f} km',
           'Colisión lateral en rebase; corte intempestivo ante el convoy (cut-in) para obligarlo a frenar; intento de detención forzada por vehículo que rebasa y frena abruptamente',
           'Observar señales de intención de rebase en espejos laterales; comunicar al conductor toda aproximación lateral; registrar placa y descripción de vehículos con comportamiento irregular',
           'No ejecutar rebases del convoy salvo necesidad operativa extrema; proteger el espacio lateral mediante posición centrada en carril; señalizar activamente la longitud del convoy con luces',
           'Si vehículo intenta cierre forzado: bocina sostenida + luces de emergencia + reducción gradual; reportar placa y descripción a base y Policía Federal inmediatamente',
        ),
        _r(4,
           'Caseta de cobro' if has_caseta else 'Punto de control / acceso restringido',
           'Reducción obligatoria de velocidad a 20 km/h; detención de 30–60 s; interacción directa con operadores y vehículos contiguos detenidos en el carril',
           'Robo aprovechando la detención obligatoria; instrucción de desvío simulando ser autoridad; colocación de objetos en la carga o ruedas durante la detención',
           'Verificar credenciales del personal si solicita inspección; observar vehículos estacionados en proximidad; revisar que nada sea colocado en el convoy durante la detención',
           'No aceptar instrucciones de desvío de persona no identificada; verificar con base cualquier ruta alternativa; mantener ventanas cerradas salvo espacio mínimo para cobro',
           'Si amenaza en caseta: no detenerse, solicitar paso de emergencia, notificar base + Policía Federal; documentar con cámara todo lo ocurrido',
        ),
        _r(5,
           'Paradero / área de descanso',
           'Detención planificada de 30–90 min; conductor descansa; ' + ('carga completa estacionada' if is_full else 'carga residual estacionada') + '; tráfico mixto de camioneros y transeúntes en el área',
           'Robo de carga durante parada prolongada; vigilancia hostil del convoy para planificar asalto posterior; adulteración o sabotaje de la mercancía',
           'OS permanece en alerta activa durante descanso del conductor; inspeccionar perímetro del vehículo cada 15 min; identificar vehículos estacionados en el área por tiempo prolongado',
           'Acceso al convoy restringido a personal autorizado únicamente; asegurar todos los puntos de acceso a los remolques; no divulgar carga, destino ni itinerario a terceros',
           'Si manipulación de carga detectada: notificar base inmediatamente, no mover el vehículo, documentar con fotografías, esperar inspección de autoridades',
        ),
        _r(6,
           'Sistema de comunicaciones / telemetría',
           'Transmisión continua de posición GPS y datos telemétricos a base; reportes periódicos del OS cada 30 min; posible pérdida de señal en zonas rurales del tramo',
           'Jamming / bloqueo intencional de señal GPS o celular; pérdida de comunicación en zona sin cobertura; falla del dispositivo de rastreo principal',
           'Verificar señal GPS y comunicación cada 30 min; confirmar recepción de reportes en base; detectar anomalías en señal o discrepancias en posición reportada',
           'No cambiar de ruta si se pierde comunicación; mantener ruta programada y reportar en la primera parada autorizada',
           'Si comunicación perdida: protocolo zona muerta (seguir ruta, primera parada segura, dispositivo de emergencia alternativo); si jamming confirmado: tratar como amenaza activa y notificar a primera autoridad disponible',
        ),
    ]

    os_profile = (
        f'El Oficial de Seguridad (OS) actúa como escolta de seguridad activo en este tramo rectilíneo. '
        f'PUEDE: monitorear el entorno y reportar amenazas en tiempo real; instruir al conductor en maniobras defensivas (reducción de velocidad, cambio de carril, detención en hombro); '
        f'documentar incidentes mediante cámara y reporte escrito; coordinar respuesta policial a través de la base de operaciones. '
        f'NO PUEDE: realizar intervenciones fuera del vehículo mientras está en movimiento; detener o interceptar vehículos de terceros en carretera federal; '
        f'emplear medidas de fuerza fuera de los protocolos de defensa propia autorizados; abandonar el convoy bajo ninguna circunstancia durante la operación. '
        f'Condición de carga: {load_state}. Perfil de valor del objetivo: {"alto — carga completa representa mayor atractivo para actores hostiles" if is_full else "medio — media carga reduce el valor pero la asimetría de peso introduce vulnerabilidad operativa"}.'
    )

    return {'tabla_proceso': rows, 'os_profile': os_profile}


# ── RECTA ASCENDENTE ───────────────────────────────────────────────────────────

def _recta_ascendente(load_state, has_rampa, has_caseta, dist_km):
    is_full = load_state == FULL_LOAD
    vel_asc = '40–50 km/h' if is_full else '50–60 km/h'
    carga_nota = 'peso máximo — el motor trabaja al límite de su capacidad térmica' if is_full else 'media carga — menor demanda al motor, pero distribución asimétrica entre ejes'

    rows = [
        _r(1,
           'Carril de ascenso lento',
           f'El convoy ({carga_nota}) circula a {vel_asc} en el carril derecho de ascenso; tráfico más rápido lo supera; exposición prolongada en la vía por baja velocidad',
           'Colisión por alcance desde vehículo que no anticipa la baja velocidad del convoy; intentos de rebase peligroso en zona de visibilidad reducida; objeto en carril que obliga maniobra brusca',
           'Monitorear espejos traseros continuamente durante el ascenso; comunicar al conductor todo vehículo rápido aproximándose desde atrás; reportar condición del tráfico a la base cada 10 min en ascensos mayores a 10 km',
           f'Activar luces de advertencia traseras durante el ascenso; mantener {vel_asc} sin intentar acelerar para alcanzar el flujo del tráfico rápido; no ejecutar rebases propios en ascenso',
           'Si vehículo choca desde atrás: asegurar al conductor, encender luces de emergencia, colocar triángulos, notificar base y servicios de emergencia (911)',
        ),
        _r(2,
           'Hombro de emergencia en rampa',
           'Zona de detención limitada: el hombro en rampa es angosto y con pendiente; detención aquí implica riesgo de movimiento involuntario del convoy',
           'Deslizamiento del convoy por pendiente si falla el freno de estacionamiento; impacto lateral de vehículo que sale del carril; acceso difícil para servicios de emergencia',
           'Verificar la disponibilidad y anchura del hombro antes de iniciar el ascenso; identificar los puntos de detención seguros a lo largo del tramo; confirmar que el freno de mano funcione correctamente',
           'Detenerse SOLO si es absolutamente necesario; aplicar freno de estacionamiento Y calzar ruedas; activar luces de emergencia de inmediato; no permitir que nadie baje del vehículo hacia el carril',
           'Si parada de emergencia: freno de mano + cuñas + triángulos + llamada a base + 911; si el convoy comienza a deslizarse: freno de servicio + bocina + comunicar a tráfico',
        ),
        _r(3,
           'Sistema mecánico del tractor (motor / transmisión / enfriamiento)',
           f'El motor trabaja a máxima demanda térmica bajo {"peso máximo del convoy" if is_full else "media carga en ascenso sostenido"}; temperatura del refrigerante, aceite y frenos aumenta progresivamente',
           'Sobrecalentamiento del motor; falla del turbocompresor; rotura de correa de transmisión; pérdida de potencia que deja el convoy varado en plena rampa',
           'Monitorear temperatura del motor en tablero cada 5 min durante el ascenso; observar humo o vapor bajo la capó; verificar nivel de combustible antes del ascenso',
           'Si temperatura supera el umbral de alerta: reducir velocidad, activar calefacción al máximo para disipar calor; detenerse en el primer punto seguro del hombro',
           'Si motor se detiene en rampa: freno + cuñas + luces de emergencia + notificar base + solicitar grúa pesada; no intentar rearrancar si hay humo o vapor; esperar inspección técnica',
        ),
        _r(4,
           'Zona posterior al convoy (tráfico detrás)',
           'El convoy en ascenso lento genera una cola de vehículos detrás; conductores impacientes intentan adelantar en zonas prohibidas; situación de tensión en carretera de montaña',
           'Conductor impaciente que adelanta en curva ciega del ascenso; vehículo que golpea el segundo remolque por distracción; convoy que bloquea carretera si se detiene',
           'Monitorear la longitud de la cola detrás mediante cámara trasera o espejo; reportar a la base si la cola supera 10 vehículos (señal de posible incidente)',
           'Mantener velocidad constante para no interrumpir el flujo detrás; señalizar claramente la presencia del convoy con luces; no acelerar abruptamente en zonas de ascenso',
           'Si se forma cola extensa y algún vehículo intenta rebase peligroso: activar señales de advertencia + reporte a base + si hay radio de comunicación con autoridades viales, activarla',
        ),
        _r(5,
           'Zona de servicios previa al ascenso (gasolinera / paradero)',
           'Detención planificada de 10–20 min antes del ascenso para revisión mecánica y reabastecimiento; interacción con personal de la estación',
           'Robo de combustible durante la carga; manipulación del vehículo durante la revisión; seguimiento del convoy por actores que observan el reabastecimiento',
           'Supervisar el proceso de abastecimiento de combustible sin apartar la vista del convoy; verificar que el personal de la estación sea personal regular del establecimiento',
           'No permitir que personas ajenas toquen el motor, ruedas o carga durante la parada; mantener al menos una persona con vista al convoy en todo momento',
           'Si se detecta manipulación durante el abastecimiento: interrumpir la operación, notificar base, solicitar inspección antes de continuar el ascenso',
        ),
        _r(6,
           'Comunicaciones en zona de posible cobertura reducida',
           'Los tramos de ascenso en sierra frecuentemente tienen cobertura celular intermitente; el convoy puede quedar sin comunicación por períodos de 5–20 min en zonas de ladera',
           'Pérdida de comunicación en el momento de mayor riesgo mecánico; imposibilidad de reportar incidente a base; falta de coordinación si ocurre avería',
           'Verificar la cobertura disponible al inicio del ascenso; establecer protocolo de check-in cada 10 min; confirmar el número de emergencia alternativo (radio, satélite) antes del tramo',
           'Si se pierde señal: mantener ruta, no detenerse salvo emergencia mecánica, reestablecer comunicación en la primera zona con cobertura disponible',
           'Si la avería ocurre en zona sin cobertura: encender luces de emergencia, enviar señal visual a vehículos que pasen (brazos, triángulos), esperar ayuda; si hay radio de emergencia, activarlo',
        ),
    ]

    os_profile = (
        f'El OS actúa como escolta de seguridad y monitor mecánico-operativo en este tramo de ascenso. '
        f'PUEDE: ordenar detención del convoy ante señales confirmadas de fallo mecánico; coordinar apoyo técnico en rampa a través de la base; '
        f'mantener comunicación continua con la base durante el ascenso; instruir al conductor en el uso correcto de marchas y velocidad de ascenso. '
        f'NO PUEDE: efectuar reparaciones mecánicas en la vía; forzar la continuación del ascenso si hay riesgo mecánico confirmado; '
        f'abandonar el convoy para buscar ayuda dejando al conductor solo en la rampa. '
        f'Condición de carga: {load_state} ({("máxima demanda al motor; mayor probabilidad de fallo mecánico" if is_full else "menor demanda mecánica; mayor agilidad de detención si es necesario")}).'
    )

    return {'tabla_proceso': rows, 'os_profile': os_profile}


# ── RECTA DESCENDENTE ──────────────────────────────────────────────────────────

def _recta_descendente(load_state, has_rampa, has_caseta, dist_km):
    is_full = load_state == FULL_LOAD
    vel_desc = '40 km/h' if is_full else '50 km/h'
    carga_desc = 'carga completa: máxima inercia gravitacional en el eje longitudinal' if is_full else 'media carga: menor inercia pero posible distribución asimétrica que genera torsión en frenos'

    rows = [
        _r(1,
           'Carril de descenso',
           f'El convoy ({carga_desc}) desciende a velocidad controlada de máximo {vel_desc}; la gravedad actúa continuamente sobre el sistema de frenado; tráfico de vehículos más rápidos a la zaga',
           'Exceso de velocidad involuntario si el conductor no usa freno motor; colisión por alcance si el convoy reduce bruscamente; maniobra intempestiva del conductor al sentir pérdida de frenos',
           f'Verificar que el freno motor esté activo ANTES de iniciar el descenso; monitorear el velocímetro cada 60 s para confirmar que se mantiene bajo {vel_desc}; observar señales de humo en ruedas (fading)',
           f'Velocidad máxima de descenso: {vel_desc}; freno motor/retarder activo obligatorio; no permitir que la velocidad aumente aunque el tráfico circule más rápido',
           'Si velocidad supera el umbral: activar freno de servicio en pulsos cortos (no mantener presionado); si fading confirmado (olor, humo): dirigir al conductor a la rampa de emergencia; notificar base y 911',
        ),
        _r(2,
           'Sistema de frenos (frenos de servicio, motor y retarder)',
           'Los frenos trabajan continuamente durante el descenso; la temperatura de los discos o tambores aumenta progresivamente; ' + ('con carga completa la energía térmica generada es máxima' if is_full else 'con media carga la energía es menor pero la distribución entre ejes puede ser irregular'),
           'Fading (pérdida de efectividad) de frenos por sobrecalentamiento; rotura de manguera de frenos de aire; pérdida total de frenado (camión desbocado)',
           'Observar temperatura de frenos si el vehículo tiene sensor; detectar olor a quemado o humo en ruedas traseras; verificar el comportamiento del convoy ante pulsos de freno',
           'Detener el convoy en el primer punto seguro si hay señales de sobrecalentamiento de frenos; no continuar el descenso con frenos calientes sin tiempo de enfriamiento (mínimo 10–15 min)',
           'Si pérdida total de frenos: dirigir conductor a RAMPA DE EMERGENCIA' + (' (disponible en este tramo)' if has_rampa else ' (no identificada — el guardarrail lado montaña es el último recurso)') + '; notificar base y 911 simultáneamente',
        ),
        _r(3,
           'Rampa de emergencia' + (' (disponible en este tramo)' if has_rampa else ' (no identificada en este tramo)'),
           'La rampa de emergencia es el dispositivo de último recurso para detener un camión desbocado; su efectividad depende de que el conductor la conozca y la use correctamente',
           'Conductor que desconoce la ubicación exacta de la rampa y la sobrepasa; rampa obstruida por otro vehículo; conductor que no toma la decisión de usar la rampa a tiempo',
           'Confirmar la posición kilométrica de la rampa ANTES de iniciar el descenso' + (' — rampa presente en este tramo' if has_rampa else ' — sin rampa en este tramo: reportar este dato a base previo al descenso') + '; comunicar al conductor su ubicación',
           'La decisión de usar la rampa es del conductor; el OS DEBE apoyar esa decisión; no contradecir al conductor si decide usar la rampa aunque parezca innecesario',
           'Si convoy se dirige a rampa: comunicar a base la situación; al detenerse en rampa: luces de emergencia + triángulos + notificar 911 para asistencia de recuperación',
        ),
        _r(4,
           'Hombro lateral en descenso',
           'El hombro en descenso puede ser angosto o inexistente; una detención aquí implica riesgo de movimiento por pendiente y exposición al tráfico',
           'Deslizamiento del convoy si falla el freno de estacionamiento en pendiente; impacto lateral desde carril de descenso; imposibilidad de detenerse con seguridad si el hombro es inexistente',
           'Verificar la disponibilidad del hombro al inicio del descenso; identificar puntos de detención seguros en el tramo; evaluar si el hombro tiene anchura suficiente para el convoy',
           'Detenerse en hombro de descenso SOLO como último recurso si no hay rampa de emergencia; aplicar freno de mano + cuñas + señalización inmediata',
           'Si forzado a detenerse en hombro de descenso: freno + cuñas SIEMPRE en los dos ejes del último remolque; triángulos a 100 m y 200 m hacia arriba del descenso; notificar base + 911',
        ),
        _r(5,
           'Zona de incorporación / pie del descenso',
           'Al final del descenso, el convoy se incorpora al flujo vehicular normal con alta velocidad residual; posible cambio brusco de carretera a zona urbana o de tráfico denso',
           'Exceso de velocidad residual al llegar al pie del descenso; incorporación a flujo denso sin espacio suficiente; semáforo o stop no anticipado por el conductor',
           'Comunicar al conductor la proximidad del pie del descenso y los cambios de condición vial; verificar en el mapa la presencia de incorporaciones, semáforos o cruces al final del tramo',
           'Reducir velocidad progresivamente en el último tercio del descenso; verificar condición de frenos (temperatura) antes de la incorporación al tráfico normal',
           'Si el convoy llega al pie del descenso a velocidad excesiva y no puede detenerse: activar bocina continua para alertar al tráfico, mantener carril, reportar a base y 911',
        ),
        _r(6,
           'Área de carga — remolques en descenso',
           f'La carga ({("completa" if is_full else "residual — distribución asimétrica")}) ejerce presión hacia el frente durante el descenso y las frenadas; el segundo remolque puede oscilar o empujar al primero',
           'Desplazamiento de carga hacia el frente del remolque en frenadas bruscas; oscilación del segundo remolque (efecto bamboleo o jackknife parcial); ruptura de cinchos de sujeción por tensión acumulada',
           'Observar mediante espejo o cámara trasera el comportamiento del segundo remolque durante el descenso; verificar que no haya sonidos inusuales de la carga en movimiento',
           'Verificar y tensar la sujeción de la carga ANTES del inicio del descenso; reportar cualquier sonido de carga en movimiento y detenerse para inspección',
           'Si se detecta bamboleo del segundo remolque: instruir al conductor a reducir velocidad gradualmente SIN frenar bruscamente (agrava el bamboleo); detenerse en el primer punto seguro para inspección de la carga',
        ),
    ]

    os_profile = (
        f'El OS opera en el escenario de mayor riesgo de frenado del viaje. '
        f'PUEDE: verificar la activación del freno motor antes del descenso; comunicar la posición de la rampa de emergencia al conductor; '
        f'ordenar detención preventiva ante señales de fading (olor, humo, pérdida de respuesta); coordinar asistencia de emergencia desde la base. '
        f'NO PUEDE: impedir que el conductor tome la rampa de emergencia si lo decide; contradecir las decisiones del conductor en situación de pérdida inminente de frenos; '
        f'controlar mecánicamente el vehículo desde su posición. '
        f'Condición de carga: {load_state}. '
        f'{"Carga completa = máxima inercia en descenso = máxima exigencia al sistema de frenos. Perfil de riesgo: CRÍTICO." if is_full else "Media carga = menor inercia pero distribución asimétrica puede generar frenado desigual por eje. Perfil de riesgo: ALTO."}'
    )

    return {'tabla_proceso': rows, 'os_profile': os_profile}


# ── CURVA ASCENDENTE ───────────────────────────────────────────────────────────

def _curva_ascendente(load_state, has_rampa, has_caseta, dist_km):
    is_full = load_state == FULL_LOAD
    vel_curva = '35–45 km/h' if is_full else '45–55 km/h'
    cg_nota = 'centro de gravedad en su posición más alta — riesgo de vuelco maximizado' if is_full else 'centro de gravedad desplazado por asimetría de carga — comportamiento en curva impredecible'

    rows = [
        _r(1,
           'Zona de entrada a la curva',
           f'El convoy ({cg_nota}) debe reducir velocidad a {vel_curva} ANTES de entrar a la curva; la fuerza centrífuga y el gradiente de ascenso actúan simultáneamente desde el inicio de la curva',
           'Velocidad excesiva de entrada a la curva; frenada tardía que lleva el convoy al interior de la curva a velocidad crítica; superficie húmeda o con gravilla en la zona de entrada',
           f'Verificar la velocidad del convoy al acercarse a la curva: debe estar bajo {vel_curva} antes de la entrada; observar la señalización de velocidad recomendada; reportar condición del pavimento a la base',
           f'Instruir al conductor a reducir velocidad a {vel_curva} como mínimo 200 m antes de la curva; no intentar cambio de marcha dentro de la curva; señalizar la presencia del convoy con luces',
           'Si el convoy entra a la curva con velocidad excesiva: instruir reducción gradual (no frenar bruscamente); si el convoy se sale de carril: activar bocina y luces; reportar inmediatamente a base y 911',
        ),
        _r(2,
           'Interior / ápex de la curva ascendente',
           'El punto de máxima fuerza centrífuga + gradiente máximo del ascenso; el convoy está en su posición de mayor inestabilidad lateral; el segundo remolque tiende a amplificar el ángulo de giro',
           'Vuelco lateral del segundo remolque; invasión del carril contrario por el segundo remolque (excede el radio de giro del tracto); pérdida de tracción en los ejes motrices',
           'Observar mediante espejo trasero el ángulo del segundo remolque en la curva; verificar que el convoy permanezca dentro de su carril; comunicar al conductor cualquier desvío del segundo remolque',
           'No adelantar ni cambiar de carril en el ápex de la curva; mantener velocidad constante (no acelerar ni frenar abruptamente dentro del ápex); mantenerse al extremo derecho del carril',
           'Si el segundo remolque invade el carril contrario: activar bocina + luces de emergencia; reducir velocidad gradual; detenerse en el primer punto seguro posterior a la curva para inspección',
        ),
        _r(3,
           'Exterior de la curva (zona de salida de vía)',
           'El exterior de la curva es donde el convoy puede ser expulsado si la velocidad supera el umbral de vuelco; la barrera de contención (guardarrail) o el talud es el único elemento que detiene la salida',
           'Vuelco lateral hacia el exterior; salida de vía por exceso de velocidad en la curva; impacto contra el guardarrail exterior con posible ruptura',
           'Verificar la existencia y condición del guardarrail en el exterior de la curva al iniciar el tramo; reportar ausencia de barrera a la base; observar el espacio de maniobra disponible',
           'Mantener el convoy alejado del borde exterior del carril; si el pavimento en el exterior muestra deterioro (grietas, bordes sueltos) reportar a base y reducir velocidad adicional',
           'Si el convoy se dirige al exterior de la curva: instruir giro suave hacia el interior (no frenar bruscamente); si el impacto con guardarrail es inminente: activar bocina, preparar comunicación de emergencia',
        ),
        _r(4,
           'Carril de sentido contrario',
           'El segundo remolque del convoy, en curvas cerradas ascendentes, puede sobresalir hacia el carril contrario por el radio de giro extendido; vehículos en sentido contrario no anticipan esta invasión',
           'Colisión frontal con vehículo en sentido contrario invadido por el segundo remolque; vehículo en sentido contrario que también invade el carril del convoy (doble invasión)',
           'Observar la visibilidad hacia el carril contrario antes de entrar a la curva; identificar vehículos que vienen en sentido contrario y comunicar al conductor; verificar la señalización de carril único si aplica',
           'Activar las luces de advertencia y presencia antes de entrar a la curva cerrada; reducir al máximo el ancho ocupado en el carril propio; si es posible, ceder momentáneamente el paso al vehículo contrario',
           'Si colisión frontal inminente: bocina continua + reducir a velocidad mínima; si impacto ocurre: asegurar al conductor, luces de emergencia, triángulos, notificar base y 911',
        ),
        _r(5,
           'Zona de articulación del doble remolque',
           'Los dos puntos de articulación del convoy (entre tracto y 1er remolque, y entre remolques) están bajo máxima tensión torsional en curva + ascenso; la conexión entre remolques es el punto más débil',
           'Ruptura o desacoplamiento de la conexión entre remolques en plena curva; exceso de ángulo de articulación que deja el segundo remolque perpendicular al carril; jackknifing parcial en curva ascendente',
           'Verificar el estado de los enganches y la quinta rueda ANTES del tramo de curvas; observar el ángulo de articulación mediante cámara trasera durante la curva; reportar cualquier sonido metálico inusual de los enganches',
           'Velocidad máxima en curva ajustada al radio de curvatura; no acelerar abruptamente dentro de la curva para no aumentar el ángulo de articulación; revisar el enganche en toda parada previa al tramo',
           'Si se detecta movimiento anómalo en la articulación: detención en el primer punto seguro + inspección de enganche + no continuar si hay daño visible; notificar base y solicitar asistencia técnica',
        ),
        _r(6,
           'Control de velocidad y comunicación en curva',
           f'El OS debe coordinar activamente la velocidad del convoy durante el ascenso en curva ({vel_curva}); la comunicación con la base puede ser intermitente en zonas de ladera y curva',
           'Conductor que no respeta la velocidad máxima recomendada en curva; falta de comunicación con la base en el momento de mayor riesgo; conductor distraído por comunicación en plena curva',
           'Verificar la velocidad del convoy en tiempo real durante la curva; no iniciar comunicaciones con la base mientras el convoy está en el ápex de la curva (distrae al conductor)',
           'Toda comunicación verbal entre OS y conductor debe realizarse ANTES o DESPUÉS de la curva, nunca durante; el OS no debe solicitar atención del conductor en el punto de mayor demanda',
           'Si se necesita comunicar una emergencia dentro de la curva: señales visuales (toque en hombro, señal convenida) en lugar de comunicación verbal; verbalizar la situación solo al salir de la curva',
        ),
    ]

    os_profile = (
        f'El OS actúa como controlador de velocidad y estabilidad lateral en este tramo de curva ascendente. '
        f'PUEDE: verificar la velocidad de entrada a la curva vs. el umbral seguro ({vel_curva}); '
        f'alertar al conductor de vehículos en sentido contrario; ordenar detención antes de la curva si las condiciones de la superficie son adversas; '
        f'coordinar con la base durante los tramos rectos entre curvas. '
        f'NO PUEDE: tomar el control del vehículo; instruir maniobras en el ápex de la curva que distraigan al conductor; '
        f'garantizar la estabilidad del convoy si la velocidad de entrada supera el umbral crítico. '
        f'Condición de carga: {load_state}. '
        f'{"Carga completa = centro de gravedad máximo = umbral de vuelco más bajo. Perfil: CRÍTICO." if is_full else "Media carga asimétrica = comportamiento impredecible del segundo remolque en curva. Perfil: ALTO."}'
    )

    return {'tabla_proceso': rows, 'os_profile': os_profile}


# ── CURVA DESCENDENTE ──────────────────────────────────────────────────────────

def _curva_descendente(load_state, has_rampa, has_caseta, dist_km):
    is_full = load_state == FULL_LOAD
    vel_critica = '30–40 km/h' if is_full else '40–50 km/h'
    escenario = 'Máximo riesgo del viaje: fuerza gravitacional + fuerza centrífuga + ' + (
        'masa completa del convoy' if is_full else 'masa asimétrica por media carga'
    ) + ' actúan simultáneamente'

    rows = [
        _r(1,
           'Zona previa de frenado (antes de entrar a la curva)',
           f'{escenario}. El convoy DEBE llegar a la curva a {vel_critica} o menos; si los frenos ya están comprometidos por un descenso previo, esta zona es el punto de decisión crítica',
           'Frenos calientes desde descenso previo que no tienen capacidad residual; conductor que subestima la velocidad de entrada necesaria; superficie húmeda que reduce la adherencia en la fase de frenado',
           f'Verificar temperatura de frenos ANTES de la curva (olor, humo, comportamiento del pedal); confirmar que la velocidad está bajo {vel_critica} al menos 300 m antes de la curva; revisar el estado del pavimento en la zona de entrada',
           f'Ordenar detención preventiva en el primer punto seguro si los frenos presentan cualquier señal de compromiso; velocidad de entrada a la curva: máximo {vel_critica}; freno motor activo obligatorio desde antes del inicio de la curva',
           'Si frenos comprometidos antes de la curva: dirigir al conductor a la rampa de emergencia' + (' (identificada en este tramo)' if has_rampa else ' (sin rampa — mantener velocidad mínima posible y dirigirse al guardarrail de montaña como último recurso)') + '; notificar base y 911',
        ),
        _r(2,
           'Ápex de la curva descendente',
           'El punto de máxima demanda simultánea del viaje: frenos + fuerza centrífuga + peso + gradiente + visibilidad reducida; cualquier error de velocidad o dirección en este punto puede ser fatal',
           'Vuelco lateral en el ápex; jackknifing por frenada brusca; salida de vía hacia el talud exterior; colisión frontal con vehículo en sentido contrario',
           'Observar el ángulo del segundo remolque mediante espejo o cámara; verificar que el convoy permanezca dentro del carril; detectar cualquier señal de pérdida de adherencia (deslizamiento)',
           'CERO comunicaciones verbales durante el ápex; no tocar al conductor ni distraerlo de ninguna manera; el OS se mantiene en observación silenciosa durante el ápex',
           'Si el convoy comienza a descontrolarse en el ápex: señal visual al conductor (señal convenida de emergencia); activar bocina si hay vehículo en sentido contrario; reportar a base al salir de la curva',
        ),
        _r(3,
           'Exterior de la curva descendente (zona de salida de vía)',
           'El exterior de la curva descendente es el punto de mayor probabilidad de salida de vía en todo el viaje; la velocidad + la fuerza centrífuga + la pendiente impulsan el convoy hacia el exterior',
           'Salida de vía hacia talud exterior o barranca; impacto del convoy contra guardarrail a alta velocidad; vuelco lateral hacia el exterior con caída por ladera',
           'Verificar la existencia y robustez del guardarrail exterior al inicio del tramo; reportar ausencia de barrera a la base como factor de riesgo adicional; observar el espacio entre el convoy y el borde',
           'El OS NO debe dar instrucciones al conductor sobre el carril durante la curva descendente si ya se han dado antes; toda instrucción debe ser anterior al ingreso a la curva',
           'Si el convoy se dirige al exterior: el conductor DECIDE si usa la rampa o el guardarrail; el OS reporta a base; al detenerse: luces de emergencia + triángulos + 911',
        ),
        _r(4,
           'Rampa de emergencia' + (' (identificada en este tramo)' if has_rampa else ' (no identificada en este tramo)'),
           'La rampa de emergencia es el único dispositivo de rescate para un convoy desbocado; su uso requiere que el conductor la conozca, la identifique a tiempo y tome la decisión a la velocidad correcta',
           'Conductor que no conoce la ubicación de la rampa; rampa obstruida por otro vehículo o mal conservada; conductor que decide no usarla por miedo al daño del vehículo',
           'Confirmar la posición kilométrica de la rampa ANTES de iniciar el descenso; comunicar al conductor su ubicación con referencia visual clara; verificar si la rampa está visible y despejada',
           'El OS APOYA ACTIVAMENTE la decisión del conductor de usar la rampa; no debe haber dudas ni debate sobre usar la rampa si los frenos están fallando' + ('; rampa confirmada en este tramo' if has_rampa else '; sin rampa en este tramo: comunicar esta información al conductor antes del descenso'),
           'Si convoy se dirige a rampa: comunicar inmediatamente a base; al detenerse: luces + triángulos + 911 para asistencia de recuperación; no mover el vehículo hasta inspección completa',
        ),
        _r(5,
           'Carril de sentido contrario en curva descendente',
           'El segundo remolque puede invadir el carril contrario en la curva descendente; un vehículo en sentido contrario que también ocupa el centro provoca una colisión frontal a suma de velocidades',
           'Colisión frontal por invasión recíproca de carriles; vehículo pequeño no visible hasta el ápex por la geometría de la curva; vehículo de alta velocidad en sentido contrario sin anticipar la invasión del convoy',
           'Verificar visibilidad hacia el carril contrario antes de entrar a la curva; comunicar al conductor si hay tráfico visible en sentido contrario; observar señalización de carril único o de preferencia si aplica',
           'Activar luces de advertencia (alta visibilidad) antes de entrar a la curva; si hay camión o vehículo grande en sentido contrario, reducir velocidad adicional y ceder espacio lateral máximo posible',
           'Si colisión frontal inminente: bocina continua + velocidad mínima; si impacto: asegurar al conductor, luces de emergencia, triángulos hacia ambos lados de la curva, notificar base y 911',
        ),
        _r(6,
           'Sistema de frenos y comunicaciones en curva descendente',
           f'La combinación de descenso + curva genera la demanda más alta de frenos en todo el viaje; la comunicación con la base puede ser intermitente; el OS debe haber coordinado todos los protocolos ANTES del tramo',
           'Pérdida total de frenos en el punto de mayor exigencia; imposibilidad de comunicar a la base en zona sin cobertura; conductor que entra a la curva sin haber verificado el estado de los frenos',
           'Confirmar el estado de los frenos en el paradero o punto de verificación previo al tramo; establecer protocolo de comunicación antes de entrar (última posición reportada, tiempo estimado de salida de la curva)',
           'Toda verificación de frenos y comunicación de protocolos debe realizarse ANTES de entrar al tramo; dentro de la curva descendente el OS solo observa y usa señales visuales de emergencia si es necesario',
           'Si pérdida total de frenos en curva descendente: rampa de emergencia si está disponible; si no: reducción de velocidad usando el motor, cambio a marcha baja, guardarrail de montaña como último recurso; notificar base en cuanto haya señal',
        ),
    ]

    os_profile = (
        f'El OS opera en el segmento de MÁXIMO RIESGO COMBINADO del viaje (descenso + curva + {load_state.lower()}). '
        f'PUEDE: verificar la temperatura de frenos antes del tramo; comunicar la posición exacta de la rampa de emergencia; '
        f'ordenar detención preventiva ante cualquier señal de fading; usar señales visuales de emergencia dentro de la curva. '
        f'NO PUEDE: garantizar la detención del convoy si los frenos fallan totalmente; '
        f'instruir verbalmente al conductor durante el ápex de la curva (máxima concentración del conductor requerida); '
        f'tomar el control mecánico del vehículo desde su posición. '
        f'Condición de carga: {load_state}. '
        f'{"Carga completa = máxima inercia + mayor momento volcador. Cualquier error de velocidad puede ser fatal. Perfil: CRÍTICO MÁXIMO." if is_full else "Media carga asimétrica = comportamiento impredecible del segundo remolque. El frenado desigual por eje es el mayor peligro. Perfil: CRÍTICO."}'
    )

    return {'tabla_proceso': rows, 'os_profile': os_profile}


# ── Dispatch ───────────────────────────────────────────────────────────────────

_BUILDERS = {
    'Recta':             _recta,
    'Recta Ascendente':  _recta_ascendente,
    'Recta Descendente': _recta_descendente,
    'Curva Ascendente':  _curva_ascendente,
    'Curva Descendente': _curva_descendente,
}


def _has(referencias, keyword):
    return any(keyword.lower() in r.lower() for r in referencias)


def generate_risk_analysis(tramo: dict, load_state: str) -> dict:
    """
    Return PROCESO operational risk analysis for a single tramo.

    Returns:
    {
      'load_state':      str,
      'load_state_flag': bool,
      'tabla_proceso':   [ [#, Area, Dinamica, Amenazas, Vigilancia, Restriccion, Intervencion], ... ],
      'os_profile':      str,
    }
    """
    trazo    = tramo.get('trazo_topografia', 'Recta')
    refs     = tramo.get('referencias', [])
    dist_km  = tramo.get('distancia_km', 0.0)
    has_rampa  = _has(refs, 'rampa')
    has_caseta = _has(refs, 'caseta') or _has(refs, 'paradero')

    builder = _BUILDERS.get(trazo, _recta)
    result  = builder(load_state, has_rampa, has_caseta, dist_km)

    load_state_flag = (load_state == HALF_LOAD) and (trazo in _HALF_LOAD_FLAG_TRAZOS)

    return {
        'load_state':      load_state,
        'load_state_flag': load_state_flag,
        'tabla_proceso':   result['tabla_proceso'],
        'os_profile':      result['os_profile'],
    }
