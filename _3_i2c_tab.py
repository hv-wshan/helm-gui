from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText as tkst
from ctypes import *
import time


class I2CTab:
    def __init__(self, parent):
        self.p = parent
        self.gui = self.p.gui
        self.reg = self.p.reg
        self.i2c = self.p.i2c
        self.eep = self.p.eep
        self.tst = self.p.tst
        self.spl = self.p.spl
        self.mer = self.p.mer
        self.adr = self.p.adr
        self.reg_tab = self.p.reg_tab

        self.helper = cdll.LoadLibrary("C:/Windows/System32/sub20.dll")
        self.hdev = self.helper.sub_open(0)  # first SUB-20 device handle

        sub_i2c_freq = self.helper.sub_i2c_freq
        sub_i2c_freq.argtypes = [c_int, c_char_p]
        i2c_freq = create_string_buffer(100)
        i2c_freq.value = b"\xa0\x86\x01"  # 100kHz setting
        sub_i2c_freq(self.hdev, i2c_freq)

        i2c_frm = ttk.Frame(self.p.i2c_frm)
        i2c_frm.pack(fill=BOTH, expand=YES)
        frm0 = ttk.Frame(i2c_frm)
        frm1 = ttk.Frame(i2c_frm)
        frm0.place(relx=0.07, rely=0.1, relwidth=0.5, relheight=0.9)
        frm1.place(relx=0.57, rely=0.1, relwidth=0.43, relheight=0.9)

        ttk.Label(frm0, text="I\u00b2C Slave Address (hex) ").grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky=NE)
        ttk.Entry(frm0, textvariable=self.i2c.v.slave_addr, width=2).grid(row=0, column=2, pady=(0, 5), sticky=NW)
        ttk.Label(frm0, text="I\u00b2C Access Address (hex, 2-byte) ").grid(row=1, column=0, columnspan=2, pady=(0, 30), sticky=NE)
        ttk.Entry(frm0, textvariable=self.i2c.v.access_addr, width=5).grid(row=1, column=2, pady=(0, 5), sticky=NW)
        ttk.Label(frm0, text="I\u00b2C Access Data").grid(row=2, column=0, columnspan=3, padx=(0, 50), pady=(0, 5), sticky=N)
        ttk.Button(frm0, text="Write", command=self.write).grid(row=3, column=0, padx=(0, 5), pady=(0, 10), sticky=NE)
        ttk.Entry(frm0, textvariable=self.i2c.v.write, width=30).grid(row=3, column=1, columnspan=2, pady=(0, 10), sticky=W)
        ttk.Label(frm0, text="# of Reading Bytes (dec) ").grid(row=4, column=0, pady=(0, 5), sticky=NE)
        ttk.Entry(frm0, textvariable=self.i2c.v.read_num, width=2).grid(row=4, column=1, pady=(0, 5), sticky=NW)
        ttk.Button(frm0, text="Read", command=self.read).grid(row=5, column=0, padx=(0, 5), sticky=NE)
        self.tkst_read = tkst(frm0, width=30, height=12)
        self.tkst_read.grid(row=5, column=1, columnspan=2, sticky=NW)
        self.tkst_read.insert(END, "-")
        self.tkst_read.configure(state=DISABLED)

        ttk.Button(frm1, text="Write Secret Key to Open I\u00b2C I/F", width=28, command=self.write_secret_key).grid(row=1, column=0, columnspan=2, padx=(20, 15), pady=(15, 0), ipady=3, sticky=N)
        ttk.Button(frm1, text="Write All Modified Register Values", width=28, command=self.write_mod_reg).grid(row=2, column=0, columnspan=2, padx=(20, 15), pady=(15, 0), ipady=3, sticky=N)
        ttk.Button(frm1, text="Write Update-Key to T-CON", width=28, command=self.write_tcon_update).grid(row=3, column=0, columnspan=2, padx=(20, 15), pady=(15, 0), ipady=3, sticky=N)
        ttk.Button(frm1, text="Resume Main FSM", width=28, command=self.write_resume_fsm).grid(row=4, column=0, columnspan=2, padx=(20, 15), pady=(15, 0), ipady=3, sticky=N)
        ttk.Button(frm1, text="Generate Simulation Command\nin Verilog Format", width=28, style="Center.TButton", state=DISABLED).grid(row=5, column=0, columnspan=2, padx=(20, 15), pady=(15, 0), ipadx=3, ipady=3, sticky=N)
        ttk.Label(frm1, text="Write Registers").grid(row=6, column=0, pady=(50, 0), sticky=NW)
        ttk.Button(frm1, text="ALL", width=14).grid(row=7, column=0, pady=(15, 0), sticky=N)
        ttk.Label(frm1, text="Read Registers").grid(row=6, column=1, padx=(50, 0), pady=(50, 0), sticky=NW)
        ttk.Button(frm1, text="ALL", width=14, command=self.read_all_reg).grid(row=7, column=1, padx=(50, 0), pady=(15, 0), sticky=N)
        ttk.Button(frm1, text="All Rewritable", width=14, command=self.read_all_wonly_reg).grid(row=8, column=1, padx=(50, 0), pady=(15, 0), sticky=N)
        ttk.Button(frm1, text="Mod by EEPROM", width=14, command=self.read_all_eep_mod_reg).grid(row=9, column=1, padx=(50, 0), pady=(15, 0), sticky=N)

    # SUB-20
    def sub20_i2c_read(self, slv_addr, mem_addr, data_num):
        """
        READ i2c
        slv_addr : Slave address (7-bit integer)
        mem_addr : Memory address (2-Byte integer)
        data_num : number of READing bytes (integer)
        """
        dr = create_string_buffer(data_num)
        sub_errno = self.helper.sub_i2c_read(self.hdev, slv_addr, mem_addr, 2, dr, data_num)
        read_str = " ".join([f"{ord(x):02X}" for x in dr]).strip()
        result_txt = "Slave = " + f"{slv_addr:02X}" + ", Memory address = " + f"{mem_addr:04X}" + ", Data = " + read_str
        if self.gui.v.i2c_bool.get():
            print(result_txt)
        if self.gui.v.log_bool.get():
            if sub_errno != 0:
                logfile = open(self.gui.v.logfilename.get(), "a")
                logfile.write("RF: " + result_txt + "\n")
                logfile.close()
            else:
                logfile = open(self.gui.v.logfilename.get(), "a")
                logfile.write("R: " + result_txt + "\n")
                logfile.close()
        if sub_errno != 0:
            return sub_errno, ""
        else:
            return dr, result_txt

    def sub20_i2c_write(self, slv_addr, mem_addr, byte_list):
        """
        Write i2c
        slv_addr : Slave address (7-bit integer)
        mem_addr : Memory address (2-Byte integer)
        byte_list: Write data (list of 1-Byte integer)
        """
        data_num = len(byte_list)
        sub_errno = self.helper.sub_i2c_write(self.hdev, slv_addr, mem_addr, 2, byte_list, data_num)
        write_str = " ".join([f"{ord(x):02X}" for x in byte_list]).strip()
        result_txt = "Slave = " + f"{slv_addr:02X}" + ", Memory address = " + f"{mem_addr:04X}" + ", Data = " + write_str
        if self.gui.v.i2c_bool.get():
            print(result_txt)
        if self.gui.v.log_bool.get():
            if sub_errno != 0:
                logfile = open(self.gui.v.logfilename.get(), "a")
                logfile.write("WF: " + result_txt + "\n")
                logfile.close()
            else:
                logfile = open(self.gui.v.logfilename.get(), "a")
                logfile.write("W: " + result_txt + "\n")
                logfile.close()
        return sub_errno, result_txt

    def sub20_i2c_direct_read(self, slv_addr, data_num):
        """
        READ i2c
        slv_addr : Slave address (7-bit integer)
        data_num : number of READing bytes (integer)
        """
        dr = create_string_buffer(data_num)
        sub_errno = self.helper.sub_i2c_read(self.hdev, slv_addr, 0, 0, dr, data_num)
        read_str = " ".join([f"{ord(x):02X}" for x in dr]).strip()
        result_txt = "Slave = " + f"{slv_addr:02X}" + ", Data = " + read_str
        if self.gui.v.i2c_bool.get():
            print(result_txt)
        if self.gui.v.log_bool.get():
            if sub_errno != 0:
                logfile = open(self.gui.v.logfilename.get(), "a")
                logfile.write("RF: " + result_txt + "\n")
                logfile.close()
            else:
                logfile = open(self.gui.v.logfilename.get(), "a")
                logfile.write("R: " + result_txt + "\n")
                logfile.close()
        if sub_errno != 0:
            return sub_errno, ""
        else:
            return dr, result_txt

    def sub20_i2c_direct_write(self, slv_addr, byte_list):
        """
        Write i2c
        slv_addr : Slave address (7-bit integer)
        byte_list: Write data (list of 1-Byte integer)
        """
        data_num = len(byte_list)
        sub_errno = self.helper.sub_i2c_write(self.hdev, slv_addr, 0, 0, byte_list, data_num)
        write_str = " ".join([f"{ord(x):02X}" for x in byte_list]).strip()
        result_txt = "Slave = " + f"{slv_addr:02X}" + ", Data = " + write_str
        if self.gui.v.i2c_bool.get():
            print(result_txt)
        if self.gui.v.log_bool.get():
            if sub_errno != 0:
                logfile = open(self.gui.v.logfilename.get(), "a")
                logfile.write("WF: " + result_txt + "\n")
                logfile.close()
            else:
                logfile = open(self.gui.v.logfilename.get(), "a")
                logfile.write("W: " + result_txt + "\n")
                logfile.close()
        return sub_errno, result_txt

    def sub20_i2c_busy(self, slv_addr, mem_addr):
        """
        Check busy for i2c write
        slv_addr : Slave address (7-bit integer)
        mem_addr : Memory address (2-Byte integer)
        """
        byte_list = create_string_buffer(1)
        byte_list[0:1] = bytearray().fromhex("00")
        sub_errno = self.helper.sub_i2c_write(self.hdev, slv_addr, mem_addr, 2, byte_list, 1)
        return sub_errno

    # I2C Read/Write Functions
    def write_byte_list(self, write_list):
        err_list = []
        for (mem_addr, write_str) in write_list:
            n = len(write_str.split())
            byte_list = create_string_buffer(n)
            byte_list[0:n] = bytearray().fromhex(write_str)
            sub_errno, result = self.sub20_i2c_write(int(self.i2c.i2c_slave_addr.get(), 16), mem_addr, byte_list)
            if sub_errno != 0:
                err_list.append(result)
            time.sleep(0.1)

        if len(err_list) > 0:
            messagebox.showerror("I\u00b2C Write Result", "Write Modified Registers Failed!\n" + "\n".join(err_list))

    def bytes_read(self, slv_addr, mem_addr, read_num):
        read_list, result = self.sub20_i2c_read(slv_addr, mem_addr, read_num)
        time.sleep(0.1)
        try:
            len(read_list)
        except TypeError:
            messagebox.showerror("I\u00b2C Read Result", "Read Failed!\n" + result)
        return read_list

    def write_reg(self, pages, cnt):
        err_pg = []
        for page in pages:
            try:
                pg = page
                idx = self.spl.l.pages_unique.index(pg)
            except ValueError:
                try:
                    pg = int(page)
                    idx = self.spl.l.pages_unique.index(pg)
                except ValueError:
                    err_pg.append(page)
                    continue

            if self.tst.l.pg_not_used[idx]:
                continue

            n = cnt[idx] + 1
            write_list = ["XX"] * n
            for i in range(n):
                write_list[i] = [lambda: self.adr.l.hexa_per_pg_mod[idx][i], lambda: "00"][self.adr.l.hexa_per_pg_mod[idx][i] == "-"]()
            byte_list = create_string_buffer(n)
            byte_list[0:n] = bytearray().fromhex(" ".join(write_list))
            sub_errno, result = self.sub20_i2c_write(int(self.i2c.i2c_slave_addr.get(), 16), page * 256, byte_list)
            time.sleep(0.1)

        if len(err_pg) > 0:
            if len(err_pg) == 1:
                messagebox.showwarning("PAGE ERROR", "Following Page Does Not Exist:\n" + err_pg[0])
            else:
                messagebox.showwarning("PAGE ERROR", "Following Pages Do Not Exist:\n" + ", ".join(err_pg))

    def read_reg(self, pages, cnt, check_used):
        err_pg = []
        for page in pages:
            try:
                pg = page
                idx = self.spl.l.pages_unique.index(pg)
            except ValueError:
                try:
                    pg = int(page)
                    idx = self.spl.l.pages_unique.index(pg)
                except ValueError:
                    err_pg.append(page)
                    continue

            if (check_used & self.tst.l.pg_not_used[idx]) | (cnt[idx] < 0):
                continue

            read_bytes = self.bytes_read(int(self.i2c.i2c_slave_addr.get(), 16), pg * 256, cnt[idx] + 1)

            try:
                len(read_bytes)
            except TypeError:
                continue

            for num in range(cnt[idx] + 1):
                new_bin = f"{int.from_bytes(read_bytes[num], byteorder='big', signed=False):08b}"
                old_bin = f"{int([[lambda: x, lambda: '00'][x == '-']() for x in self.adr.l.hexa_per_pg_mod[idx]][num], 16):08b}"
                if new_bin != old_bin:
                    self.reg_tab.modify1(str(pg) + " " + self.adr.num_range[idx][num // 16], str(pg), num, f"{int(new_bin, 2):02X}")

        if len(err_pg) > 0:
            if len(err_pg) == 1:
                messagebox.showwarning("PAGE ERROR", "Following Page Does Not Exist:\n" + err_pg[0])
            else:
                messagebox.showwarning("PAGE ERROR", "Following Pages Do Not Exist:\n" + ", ".join(err_pg))

    def read_one_name(self, name, modify=False):
        if name not in self.spl.l.names_wo_width:
            messagebox.showwarning("WARNING", "Must Add Excel")
            return ""

        bin = self.mer.l.bina_mod[self.mer.l.names.index(name)]
        for (i, item) in list(enumerate(self.spl.l.names_wo_width)):
            if name == item:
                pg, num = [int(x) for x in self.spl.l.addr_total[i].split("(")[0].split("-")]
                addr_dec = int(f"{pg:02X}" + f"{num:02X}", 16)
                read_byte = self.bytes_read(int(self.i2c.v.slave_addr.get(), 16), addr_dec, 1)
                try:
                    len(read_byte)
                except TypeError:
                    messagebox.showerror("ERROR", "I\u00b2C Read Error")
                    return ""
                else:
                    read_bin = f"{int.from_bytes(read_byte, byteorder='big', signed=False):08b}"

                width = self.spl.l.widths[i]
                if width == "-":
                    width_l, width_r = None, 0
                elif ":" in width:
                    width_l, width_r = [int(x) for x in width.split(":")]
                else:
                    width_l, width_r = None, int(width)

                bits = self.spl.l.addr_bits[i]
                if ":" in bits:
                    bit_l, bit_r = [int(x) for x in bits.split(":")]
                    bin_part = read_bin[8 - bit_l - 1:8 - bit_r]
                else:
                    bit_l, bit_r = None, int(bits)
                    bin_part = read_bin[8 - bit_r - 1]

                bin = self.p.replace_text(width_r, width_l, bin_part, bin)

        if modify:
            self.p.set_val_by_name(name, "#2", bin)

        return bin

    def read_one_addr(self, addr, modify=False):
        pg, num = [int(x) for x in addr.split("-")]
        pg_idx = self.spl.pages_unique.index(pg)
        addr_dec = int(f"{pg:02X}" + f"{num:02X}", 16)
        read_byte = self.bytes_read(int(self.i2c.v.slave_addr.get(), 16), addr_dec, 1)
        try:
            len(read_byte)
        except TypeError:
            messagebox.showerror("ERROR", "I\u00b2C Read Error")
            return []
        else:
            read_bin = f"{int.from_bytes(read_byte, byteorder='big', signed=False):08b}"

        if modify:
            self.reg_tab.modify1(str(pg) + " " + self.adr.num_range[pg_idx][num // 16], str(pg), num, f"{read_bin:02X}")

        return read_bin

    # Button Functions
    def write(self):
        write_str = self.i2c.v.write.get()
        n = len(write_str.split())
        byte_list = create_string_buffer(n)
        byte_list[0:n] = bytearray().fromhex(write_str)
        sub_errno, result = self.sub20_i2c_write(int(self.i2c.i2c_slave_addr.get(), 16), int("".join(self.i2c.i2c_access_addr.get().split()), 16), byte_list)
        time.sleep(0.1)
        if sub_errno != 0:
            messagebox.showinfo("I\u00b2C Write Result", "Write Failed!\n" + result)
        self.p.tkst_write(self.tkst_read, delete=True)
        self.p.tkst_write(self.tkst_read, text="-")

    def read(self):
        self.p.tkst_write(self.tkst_read, delete=True)
        read_list = self.bytes_read(int(self.i2c.i2c_slave_addr.get(), 16), int("".join(self.i2c.i2c_access_addr.get().split()), 16), int(self.i2c.v.read_num.get()))
        try:
            len(read_list)
        except TypeError:
            self.p.tkst_write(self.tkst_read, text="ERROR")
        else:
            read_str = " ".join([f"{ord(x):02X}" for x in read_list])
            self.p.tkst_write(self.tkst_read, text=read_str)

    def write_secret_key(self):
        key_write_list = [
                (19284, "DD CC BB AA"),		# 4B 54
                (19334, "DD CC BB AA"),		# 4B 86
                (18944, "01 4A EC 16")		# 4A 00 - FSM
                ]
        self.write_byte_list(key_write_list)

    def write_mod_reg(self):
        if len(self.reg.l.modified_pg) == 0:
            return

        write_list = []
        for (pg_idx, pg) in self.spl.pages_unique:
            for (num, hex) in self.adr.l.hexa_per_pg_mod[pg_idx]:
                if hex != self.adr.l.hexa_per_pg[num]:
                    write_list.append((int(f"{pg:02X}" + f"{num:02X}", 16), hex.upper().zfill(2)))

        self.p.set_all_defaults()
        self.write_byte_list(write_list)

    def write_tcon_update(self):
        if len(self.spl.names_wo_width) == 0:
            messagebox.showerror("ERROR", "Must Import Excel")
            return
        if "UPDATE_KEY" not in self.spl.names_wo_width:
            messagebox.showwarning("WARNING", "Must Add Excel")
            return

        self.write_mod_reg()
        self.p.set_val_by_name("UPDATE_KEY", "#4", "1")
        self.write_mod_reg()
        self.p.set_val_by_name("UPDATE_KEY", "#4", "0")
        self.p.set_all_defaults()

    def write_resume_fsm(self):
        if len(self.spl.names_wo_width) == 0:
            messagebox.showerror("ERROR", "Must Import Excel")
            return
        if "cfg_skip_state_i" not in self.spl.names_wo_width:
            messagebox.showwarning("WARNING", "Must Add Excel")
            return

        self.write_mod_reg()
        self.p.set_val_by_name("cfg_skip_state_i", "#4", "000400")
        self.write_mod_reg()

    def write_all_reg(self):
        if len(self.spl.l.pages_unique) == 0:
            messagebox.showerror("ERROR", "Must Import Excel")
            return

        self.write_reg(self.spl.l.pages_unique, self.tst.l.wo_cnt)
        messagebox.showinfo("Write Registers", "Complete")

    def read_all_reg(self):
        if len(self.spl.l.pages_unique) == 0:
            messagebox.showerror("ERROR", "Must Import Excel")
            return

        self.read_reg(self.spl.l.pages_unique, self.tst.l.rw_cnt, True)
        messagebox.showinfo("Read Registers", "Complete")

    def read_all_wonly_reg(self):
        if len(self.spl.l.pages_unique) == 0:
            messagebox.showerror("ERROR", "Must Import Excel")
            return

        self.read_reg(self.spl.l.pages_unique, self.tst.l.wo_cnt, True)
        messagebox.showinfo("Read Registers", "Complete")

    def read_all_eep_mod_reg(self):
        eep_pages = []
        new_bin = self.read_one_name("cfg_eeprom_total", modify=True)
        n = int(new_bin, 2)
        eep_addr = 0
        for i in range(n):
            read_list, result = self.sub20_i2c_read(int(self.eep.v.slave_addr, 16), eep_addr, 2)
            time.sleep(0.1)
            try:
                len(read_list)
            except TypeError:
                messagebox.showinfo("I\u00b2C Read Result", "Read Failed\n" + result)
                return

            eep_pages.append(ord(read_list[0]))
            pg_len = ord(read_list[1])
            eep_addr += pg_len + 4

        self.read_reg(eep_pages, self.tst.l.wo_cnt, False)