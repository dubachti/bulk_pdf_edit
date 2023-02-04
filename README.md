# bulk_pdf_edit

Change the opacity of multiple PDF files at once and merge them into one file.

# Overview
Collect all PDF files you want to edit in a directory.
Next using the command
```bash
~$ python3 bulk_pdf_edit.py -p 'path to dir' -a opacity -o 'opacity val'
```
the opacity of the files in directory can be changed by 'opacity val' (value in [0,100]). Additionally by setting the flag '-w True' the files will get overwritten by the modified ones.


### explain merge action
