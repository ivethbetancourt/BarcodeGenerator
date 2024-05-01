import os
import tempfile
from subprocess import Popen
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import barcode
from barcode.writer import ImageWriter

tmp_path = 'BarcodeGenerator.png'

barcode_types = ['code128']

def generate_barcode(event):
    global tmp_path
    delete_temp_image()
    barcode_txt = ent_barcode_txt.get()
    code_type = ent_code_type.get()
    if len(barcode_txt) == 0:
        notify('Nothing to do')
        return
    print(f'Code type: {code_type}')
    print(f'Text to generate: {barcode_txt}')
    b_class = barcode.get_barcode_class(code_type)
    iw = barcode.writer.ImageWriter()
    iw.set_options({'dpi': 140})
    try:
        bar = b_class(str(barcode_txt), writer=iw)
        notify('Format success')
    except (barcode.errors.WrongCountryCodeError,
            barcode.errors.BarcodeError,
            barcode.errors.BarcodeNotFoundError,
            barcode.errors.IllegalCharacterError,
            barcode.errors.NumberOfDigitsError,
            ValueError) as e:
        return notify(str(e))
    path = os.path.join(tempfile.gettempdir(), barcode_txt)
    tmp_path = bar.save(path, text=barcode_txt)
    print(f'temporary image: {tmp_path}')


def delete_temp_image():
    global tmp_path
    if tmp_path == 'BarcodeGenerator.png':
        return
    os.remove(tmp_path)
    tmp_path = 'BarcodeGenerator.png'


def preview_image():
    tmp_img = PhotoImage(file=tmp_path)
    pnl_image.config(image=tmp_img)
    pnl_image.image = tmp_img
    pnl_image.after(200, preview_image)


def open_image(event=None):
    os_name = os.name
    if os_name == 'nt':
        try:
            Popen(['mspaint', tmp_path])
        except (FileNotFoundError, NameError):
            notify('MS Paint not found')
    elif os_name == 'posix':
        # for Ubuntu maybe others
        try:
            Popen(['shotwell', tmp_path])
        except (FileNotFoundError, NameError):
            notify('Shotwell not found')


def save_image(event=None):
    file = filedialog.asksaveasfile(
        mode="wb", title="Save Image", defaultextension=".png",
        initialfile=tmp_path.split(os.sep)[-1],
        filetypes=(("png files", "*.png"), ("all files", "*.*")))
    if file:
        try:
            image = open(tmp_path, 'rb').read()
            file.write(image)
            file.close()
            notify('Image saved')
        except AttributeError as e:
            notify(str(e))


def notify(string='Press Enter to generate barcode'):
    lbl_notify.config(text=string)


master = Tk()


lbl_preview = Label(master, text='Preview')
lbl_preview.place(x=240, y=180)

img = PhotoImage(file=tmp_path)
pnl_image = Label(master, image=img)
pnl_image.place(x=220, y=130)

lbl_notify = Label(master, text='None')
lbl_notify.place(x=5, y=290)



master.iconbitmap(r'icon.ico')
master.wm_title("BarcodeGenerator")
master.geometry("540x320")
preview_image()
notify()
master.mainloop()
delete_temp_image()
