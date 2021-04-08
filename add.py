import os
import argparse
from tinytag import TinyTag


def read_tracks(path=os.getcwd()):
    track_list = []
    for element in os.listdir(path):
        if element.endswith(".mp3"):
            track_list.append(element)
    return track_list


def get_tags(track_list, src_dir=os.getcwd(), dst_dir=os.getcwd()):
    for music in track_list:
        music_path = os.path.join(src_dir, music)
        song = TinyTag.get(music_path)
        if song.artist and song.album:
            if song.title is None:
                name = music
            else:
                name = song.artist + "-" + song.title + "-" + song.album + ".mp3"
            path_after = os.path.join(dst_dir, song.artist)
            try:
                os.mkdir(path_after)
                path_after = os.path.join(path_after, song.album)
                try:
                    os.mkdir(path_after)
                    path_after = os.path.join(path_after, name)
                    os.rename(music_path, path_after)
                    print(music_path, "->", path_after)
                except OSError:
                    path_after = os.path.join(path_after, name)
                    os.rename(music_path, path_after)
                    print(music_path, "->", path_after)
            except OSError:
                path_after = os.path.join(path_after, song.album)
                try:
                    os.mkdir(path_after)
                    path_after = os.path.join(path_after, name)
                    os.rename(music_path, path_after)
                    print(music_path, "->", path_after)
                except OSError:
                    path_after = os.path.join(path_after, name)
                    os.rename(music_path, path_after)
                    print(music_path, "->", path_after)
        else:
            print("Отсутсвует тег у файла", music)


parser = argparse.ArgumentParser(description="Сортировка музыкальных файлов")
parser.add_argument("--src", help="Исходный путь с музыкой", default="", required=True)
parser.add_argument("--dst", help="Конечный путь с отсортированной музыкой", default="", required=True)
args = parser.parse_args()
src_dir = args.src
dst_dir = args.dst
if not os.path.exists(src_dir):
    print("Не существует введенного исходного пути")
    exit(0)
if not os.path.exists(dst_dir):
    print("Не существует введенного конечного пути")
    exit(0)
if not os.access(src_dir, os.W_OK) and not os.access(src_dir, os.R_OK):
    print("Нет прав доступа к исходной директории")
if not os.access(dst_dir, os.W_OK) and not os.access(dst_dir, os.R_OK):
    print("Нет прав доступа к конечной директории")

var = read_tracks(src_dir)
get_tags(var, src_dir, dst_dir)
