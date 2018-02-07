import fnmatch
import copy
from terminaltables import AsciiTable

# Función auxiliar utilizada para reemplazar en una cadena de derecha a izquierda
def replace_right(source, target, replacement, replacements=None):
    return replacement.join(source.rsplit(target, replacements))

# Conjugator: provee diferentes funciones para conjugar verbos en español a los
# siguientes tiempos:
# - Indicativo
# --- Presente
# --- Preterito imperfecto
# --- Preterito perfecto
# --- Condicional
# --- Futuro
# - Subjuntivo
# --- Preterito imperfecto (2)
# - Imperativo (diferentes variaciones y adaptaciones al dialecto argentino)
class Conjugator:

    # Estas clases sirven de referencia para determinar si una conjugacion se
    # efectua sobre el singular, plural y en que persona.
    singular = [0, 1, 2]
    plural = [3, 4, 5]

    primera_persona = [0, 3]
    segunda_persona = [1, 4]
    tercera_persona = [2, 5]

    # Este diccionario contiene las excepciones de los verbos totalmente irregulares
    # o los que finalizan familias de verbos (hacer, leer, caer, etc).
    # La misma se inicializa al momento de instanciar la clase a través del constructor.
    irregular_verbs = { }


    # A continuación se enumeran grupos de verbos irregulares que comparten
    # caracteristicas similares en cuanto a los cambios que debe realizarceles
    # al momento de conjugarlos.
    irregular_verbs_grupo_01_ar = ['acertar', 'acrecentar', 'alentar', 'apretar',
    'arrendar', 'asentar', 'asosegar', 'aterrar', 'atravesar', 'calentar', 'cegar', 'cerrar',
    'comenzar', 'concertar', 'confesar', 'denegar', 'desalentar', 'desasosegar',
    'desconcertar', 'desenterrar', 'deshelar', 'desmembrar', 'despertar', 'desplegar',
    'desterrar', 'emparentar', 'empezar', 'encerrar', 'encomendar', 'enmendar',
    'ensangrentar', 'enterrar', 'escarmentar', 'fregar', 'gobernar', 'helar',
    'herrar', 'invernar', 'manifestar', 'mentar', 'merendar', 'negar', 'nevar', 'pensar',
    'plegar', 'quebrar', 'recalentar', 'recomendar', 'refregar', 'regar', 'remendar',
    'renegar', 'repensarse', 'replegar', 'restregar', 'reventar', 'salpimentar', 'segar',
    'sembrar', 'sentar', 'serrar', 'sosegar', 'soterrar', 'subarrendar', 'temblar', 'tentar',
    'tropezar']

    irregular_verbs_grupo_01_er = ['ascender', 'atender', 'defender', 'desatender',
    'descender', 'encender', 'entender', 'extender', 'heder', 'perder', 'sobrentender',
    'tender', 'trascender', 'verter']

    irregular_verbs_grupo_01_ir = ['cernir', 'concernir', 'discernir']

    irregular_verbs_grupo_02_ar = ['acordar', 'almorzar', 'apostar', 'aprobar',
    'asolar', 'avergonzar', 'colar', 'colgar', 'comprobar', 'concordar', 'consolar',
    'contar', 'costar', 'degollar', 'demostrar', 'desaprobar', 'descolgar', 'descontar',
    'desosar', 'desollar', 'despoblarse', 'encontrar', 'engrosar', 'esforzarse',
    'forzar', 'mostrar', 'poblar', 'probar', 'recordar', 'recostar', 'reforzar',
    'renovar', 'repoblar', 'reprobar', 'resollar', 'resonar', 'revolcar', 'rodar',
    'rogar', 'sobrevolar', 'soldar', 'soltar', 'sonar', 'soñar', 'tostar', 'trastocarse',
    'tronar', 'volar', 'volcar']

    irregular_verbs_grupo_02_er = ['absolver', 'cocer', 'conmover', 'demoler',
    'desenvolver', 'devolver', 'disolver', 'doler', 'envolver', 'escocer', 'llover',
    'moler', 'morder', 'mover', 'oler', 'promover', 'remorder', 'remover', 'resolver',
    'retorcer', 'revolver', 'soler', 'torcer', 'volver']

    irregular_verbs_grupo_03_acer = ['complacer', 'nacer', 'pacer', 'renacer']

    irregular_verbs_grupo_03_ecer = ['abastecer', 'aborrecer', 'acaecer', 'acontecer',
    'adolecer', 'agradecer', 'amanecer', 'anochecer', 'aparecer', 'apetecer', 'atardecer',
    'carecer', 'compadecer', 'comparecer', 'convalecer', 'crecer', 'decrecer',
    'desaparecer', 'desentumecer', 'desfallecer', 'desfavorecer', 'desobedecer',
    'desvanecerse', 'embellecer', 'embrutecer', 'empobrecer', 'enaltecer', 'enardecer',
    'encarecer', 'endurecer', 'enfurecer', 'enloquecer', 'enmohecer', 'enmudecer',
    'ennegrecer', 'ennoblecer', 'enorgullecer', 'enrarecer', 'enriquecer',
    'enrojecer', 'ensombrecer', 'ensordecer', 'enternecer', 'entorpecer',
    'entristecer', 'entumecer', 'envejecer', 'envilecer', 'esclarecer', 'establecer',
    'estremecer', 'fallecer', 'favorecer', 'florecer', 'fortalecer', 'guarecer',
    'humedecer', 'languidecer', 'merecer', 'obedecer', 'ofrecer', 'oscurecer',
    'padecer', 'palidecer', 'parecer', 'perecer', 'permanecer', 'pertenecer',
    'prevalecer', 'reaparecer', 'reblandecer', 'recrudecer', 'rejuvenecer',
    'resplandecer', 'restablecer']

    irregular_verbs_grupo_03_ocer = ['conocer', 'desconocer', 'reconocer']

    irregular_verbs_grupo_03_ucer = ['balbucir', 'deslucir', 'lucir', 'relucir']

    irregular_verbs_grupo_04_ducir = ['aducir', 'conducir', 'deducir', 'inducir',
    'introducir', 'producir', 'reducir', 'reproducir', 'seducir', 'traducir']

    irregular_verbs_grupo_05_er =['atañer', 'tañer']

    irregular_verbs_grupo_05_ñir =['gruñir', 'restriñir']

    irregular_verbs_grupo_05_ullir =['bullir', 'engullir', 'escabullir', 'zambullir']

    irregular_verbs_grupo_06_ir = ['comedir', 'competir', 'concebir', 'conseguir',
    'corregir', 'derretir', 'despedir', 'desvestir', 'elegir', 'embestir', 'expedir',
    'gemir', 'impedir', 'investir', 'medir', 'pedir', 'perseguir', 'proseguir',
    'reelegir', 'regir', 'rendir', 'repetir', 'reseguir', 'revestir', 'seguir', 'servir',
    'transgredir', 'trasgredir', 'trasvestir', 'vestir']

    irregular_verbs_grupo_07_eñir = ['ceñir', 'desteñir', 'mullir', 'reñir', 'teñir']

    irregular_verbs_grupo_07_eir = ['desleír', 'freír', 'reír', 'sonreír', 'sofreír']

    irregular_verbs_grupo_08_ir = ['adherir', 'advertir', 'arrepentirse', 'asentir',
    'conferir', 'consentir', 'convertir', 'desmentir', 'diferir', 'digerir',
    'disentir', 'divertir', 'herir', 'hervir', 'ingerir', 'injerir', 'inserir',
    'invertir', 'malherir', 'mentir', 'pervertir', 'preferir', 'presentir',
    'proferir', 'referir', 'requerir', 'resentirse', 'revertir', 'sentir',
    'sugerir', 'transferir']

    irregular_verbs_grupo_09_u = ['jugar']

    irregular_verbs_grupo_10_irir = ['adquirir', 'inquirir']

    irregular_verbs_grupo_11_uir = ['afluir', 'atribuir', 'concluir', 'confluir',
    'constituir', 'construir', 'contribuir', 'derruir', 'destituir', 'destruir',
    'diluir', 'disminuir', 'distribuir', 'excluir', 'fluir', 'huir', 'imbuir',
    'incluir', 'inmiscuir', 'influir', 'instituir', 'instruir', 'intuir',
    'obstruir', 'prostituir', 'reconstruir', 'recluir', 'rehuir', 'restituir',
    'retribuir', 'substituir', 'sustituir']

    irregular_verbs_grupo_12_o = ['dormir', 'morir']

    irregular_verbs_grupo_13_aler = ['equivaler', 'valer']

    irregular_verbs_grupo_13_alir = ['salir', 'sobresalir']

    # Excepciones al diptongo ue
    h_exceptions = ['desosar', 'oler']


    # Constructor. Setea el modo en el que se utilizará el conjugador e inicializa
    # el diccionario de verbos irregulares base.
    # <modo> valor numerico entero que define el modo de uso:
    # --> 0: dialecto argentino, se reemplaza la conjugación de la segunda persona
    # singular para adaptarlo al "voseo" caracteristico del dialecto.
    # --> != 0: dialecto general. Se deja como valor numerico y no como booleano
    # pensando en la posibilidad de adaptar el conjugador a nuevos modos.
    #
    #
    # TODO: Ver la forma de extraer el listado de verbos irregulares a un listado
    # externo que se cargue al cargar el conjugador.
    def __init__(self, mode):
        self.mode = mode
        self.irregular_verbs['ir'] = {
            'inf': ['ir'],
            'ger' : ['yendo'],
            'part': self.participio('ir', True),
            'pres': ['voy', 'vas', 'vas', 'vamos', 'vais', 'van'],
            'pret_perf': ['fuí', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron'],
            'pret_imperf': ['iba', 'ibas', 'iba', 'ibamos', 'ibais', 'iban'],
            'fut': self.futuro_simple_conj('ir', True),
            'impA': ['', 've', 'vaya', 'vayamos', 'id', 'vayan'],
            'impB': ['','','','','',''],
            'impC': self.imperativo_C_conj('ir', True),
            'condA': self.condicional_simple_A_conj('ir', True),
            'condB': ['fuese', 'fueses', 'fuese', 'fuésemos', 'fueseis', 'fuesen']
        }
        if self.mode == 0:
            self.irregular_verbs['ir']['impA'][1] = 'andá'
        self.irregular_verbs['andar'] = {
            'inf': ['andar'],
            'ger' : self.gerundio('andar', True),
            'part': self.participio('andar', True),
            'pres': self.presente_conj('andar', True),
            'pret_perf': ['anduve', 'anduviste', 'anduvo', 'anduvimos', 'anduvisteis', 'anduvieron'],
            'pret_imperf': self.preterito_imperf_conj('andar', True),
            'fut': self.futuro_simple_conj('andar', True),
            'impA': self.imperativo_A_conj('andar', True),
            'impB': self.imperativo_B_conj('andar', True),
            'impC': self.imperativo_C_conj('andar', True),
            'condA': self.condicional_simple_A_conj('andar', True),
            'condB': ['anduviese', 'anduvieses', 'anduviese', 'anduviésemos', 'anduvieseis', 'anduviesen']
        }
        self.irregular_verbs['asir'] = {
            'inf': ['asir'],
            'ger' : self.gerundio('asir', True),
            'part': self.participio('asir', True),
            'pres': ['asgo', 'ases', 'ase', 'asimos', 'asís', 'asen'],
            'pret_perf': self.preterito_perf_simple_conj('asir', True),
            'pret_imperf': self.preterito_imperf_conj('asir', True),
            'fut': self.futuro_simple_conj('asir', True),
            'impA': self.imperativo_A_conj('asir', True),
            'impB': self.imperativo_B_conj('asir', True),
            'impC': self.imperativo_C_conj('asir', True),
            'condA': self.condicional_simple_A_conj('asir', True),
            'condB': self.condicional_simple_B_conj('asir', True)
        }
        if self.mode == 0:
            self.irregular_verbs['asir']['pres'][1] = 'asís'
        self.irregular_verbs['caber'] = {
            'inf': ['caber'],
            'ger' : self.gerundio('caber', True),
            'part': self.participio('caber', True),
            'pres': ['quepo', 'cabes', 'cabe', 'cabemos', 'cabéis', 'caben'],
            'pret_perf': ['cupe', 'cupiste', 'cupo', 'cupimos', 'cupisteis', 'cupieron'],
            'pret_imperf': self.preterito_imperf_conj('caber', True),
            'fut': self.futuro_simple_conj('caber', True),
            'impA': self.imperativo_A_conj('caber', True),
            'impB': self.imperativo_B_conj('caber', True),
            'impC': self.imperativo_C_conj('caber', True),
            'condA': ['cabría', 'cabrías', 'cabría', 'cabríamos', 'cambríais', 'cabriamos'],
            'condB': ['cupiese', 'cupieses', 'cupiese', 'cupiésemos', 'cupieseis', 'cupiesen']
        }
        if self.mode == 0:
            self.irregular_verbs['caber']['pres'][1] = 'cabés'
        self.irregular_verbs['caer'] = {
            'inf': ['caer'],
            'ger' : ['cayendo'],
            'part': self.participio('caer', True),
            'pres': ['caigo', 'caés', 'cae', 'caemos', 'caéis', 'caen'],
            'pret_perf': ['caí', 'caiste', 'cayó', 'caimos', 'caisteis', 'cayeron'],
            'pret_imperf': self.preterito_imperf_conj('caer', True ),
            'fut': self.futuro_simple_conj('caer', True),
            'impA': ['', 'cae', 'caiga', 'caigamos', 'caed', 'caigan'],
            'impB': self.imperativo_B_conj('caer', True),
            'impC': self.imperativo_C_conj('caer', True),
            'condA': self.condicional_simple_A_conj('caer', True),
            'condB': ['cayese', 'cayeses', 'cayese', 'cayésemos', 'cayeseis', 'cayesen']
        }
        if self.mode == 0:
            self.irregular_verbs['caer']['pres'][1] = 'caés'
            self.irregular_verbs['caer']['impA'][1] = 'caé'
        self.irregular_verbs['dar'] = {
            'inf': ['dar'],
            'ger' : self.gerundio('dar', True),
            'part': self.participio('dar', True),
            'pres': ['doy', 'das', 'da', 'damos', 'dáis', 'dan'],
            'pret_perf': ['dí', 'diste', 'dió', 'dimos', 'disteis', 'dieron'],
            'pret_imperf': self.preterito_imperf_conj('dar', True ),
            'fut': self.futuro_simple_conj('dar', True),
            'impA': self.imperativo_A_conj('dar', True),
            'impB': self.imperativo_B_conj('dar', True),
            'impC': self.imperativo_C_conj('dar', True),
            'condA': self.condicional_simple_A_conj('dar', True),
            'condB': ['diese', 'dieses', 'diese', 'diesemos', 'dieseis', 'diesen']
        }
        self.irregular_verbs['erguir'] = {
            'inf': ['erguir'],
            'ger' : ['irguiendo'],
            'part': self.participio('erguir', True),
            'pres': ['yergo', 'yergues', 'yergue', 'erguimos', 'erguis', 'yerguen'],
            'pret_perf': ['erguí', 'erguiste', 'irguió', 'erguimos', 'erguisteis', 'irguieron'],
            'pret_imperf': self.preterito_imperf_conj('erguir', True ),
            'fut': self.futuro_simple_conj('erguir', True),
            'impA': ['', 'yergue', 'yerga', 'yergamos', 'erguid', 'yergan'],
            'impB': self.imperativo_B_conj('erguir', True),
            'impC': self.imperativo_C_conj('erguir', True),
            'condA': self.condicional_simple_A_conj('erguir', True),
            'condB': ['irguiese', 'irguieses', 'irguiese', 'irguiésemos', 'irguieseis', 'irguiesen']
        }
        if self.mode == 0:
            self.irregular_verbs['erguir']['pres'][1] = 'erguís'
            self.irregular_verbs['erguir']['impA'][1] = 'erguí'
        self.irregular_verbs['estar'] = {
            'inf': ['estar'],
            'ger' : self.gerundio('estar', True),
            'part': self.participio('erguir', True),
            'pres': ['estoy', 'estás', 'está', 'estamos', 'estáis', 'están'],
            'pret_perf': ['estuve', 'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron'],
            'pret_imperf': self.preterito_imperf_conj('estar', True ),
            'fut': self.futuro_simple_conj('estar', True),
            'impA': self.imperativo_A_conj('estar', True),
            'impB': self.imperativo_B_conj('estar', True),
            'impC': self.imperativo_C_conj('estar', True),
            'condA': self.condicional_simple_A_conj('estar', True),
            'condB': ['estuviese', 'estuvieses', 'estuviese', 'estuviesemos', 'estuvieseis', 'estuviesemos']
        }
        if self.mode == 0:
            self.irregular_verbs['estar']['pres'][1] = 'estate'
        self.irregular_verbs['haber'] = {
            'inf': ['haber'],
            'ger' : self.gerundio('haber', True),
            'part': self.participio('haber', True),
            'pres': ['he', 'has', 'ha', 'hemos', 'habéis', 'han'],
            'pret_perf': ['hube', 'hubiste', 'hubo', 'hubimos', 'hubistéis', 'hubieron'],
            'pret_imperf': self.preterito_imperf_conj('haber', True ),
            'fut': ['habré', 'habrás', 'habrá', 'habremos', 'habréis', 'habrán'],
            'impA': ['', '', '', '', '', ''],
            'impB': self.imperativo_B_conj('haber', True),
            'impC': self.imperativo_C_conj('haber', True),
            'condA': ['habría', 'habrías', 'habría', 'habríamos', 'habríais', 'habrían'],
            'condB': ['hubiese', 'hubieses', 'hubiese', 'hubiésemos', 'hubieseis', 'hubiesen']
        }
        self.irregular_verbs['leer'] = {
            'inf': ['leer'],
            'ger' : ['leyendo'],
            'part': ['leído', 'leída', 'leerse'],
            'pres': self.presente_conj('leer',  True),
            'pret_perf': ['leí', 'leiste', 'leyó', 'leimos', 'leístes', 'leyeron'],
            'pret_imperf': self.preterito_imperf_conj('leer', True ),
            'fut': self.futuro_simple_conj('leer', True),
            'impA': self.imperativo_A_conj('leer', True),
            'impB': self.imperativo_B_conj('leer', True),
            'impC': self.imperativo_C_conj('leer', True),
            'condA': self.condicional_simple_A_conj('leer', True),
            'condB': ['leyese', 'leyeses', 'leyese', 'leyésemos', 'leyeseis', 'leyesen']
        }
        if self.mode != 0:
            self.irregular_verbs['leer']['impA'][1] = 'lee'
        self.irregular_verbs['oír'] = {
            'inf': ['oír'],
            'ger' : ['oyendo'],
            'part': self.participio('oír', True),
            'pres': ['oigo', 'oyes', 'oye', 'oimos', 'oís', 'oyen'],
            'pret_perf': ['oí', 'oiste', 'oyó', 'oimos', 'oisteis', 'oyeron'],
            'pret_imperf': self.preterito_imperf_conj('oír', True ),
            'fut': self.futuro_simple_conj('oír', True),
            'impA': ['', 'oye', 'oiga', 'oigamos', 'oíd', 'oigan'],
            'impB': self.imperativo_B_conj('oír', True),
            'impC': self.imperativo_C_conj('oír', True),
            'condA': self.condicional_simple_A_conj('oír', True),
            'condB': ['oyese', 'oyeses', 'oyese', 'oyésemos', 'oyeseis', 'oyesen']
        }
        if self.mode == 0:
            self.irregular_verbs['oír']['pres'][1] = 'oís'
            self.irregular_verbs['oír']['impA'][1] = 'oí'
        self.irregular_verbs['poder'] = {
            'inf': ['poder'],
            'ger' : ['pudiendo'],
            'part': self.participio('poder', True),
            'pres': ['puedo', 'puedes', 'pueden', 'podemos', 'podéis', 'pueden'],
            'pret_perf': ['pude', 'pudiste', 'pudo', 'pudimos', 'pudisteis', 'pudieron'],
            'pret_imperf': self.preterito_imperf_conj('poder', True ),
            'fut': ['podré', 'podrás', 'podrá', 'podremos', 'podréis', 'podrán'],
            'impA': ['', 'puede', 'pueda', 'podamos', 'poded', 'puedan'],
            'impB': self.imperativo_B_conj('poder', True),
            'impC': self.imperativo_C_conj('poder', True),
            'condA': ['podría', 'podrías', 'podría', 'podríamos', 'podríais', 'podrían'],
            'condB': ['pudiese', 'pudieses', 'pudiese', 'pudiésemos', 'pudieseis', 'pudiesen']
        }
        if self.mode == 0:
            self.irregular_verbs['poder']['pres'][1] = 'podés'
            self.irregular_verbs['poder']['impA'][1] = 'podé'
        self.irregular_verbs['poner'] = {
            'inf': ['poner'],
            'ger' : self.gerundio('poner', True),
            'part': ['puesto', 'puesta', 'ponerse'],
            'pres': ['pongo', 'pones', 'pone', 'ponemos', 'ponéis', 'ponen'],
            'pret_perf': ['puse', 'pusiste', 'puso', 'pusimos', 'pusisteis', 'pusieron'],
            'pret_imperf': self.preterito_imperf_conj('poner', True ),
            'fut': ['pondré', 'pondrás', 'pondrá', 'pondremos', 'pondréis', 'pondrán'],
            'impA': ['', 'pon', 'ponga', 'pongamos', 'poned', 'pongan'],
            'impB': self.imperativo_B_conj('poner', True),
            'impC': self.imperativo_C_conj('poner', True),
            'condA': ['pondría', 'pondrías', 'pondría', 'pondríamos', 'pondríais', 'pondrían'],
            'condB': ['pusiese', 'pusieses', 'pusiese', 'pusiésemos', 'pusieseis', 'pusiesen']
        }
        if self.mode == 0:
            self.irregular_verbs['poner']['pres'][1] = 'ponés'
            self.irregular_verbs['poner']['impA'][1] = 'poné'
        self.irregular_verbs['podrir'] = {
            'inf': ['podrir'],
            'ger' : self.gerundio('pudrir', True),
            'part': self.participio('podrir', True),
            'pres': self.presente_conj('pudrir', True),
            'pret_perf': self.preterito_perf_simple_conj('podrir', True),
            'pret_imperf': self.preterito_imperf_conj('podrir', True),
            'fut': self.futuro_simple_conj('podrir', True),
            'impA': self.imperativo_A_conj('podrir', True),
            'impB': self.imperativo_B_conj('podrir', True),
            'impC': self.imperativo_C_conj('podrir', True),
            'condA': self.condicional_simple_A_conj('podrir', True),
            'condB': self.condicional_simple_B_conj('pudrir', True)
        }
        if self.mode == 0:
            self.irregular_verbs['poner']['pres'][1] = 'ponés'
            self.irregular_verbs['poner']['impA'][1] = 'poné'
        self.irregular_verbs['querer'] = {
            'inf': ['querer'],
            'ger' : self.gerundio('querer', True),
            'part': self.participio('querer', True),
            'pres': ['quiero', 'quieres', 'quiere', 'queremos', 'queréis', 'quieren'],
            'pret_perf': ['quise', 'quisiste', 'quiso', 'quisimos', 'quisisteis', 'quisieron'],
            'pret_imperf': self.preterito_imperf_conj('querer', True),
            'fut': ['querré', 'querrás', 'querrá', 'querremos', 'querréis', 'querrán'],
            'impA': ['', 'quiere', 'quiera', 'queramos', 'quered', 'quieran'],
            'impB': self.imperativo_B_conj('querer', True),
            'impC': self.imperativo_C_conj('querer', True),
            'condA': ['querría', 'querrías', 'querría', 'querriamos', 'querríais', 'querrían'],
            'condB': ['quisiese', 'quisieses', 'quisiese', 'quisiésemos', 'quisieseis', 'quisiesen']
        }
        if self.mode == 0:
            self.irregular_verbs['querer']['pres'][1] = 'querés'
            self.irregular_verbs['querer']['impA'][1] = 'queré'
        self.irregular_verbs['roer'] = {
            'inf': ['roer'],
            'ger' : ['royendo'],
            'part': self.participio('roer', True),
            'pres': self.presente_conj('roer', True),
            'pret_perf': ['roí', 'roiste', 'royó', 'roimos', 'roísteis', 'royeron'],
            'pret_imperf': self.preterito_imperf_conj('roer', True),
            'fut': self.futuro_simple_conj('roer', True),
            'impA': self.imperativo_A_conj('roer', True),
            'impB': self.imperativo_B_conj('roer', True),
            'impC': self.imperativo_C_conj('roer', True),
            'condA': self.condicional_simple_A_conj('roer', True),
            'condB': ['royese', 'royeses', 'royese', 'royésemos', 'royeseis', 'royesen']
        }
        self.irregular_verbs['saber'] = {
            'inf': ['saber'],
            'ger' : self.gerundio('saber', True),
            'part': self.participio('saber', True),
            'pres': ['sé', 'sabes', 'sabe', 'sabemos', 'sabéis', 'saben'],
            'pret_perf': ['supe', 'supiste', 'supo', 'supimos', 'supisteis', 'supieron'],
            'pret_imperf': self.preterito_imperf_conj('saber', True),
            'fut': ['sabré', 'sabrás', 'sabrá', 'sabremos', 'sabréis', 'sabrán'],
            'impA': ['', 'sabe', 'sepa', 'sepamos', 'sabed', 'sepan'],
            'impB': self.imperativo_B_conj('saber', True),
            'impC': self.imperativo_C_conj('saber', True),
            'condA': ['sabría', 'sabrías', 'sabría', 'sabríamos', 'sabríais', 'sabrían'],
            'condB': ['supiese', 'supieses', 'supiese', 'supiésemos', 'supieseis', 'supiesen']
        }
        if self.mode == 0:
            self.irregular_verbs['saber']['pres'][1] = 'sabés'
            self.irregular_verbs['saber']['impA'][1] = 'sabé'
        self.irregular_verbs['ser'] = {
            'inf': ['ser'],
            'ger' : self.gerundio('ser', True),
            'part': ['sido', '', ''],
            'pres': ['soy', 'eres', 'es', 'somos', 'sois', 'son'],
            'pret_perf': ['fui', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron'],
            'pret_imperf': ['era', 'eras', 'era', 'eramos', 'eraís', 'eran'],
            'fut': self.futuro_simple_conj('ser', True),
            'impA': ['', 'se', 'sea', 'seamos', 'sed', 'sean'],
            'impB': self.imperativo_B_conj('ser', True),
            'impC': self.imperativo_C_conj('ser', True),
            'condA': self.condicional_simple_A_conj('ser', True),
            'condB': ['fuese', 'fueses', 'fuese', 'fuésemos', 'fueseis', 'fuesen']
        }
        if self.mode == 0:
            self.irregular_verbs['ser']['pres'][1] = 'sos'
            self.irregular_verbs['ser']['impA'][1] = 'sé'
        self.irregular_verbs['tener'] = {
            'inf': ['tener'],
            'ger' : self.gerundio('tener', True),
            'part': self.participio('tener', True),
            'pres': ['tengo', 'tienes', 'tiene', 'tenemos', 'tenéis', 'tienen'],
            'pret_perf': ['tuve', 'tuviste', 'tuvo', 'tuvimos', 'tuvisteis', 'tuvieron'],
            'pret_imperf': self.preterito_imperf_conj('tener', True),
            'fut': ['tendré', 'tendrás', 'tendrá', 'tendremos', 'tendréis', 'tendrán'],
            'impA': ['', 'ten', 'tenga', 'tengamos', 'tened', 'tengan'],
            'impB': self.imperativo_B_conj('tener', True),
            'impC': self.imperativo_C_conj('tener', True),
            'condA': ['tendría', 'tendrías', 'tendría', 'tendríamos', 'tendríais', 'tendrían'],
            'condB': ['tuviese', 'tuvieses', 'tuviese', 'tuviésemos', 'tuvieseis', 'tuviesen']
        }
        if self.mode == 0:
            self.irregular_verbs['tener']['pres'][1] = 'tenés'
            self.irregular_verbs['tener']['impA'][1] = 'tené'
        self.irregular_verbs['traer'] = {
            'inf': ['traer'],
            'ger' : ['trayendo'],
            'part': self.participio('traer', True),
            'pres': ['traigo', 'traes', 'trae', 'traemos', 'traéis', 'traen'],
            'pret_perf': ['traje', 'trajiste', 'trajo', 'trajimos', 'trajisteis', 'trajeron'],
            'pret_imperf': self.preterito_imperf_conj('traer', True),
            'fut': self.futuro_simple_conj('traer', True),
            'impA': ['', 'trae', 'traiga', 'traigamos', 'traed', 'traigan'],
            'impB': self.imperativo_B_conj('traer', True),
            'impC': self.imperativo_C_conj('traer', True),
            'condA': self.condicional_simple_A_conj('traer', True),
            'condB': ['trajese', 'trajeses', 'trajese', 'trajésemos', 'trajeseis', 'trajesen']
        }
        if self.mode == 0:
            self.irregular_verbs['traer']['pres'][1] = 'traés'
            self.irregular_verbs['traer']['impA'][1] = 'traé'
        self.irregular_verbs['venir'] = {
            'inf': ['venir'],
            'ger' : ['viniendo'],
            'part': self.participio('venir', True),
            'pres': ['vengo', 'vienes', 'viene', 'venimos', 'venís', 'vienen'],
            'pret_perf': ['vine', 'viniste', 'vino', 'vinimos', 'vinisteis', 'vinieron'],
            'pret_imperf': self.preterito_imperf_conj('venir', True),
            'fut': ['vendré', 'vendrás', 'vendrá', 'vendremos', 'vendréis', 'vendrán'],
            'impA': ['', 'ven', 'venga', 'vengamos', 'venid', 'vengan'],
            'impB': self.imperativo_B_conj('venir', True),
            'impC': self.imperativo_C_conj('venir', True),
            'condA': ['vendría', 'vendrías', 'vendría', 'vendríamos', 'vendríais', 'vendrían'],
            'condB': ['viniese', 'vinieses', 'viniese', 'viniésemos', 'vinieseis', 'viniesen']
        }
        if self.mode == 0:
            self.irregular_verbs['venir']['pres'][1] = 'venís'
            self.irregular_verbs['venir']['impA'][1] = 'vení'
        self.irregular_verbs['ver'] = {
            'inf': ['ver'],
            'ger' : self.gerundio('ver', True),
            'part': ['visto', 'vista', 'verse'],
            'pres': ['veo', 'ves', 've', 'vemos', 'véis', 'ven'],
            'pret_perf': self.preterito_perf_simple_conj('ver', True),
            'pret_imperf': ['veía', 'veías', 'veía', 'veiamos', 'veíais', 'veían'],
            'fut': self.futuro_simple_conj('ver', True),
            'impA': ['', 've', 'vea', 'veamos', 'ved', 'vean'],
            'impB': self.imperativo_B_conj('ver', True),
            'impC': self.imperativo_C_conj('ver', True),
            'condA': self.condicional_simple_A_conj('ver', True),
            'condB': self.condicional_simple_B_conj('ver', True)
        }
        if self.mode == 0:
            self.irregular_verbs['ver']['pres'][1] = 'ves'
            self.irregular_verbs['ver']['impA'][1] = 've'
        self.irregular_verbs['yacer'] = {
            'inf': ['yacer'],
            'ger' : self.gerundio('yacer', True),
            'part': self.participio('yacer', True),
            'pres': ['yazgo', 'yaces', 'yace', 'yacemos', 'yacéis', 'yacen'],
            'pret_perf': self.preterito_perf_simple_conj('yacer', True),
            'pret_imperf': self.preterito_imperf_conj('yacer', True),
            'fut': self.futuro_simple_conj('yacer', True),
            'impA': ['', 'yace', 'yazga', 'yazgamos', 'yaced', 'yazgan'],
            'impB': self.imperativo_B_conj('yacer', True),
            'impC': self.imperativo_C_conj('yacer', True),
            'condA': self.condicional_simple_A_conj('yacer', True),
            'condB': self.condicional_simple_B_conj('yacer', True)
        }
        if self.mode == 0:
            self.irregular_verbs['yacer']['pres'][1] = 'yacés'
            self.irregular_verbs['yacer']['impA'][1] = 'yacé'
        self.irregular_verbs['creer'] = {
            'inf': ['creer'],
            'ger' : ['creyendo'],
            'part': self.participio('creer', True),
            'pres': self.presente_conj('creer', True),
            'pret_perf': ['creí', 'creiste', 'creyó', 'creimos', 'creisteis', 'creyeron'],
            'pret_imperf': self.preterito_imperf_conj('creer', True),
            'fut': self.futuro_simple_conj('creer', True),
            'impA': self.imperativo_A_conj('creer', True),
            'impB': self.imperativo_B_conj('creer', True),
            'impC': self.imperativo_C_conj('creer', True),
            'condA': self.condicional_simple_A_conj('creer', True),
            'condB': ['creyese', 'creyeses', 'creyese', 'creyésemos', 'creyeseis', 'creyesen']
        }
        if self.mode == 0:
            self.irregular_verbs['yacer']['pres'][1] = 'yacés'
            self.irregular_verbs['yacer']['impA'][1] = 'yacé'


    # Genera un diccionario con el verbo pasado como parametro conjugado en los
    # distintos tiempos disponibles.
    # <verb> : debe ser una cadena de caracteres finalizada en uno de {ar, er, ir,
    # ár, ér, ír}. De no ser así se devuelve un diccionario vacio.
    def generar_diccionario_conjugacion(self, verb):
        if not any(fnmatch.fnmatch(verb, suffix) for suffix in ['*ar', '*er', '*ir', '*ár', '*ér', '*ír']):
            return {}
        key = self.extract_key(verb)
        if key != 'invalid':
            if key == '':
                conjugation = copy.deepcopy(self.irregular_verbs[verb])
                base_verb = ''
            else:
                conjugation = copy.deepcopy(self.irregular_verbs[key])
                base_verb = verb.replace(key, '')
            for key in conjugation.keys():
                i = 0
                while i < len(conjugation[key]):
                    if conjugation[key][i] != '':
                        conjugation[key][i] = base_verb + conjugation[key][i]
                    i += 1
            return conjugation
        else:
            return {'inf': [verb],
                    'ger' : self.gerundio(verb, False),
                    'part': self.participio(verb, False),
                    'pres': self.presente_conj(verb, False),
                    'pret_perf': self.preterito_perf_simple_conj(verb, False),
                    'pret_imperf': self.preterito_imperf_conj(verb, False),
                    'fut': self.futuro_simple_conj(verb, False),
                    'impA': self.imperativo_A_conj(verb, False),
                    'impB': self.imperativo_B_conj(verb, False),
                    'impC': self.imperativo_C_conj(verb, False),
                    'condA': self.condicional_simple_A_conj(verb, False),
                    'condB': self.condicional_simple_B_conj(verb, False)
        }

    # Verifica que un verbo no termine con la clave de uno de los verbos irregulares
    # declarados en el diccionario de verbos irregulares. Si efectivamente es así,
    # devuelve la cadena 'invalid' (que queda reservada para el conjugador).
    # En caso contrario si el verbo coincide completamente (no es subcadena) devuelve
    # una clave vacia. O si es una subcadena, devuelve la subcadena que ha
    # matcheado.
    def extract_key(self, verb):
        for key in self.irregular_verbs:
            if fnmatch.fnmatch(verb, '*' + key) and key != 'dar' and key != 'ir' and key != 'estar' and key != 'mandar' and key != 'ser' and key != 'ver':
                if key != verb:
                    return key
                else:
                    return ''
        return 'invalid'

    # Devuelve un diccionario con el formato estándar y las posiciones reservadas,
    # pero con cadenas vacias. Se utiliza para cuando table_view recibe un
    # verbo no válido.
    def empty_dict(self):
        return {'inf': [''],
                'ger' : [''],
                'part': ['','',''],
                'pres': ['','','','','',''],
                'pret_perf': ['','','','','',''],
                'pret_imperf': ['','','','','',''],
                'fut': ['','','','','',''],
                'impA': ['','','','','',''],
                'impB': ['','','','','',''],
                'impC': ['','','','','',''],
                'condA': ['','','','','',''],
                'condB': ['','','','','','']
        }

    # Recibe un verbo, lo conjuga y devuelve por consola una tabla con las
    # conjugaciones obtenidas. Utiliza la libreria 'terminaltables'.
    # <verb> : debe ser una cadena de caracteres finalizada en uno de {ar, er, ir,
    # ár, ér, ír}. De no ser así se devuelve una tabla vacía.
    def table_view(self, verb):
        conjugation = self.generar_diccionario_conjugacion(verb)
        if conjugation == {}:
            conjugation = self.empty_dict()
        table_data_1 = [
            ['', 'Presente', 'Preterito imperfecto', 'Preterito perfecto simple', 'Condicional'],
            ['yo', conjugation['pres'][0], conjugation['pret_imperf'][0], conjugation['pret_perf'][0], conjugation['condA'][0]],
            ['tu/vos', conjugation['pres'][1], conjugation['pret_imperf'][1], conjugation['pret_perf'][1], conjugation['condA'][1]],
            ['el', conjugation['pres'][2], conjugation['pret_imperf'][2], conjugation['pret_perf'][2], conjugation['condA'][2]],
            ['nos', conjugation['pres'][3], conjugation['pret_imperf'][3], conjugation['pret_perf'][3], conjugation['condA'][3]],
            ['vosotros', conjugation['pres'][4], conjugation['pret_imperf'][4], conjugation['pret_perf'][4], conjugation['condA'][4]],
            ['ellos', conjugation['pres'][5], conjugation['pret_imperf'][5], conjugation['pret_perf'][5], conjugation['condA'][5]]
        ]
        table_01 = AsciiTable(table_data_1)
        table_data_2 = [
            ['', 'Futuro', 'pret_imperf subjuntivo', 'Imperativo_A','Imperativo_B','Imperativo_C'],
            ['yo', conjugation['fut'][0], conjugation['condB'][0], conjugation['impA'][0], conjugation['impB'][0], conjugation['impC'][0]],
            ['tu/vos', conjugation['fut'][1], conjugation['condB'][1], conjugation['impA'][1], conjugation['impB'][1], conjugation['impC'][1]],
            ['el', conjugation['fut'][2], conjugation['condB'][2], conjugation['impA'][2], conjugation['impB'][2], conjugation['impC'][2]],
            ['nos', conjugation['fut'][3], conjugation['condB'][3], conjugation['impA'][3], conjugation['impB'][3], conjugation['impC'][3]],
            ['vosotros', conjugation['fut'][4], conjugation['condB'][4], conjugation['impA'][4], conjugation['impB'][4], conjugation['impC'][4]],
            ['ellos', conjugation['fut'][5], conjugation['condB'][5], conjugation['impA'][5], conjugation['impB'][5], conjugation['impC'][5]]
        ]
        table_02 = AsciiTable(table_data_2)
        table_data_3 = [
            ['', ''],
            ['Infinitivo', conjugation['inf'][0]],
            ['Gerundio', conjugation['ger'][0]],
            ['Participio 1', conjugation['part'][0]],
            ['Participio 2', conjugation['part'][1]],
            ['Participio 3', conjugation['part'][2]]
        ]
        table_03 = AsciiTable(table_data_3)
        print(table_03.table)
        print('')
        print(table_01.table)
        print('')
        print(table_02.table)


    # Recibe un verbo y devuelve su conjugación en presente indicativo.
    # <verb> verbo a conjugar debe ser una cadena de caracteres terminada en
    # uno de {ar, er, ir, ár, ér, ír}. De no ser asi devuelve un vector vacio.
    # <force_conj>: valor booleano. Si es verdadero fuerza a que el verbo
    # sea conjugado por la función sin recurrir al diccionario de irregulares
    # (aún si el mismo se encontrase allí)
    def presente_conj(self, verb, force_conj):
        if not any(fnmatch.fnmatch(verb, suffix) for suffix in ['*ar', '*er', '*ir', '*ár', '*ér', '*ír']):
            return ['','','','','','']
        verb_conj = []
        suffix_conj = []
        base_verb = verb[0:len(verb)-2]
        ncer_flag = False
        ger_gir_flag = False
        guir_flag = False
        if not verb in self.irregular_verbs.keys() or force_conj:
            if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
                if self.mode == 0:
                    suffix_conj = ['o', 'ás', 'a', 'amos', 'áis', 'an']
                else:
                    suffix_conj = ['o', 'as', 'a', 'amos', 'áis', 'an']
            if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
                if fnmatch.fnmatch(verb, '*ncer'):
                    ncer_flag = True
                if fnmatch.fnmatch(verb, '*ger'):
                    ger_gir_flag = True
                if self.mode == 0:
                    suffix_conj = ['o', 'és', 'e', 'emos', 'éis', 'en']
                else:
                    suffix_conj = ['o', 'es', 'e', 'emos', 'éis', 'en']
            if fnmatch.fnmatch(verb, '*ir') or fnmatch.fnmatch(verb, '*ír'):
                if fnmatch.fnmatch(verb, '*gir'):
                    ger_gir_flag = True
                if fnmatch.fnmatch(verb, '*guir'):
                    guir_flag = True
                if self.mode == 0:
                    suffix_conj = ['o', 'ís', 'e', 'imos', 'ís', 'en']
                else:
                    suffix_conj = ['o', 'es', 'e', 'imos', 'ís', 'en']
        else:
            return self.irregular_verbs[verb]['pres']
        for i in range(0, 6):
            base_form = base_verb

            # Conjugación sobre singular no modo argentino (vos en lugar de tú)
            # Conjugación sobre singular con modo argentino activado
            # Conjugación sobre plural de la tercera persona.
            if (i in self.singular and not self.mode == 0) or (self.mode == 0 and i in self.singular and not i in self.segunda_persona) or (i in self.plural and i in self.tercera_persona):

            # Cambio a la forma base según grupo 01 de los verbos irregulares.
            # e --> ie
                base_form = self.irregular_cast_group_01(verb, base_form)
            # Cambio a la forma base según grupo 02 de los verbos irregulares.
            # o --> ue
                base_form = self.irregular_cast_group_02(verb, base_form)
            # Cambio a la forma base según grupo 06 de los verbos irregulares.
            # e --> i
                base_form = self.irregular_cast_group_06(verb, base_form)
            # Cambio a la forma base según grupo 06 de los verbos irregulares.
            # e --> i
                base_form = self.irregular_cast_group_07(verb, base_form)

            # Cambio a la forma base según grupo 08 de los verbos irregulares.
            # e --> ie
                base_form = self.irregular_cast_group_08_a(verb, base_form)
            #    base_form = self.irregular_cast_group_08_b(verb, base_form)
            #    base_form = self.irregular_cast_group_09(verb, base_form)

            # Cambio a la forma base según grupo 09 de los verbos irregulares.
            # u --> ue
                base_form = self.irregular_cast_group_09(verb, base_form)

            # Cambio a la forma base según grupo 09 de los verbos irregulares.
            # i --> ie
                base_form = self.irregular_cast_group_10(verb, base_form)

            # Cambio a la forma base según grupo 09 de los verbos irregulares.
            # i --> y
                base_form = self.irregular_cast_group_11(verb, base_form)

            # Cambio a la forma base según grupo 09 de los verbos irregulares.
            # o --> ue
                base_form = self.irregular_cast_group_12_a(verb, base_form)

            # Cambia la forma base de los verbos terminados en 'decir'
            # 'dec' -> 'dic'
                if fnmatch.fnmatch(verb, '*decir') and not i in self.primera_persona:
                    base_form = base_form.replace("dec", "dic")

            # Conjugación sobre primera persona singular.
            if i in self.singular and i in self.primera_persona:
                # Si el verbo infinitivo termina en ncer se modifica el singular
                # de la primera persona:
                # c --> z
                if ncer_flag:
                    base_form = base_form[:len(base_form)-1] + 'z'

                # Si el verbo infinitivo termina en ger/gir se modifica el singular
                # de la primera persona:
                # g --> j
                if ger_gir_flag:
                    base_form = base_form[:len(base_form)-1] + 'j'

                # Si el verbo infinitivo termina en guir se modifica el singular
                # de la primera persona:
                # gu --> g
                if guir_flag:
                    base_form = base_form[:len(base_form)-2] + 'g'

                # Si el verbo infinitivo termina en 'decir' se modifica el singular
                # de la primera persona
                if fnmatch.fnmatch(verb, '*decir'):
                    base_form = base_form.replace('dec', 'dig')

                # Cambia la forma base para los verbos terminados en hacer.
                # c --> g
                if fnmatch.fnmatch(verb, '*hacer'):
                    base_form = base_form[:len(base_form)-1] + 'g'

            # Cambio a la forma base según grupo 03 de los verbos irregulares.
            # c --> zc
                base_form = self.irregular_cast_group_03(verb, base_form)
            # Cambio a la forma base según grupo 04 de los verbos irregulares.
            # c --> zc
                base_form = self.irregular_cast_group_04_b(verb, base_form)
            # Cambio a la forma base según grupo 13 de los verbos irregulares.
            # base_verb + g
                base_form = self.irregular_cast_group_13_a(verb, base_form)


            verb_conj.append(base_form + suffix_conj[i])

            # Salvedad para el caso puntual del verbo delinquir.
            if verb == 'delinquir' and i in self.primera_persona and i in self.singular:
                verb_conj[-1] = 'delinco'
        return verb_conj

    # Recibe un verbo y devuelve su conjugación en preterito perfecto simple indicativo.
    # <verb> verbo a conjugar debe ser una cadena de caracteres terminada en
    # uno de {ar, er, ir, ár, ér, ír}. De no ser asi devuelve un vector vacio.
    # <force_conj>: valor booleano. Si es verdadero fuerza a que el verbo
    # sea conjugado por la función sin recurrir al diccionario de irregulares
    # (aún si el mismo se encontrase allí)
    def preterito_perf_simple_conj(self, verb, force_conj):
        if not any(fnmatch.fnmatch(verb, suffix) for suffix in ['*ar', '*er', '*ir', '*ár', '*ér', '*ír']):
            return ['','','','','','']
        verb_conj = []
        suffix_conj = []
        base_verb = verb[0:len(verb)-2]
        car_flag = False
        zar_flag = False
        if not verb in self.irregular_verbs.keys() or force_conj:
            if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
                if fnmatch.fnmatch(verb, '*car'):
                    car_flag = True
                if fnmatch.fnmatch(verb, '*zar'):
                    zar_flag = True
                if fnmatch.fnmatch(verb, '*zar'):
                    zar_flag = True
                if fnmatch.fnmatch(verb, '*gar'):
                    suffix_conj = ['ué', 'aste', 'ó', 'amos', 'asteis', 'aron']
                elif fnmatch.fnmatch(verb, '*guar'):
                    suffix_conj = ['üé', 'aste', 'ó', 'amos', 'asteis', 'aron']
                else:
                    suffix_conj = ['é', 'aste', 'ó', 'amos', 'asteis', 'aron']
            if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
                suffix_conj = ['í', 'iste', 'ió', 'imos', 'isteis', 'ieron']
            if fnmatch.fnmatch(verb, '*ir') or fnmatch.fnmatch(verb, '*ír'):
                suffix_conj = ['í', 'iste', 'ió', 'imos', 'isteis', 'ieron']
        else:
            return self.irregular_verbs[verb]['pret_perf']
        for i in range(0, 6):
            if  fnmatch.fnmatch(verb, '*decir'):
                base_form = base_verb.replace('dec', 'dij')
            elif fnmatch.fnmatch(verb, '*hacer'):
                base_form = base_verb.replace('hac', 'hic')
            else:
                base_form = base_verb

            # Si el verbo infinitivo termina en ncer se modifica el singular
            # de la tercera persona:
            # c --> qu
            if car_flag and i in self.primera_persona and i in self.singular:
                base_form = base_form[:len(base_form)-1] + 'qu'

            # Si el verbo infinitivo termina en zar se modifica el singular
            # de la tercera persona:
            # z --> c
            if zar_flag and i in self.primera_persona and i in self.singular:
                base_form = base_form[:len(base_form)-1] + 'c'

            # Para los verbos contenidos en el grupo 04 se aplica el cambio de base
            # según lo definido para el preterito del grupo 04 de verbos irregulares.
            # c --> j
            base_form = self.irregular_cast_group_04_a(verb, base_form)

            # Conjugación sobre la tercera persona de los verbos en el grupo 05.
            if i in self.tercera_persona:

                if verb in self.irregular_verbs_grupo_05_er or verb in self.irregular_verbs_grupo_05_ñir or verb in self.irregular_verbs_grupo_05_ullir:
                # Elimina la i inicial al sufijo para la conjugación.
                    suffix_conj[i] = suffix_conj[i][1:]

                # Cambia la forma base del grupo segun lo dispueto para el grupo 06.
                # e --> i
                base_form = self.irregular_cast_group_06(verb, base_form)

                # Cambia la forma base del grupo segun lo dispueto para el grupo 07.
                # e --> i
                base_form = self.irregular_cast_group_07(verb, base_form)

                # Cambia la forma base del grupo segun lo dispueto para el grupo 08.
                # e --> i
                base_form = self.irregular_cast_group_08_b(verb, base_form)

                # Cambia la forma base del grupo segun lo dispueto para el grupo 11.
                # base_form + y
                base_form = self.irregular_cast_group_11(verb, base_form)

                # Cambia la forma base del grupo segun lo dispueto para el grupo 12.
                # o --> u
                base_form = self.irregular_cast_group_12_b(verb, base_form)

                # Cambia la forma base para los verbos terminados en hacer (singular).
                # c --> z
                if i in self.singular and fnmatch.fnmatch(verb, '*hacer'):
                    base_form = base_form[:len(base_form)-1] + 'z'


            # Elimina la i sobrante que queda al conjugar estos verbos.
            if i in self.tercera_persona and (verb in self.irregular_verbs_grupo_07_eir or verb in self.irregular_verbs_grupo_07_eñir or fnmatch.fnmatch(verb, '*uir')):
                suffix_conj[i] = suffix_conj[i][1:]

            # Elimina la i sobrante que queda al conjugar los verbos del grupo 04
            # en el plural de la tercera persona
            if i in self.tercera_persona and i in self.plural and (verb in self.irregular_verbs_grupo_04_ducir or fnmatch.fnmatch(verb, '*decir')):
                suffix_conj[i] = suffix_conj[i][1:]

            # Modifica el sufijo para los verbos del grupo 04 en primera y tercera
            # persona.
            # Primera persona: é por e
            # Tercera persona: ó por o
            if i in self.primera_persona and i in self.singular and (verb in self.irregular_verbs_grupo_04_ducir  or fnmatch.fnmatch(verb, '*decir') or fnmatch.fnmatch(verb, '*hacer')):
                verb_conj.append(base_form + 'e')
            elif i in self.tercera_persona and i in self.singular and (verb in self.irregular_verbs_grupo_04_ducir  or fnmatch.fnmatch(verb, '*decir') or fnmatch.fnmatch(verb, '*hacer')):
                verb_conj.append(base_form + 'o')
            else:
                verb_conj.append(base_form + suffix_conj[i])

        return verb_conj

    # Recibe un verbo y devuelve su conjugación en preterito imperfecto indicativo.
    # <verb> verbo a conjugar debe ser una cadena de caracteres terminada en
    # uno de {ar, er, ir, ár, ér, ír}. De no ser asi devuelve un vector vacio.
    # <force_conj>: valor booleano. Si es verdadero fuerza a que el verbo
    # sea conjugado por la función sin recurrir al diccionario de irregulares
    # (aún si el mismo se encontrase allí)
    def preterito_imperf_conj(self, verb, force_conj):
        if not any(fnmatch.fnmatch(verb, suffix) for suffix in ['*ar', '*er', '*ir', '*ár', '*ér', '*ír']):
            return ['','','','','','']
        verb_conj = []
        suffix_conj = []
        base_verb = verb[0:len(verb)-2]
        if not verb in self.irregular_verbs.keys() or force_conj:
            if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
                suffix_conj = ['aba', 'abas', 'aba', 'ábamos', 'abais', 'aban']
            if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
                suffix_conj = ['ía', 'ías', 'ía', 'íamos', 'íais', 'ían']
            if fnmatch.fnmatch(verb, '*ir') or fnmatch.fnmatch(verb, '*ír'):
                suffix_conj = ['ía', 'ías', 'ía', 'íamos', 'íais', 'ían']
        else:
            return self.irregular_verbs[verb]['pret_imperf']
        for suffix in suffix_conj:
            verb_conj.append(base_verb + suffix)
        return verb_conj

    # Recibe un verbo y devuelve su conjugación en futuro indicativo.
    # <verb> verbo a conjugar debe ser una cadena de caracteres terminada en
    # uno de {ar, er, ir, ár, ér, ír}. De no ser asi devuelve un vector vacio.
    # <force_conj>: valor booleano. Si es verdadero fuerza a que el verbo
    # sea conjugado por la función sin recurrir al diccionario de irregulares
    # (aún si el mismo se encontrase allí)
    def futuro_simple_conj(self, verb, force_conj):
        if not any(fnmatch.fnmatch(verb, suffix) for suffix in ['*ar', '*er', '*ir', '*ár', '*ér', '*ír']):
            return ['','','','','','']
        verb_conj = []
        suffix_conj = []
        if fnmatch.fnmatch(verb, '*hacer'):
            verb = verb.replace('hacer', 'hacar')
        base_verb = verb[0:len(verb)-2]
        if not verb in self.irregular_verbs.keys() or force_conj:
            if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
                suffix_conj = ['aré', 'arás', 'ará', 'aremos', 'aréis', 'arán']
            if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
                suffix_conj = ['eré', 'erás', 'erá', 'eremos', 'eréis', 'erán']
            if fnmatch.fnmatch(verb, '*ir') or fnmatch.fnmatch(verb, '*ír'):
                suffix_conj = ['iré', 'irás', 'irá', 'iremos', 'iréis', 'irán']
        else:
            return self.irregular_verbs[verb]['fut']
        for suffix in suffix_conj:
            if  fnmatch.fnmatch(verb, '*decir'):
                base_form = base_verb.replace('dec', 'd')
            elif fnmatch.fnmatch(verb, '*hacar'):
                base_form = base_verb.replace('hac', 'h')
            else:
                base_form = base_verb

            # Mofifica el verbo base para los verbos en el grupo 13
            # base_verb + d
            base_form = self.irregular_cast_group_13_b(verb, base_form)

            # Elimina la i que resulta en un sobrante para los verbos del
            # grupo 13
            if verb in self.irregular_verbs_grupo_13_alir or verb in self.irregular_verbs_grupo_13_aler:
                suffix = suffix[1:]

            verb_conj.append(base_form + suffix)
        return verb_conj

    # Recibe un verbo y devuelve su conjugación en condicional indicativo.
    # <verb> verbo a conjugar debe ser una cadena de caracteres terminada en
    # uno de {ar, er, ir, ár, ér, ír}. De no ser asi devuelve un vector vacio.
    # <force_conj>: valor booleano. Si es verdadero fuerza a que el verbo
    # sea conjugado por la función sin recurrir al diccionario de irregulares
    # (aún si el mismo se encontrase allí)
    def condicional_simple_A_conj(self, verb, force_conj):
        if not any(fnmatch.fnmatch(verb, suffix) for suffix in ['*ar', '*er', '*ir', '*ár', '*ér', '*ír']):
            return ['','','','','','']
        verb_conj = []
        suffix_conj = []
        if fnmatch.fnmatch(verb, '*hacer'):
            verb = verb.replace('hacer', 'hacar')
        base_verb = verb[0:len(verb)-2]
        if not verb in self.irregular_verbs.keys() or force_conj:
            if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
                suffix_conj = ['aría', 'arías', 'aría', 'aríamos', 'aríais', 'arían']
            if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
                suffix_conj = ['ería', 'erías', 'ería', 'eríamos', 'eríais', 'erían']
            if fnmatch.fnmatch(verb, '*ir') or fnmatch.fnmatch(verb, '*ír'):
                suffix_conj = ['iría', 'irías', 'iría', 'iríamos', 'iríais', 'irían']
        else:
            return self.irregular_verbs[verb]['condA']
        for suffix in suffix_conj:
            if  fnmatch.fnmatch(verb, '*decir'):
                base_form = base_verb.replace('dec', 'd')
            elif fnmatch.fnmatch(verb, '*hacar'):
                base_form = base_verb.replace('hac', 'h')
            else:
                base_form = base_verb

            # Mofifica el verbo base para los verbos en el grupo 13
            # base_verb + d
            base_form = self.irregular_cast_group_13_b(verb, base_form)

            # Elimina la i que resulta en un sobrante para los verbos del
            # grupo 13
            if verb in self.irregular_verbs_grupo_13_alir or verb in self.irregular_verbs_grupo_13_aler:
                suffix = suffix[1:]

            verb_conj.append(base_form + suffix)
        return verb_conj

    # Recibe un verbo y devuelve su conjugación en preterito imperfecto subjuntivo.
    # <verb> verbo a conjugar debe ser una cadena de caracteres terminada en
    # uno de {ar, er, ir, ár, ér, ír}. De no ser asi devuelve un vector vacio.
    # <force_conj>: valor booleano. Si es verdadero fuerza a que el verbo
    # sea conjugado por la función sin recurrir al diccionario de irregulares
    # (aún si el mismo se encontrase allí)
    def condicional_simple_B_conj(self, verb, force_conj):
        if not any(fnmatch.fnmatch(verb, suffix) for suffix in ['*ar', '*er', '*ir', '*ár', '*ér', '*ír']):
            return ['','','','','','']
        verb_conj = []
        suffix_conj = []
        base_verb = verb[0:len(verb)-2]
        if not verb in self.irregular_verbs.keys() or force_conj:
            if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
                suffix_conj = ['ase', 'ases', 'ase', 'ásemos', 'aseis', 'asen']
            if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
                suffix_conj = ['iese', 'ieses', 'iese', 'iésemos', 'ieseis', 'iesen']
            if fnmatch.fnmatch(verb, '*ir') or fnmatch.fnmatch(verb, '*ír'):
                suffix_conj = ['iese', 'ieses', 'iese', 'iésemos', 'ieseis', 'iesen']
        else:
            return self.irregular_verbs[verb]['condB']
        for i in range(0, 6):
            if  fnmatch.fnmatch(verb, '*decir'):
                base_form = base_verb.replace('dec', 'dij')
            elif  fnmatch.fnmatch(verb, '*hacer'):
                base_form = base_verb.replace('hac', 'hic')
            else:
                base_form = base_verb

            # Para los verbos en el grupo 04 se aplica el cambio de base
            # definido para el pret imperfecto subjuntivo.
            # c --> j
            base_form = self.irregular_cast_group_04_a(verb, base_form)

            # Para los verbos en el grupo 06 se aplica el cambio de base
            # definido para el pret imperfecto subjuntivo.
            # e --> i
            base_form = self.irregular_cast_group_06(verb, base_form)

            # Para los verbos en el grupo 07 se aplica el cambio de base
            # definido para el pret imperfecto subjuntivo.
            # e --> i
            base_form = self.irregular_cast_group_07(verb, base_form)

            # Para los verbos en el grupo 08 se aplica el cambio de base
            # definido para el pret imperfecto subjuntivo.
            # e --> i
            base_form = self.irregular_cast_group_08_b(verb, base_form)

            # Para los verbos en el grupo 12 se aplica el cambio de base
            # definido para el pret imperfecto subjuntivo.
            # o --> u
            base_form = self.irregular_cast_group_12_b(verb, base_form)

            # Para los verbos terminados en 'uir' agrega una 'y' a la forma
            # base.
            if fnmatch.fnmatch(verb, '*uir'):
                base_form += 'y'


            # Elimina la i del sufijo para los verbos del grupo 04, 05 y los
            # terminados en 'uir'.
            if verb in self.irregular_verbs_grupo_04_ducir or verb in self.irregular_verbs_grupo_05_er or verb in self.irregular_verbs_grupo_05_ñir or verb in self.irregular_verbs_grupo_05_ullir or verb in self.irregular_verbs_grupo_07_eir or verb in self.irregular_verbs_grupo_07_eñir or fnmatch.fnmatch(verb, '*uir') or fnmatch.fnmatch(verb, '*decir'):
                if fnmatch.fnmatch(suffix_conj[i], 'i*'):
                    suffix_conj[i] = suffix_conj[i][1:]

            verb_conj.append(base_form + suffix_conj[i])

        return verb_conj

    # Recibe un verbo y devuelve su conjugación en imperativo.
    # <verb> verbo a conjugar debe ser una cadena de caracteres terminada en
    # uno de {ar, er, ir, ár, ér, ír}. De no ser asi devuelve un vector vacio.
    # <force_conj>: valor booleano. Si es verdadero fuerza a que el verbo
    # sea conjugado por la función sin recurrir al diccionario de irregulares
    # (aún si el mismo se encontrase allí)
    def imperativo_A_conj(self, verb, force_conj):
        if not any(fnmatch.fnmatch(verb, suffix) for suffix in ['*ar', '*er', '*ir', '*ár', '*ér', '*ír']):
            return ['','','','','','']
        verb_conj = []
        suffix_conj = []
        base_verb = verb[0:len(verb)-2]
        ncer_flag = False
        ger_gir_flag = False
        car_flag = False
        zar_flag = False
        guir_flag = False
        guar_flag = False
        if not verb in self.irregular_verbs.keys() or force_conj:
            if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
                if fnmatch.fnmatch(verb, '*car'):
                    car_flag = True
                if fnmatch.fnmatch(verb, '*zar'):
                    zar_flag = True
                if fnmatch.fnmatch(verb, '*guar'):
                    guar_flag = True
                if fnmatch.fnmatch(verb, '*gar'):
                    suffix_conj = ['', 'á', 'ue', 'uemos', 'ad', 'uen']
                else:
                    suffix_conj = ['', 'á', 'e', 'emos', 'ad', 'en']
                if self.mode != 0:
                    suffix_conj[1] = 'a'
            if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
                if fnmatch.fnmatch(verb, '*ncer'):
                    ncer_flag = True
                if fnmatch.fnmatch(verb, '*ger'):
                    ger_gir_flag = True
                suffix_conj = ['', 'é', 'a', 'amos', 'ed', 'an']
            if fnmatch.fnmatch(verb, '*ir'):
                if fnmatch.fnmatch(verb, '*gir'):
                    ger_gir_flag = True
                if fnmatch.fnmatch(verb, '*guír'):
                    guir_flag = True
                if self.mode == 0:
                    suffix_conj = ['', 'í', 'a', 'amos', 'id', 'an']
                else:
                    suffix_conj = ['', 'e', 'a', 'amos', 'id', 'an']
            if fnmatch.fnmatch(verb, '*ír'):
                if fnmatch.fnmatch(verb, '*gír'):
                    ger_gir_flag = True
                if fnmatch.fnmatch(verb, '*guír'):
                    guir_flag = True
                if self.mode == 0:
                    suffix_conj = ['', 'eí', 'ía', 'iamos', 'eíd', 'ían']
                else:
                    suffix_conj = ['', 'íe', 'ía', 'iamos', 'eíd', 'ían']
        else:
            return self.irregular_verbs[verb]['impA']
        verb_conj.append('')
        for i in range(1, 6):
            base_form = base_verb

            # Conjugación sobre singular no modo argentino (vos en lugar de tú)
            # Conjugación sobre singular con modo argentino activado
            # Conjugación sobre plural de la tercera persona.
            if (i in self.singular and not self.mode == 0) or (self.mode == 0 and i in self.singular and not i in self.segunda_persona) or (i in self.plural and i in self.tercera_persona):

                # Cambio a la forma definida para el grupo de irregulares 01
                # e --> ie
                base_form = self.irregular_cast_group_01(verb, base_form)
                # Cambio a la forma definida para el grupo de irregulares 02
                # o --> ue
                base_form = self.irregular_cast_group_02(verb, base_form)


            # Conjugación para todas las formas con excepción del singular de
            # la segunda persona.
            if not (i in self.segunda_persona):

                # Cambio a la forma definida pra el grupo de irregulares 03
                # c --> zc
                base_form = self.irregular_cast_group_03(verb, base_form)

                # Cambio a la forma definida para el grupo de irregulares 04,
                # c --> zc
                base_form = self.irregular_cast_group_04_b(verb, base_form)

            # Conjugación para todas las formas con excepción del plural de la
            # segunda persona (en modo "vos" se omite también la segunda).
            if self.mode != 0 and not (i in self.segunda_persona and i in self.plural) or not i in self.segunda_persona:
                # Cambio según los dispuesto para los verbos del grupo 06.
                # e --> i
                base_form = self.irregular_cast_group_06(verb, base_form)

                # Cambio según los dispuesto para los verbos del grupo 07.
                # e --> i
                base_form = self.irregular_cast_group_07(verb, base_form)

                # Cambio según los dispuesto para los verbos del grupo 10.
                # e --> ie
                base_form = self.irregular_cast_group_10(verb, base_form)

                # Cambio a la forma base según grupo 09 de los verbos irregulares.
                # i --> y
                base_form = self.irregular_cast_group_11(verb, base_form)

            # Conjugación para todas las formas con excepción del plural de la
            # segunda y primea persona (en modo "vos" se omite también la segunda singular).
            if (not self.mode == 0 and (i in self.singular or i in self.tercera_persona)) or (self.mode == 0 and ((i in self.singular and not i in self.segunda_persona) or i in self.tercera_persona)):

                # Cambio según los dispuesto para los verbos del grupo 08.
                # e --> ie
                base_form = self.irregular_cast_group_08_a(verb, base_form)

                # Cambio según los dispuesto para los verbos del grupo 12.
                # o --> u
                base_form = self.irregular_cast_group_12_a(verb, base_form)

            # Conjugación para tercera persona plural.
            if i in self.primera_persona and i in self.plural:

                # Cambio según los dispuesto para los verbos del grupo 08.
                # e --> i
                base_form = self.irregular_cast_group_08_b(verb, base_form)

                # Cambio según los dispuesto para los verbos del grupo 12.
                # o --> u
                base_form = self.irregular_cast_group_12_b(verb, base_form)


            if i in self.tercera_persona:

                # Cambio según los dispuesto para los verbos del grupo 09.
                # u --> ue
                base_form = self.irregular_cast_group_09(verb, base_form)

            # Conjugación para tercera persona y primera persona
            if i in self.primera_persona or i in self.tercera_persona:

                # Cambio exclusivo para el verbo delinquir.
                # qu --> c
                if verb == 'delinquir':
                    base_form.replace('qu', 'c')

                # Si el verbo infinitivo termina en ncer:
                # c --> z
                if ncer_flag:
                    base_form = base_form[:len(base_form)-1] + 'z'

                # Si el verbo infinitivo termina en ger/gir:
                # g --> j
                if ger_gir_flag:
                    base_form = base_form[:len(base_form)-1] + 'j'

                # Si el verbo infinitivo termina en car:
                # c --> qu
                if car_flag:
                    base_form = base_form[:len(base_form)-1] + 'qu'

                # Si el verbo infinitivo termina en zar:
                # z --> c
                if zar_flag:
                    base_form = base_form[:len(base_form)-1] + 'c'

                # Si el verbo infinitivo termina en guir:
                # gu --> g
                if guir_flag:
                    base_form = base_form[:len(base_form)-2] + 'g'

                # Si el verbo infinitivo termina en guir:
                # u --> ü
                if guir_flag:
                    base_form = base_form[:len(base_form)-1] + 'ü'

            # Conjugacion para primera persona y tercera persona
            if i in self.tercera_persona or i in self.primera_persona:

                # Cambio según los dispuesto para los verbos del grupo 13.
                # base_form + g
                base_form = self.irregular_cast_group_13_a(verb, base_form)

                # Cambio para los verbos terminados en 'decir'
                # dec --> dig
                if fnmatch.fnmatch(verb, '*decir'):
                    base_form = base_form.replace('dec', 'dig')

                # Cambio para los verbos terminados en 'hacer'
                # hac --> hag
                if fnmatch.fnmatch(verb, '*hacer'):
                    base_form = base_form.replace('hac', 'hag')

            if i in self.segunda_persona and i in self.singular:

                # Cambio para los verbos terminados en 'decir'
                # dec --> d
                if fnmatch.fnmatch(verb, '*decir'):
                    if self.mode != 0:
                        base_form = base_form.replace('dec', 'd')
                    suffix_conj[i] = 'í'

                # Cambio para los verbos terminados en 'hacer'
                if fnmatch.fnmatch(verb, '*hacer'):
                    if self.mode != 0:
                        base_form = base_form.replace('hac', 'ha')
                        suffix_conj[i] = 'z'


                # Cambio para los verbos en el grupo 09 (modo vos desactivado).
                # u --> ue
                if self.mode != 0:
                    base_form = self.irregular_cast_group_09(verb, base_form)


            # Elimina el último caracter a los verbos del grupo 07, de modo
            # de aprovechar el sufijo especifico para los verbor terminado en
            # ír.
            if verb in self.irregular_verbs_grupo_07_eir:
                base_form = base_form[:len(base_form)-1]

            verb_conj.append(base_form + suffix_conj[i])
        return verb_conj

    # Recibe un verbo y devuelve su conjugación en imperativo (variante argentina I).
    # <verb> verbo a conjugar debe ser una cadena de caracteres terminada en
    # uno de {ar, er, ir, ár, ér, ír}. De no ser asi devuelve un vector vacio.
    # <force_conj>: valor booleano. Si es verdadero fuerza a que el verbo
    # sea conjugado por la función sin recurrir al diccionario de irregulares
    # (aún si el mismo se encontrase allí)
    def imperativo_B_conj(self, verb, force_conj):
        if not any(fnmatch.fnmatch(verb, suffix) for suffix in ['*ar', '*er', '*ir', '*ár', '*ér', '*ír']):
            return ['','','','','','']
        verb_conj = []
        suffix_conj = []
        base_verb = verb[0:len(verb)-2]
        if not verb in self.irregular_verbs.keys() or force_conj:
            if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
                suffix_conj = ['ame', 'ate', 'ale', 'anos', 'aleis', 'ales']
            if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
                suffix_conj = ['eme', 'ete', 'ele', 'enos', 'eleis', 'eles']
            if fnmatch.fnmatch(verb, '*ir') or fnmatch.fnmatch(verb, '*ír'):
                suffix_conj = ['ime', 'ite', 'ile', 'inos', 'ileis', 'iles']
        else:
            return self.irregular_verbs[verb]['impB']
        for suffix in suffix_conj:
            verb_conj.append(base_verb + suffix)
        return verb_conj

    # Recibe un verbo y devuelve su conjugación en imperativo (variante argentina II).
    # <verb> verbo a conjugar debe ser una cadena de caracteres terminada en
    # uno de {ar, er, ir, ár, ér, ír}. De no ser asi devuelve un vector vacio.
    # <force_conj>: valor booleano. Si es verdadero fuerza a que el verbo
    # sea conjugado por la función sin recurrir al diccionario de irregulares
    # (aún si el mismo se encontrase allí)
    def imperativo_C_conj(self, verb, force_conj):
        if not any(fnmatch.fnmatch(verb, suffix) for suffix in ['*ar', '*er', '*ir', '*ár', '*ér', '*ír']):
            return ['','','','','','']
        verb_conj = []
        suffix_conj = []
        base_verb = verb[0:len(verb)-2]
        if not verb in self.irregular_verbs.keys() or force_conj:
            if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
                suffix_conj = ['arme', 'arte', 'arle', 'arnos', 'arleis', 'arles']
            if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
                suffix_conj = ['erme', 'erte', 'erle', 'ernos', 'erleis', 'erles']
            if fnmatch.fnmatch(verb, '*ir') or fnmatch.fnmatch(verb, '*ír'):
                suffix_conj = ['irme', 'irte', 'irle', 'irnos', 'irleis', 'irles']
        else:
            return self.irregular_verbs[verb]['impC']
        for suffix in suffix_conj:
            verb_conj.append(base_verb + suffix)
        return verb_conj

    # Recibe un verbo y devuelve su participio (se agrega participio en femenino
    # y una variante más).
    # <verb> verbo a conjugar debe ser una cadena de caracteres terminada en
    # uno de {ar, er, ir, ár, ér, ír}. De no ser asi devuelve un vector vacio.
    # <force_conj>: valor booleano. Si es verdadero fuerza a que el verbo
    # sea conjugado por la función sin recurrir al diccionario de irregulares
    # (aún si el mismo se encontrase allí)
    def participio(self, verb, force_conj):
        if not any(fnmatch.fnmatch(verb, suffix) for suffix in ['*ar', '*er', '*ir', '*ár', '*ér', '*ír']):
            return ['','','']
        verb_conj = []
        suffix_conj = []
        base_verb = verb[0:len(verb)-2]
        if not verb in self.irregular_verbs.keys() or force_conj:
            if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
                suffix_conj = ['ado', 'ada', 'arse']
            if fnmatch.fnmatch(verb, '*er',) or fnmatch.fnmatch(verb, '*ér'):
                suffix_conj = ['ido', 'ida', 'erse']
            if fnmatch.fnmatch(verb, '*ir') or fnmatch.fnmatch(verb, '*ír'):
                suffix_conj = ['ido', 'ida', 'irse']
        else:
            return self.irregular_verbs[verb]['part']
        for suffix in suffix_conj:
            verb_conj.append(base_verb + suffix)

        #Verfica que el verbo no se encuentre en las excepciones del participio.
        #Verbos terminados con "olver", tienen su participio terminado con "uelto"
        if fnmatch.fnmatch(verb, '*olver'):
            verb_conj[0] = verb[0:len(verb)-5] + "uelto"
            verb_conj[1] = verb[0:len(verb)-5] + "uelta"

        # Cambio para los verbos terminados en 'decir'
        # iendo --> icho
        if fnmatch.fnmatch(verb, '*decir'):
            verb_conj[0] = verb[0:len(verb)-4] + "icho"
            verb_conj[1] = verb[0:len(verb)-4] + "icha"

        # Cambio para los verbos terminados en 'hacer'
        # iendo --> echo
        if fnmatch.fnmatch(verb, '*hacer'):
            verb_conj[0] = verb[0:len(verb)-4] + "echo"
            verb_conj[1] = verb[0:len(verb)-4] + "echa"

        # Cambio para 'pudir'
        # pudrido --> podrido
        if fnmatch.fnmatch(verb, '*pudrir'):
            verb_conj[0] = verb_conj[0].replace('u', 'o', 1)
            verb_conj[1] = verb_conj[1].replace('u', 'o', 1)

        return verb_conj

    # Recibe un verbo y devuelve su gerundio.
    # <verb> verbo a conjugar debe ser una cadena de caracteres terminada en
    # uno de {ar, er, ir, ár, ér, ír}. De no ser asi devuelve un vector vacio.
    # <force_conj>: valor booleano. Si es verdadero fuerza a que el verbo
    # sea conjugado por la función sin recurrir al diccionario de irregulares
    # (aún si el mismo se encontrase allí)
    def gerundio(self, verb, force_conj):
        if not any(fnmatch.fnmatch(verb, suffix) for suffix in ['*ar', '*er', '*ir', '*ár', '*ér', '*ír']):
            return ['']
        verb_conj = []
        suffix_conj = []
        base_verb = verb[0:len(verb)-2]
        if not verb in self.irregular_verbs.keys() or force_conj:
            if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
                suffix_conj = ['ando']
            if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
                suffix_conj = ['iendo']
            if fnmatch.fnmatch(verb, '*ir') or fnmatch.fnmatch(verb, '*ír'):
                suffix_conj = ['iendo']
        else:
            return self.irregular_verbs[verb]['ger']
        for suffix in suffix_conj:
            base_form = base_verb

            # Cambia la forma base del verbo según los dispuesto para el grupo 06.
            # e --> i
            base_form = self.irregular_cast_group_06(verb, base_form)

            # Cambia la forma base del verbo según los dispuesto para el grupo 06.
            # e --> i
            base_form = self.irregular_cast_group_07(verb, base_form)


            # Cambia la forma base del grupo segun lo dispueto para el grupo 11.
            # base_form + y
            base_form = self.irregular_cast_group_11(verb, base_form)

            # Cambia la forma base del grupo segun lo dispueto para el grupo 12.
            # o --> u
            base_form = self.irregular_cast_group_12_b(verb, base_form)

            #Para los verbos en el grupo 11 se elimina la i de 'iendo'
            if verb in self.irregular_verbs_grupo_11_uir or verb in self.irregular_verbs_grupo_07_eir or verb in self.irregular_verbs_grupo_07_eñir or verb in self.irregular_verbs_grupo_05_er or verb in self.irregular_verbs_grupo_05_ñir or verb in self.irregular_verbs_grupo_05_ullir :
                suffix = suffix[1:]

            verb_conj.append(base_form + suffix)

        return verb_conj


    # Las funciones/métodos implementados a continuación definen los cambios
    # a realizar para cada grupo particular de verbos irregulares.
    # Esto no incluye a los verbos incluidos en el diccionario de verbos
    # irregulares, sino que atañe a los verbos en los 
    def irregular_cast_group_01(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_01_ar or verb in self.irregular_verbs_grupo_01_er or verb in self.irregular_verbs_grupo_01_ir:
            return replace_right(base_verb, 'e', 'ie', 1)
        else:
            return base_verb

    def irregular_cast_group_02(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_02_ar or verb in self.irregular_verbs_grupo_02_er:
            # Verifica la existencia del diptongo "ue" que pasa a "hue"
            if verb in self.h_exceptions:
                return replace_right(base_verb, 'o', 'hue', 1)
            else:
                return replace_right(base_verb, 'o', 'ue', 1)
        else:
            return base_verb

    def irregular_cast_group_03(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_03_acer or verb in self.irregular_verbs_grupo_03_ecer or verb in self.irregular_verbs_grupo_03_ocer or verb in self.irregular_verbs_grupo_03_ucer:
            return replace_right(base_verb, 'c', 'zc', 1)
        else:
            return base_verb

    def irregular_cast_group_04_a(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_04_ducir:
            return replace_right(base_verb, 'c', 'j', 1)
        else:
            return base_verb

    def irregular_cast_group_04_b(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_04_ducir:
            return replace_right(base_verb, 'c', 'zc', 1)
        else:
            return base_verb

    def irregular_cast_group_05(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_05_er or verb in self.irregular_verbs_grupo_05_ñir or verb in self.irregular_verbs_grupo_05_ullir:
            return replace_right(base_verb, 'i', '', 1)
        else:
            return base_verb

    def irregular_cast_group_05_a(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_05_er or verb in self.irregular_verbs_grupo_05_ñir or verb in self.irregular_verbs_grupo_05_ullir:
            modified_verb = replace_right(base_verb, 'i', '$', 1)
            modified_verb = replace_right(modified_verb, 'i', '', 1)
            return replace_right(modified_verb, '$', 'i', 1)
        else:
            return base_verb

    def irregular_cast_group_06(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_06_ir:
            return replace_right(base_verb, 'e', 'i', 1)
        else:
            return base_verb

    def irregular_cast_group_07(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_07_eir or verb in self.irregular_verbs_grupo_07_eñir:
            return replace_right(base_verb, 'e', 'i', 1)
        else:
            return base_verb

    def irregular_cast_group_07_a(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_07_eir or verb in self.irregular_verbs_grupo_07_eñir:
            return replace_right(base_verb, 'i', '', 1)
        else:
            return base_verb

    def irregular_cast_group_07_b(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_07_eir or verb in self.irregular_verbs_grupo_07_eñir:
            modified_verb = replace_right(base_verb, 'i', '$', 1)
            modified_verb = replace_right(modified_verb, 'i', '', 1)
            return replace_right(modified_verb, '$', 'i', 1)
        else:
            return base_verb

    def irregular_cast_group_08_a(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_08_ir:
            return replace_right(base_verb, 'e', 'ie', 1)
        else:
            return base_verb

    def irregular_cast_group_08_b(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_08_ir:
            return replace_right(base_verb, 'e', 'i', 1)
        else:
            return base_verb

    def irregular_cast_group_09(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_09_u:
            return replace_right(base_verb, 'u', 'ue', 1)
        else:
            return base_verb

    def irregular_cast_group_10(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_10_irir:
            return replace_right(base_verb, 'i', 'ie', 1)
        else:
            return base_verb

    def irregular_cast_group_11(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_11_uir:
            return base_verb + 'y'
        else:
            return base_verb

    def irregular_cast_group_12_a(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_12_o:
            return replace_right(base_verb, 'o', 'ue', 1)
        else:
            return base_verb

    def irregular_cast_group_12_b(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_12_o:
            return replace_right(base_verb, 'o', 'u', 1)
        else:
            return base_verb

    def irregular_cast_group_13_a(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_13_aler or verb in self.irregular_verbs_grupo_13_alir:
            return base_verb + 'g'
        else:
            return base_verb

    def irregular_cast_group_13_b(self, verb, base_verb):
        if verb in self.irregular_verbs_grupo_13_aler or verb in self.irregular_verbs_grupo_13_alir:
            return base_verb + 'd'
        else:
            return base_verb
