from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from ctypes import *
import time


class FlashTab:
    def __init__(self, parent):
        self.p = parent
        self.gui = self.p.gui
        self.i2c = self.p.i2c
        self.fls = self.p.fls
        self.i2c_tab = self.p.i2c_tab

        top_frm = ttk.Frame(self.p.flash_frm, padding=self.gui.v.pad.get())
        flash_note = ttk.Notebook(self.p.flash_frm)
        top_frm.pack(fill=X)
        flash_note.pack(fill=BOTH, expand=YES)

        ttk.Label(top_frm, text="I\u00b2C Slave Address (hex) ").grid(row=0, column=0, sticky=NE)
        ttk.Entry(top_frm, textvariable=self.i2c.v.slave_addr, width=2).grid(row=0, column=1, sticky=NW)

        sp_frm = ttk.Frame(flash_note, padding=self.gui.v.pad.get() * 5)
        flash_note.add(sp_frm, text=" SP Flash ")

        sp0 = ttk.Frame(sp_frm)
        sp1 = ttk.Frame(sp_frm)
        sp0.pack(fill=X)
        sp1.pack(fill=X)

        ttk.Label(sp0, text="Test Mode: ").grid(row=0, column=0, sticky=W)
        ttk.Button(sp0, text="ON", width=5, command=self.test_on).grid(row=0, column=1, stick=NW)
        ttk.Button(sp0, text="OFF", width=5, command=self.test_off).grid(row=0, column=2, stick=NW)
        ttk.Label(sp0, text="\n\n").grid(row=1, column=0)

        ttk.Label(sp1, text="Flash Address ").grid(row=0, column=0, sticky=NE)
        ttk.Entry(sp1, textvariable=self.fls.v.flash_addr).grid(row=0, column=1, sticky=NW)
        ttk.Label(sp1, text="").grid(row=1, column=0, columnspan=3)
        ttk.Button(sp1, text="Sector Erase", width=12, command=self.sector_erase).grid(row=2, column=0, padx=(0, 5), pady=(5, 0), sticky=NE)
        ttk.Button(sp1, text="Write 24 Bytes", width=12, command=self.write_24_bytes).grid(row=3, column=0, padx=(0, 5), pady=(5, 0), sticky=NE)
        ttk.Button(sp1, text="Read 24 Bytes", width=12, command=self.read_24_bytes).grid(row=4, column=0, padx=(0, 5), pady=(5, 0), sticky=NE)
        ttk.Entry(sp1, textvariable=self.fls.v.w_24, width=60).grid(row=3, column=1, columnspan=2, pady=(5, 0), sticky=W)
        ttk.Entry(sp1, textvariable=self.fls.v.r_24, width=60, state="readonly").grid(row=4, column=1, columnspan=2, pady=(5, 0), sticky=W)
        ttk.Label(sp1, text="").grid(row=5, column=0, columnspan=3)
        ttk.Button(sp1, text="Erase Sectors", width=12, command=self.sector_erase_range).grid(row=6, column=0, padx=(0, 5), sticky=NE)
        ttk.Button(sp1, text="Backup to Files", width=12, command=self.backup).grid(row=7, column=0, padx=(0, 5), pady=(5, 0), sticky=NE)
        ttk.Label(sp1, text="From ").grid(row=6, column=1, sticky=NE)
        ttk.Label(sp1, text="To ").grid(row=7, column=1, pady=(5, 0), sticky=NE)
        ttk.Entry(sp1, textvariable=self.fls.v.flash_from, width=8).grid(row=6, column=2, sticky=NW)
        ttk.Entry(sp1, textvariable=self.fls.v.flash_to, width=8).grid(row=7, column=2, pady=(5, 0), sticky=NW)
        ttk.Label(sp1, text="").grid(row=8, column=0, columnspan=3)
        ttk.Button(sp1, text="Write from File", width=12, command=self.file_write).grid(row=9, column=0, padx=(0, 5), sticky=NE)
        ttk.Button(sp1, text="Write & Backup", width=12, command=self.write_backup).grid(row=10, column=0, padx=(0, 5), pady=(5, 0), sticky=NE)

    def flash_write(self, addr_str, data_str):
        self.write_addr(addr_str)
        self.write_data(data_str)
        self.write_1_byte("9536", "02")  # Write
        self.write_1_byte("9536", "00")  # Wait

    def write_1_byte(self, addr, byte):
        byte_list = create_string_buffer(1)
        byte_list[0:1] = bytearray().fromhex(byte)
        sub_errno, result = self.i2c_tab.sub20_i2c_write(int(self.i2c.v.slave_addr.get(), 16), int(addr, 16), byte_list)
        if sub_errno != 0:
            messagebox.showinfo("I\u00b2C Write Result", "Write Failed\n" + result)
    
    def write_addr(self, addr_str):
        rm_sp = re.compile(r"\s+")
        addr_flip = re.compile(r"..?")
        addr_list = addr_flip.findall(rm_sp.sub("", addr_str))
        byte_list = create_string_buffer(3)
        byte_list[0:3] = bytearray().fromhex(" ".join(reversed(addr_list)))
        sub_errno, result = self.i2c_tab.sub20_i2c_write(int(self.i2c.v.slave_addr.get(), 16), int("9537", 16), byte_list)
        if sub_errno != 0:
            messagebox.showinfo("I\u00b2C Write Result", "Write Failed\n" + result)

    def write_data(self, str_24b):
        byte_list = create_string_buffer(24)
        byte_list[0:24] = bytearray().fromhex(str_24b)
        sub_errno, result = self.i2c_tab.sub20_i2c_write(int(self.i2c.v.slave_addr.get(), 16), int("953A", 16), byte_list)
        if sub_errno != 0:
            messagebox.showinfo("I\u00b2C Write Result", "Write Failed\n" + result)

    def read_data(self, n):
        read_list, result = self.i2c_tab.sub20_i2c_read(int(self.i2c.v.slave_addr.get(), 16), int("958F", 16), n)
        time.sleep(0.1)
        try:
            len(read_list)
        except TypeError:
            messagebox.showinfo("I\u00b2C Read Result", "Read Failed\n" + result)
            return "-"
        return read_list

    # Button Functions
    def test_on(self):
        self.write_1_byte("9506", "01")

    def test_off(self):
        self.write_1_byte("9506", "00")

    def sector_erase(self):
        self.write_1_byte("9525", "80")
        self.write_addr(self.fls.v.flash_addr.get())
        self.write_1_byte("9536", "04")  # Erase
        self.write_1_byte("9536", "00")  # Wait
        time.sleep(0.4)

    def write_24_bytes(self):
        str_list = self.fls.v.w_24.get().split()
        if len(str_list) < 24:
            str_list[len(str_list):24] = ["FF"] * (24 - len(str_list))
        self.flash_write(self.fls.v.flash_addr.get(), " ".join(str_list))

    def read_24_bytes(self):
        self.write_addr(self.fls.v.flash_addr.get())
        self.write_1_byte("9536", "C1")  # Read 24byte
        self.write_1_byte("9536", "00")  # Wait
        read_list = self.read_data(24)
        if len(read_list) == 1:
            self.fls.v.r_24.set("error")
        else:
            self.fls.v.r_24.set(" ".join([f"{ord(x):02X}" for x in read_list]))

    def sector_erase_range(self):
        er_start = int(self.fls.v.flash_from.get(), 16)
        er_end = int(self.fls.v.flash_to.get(), 16)
        self.write_1_byte("9525", "80")
        for k in range(er_start, er_end, 2 ** 12):
            self.write_addr(f"{k:06X}")
            self.write_1_byte("9536", "04")  # Erase
            self.write_1_byte("9536", "00")  # Wait
            time.sleep(0.2)
        time.sleep(0.2)

    def backup(self):
        bk_start = int(self.fls.v.flash_from.get(), 16)
        bk_end = int(self.fls.v.flash_to.get(), 16)

        filename = filedialog.asksaveasfilename(filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        backup = open(filename, "w")
        for addr in range(bk_start, bk_end, 16):
            addr_str = f"{addr:06X}"
            backup.write("@" + addr_str + " ")
            self.write_addr(addr_str)
            self.write_1_byte("9536", "81")  # Read 16byte
            self.write_1_byte("9536", "00")  # Wait
            read_list = self.read_data(16)
            if len(read_list) == 1:
                messagebox.showerror("ERROR", "Error")
                break
            backup.write(" ".join([f"{ord(x):02X}" for x in read_list]))
            backup.write("\n")
        backup.close()

    def file_write(self):
        filename = filedialog.askopenfilename()
        fflash = open(filename, "r")
        addr0 = -1
        addr = 0
        str_24b = []
        for line in fflash:
            flist = line.strip().split()
            faddr = flist[0].lstrip("@")
            if addr0 < 0:
                addr = int(faddr, 16)
            elif addr0 + 16 != int(faddr, 16):
                if len(str_24b) > 0:
                    str_24b[len(str_24b):24] = ["FF"] * (24 - len(str_24b))
                    self.flash_write(f"{addr:06X}", " ".join(str_24b))
                str_24b = flist[1:]
                addr0 = int(faddr, 16)
                addr = addr0
                continue

            addr0 = int(faddr, 16)
            if len(str_24b) + len(flist) - 1 < 24:
                str_24b.extend(flist[1:])
                continue

            flist_cut = 25 - len(str_24b)
            str_24b.extend(flist[1:flist_cut])

            self.flash_write(f"{addr:06X}", " ".join(str_24b))
            str_24b = flist[flist_cut:]
            addr = addr + 24
        fflash.close()

        if len(str_24b) > 0:
            str_24b[len(str_24b):24] = ["FF"] * (24 - len(str_24b))
            self.flash_write(f"{addr:06X}", " ".join(str_24b))

    def write_backup(self):
        wname = filedialog.askopenfilename()
        bname = filedialog.asksaveasfilename(filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        bk_start = int(self.fls.v.flash_from.get(), 16)
        bk_end = int(self.fls.v.flash_to.get(), 16)

        fflash = open(wname, "r")
        addr0 = -1
        addr = 0
        str_24b = []
        for line in fflash:
            flist = line.strip().split()
            faddr = flist[0].lstrip("@")
            if addr0 < 0:
                addr = int(faddr, 16)
            elif addr0 + 16 != int(faddr, 16):
                if len(str_24b) > 0:
                    str_24b[len(str_24b):24] = ["FF"] * (24 - len(str_24b))
                    self.flash_write(f"{addr:06X}", " ".join(str_24b))
                str_24b = flist[1:]
                addr0 = int(faddr, 16)
                addr = addr0
                continue
            addr0 = int(faddr, 16)
            if len(str_24b) + len(flist) - 1 < 24:
                str_24b.extend(flist[1:])
                continue
            flist_cut = 25 - len(str_24b)
            str_24b.extend(flist[1:flist_cut])
            self.flash_write(f"{addr:06X}", " ".join(str_24b))
            str_24b = flist[flist_cut:]
            addr = addr + 24
        fflash.close()
        if len(str_24b) > 0:
            str_24b[len(str_24b):24] = ["FF"] * (24 - len(str_24b))
            self.flash_write(f"{addr:06X}", " ".join(str_24b))

        backup = open(bname, "w")
        for addr in range(bk_start, bk_end, 16):
            addr_str = f"{addr:06X}"
            backup.write("@" + addr_str + " ")
            self.write_addr(addr_str)
            self.write_1_byte("9536", "81")  # Read 16byte
            self.write_1_byte("9536", "00")  # Wait
            read_list = self.read_data(16)
            if len(read_list) == 1:
                messagebox.showerror("ERROR", "Error")
                break
            backup.write(" ".join([f"{ord(x):02X}" for x in read_list]))
            backup.write("\n")
        backup.close()