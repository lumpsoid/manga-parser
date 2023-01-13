import os
import zipfile


def dir_check(path_to_dir, list_of_dirs):
    compiled_paths = [os.path.join(path_to_dir, f) for f in list_of_dirs]
    for i,f in enumerate(compiled_paths):
        if os.path.basename(f) == "cbz" or os.path.basename(f) == "manga_dict":  # funct dirs
            compiled_paths.pop(i)
        if not os.path.isdir(f):
            compiled_paths.pop(i)
    return compiled_paths


def archive_creating(output_path, manga_path, list_of_files):
    title = os.path.basename(manga_path)
    list_of_files.sort()
    with zipfile.ZipFile(f'{output_path}/{title}.cbz', 'w', zipfile.ZIP_DEFLATED) as zipf:
        print(f'archiving {title}')
        for file in list_of_files:
            zipf.write(file)


def slide_window_archiving(title_path, output_path, bunch=1):
    chapters = sorted(os.scandir(title_path), key=lambda entry: entry.name)
    for i in range(0, len(chapters), bunch):
        path_to_archive = f'{output_path}/{os.path.basename(title_path)}_{i}.cbz'
        zipf = zipfile.ZipFile(path_to_archive, 'w', zipfile.ZIP_DEFLATED)
        for chapter in chapters[i:i+bunch]:
            for page in os.scandir(chapter):
                zipf.write(page.path)
        zipf.close()
        print(f'wrote {path_to_archive}')
    print('Sliding is over')


def manga_convert_cbz(manga_dir, output_path, filter=[], bunch=0):
    for_archiving = []
    if not filter :  # заполнение фильтра папками
        filter = os.listdir(manga_dir)
    filter = dir_check(manga_dir, filter)
    print(filter)
    if bunch:
        for manga_path in filter:
            print(manga_path)
            slide_window_archiving(manga_path, output_path, bunch)
        return print('Script is done')
    for manga_path in filter:
        for root, dirs, files in os.walk(manga_path):
            if root == manga_path:
                continue
            for_archiving.extend([os.path.join(root, f) for f in files])
        archive_creating(output_path, manga_path, for_archiving)
        for_archiving = []
    print('Script is done')


if __name__ == '__main__':
    manga_convert_cbz(
        manga_dir='/home/qq/Downloads/manga',
        output_path='/home/qq/Downloads/manga/cbz',
        filter=['skeleton-soldier-skeleton-soldier-couldnt-protect-the-dungeon'],
        bunch=0
    )
    # slide_window_archiving(
    #         title_path='/home/qq/Downloads/manga/skeleton-soldier-skeleton-soldier-couldnt-protect-the-dungeon',
    #         output_path='/home/qq/Downloads/manga/cbz/test',
    #         bunch=1
    # )
# for root, dirs, files in sorted(os.walk(manga_dir), key=lambda entry: entry[0]):