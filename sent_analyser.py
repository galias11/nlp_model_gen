import spacy
from spacy.tokens import Doc, Span, Token
from os import scandir, getcwd
from os.path import abspath
from termcolor import colored, cprint
import enchant
import glob
import ast


def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1,lenstr1+1):
        d[(i,-1)] = i+1
    for j in range(-1,lenstr2+1):
        d[(-1,j)] = j+1

    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i,j)] = min(
                           d[(i-1,j)] + 1, # deletion
                           d[(i,j-1)] + 1, # insertion
                           d[(i-1,j-1)] + cost, # substitution
                          )
            if i and j and s1[i]==s2[j-1] and s1[i-1] == s2[j]:
                d[(i,j)] = min (d[(i,j)], d[i-2,j-2] + cost) # transposition

    return d[lenstr1-1,lenstr2-1]

#Sentence by sentence analysis of each token.
def sent_analyse(sent):
    sent_analysis = []
    for token in sent:
        text = token.text
        lemma = token.lemma_
        pos = token.pos_
        tag = token.tag_
        dep = token.dep_
        shape = token.shape_
        is_alpha = token.is_alpha
        is_stop = token.is_stop
        sent_analysis.append(
        {'token':text, 'lemma':lemma, 'pos':pos, 'tag' : tag, 'dep' : dep,
        'shape':shape, 'is_alpha':is_alpha, 'is_stop':is_stop})
    return sent_analysis

#Prints a table with token analisys for each token in sentence.
def print_token_table(sent):
    sent_analysis = sent_analyse(sent)
    print("TOKEN\tLEMMA\tPOS\tTAG\tDEP\tSHAPE\tALPHA?\tCOMMON")
    for token in sent_analysis:
        print(token['token'][:6] + "\t"
        + token['lemma'][:6] + '\t'
        + token['pos'] + '\t'
        + token['tag'][:6] + '\t'
        + token['dep'] + '\t'
        + token['shape'] + '\t'
        + str(token['is_alpha']) + '\t'
        + str(token['is_stop']))

def msg_analysis(msg_file):
    for line in msg_file.realines():
        doc = nlp(line)
        for sent in doc.sents:
            flag = False
            for token in sent:
                if not flag and token.lemma_ in target:
                    flag = True
                    for token in sent:
                        print((colored(token, 'red') if token.lemma_ in target else colored(token, 'green')) + ' ', end = '')
                    print('\n')


def nlp_load(model):
    nlp = spacy.load(model)
    print('Model loaded...')
    nlp_load_drug_token_detection()
    print('Token detection module loaded...')
    return nlp

#path_default:"Training/Models/Diccionarios/dic_drogas.dic"
def nlp_load_drug_token_detection():
    target_comercio_acto = ['cobrar', 'comercializar', 'comerciar', 'comprar', 'negociar', 'pagar', 'vender']
    target_comercio_dinero_sing = ast.literal_eval(open("Training/Models/Diccionarios/v2/Changed_words/len_1/Compra_venta/Nouns/Dinero/Diccionario/dict_dinero_sing.dic", "r").read())
    target_comercio_dinero_plur = ast.literal_eval(open("Training/Models/Diccionarios/v2/Changed_words/len_1/Compra_venta/Nouns/Dinero/Diccionario/dict_dinero_plur.dic", "r").read())
    target_comercio_vendor_sing = ast.literal_eval(open("/home/infolab/Documentos/SAVE/Training/Models/Diccionarios/v2/Changed_words/len_1/Compra_venta/Nouns/Vendedores/Diccionario/dict_vendors_sing.dic", "r").read())
    target_comercio_vendor_plur = ast.literal_eval(open("/home/infolab/Documentos/SAVE/Training/Models/Diccionarios/v2/Changed_words/len_1/Compra_venta/Nouns/Vendedores/Diccionario/dict_vendors_plur.dic", "r").read())

    target_droga_consumo = ['aspirar', 'consumir', 'fumanchar', 'fumar', 'inyectar', 'jalar', 'tomar']
    target_droga_droga = ast.literal_eval(open("Training/Models/Diccionarios/v2/Changed_words/len_1/Consumo/Nouns/Drogas/Dicccionario/diccionario_drogas.dic", "r").read())

    is_comercio_acto_getter = lambda token: token.lemma_ in target_comercio_acto
    Token.set_extension('is_comercio_acto', getter=is_comercio_acto_getter)
    has_comercio_acto_getter = lambda obj: any([t._.is_comercio_acto for t in obj])
    Doc.set_extension('has_comercio_acto', getter=has_comercio_acto_getter)
    Span.set_extension('has_comercio_acto', getter=has_comercio_acto_getter)

    is_comercio_dinero_getter = lambda token: token.text in target_comercio_dinero_sing or token.text in target_comercio_dinero_plur
    Token.set_extension('is_comercio_dinero', getter=is_comercio_dinero_getter)
    has_comercio_dinero_getter = lambda obj: any([t._.is_comercio_dinero for t in obj])
    Doc.set_extension('has_comercio_dinero', getter=has_comercio_dinero_getter)
    Span.set_extension('has_comercio_dinero', getter=has_comercio_dinero_getter)

    is_comercio_vendor_getter = lambda token: token.text in target_comercio_vendor_sing or token.text in target_comercio_vendor_plur
    Token.set_extension('is_comercio_vendor', getter=is_comercio_vendor_getter)
    has_comercio_vendor_getter = lambda obj: any([t._.is_comercio_vendor for t in obj])
    Doc.set_extension('has_comercio_vendor', getter=has_comercio_vendor_getter)
    Span.set_extension('has_comercio_vendor', getter=has_comercio_vendor_getter)

    is_droga_consumo_getter = lambda token: token.lemma_ in target_droga_consumo
    Token.set_extension('is_droga_consumo', getter=is_droga_consumo_getter)
    has_droga_consumo_getter = lambda obj: any([t._.is_droga_consumo for t in obj])
    Doc.set_extension('has_droga_consumo', getter=has_droga_consumo_getter)
    Span.set_extension('has_droga_consumo', getter=has_droga_consumo_getter)

    is_droga_getter = lambda token: token.text in target_droga_droga
    Token.set_extension('is_droga', getter=is_droga_getter)
    has_droga_getter = lambda obj: any([t._.is_droga for t in obj])
    Doc.set_extension('has_droga', getter=has_droga_getter)
    Span.set_extension('has_droga', getter=has_droga_getter)


