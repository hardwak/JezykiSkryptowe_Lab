import sys


def media_files():
    extensions = ['.gif', '.jpg', '.jpeg', '.xbm']
    mediaFiles, allFiles = 0, 0
    for line in sys.stdin:
        parts = line.split()
        allFiles += 1
        for ext in extensions:
            if parts[6].endswith(ext):
                mediaFiles += 1
    print("Num of all files: {}".format(allFiles))
    print("Num of media files: {}".format(mediaFiles))


if __name__ == "__main__":
    media_files()