import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import traceback
import typing

root = tk.Tk()
root.withdraw()

TITLE = "Master Rallye Menu Freeze Patcher v1.1"

ORIG_BYTES  = b"\x10\xeb\x07\x8b\x54\x24\x10\x89\x56\x48\x85\xff\x75\x11\x8b\x44"
PATCH_BYTES = b"\x10\xeb\x07\x8b\x54\x24\x10\x89\x56\x48\x85\xff\x75\x00\x8b\x44"
#                                                                     ^
#                                                                  this one

class SearchFailure(Exception):
    pass


def search_executable(fname : str) -> typing.Tuple[bool, int]:
    with open(fname, "rb") as f:
        bs = f.read()
        if (addr := bs.find(ORIG_BYTES)) != -1:
            bs = bs[addr+1:]
            if ORIG_BYTES in bs or PATCH_BYTES in bs:
                raise SearchFailure("pattern found in multiple locations")

            return False, addr
        
        elif (addr := bs.find(PATCH_BYTES)) != -1:
            bs = bs[addr+1:]
            if ORIG_BYTES in bs or PATCH_BYTES in bs:
                raise SearchFailure("pattern found in multiple locations")

            return True, addr

        else:
            raise SearchFailure("pattern not found")


def apply_patch(fname : str, patch : bool, addr : int):
    with open(fname, "r+b") as f:
        f.seek(addr)
        current = f.read(len(ORIG_BYTES))
        assert current == (ORIG_BYTES if patch else PATCH_BYTES)
        f.seek(addr)
        f.write((PATCH_BYTES if patch else ORIG_BYTES))


def main():
    try:
        answer = False
        messagebox.showinfo(TITLE, "Please select path to MRallye.exe")
        fpath = filedialog.askopenfilename()
        patched, addr = search_executable(fpath)

        if not patched:
            answer = messagebox.askyesno(TITLE, 
                "This appears to be an unpatched executable. Apply patch?")
            if (answer):
                apply_patch(fpath, True, addr)

        else:
            answer = messagebox.askyesno(TITLE, 
                "This executable appears to already be patched. Remove patch?")
            if (answer):
                apply_patch(fpath, False, addr)

        if (answer):
            messagebox.showinfo(TITLE, "Process completed successfully")

    except SearchFailure as e:
        messagebox.showerror(TITLE,
            f"Unable to match instruction sequence for patching:\n{e}\n"
             "Please check this is the correct executable and you have read/write permissions for the file\n"
             "\n"
             "This script might need updating to handle this executable, "
             "consider reporting this to the developer"
        )
    except PermissionError:
        messagebox.showerror(TITLE, 
            f"Permission error accessing\n{fpath}.\nTry copying the executable to a "
             "non-admin area (such as My Documents) and try again")
    except Exception as e:
        tb = traceback.format_exc()
        messagebox.showerror(TITLE, 
            f"Unexpected exception:\n{tb}.\nPlease report this error to the developer")

if __name__ == "__main__":
    main()