def file_analyse(file_name, nlp):
    color_comercio_acto = "on_yellow"
    color_comercio_dinero = "on_blue"
    color_comercio_vendor = "on_magenta"
    color_droga_consumo = "on_green"
    color_droga = "on_red"
    cprint("************** Referencias: ********************\n", "white", attrs=['bold'])
    cprint("Amarillo: Indicio de comercialización.\n", "yellow", attrs=['bold'])
    cprint("Azul: Indicio de referencias a dinero.\n", "blue",attrs=['bold'])
    cprint("Violeta: Indicio de referencias a vendedores de droga.\n", "magenta",attrs=['bold'])
    cprint("Verde: Indicio de consumo de drogas.\n", "green",attrs=['bold'])
    cprint("Rojo: Indicio de referencias a drogas.\n", "red",attrs=['bold'])
    for line in open(file_name, "r").readlines():
        doc = nlp(line)
        flag_comercio_acto = False
        flag_comercio_dinero = False
        flag_comercio_vendor = False
        flag_droga_consumo = False
        flag_droga = False

        if doc._.has_comercio_acto:
            flag_comercio_acto = True

        if doc._.has_comercio_dinero:
            flag_comercio_dinero = True

        if doc._.has_comercio_vendor:
            flag_comercio_vendor = True

        if doc._.has_droga_consumo:
            flag_droga_consumo = True

        if doc._.has_droga:
            flag_droga = True

        if flag_comercio_acto or flag_comercio_dinero or flag_comercio_dinero or flag_droga_consumo or flag_droga:
            for token in doc:
                if token._.is_comercio_acto:
                    cprint(token, "white", color_comercio_acto, attrs=['bold'],end=' ')
                elif token._.is_comercio_dinero:
                    cprint(token, "white", color_comercio_dinero, attrs=['bold'],end=' ')
                elif token._.is_comercio_vendor:
                    cprint(token, "white", color_comercio_vendor, attrs=['bold'],end=' ')
                elif token._.is_droga_consumo:
                    cprint(token, "white", color_droga_consumo, attrs=['bold'],end=' ')
                elif token._.is_droga:
                    cprint(token, "white", color_droga, attrs=['bold'], end=' ')
                else:
                    cprint(token, 'white', end=' ')
                #print(' ', end= ' ')
            print('\n\n')



def dir_analyse(path, nlp):
    for arch in scandir(path):
        if arch.is_file():
            print(colored("Analizando --> ", "green") + colored("Archivo: " + abspath(arch.path), "blue") + "\n\n")
            file_text = open(abspath(arch.path), "r").readlines()
            doc = [nlp(line) for line in file_text]
            drug_suspicious = False
            comerce_suspicious = False
            consume_suspicious = False

            drug_suspicious_string = ""
            comerce_suspicious_string = ""
            consume_suspicious_string = ""

            for line in doc:
                if line._.has_drug:
                    drug_suspicious = True
                    for token in line:
                        drug_suspicious_string += ' ' + (colored(token, 'red') if token._.is_drug else colored(token, 'green'))
                    drug_suspicious_string += '\n'
                if line._.has_comercio:
                    comerce_suspicious = True
                    for token in line:
                        comerce_suspicious_string += ' ' + (colored(token, 'red') if token._.is_comercio else colored(token, 'green'))
                    comerce_suspicious_string += '\n'
            if drug_suspicious:
                drug_suspicious_string = colored(" --> Encontrada asociación con drogas:\n", "red") + drug_suspicious_string
                print(drug_suspicious_string)
            if comerce_suspicious:
                comerce_suspicious_string = colored(" --> Encontrada asociación con compra y venta:\n", "red") + comerce_suspicious_string
                print(comerce_suspicious_string)
            print('\n')
