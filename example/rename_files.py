import os


def rename_files(patch):
    for root, dirs, files in os.walk(patch):
        for file in files:
            file = os.path.join(root, file)
            file_ = os.path.join(root, f'{file}_')
            os.rename(file, file_)
            os.rename(file_, file)


def main():
    patch = r'D:\Folder'
    rename_files(patch=patch)


if __name__ == '__main__':
    main()
