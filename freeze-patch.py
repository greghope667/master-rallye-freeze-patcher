import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import hashlib
import traceback

root = tk.Tk()
root.withdraw()

TITLE = "Master Rallye Menu Freeze Patcher"

PATCH_ADDR = 0x0024a1bc
HASH_PATCHED = "4e87eb51874111a6065df64504f165f1"
HASH_ORIG = "1f7cb6d6371feada438dc70df6beec4f"
VAL_PATCHED = b"\x75\x00"
VAL_ORIG = b"\x75\x11"

def hash(fname : str) -> str:
    md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            md5.update(block)
    return md5.hexdigest()

def apply_patch(fname : str, patch : bool=True):
    with open(fname, "r+b") as f:
        f.seek(PATCH_ADDR)
        current = f.read(2)
        assert current == (VAL_ORIG if patch else VAL_PATCHED)
        f.seek(PATCH_ADDR)
        f.write((VAL_PATCHED if patch else VAL_ORIG))

def main():
    try:
        messagebox.showinfo(TITLE, "Please select path to MRallye.exe")
        fpath = filedialog.askopenfilename()
        fhash = hash(fpath)
        answer = False

        if (fhash == HASH_ORIG):
            answer = messagebox.askyesno(TITLE, 
                "This appears to be an unpatched executable. Apply patch?")
            if (answer):
                apply_patch(fpath, True)

        elif (fhash == HASH_PATCHED):
            answer = messagebox.askyesno(TITLE, 
                "This executable appears to already be patched. Remove patch?")
            if (answer):
                apply_patch(fpath, False)

        else:
            answer = messagebox.askyesno(TITLE, 
                "WARNING: Did not recognise the executable file. Attempt "
                "patch anyway? (potentially unsafe)")
            if (answer):
                apply_patch(fpath, True)

        if (answer):
            messagebox.showinfo(TITLE, "Process completed successfully")

    except PermissionError:
        messagebox.showerror(TITLE, 
            f"Permission error accessing\n{fpath}.\nTry copying the executable to a "
             "non-admin area (such as My Documents) and try again")
    except AssertionError:
        messagebox.showerror(TITLE, 
            "Unable to apply patch - couldn't find the instruction to fix. "
            "Please check this is the correct executable and you have read/write permissions for the file")
    except Exception as e:
        tb = traceback.format_exc()
        messagebox.showerror(TITLE, 
            f"Unexpected exception:\n{tb}.\nPlease report this error to the developer")

if __name__ == "__main__":
    main()