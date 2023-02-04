import glob
from pdf2image import convert_from_path
from PIL import Image
from PyPDF2 import PdfMerger

ALL_ACTIONS = ["opacity", "merge", "rotate", "rename"]

def bulk_handler(args):
    ## not if this is the way to go
    args["file_paths"] = glob.glob("{}/*.pdf".format(args["path"]))
    action = "bulk_" + args["action"]
    func = globals()[action]
    func(**args)

def bulk_opacity(file_paths: list[str],   # addr to directory
                 opacity_val: int, # in %
                 overwrite: bool,
                 dpi: int = 100,
                 **_
                 ) -> None:
    pages = [convert_from_path(f_path, dpi) for f_path in file_paths]

    def mod_img(img):
        img.putalpha(int(opacity_val*3.56)) 
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img,mask=img.split()[3])
        return bg

    for page in pages:
        page[:] = [mod_img(img) for img in page]

    if not overwrite: new_file_paths = [x[:-4] + "_edited.pdf" for x in file_paths]
    else: new_file_paths = file_paths

    for f_path, page in zip(new_file_paths, pages):
        page[0].save(f_path, "PDF", resolution=100.0, save_all=True, append_images=page[1:])

def bulk_merge(file_paths: list[str],
               path: str,
               out_name: str = "merged_file",
               sort: bool = True,
               **_
               ) -> None:
    if sort: file_paths.sort()
    merger = PdfMerger()
    [merger.append(file) for file in file_paths]
    merger.write(f"{path}/{out_name}.pdf")
    merger.close()

def bulk_rotate(file_paths: list[str],      # addr to directory
                rotation_val: int,   # cw rotation angle
                **_
                ) -> None:
    #print("bulk_rotate", file_paths, rotation_val)
    #https://stackoverflow.com/questions/46921452/batch-rotate-pdf-files-with-pypdf2
    raise NotImplementedError

def bulk_rename(file_paths: list[str],                         # addr to directory
                name_func: list[tuple[str, str]],   # rename func: f(old_namespace) -> new_namespace
                **_
                ) -> None:
    #print("bulk_rename", file_paths, name_func)
    raise NotImplementedError

