#!/usr/bin/python3
#Autor:l4z4rt

from shutil import rmtree
from pytube import YouTube, Stream
from pytube.cli import on_progress
import sys, os, ffmpeg  


def time(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas*60*60
    minutos = int(segundos/60)
    segundos -= minutos*60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

def sizeFile(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0
    return size

if (sys.argv[1]) == "-t":
    
    os.system('clear')

    link = YouTube(sys.argv[3])
        
    for stream in link.streams.filter(adaptive=True, type="video", resolution=sys.argv[2]):

        print(f"#--- Video File ---#")
        print("Itag: " + str(stream.itag))
        print("Resolucion: " + str(stream.resolution))
        print("Codec : " + str(stream.codecs))
        print("fps :" + str(stream.fps))
        print("---------------------------")

#    for stream in link.streams.filter(adaptive=True, type="audio"):
#
#        print(f"#--- Audio ---#")
#        print("Itag: " + str(stream.itag))
#        print("Audio: " + str(stream.abr))
#        print("Codec : " + str(stream.codecs))
#        print("---------------------------")
#    print("-----------------------")
    exit()        



elif (sys.argv[1]) == "-d":

    os.system('clear')

    link = YouTube(sys.argv[3], on_progress_callback=on_progress)
     
    filesize = link.streams.get_by_itag(sys.argv[2]).filesize
    
    print(f"Canal: {link.author}")
    print(f"Titulo: {link.title}")
    print(f"Duracion: {time(link.length)}")
    print(f"Tamaño: {sizeFile(filesize)}")
    print("\n")
    
    video = link.streams.get_by_itag(sys.argv[2]) 
    audio = link.streams.filter(only_audio=True).last()
    
    os.mkdir("resources")

    video.download(output_path="./resources", filename="videoFile.mp4")
    audio.download(output_path="./resources", filename="audioFile.webm")
    
    print("\nDescarga Completada\n")

    input_video = ffmpeg.input(r'./resources/videoFile.mp4')
    input_audio = ffmpeg.input(r'./resources/audioFile.webm')

    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f'{link.title}.mp4').run()
    rmtree("./resources")
    
    print("\nSe ah completado la descarga de su video")

else:

    print("\n   -t --table      <resolution>    <url>                           Muestra por pantalla Itag de video y audio")
    print("\n   -d --download   <Itag-Video>    <url>                           Descargar opciones seleccionadas")
    print("\n     Example:")
    print("\n             -t 1080p https://www.youtube.com/********")
    print("\n             -d 162 https://www.youtube.com/********")
    exit()

