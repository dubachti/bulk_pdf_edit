import glob
from pdf2image import convert_from_path
from PIL import Image
from PyPDF2 import PdfMerger

ALL_ACTIONS = ["opacity", "merge"]

# constructs filepaths calls appropriate func
def bulk_handler(args):
    args["file_paths"] = glob.glob("{}/*.pdf".format(args["path"]))
    action = "bulk_" + args["action"]
    func = globals()[action]
    func(**args)

# modifys opacity of 'file_paths' files
def bulk_opacity(file_paths: list[str],
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

# merges all 'file_paths' files together into one pdf file
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