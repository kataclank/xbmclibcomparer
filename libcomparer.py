#!/usr/bin/python3
import xml.etree.ElementTree as ET
import xlsxwriter
from model.movie import *

def main():
    rutaficherotuyas = '/home/rafa/Descargas/xbmc.xml'
    rutaficherocomparar = '/home/rafa/Descargas/luis.xml'
    tuspelis = processxml(rutaficherotuyas)
    comparar = processxml(rutaficherocomparar)
    listano = []
    listamejor = []
    for mov in comparar:
        if mov not in tuspelis:
            listano.append(mov)
        else:
            for pelitengo in tuspelis:
               if pelitengo.iden == mov.iden:
                    if mov.reswidth > pelitengo.reswidth or len(mov.dual) > len(pelitengo.dual): 
                        listamejor.append(mov)
    movielist2excel(listano, listamejor);
    
def movielist2excel(inexistentes, mejorables):
    print()
    workbook = xlsxwriter.Workbook('/home/rafa/Documentos/listado.xlsx')
    listatmejorablesws = workbook.add_worksheet()
    listatmejorablesws.name = 'Mejorables'
    listanows = workbook.add_worksheet()
    listanows.name = 'No tienes'
    #CABECERAS
    listatmejorablesws.write(0, 0 ,'ID')
    listatmejorablesws.write(0, 1 , 'TITLE')
    listatmejorablesws.write(0, 2 , 'WIDTH')
    listatmejorablesws.write(0, 3 , 'HEIGHT')
    listatmejorablesws.write(0, 4 , 'RUTA')
    listatmejorablesws.write(0, 5 , 'IDIOMAS')
    listanows.write(0, 0 ,'ID')
    listanows.write(0, 1 , 'TITLE')
    listanows.write(0, 2 , 'WIDTH')
    listanows.write(0, 3 , 'HEIGHT')
    listanows.write(0, 4 , 'RUTA')
    listanows.write(0, 5 , 'IDIOMAS')
    #RELLENAMOS TODO
    pos = 1
    for mejo in mejorables:
        listatmejorablesws.write(pos, 0 , mejo.iden)
        listatmejorablesws.write(pos, 1 , mejo.title)
        listatmejorablesws.write(pos, 2 , mejo.reswidth)
        listatmejorablesws.write(pos, 3 , mejo.reshei)
        listatmejorablesws.write(pos, 4 , mejo.filepath)
        listatmejorablesws.write(pos, 5 , str(mejo.dual))
        pos = pos + 1
    pos2 = 1
    for nota in inexistentes:
        listanows.write(pos2, 0 , nota.iden)
        listanows.write(pos2, 1 , nota.title)
        listanows.write(pos2, 2 , nota.reswidth)
        listanows.write(pos2, 3 , nota.reshei)
        listanows.write(pos2, 4 , nota.filepath)
        listanows.write(pos2, 5 , str(mejo.dual))
        pos2 = pos2 + 1
    workbook.close()


def processxml(ruta):
    movielist = []
    with open(ruta) as doc:
            tree = ET.parse(doc)
    for node in tree.iter('movie'):
        name = node.find('title').text
        ide = node.find('id').text
        path = node.find('path').text
        fileinfo = node.find('fileinfo')
        audiocad = []
        if fileinfo != None:
            streamdetails = fileinfo.find('streamdetails')
            width = streamdetails.find('video').find('width').text
            height = streamdetails.find('video').find('height').text
            if streamdetails != None:
                audio = streamdetails.findall("audio")
                for x in audio:
                    audiocad.append((x.find('language').text))
        movielist.append(movie(ide, name, width, height, path, audiocad))
    return movielist

if __name__ == "__main__":main()
  
