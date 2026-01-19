import os, sys, tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Notebook, Treeview, Combobox, Style
from openpyxl import Workbook, load_workbook
from datetime import datetime, timedelta

def base():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)

BASE = base()
def p(x): return os.path.join(BASE, x)

def ensure():
    files = {
        "ogrenciler.xlsx": ["ID", "No", "Ad", "Sınıf"],
        "kitaplar.xlsx": ["ID", "KitapID", "Ad", "Yazar"], 
        "odunc.xlsx": ["ID", "KitapID", "OgrNo", "Alis", "SonGun", "Durum"],
        "teslim.xlsx": ["ID", "KitapID", "OgrNo", "Alis", "Teslim"]
    }
    for f, h in files.items():
        if not os.path.exists(p(f)):
            wb = Workbook()
            ws = wb.active
            ws.append(h)
            wb.save(p(f))

ensure()

root = tk.Tk()
root.title("📚 Okul Kütüphanesi Yönetim Sistemi")
root.state("zoomed")
root.configure(bg="#f4f6f7")

style = Style()
style.theme_use("default")

style.configure(
    "Treeview",
    background="white",
    foreground="#2c3e50",
    rowheight=28,
    fieldbackground="white",
    font=("Arial", 11)
)
style.configure(
    "Treeview.Heading",
    font=("Arial", 12, "bold"),
    background="#d6dbdf",
    foreground="#2c3e50"
)
style.map("Treeview", background=[("selected", "#aed6f1")])

nb = Notebook(root)
nb.pack(fill="both", expand=True, padx=8, pady=8)

tab_main = tk.Frame(nb, bg="#f4f6f7")
tab_add  = tk.Frame(nb, bg="#f4f6f7")
tab_io   = tk.Frame(nb, bg="#f4f6f7")
tab_search = tk.Frame(nb, bg="#f4f6f7")
tab_reports = tk.Frame(nb, bg="#f4f6f7")

nb.add(tab_main, text="📊 Ana Tablolar")
nb.add(tab_add,  text="➕ Öğrenci / Kitap Ekle")
nb.add(tab_io,   text="🔄 Ödünç / Teslim")
nb.add(tab_reports, text="📈 Raporlar")
nb.add(tab_search, text="🔍 Arama / Silme")

def table(frame, cols, title):
    table_frame = tk.Frame(frame, bg="#f4f6f7")
    table_frame.pack(fill="both", expand=True, padx=4, pady=4)

    tk.Label(
        table_frame, text=title,
        font=("Arial",16,"bold"),
        bg="#f4f6f7", fg="#2c3e50"
    ).pack(pady=6)

    tree_container = tk.Frame(table_frame)
    tree_container.pack(fill="both", expand=True, padx=6)

    tv = Treeview(tree_container, columns=cols, show="headings")
    vsb = tk.Scrollbar(tree_container, orient="vertical", command=tv.yview)
    hsb = tk.Scrollbar(tree_container, orient="horizontal", command=tv.xview)
    tv.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    tv.pack(side="left", fill="both", expand=True)

    for c in cols:
        tv.heading(c, text=c)
        tv.column(c, width=120, anchor="center")
    return tv

top = tk.Frame(tab_main, bg="#f4f6f7")
bot = tk.Frame(tab_main, bg="#f4f6f7")
top.pack(fill="both", expand=True)
bot.pack(fill="both", expand=True)

tv_students = table(top, ["ID","No","Ad","Sınıf"], "👩‍🎓 ÖĞRENCİLER")
tv_books    = table(top, ["ID","KitapID","Ad","Yazar"], "📘 KİTAP ENVANTERİ")

report_top = tk.Frame(tab_reports, bg="#f4f6f7")
report_mid = tk.Frame(tab_reports, bg="#f4f6f7")
report_buttons = tk.Frame(tab_reports, bg="#f4f6f7")

report_top.pack(fill="both", expand=True)
report_mid.pack(fill="both", expand=True)
report_buttons.pack(fill="x", pady=10)

tv_loans_out = table(report_top, ["ID","KitapID","Kitap Adı","OgrNo","Öğrenci Adı","Alış Tarihi","Son Teslim"], "📕 ÖDÜNÇ VERİLEN KİTAPLAR LİSTESİ")
tv_performance = table(report_mid, ["OgrNo","Öğrenci Adı","Toplam Alınan","Toplam Teslim","Ortalama Süre (Gün)"], "📈 ÖĞRENCİ KİTAP KULLANIM ÖZETİ")

tv_performance.bind("<Double-1>", lambda event: show_read_books_report(event))

tv_loans    = table(bot, ["ID","KitapID","OgrNo","Alis","SonGun","Durum"], "TÜM ÖDÜNÇ/TESLİM KAYITLARI")
tv_returns  = table(bot, ["ID","KitapID","OgrNo","Alis","Teslim"], "📗 BAŞARIYLA TESLİM EDİLENLER")

student_names_cache = {}
book_names_cache = {}

def get_student_info(ogr_no):
    if ogr_no in student_names_cache:
        return student_names_cache[ogr_no]
    wb = load_workbook(p("ogrenciler.xlsx"))
    ws = wb.active
    for row in ws.iter_rows(min_row=2, values_only=True):
        if str(row[1]) == str(ogr_no):
            student_names_cache[ogr_no] = str(row[2])
            return str(row[2])
    return "Bilinmiyor"

def get_book_info(kitap_id):
    if kitap_id in book_names_cache:
        return book_names_cache[kitap_id]
    wb = load_workbook(p("kitaplar.xlsx"))
    ws = wb.active
    for row in ws.iter_rows(min_row=2, values_only=True):
        if str(row[1]) == str(kitap_id):
            book_names_cache[kitap_id] = str(row[2])
            return str(row[2])
    return "Bilinmiyor"

def get_book_author(kitap_id):
    wb = load_workbook(p("kitaplar.xlsx"))
    ws = wb.active
    for row in ws.iter_rows(min_row=2, values_only=True):
        if str(row[1]) == str(kitap_id):
            return str(row[3])
    return "Bilinmiyor"


