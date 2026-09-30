import tkinter as tk

root = tk.Tk()
root.title("Kalkulator")
root.geometry("320x480")
root.resizable(False, False)
root.configure(bg="#A87836")

# ---------- Layar tampilan ----------
ekspresi = tk.StringVar()
riwayat = tk.StringVar()          

atas = tk.Frame(root, bg="#A87836")
atas.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=15, pady=(15, 10))

label_riwayat = tk.Label(
    atas,
    textvariable=riwayat,
    font=("Segoe UI", 14),
    anchor="e",
    bg="#A87836",
    fg="#FFFDD0",
    cursor="hand2",
)
label_riwayat.pack(fill="x")

layar = tk.Entry(
    atas,
    textvariable=ekspresi,
    font=("Segoe UI", 28),
    justify="right",
    bg="#FFFDD0",
    fg="black",
    bd=0,
    insertbackground="black",   
)
layar.pack(fill="x", pady=(5, 0))

# ---------- Susunan tombol ----------
susunan = [
    ["C", "⌫", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", ",",  "="],
]

# warna khusus untuk tombol tertentu
warna_merah = {
    "C": ("#C60000", "#C60000"),
    "=": ("#371D10", "#371D10"),
    "+": ("#371D10", "#371D10"),
    "⌫": ("#371D10", "#371D10"),
    "%": ("#371D10", "#371D10"),
    "-": ("#371D10", "#371D10"),
    "×": ("#371D10", "#371D10"),
    "÷": ("#371D10", "#371D10"),
}


# ---------- Format angka gaya Indonesia ----------
def format_angka(angka):
    if angka == int(angka):
        teks = f"{int(angka):,}"
    else:
        teks = f"{angka:,.2f}"

    # tukar: koma <-> titik
    teks = teks.replace(",", "TEMP").replace(".", ",").replace("TEMP", ".")
    return teks


# ---------- Logika hitung ----------
ekspresi_terakhir = ""     
sudah_hitung = False       

def hitung():
    global ekspresi_terakhir, sudah_hitung
    isi = layar.get()
    if isi == "":
        return

    ekspresi_terakhir = isi
    riwayat.set(isi + " =")          

    # bongkar format Indonesia agar bisa dihitung Python
    rumus = isi.replace(".", "").replace(",", ".")
    rumus = rumus.replace("×", "*").replace("÷", "/").replace("%", "/100")

    try:
        hasil = eval(rumus)
        teks_hasil = format_angka(hasil)
        layar.delete(0, tk.END)
        layar.insert(0, teks_hasil)
        sudah_hitung = True
    except ZeroDivisionError:
        layar.delete(0, tk.END)
        layar.insert(0, "Tidak bisa bagi 0")
    except Exception:
        layar.delete(0, tk.END)
        layar.insert(0, "Error")


# ---------- Aksi saat tombol ditekan (mouse atau keyboard) ----------
def tombol_ditekan(teks):
    global sudah_hitung

    if layar.get() in ("Error", "Tidak bisa bagi 0"):
        layar.delete(0, tk.END)

    if sudah_hitung:
        sudah_hitung = False
        if teks == "⌫":
            # kembalikan rumus ke layar supaya bisa diedit
            layar.delete(0, tk.END)
            layar.insert(0, ekspresi_terakhir)
            riwayat.set("")
            layar.icursor(tk.END)
            layar.focus_set()
            return
        elif teks in "0123456789.,":
            # angka baru: mulai hitungan baru
            layar.delete(0, tk.END)
            riwayat.set("")
        else:
            # operator: lanjut dari hasil sebelumnya
            riwayat.set("")

    posisi = layar.index(tk.INSERT)

    if teks == "C":
        layar.delete(0, tk.END)
        riwayat.set("")
    elif teks == "⌫":
        if posisi > 0:
            layar.delete(posisi - 1)
    elif teks == "=":
        hitung()
        layar.icursor(tk.END)
    else:
        layar.insert(posisi, teks)

    layar.focus_set()


# klik tulisan rumus di atas = edit ulang rumus
label_riwayat.bind("<Button-1>", lambda e: tombol_ditekan("⌫"))


# ---------- Membuat tombol-tombol ----------
for baris, isi_baris in enumerate(susunan, start=1):
    for kolom, teks in enumerate(isi_baris):

        if teks in warna_merah:
            warna_normal, warna_klik = warna_merah[teks]
            warna_teks = "white"
        else:
            warna_normal, warna_klik = "#313244", "#45475a"
            warna_teks = "white"

        btn = tk.Button(
            root,
            text=teks,
            font=("Segoe UI", 16, "bold"),
            bg=warna_normal,
            fg=warna_teks,
            bd=0,
            activebackground=warna_klik,
            activeforeground=warna_teks,
            command=lambda t=teks: tombol_ditekan(t),
        )
        btn.grid(row=baris, column=kolom, sticky="nsew", padx=4, pady=4)

# agar semua baris dan kolom melebar rata
for i in range(4):
    root.columnconfigure(i, weight=1)
for i in range(1, 6):
    root.rowconfigure(i, weight=1)


# ---------- Dukungan keyboard ----------
def keyboard_ditekan(event):
    karakter = event.char
    tombol = event.keysym

    # tombol navigasi dibiarkan bekerja normal
    if tombol in ("Left", "Right", "Home", "End", "Delete", "Tab"):
        return

    # kombinasi Ctrl (copy, paste, dll) dibiarkan normal
    if event.state & 0x4:
        return

    # tombol yang dikenali lewat namanya (termasuk numpad)
    if tombol in ("plus", "KP_Add"):
        tombol_ditekan("+")
    elif tombol in ("comma", "KP_Separator"):
        tombol_ditekan(",")
    elif tombol == "KP_Decimal":
        tombol_ditekan(karakter if karakter in (".", ",") else ".")
    elif karakter != "" and karakter in "0123456789.,+-%":
        tombol_ditekan(karakter)
    elif karakter in ("*", "x", "X"):
        tombol_ditekan("×")
    elif karakter == "/":
        tombol_ditekan("÷")
    elif tombol in ("Return", "KP_Enter") or karakter == "=":
        tombol_ditekan("=")
    elif tombol == "BackSpace":
        tombol_ditekan("⌫")
    elif tombol == "Escape" or karakter in ("c", "C"):
        tombol_ditekan("C")

    return "break"   # blokir input bawaan Entry


layar.bind("<Key>", keyboard_ditekan)
layar.focus_set()

root.mainloop()