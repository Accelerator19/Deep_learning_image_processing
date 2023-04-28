import os


def remove_folder(folder):
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        os.remove(file_path)
