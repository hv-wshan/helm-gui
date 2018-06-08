from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from copy import deepcopy
from win32api import GetSystemMetrics

from _0_data import *
from _1_main_tab import *
from _2_register_tab import *
from _3_i2c_tab import *
from _4_eeprom_tab import *
from _5_test_tab import *
from _6_flash_tab import *
from _7_integrity_check import *


class HivicsGui:
    def __init__(self):
        self.root = Tk()
        self.gui = GUIData()
        self.main = MainTabData()
        self.reg = RegisterTabData()
        self.i2c = I2CTabData()
        self.eep = EEPROMTabData()
        self.tst = TestTabData()
        self.fls = FlashTabData()
        self.spl = SplitRegData()
        self.mer = MergedRegData()
        self.adr = AddressRegData()

        self.root.title("HivICs Helm controller GUI " + self.gui.v.version.get())
        self.root.tk.call("wm", "iconphoto", self.root._w, PhotoImage(data=self.gui.logo))
        self.detect_screen()

        style = ttk.Style()
        style.configure("Center.TButton", justify=CENTER)
        style.configure("Bigger.TButton", font=("TkDefaultFont", 10))

        t_frm = ttk.Frame(self.root)
        l_frm = ttk.Frame(self.root, padding=5)
        r_frm = ttk.Frame(self.root, padding=5)
        t_frm.place(relx=0, rely=0, relwidth=1, relheight=0.862)
        l_frm.place(relx=0, rely=0.862, relwidth=0.35, relheight=0.138)
        r_frm.place(relx=0.35, rely=0.862, relwidth=0.65, relheight=0.138)
        
        book = ttk.Notebook(t_frm)
        book.pack(fill=BOTH, expand=YES)

        self.main_frm = ttk.Frame(book)
        self.reg_frm = ttk.Frame(book)
        self.i2c_frm = ttk.Frame(book)
        self.eep_frm = ttk.Frame(book)
        self.test_frm = ttk.Frame(book)
        self.flash_frm = ttk.Frame(book)
        book.add(self.main_frm, text=" Main ")
        book.add(self.reg_frm, text=" Register ")
        book.add(self.i2c_frm, text=" I\u00b2C ")
        book.add(self.eep_frm, text=" EEPROM ")
        book.add(self.test_frm, text=" Test ")
        book.add(self.flash_frm, text=" Flash ")

        self.main_tab = MainTab(self)
        self.reg_tab = RegisterTab(self)
        self.i2c_tab = I2CTab(self)
        self.eep_tab = EEPROMTab(self)
        self.tst_tab = TestTab(self)
        self.fls_tab = FlashTab(self)

        ttk.Checkbutton(l_frm, text="Log On/Off", variable=self.gui.v.log_check, command=lambda type="log": self.tf_check(type)).grid(row=0, column=0, columnspan=3, padx=(2, 0), sticky=NW)
        ttk.Checkbutton(l_frm, text="Monitor I\u00b2C Transaction", variable=self.gui.v.i2c_check, command=lambda type="i2c": self.tf_check(type)).grid(row=1, column=0, columnspan=3, padx=(2, 0), sticky=NW)
        ttk.Checkbutton(l_frm, text="Monitor Register Transaction", variable=self.gui.v.reg_check, command=lambda type="reg": self.tf_check(type)).grid(row=2, column=0, columnspan=3, padx=(2, 0), sticky=NW)
        ttk.Button(l_frm, text="Add Excel File", width=15, command=self.add_xlsx).grid(row=3, column=0, padx=(2, 0), pady=(2, 0), sticky=NW)
        ttk.Button(l_frm, text="Remove All Excel", width=15, command=self.remove_xlsx, state=DISABLED).grid(row=3, column=1, padx=(3, 0), pady=(2, 0), sticky=NW)
        ttk.Button(l_frm, text="Set All Defaults", width=15, command=self.set_all_defaults).grid(row=3, column=2, padx=(3, 0), pady=(2, 0), sticky=NW)
        ttk.Button(l_frm, text="Launch Data Integrity Check", width=31, command=self.launch).grid(row=4, column=0, columnspan=2, padx=(2, 0), pady=(2, 0), ipadx=3, sticky=NW)
        ttk.Button(l_frm, text="Reset GUI", width=15, command=self.reset_gui).grid(row=4, column=2, padx=(3, 0), pady=(2, 0), sticky=NW)
        ttk.Label(r_frm, textvariable=self.reg.v.xlsx_names, justify=RIGHT).pack(side=TOP, anchor=E)

        #self.save_log()

    def detect_screen(self):
        w = GetSystemMetrics(0)
        h = GetSystemMetrics(1)

        if (w < 1050) | (h < 950):
            self.root.geometry("720x650")
            self.root.tk.call('tk', 'scaling', 1)
            self.gui.v.pad.set(0)
        else:
            self.root.geometry("1050x950")
            self.gui.v.pad.set(10)

    # Button Functions
    def tf_check(self, type):
        if type.lower() == "log":
            if self.gui.v.log_check.get() == 0:
                self.gui.v.log_bool.set(False)
            elif self.gui.v.log_check.get() == 1:
                self.gui.v.log_bool.set(True)
                if self.gui.v.logfilename.get() == "":
                    self.save_log()
        elif type.lower() == "i2c":
            if self.gui.v.i2c_check.get() == 0:
                self.gui.v.i2c_bool.set(False)
            elif self.gui.v.i2c_check.get() == 1:
                self.gui.v.i2c_bool.set(True)
        elif type.lower() == "reg":
            if self.gui.v.reg_check.get() == 0:
                self.gui.v.reg_bool.set(False)
            elif self.gui.v.reg_check.get() == 1:
                self.gui.v.reg_bool.set(True)

    def save_log(self):
        self.gui.v.logfilename.set(filedialog.asksaveasfilename(filetypes=(("Log Files", "*.log"), ("Text Files", "*.txt"), ("All Files", "*.*"))))
        if self.gui.v.logfilename.get() == "":
            self.gui.v.log_bool.set(False)
        else:
            if not self.gui.v.logfilename.get().lower().endswith(".log"):
                self.gui.v.logfilename.set(self.gui.v.logfilename.get() + ".log")
            self.gui.v.log_bool.set(True)
            self.gui.v.log_check.set(1)
            logfile = open(self.gui.v.logfilename.get(), "w")
            logfile.write("")
            logfile.close()

    def add_xlsx(self):
        if self.reg_tab.reg_add_xlsx():
            self.reg_tab.reg_add_treeview()
            self.tst_tab.regfile_summary_lists()
            self.tst_tab.summ_add_treeview()
            if "GPIO" in self.spl.l.groups_unique:
                self.tst_tab.test_gpio_tab.gpio_load()
                self.tst_tab.test_gpio_tab.set_defaults()
            if "EDID" in self.spl.l.groups_unique:
                self.eep_tab.ed_add_treeview()
                self.eep_tab.ed_load()
                self.eep_tab.set_defaults()

    def remove_xlsx(self):
        return

    def set_all_defaults(self):
        if len(self.reg_tab.name_tree.get_children()) == 0:
            messagebox.showwarning("WARNING", "Must Import EEPROM")
            return

        self.spl.l.bina = self.spl.l.bina_mod.copy()
        self.spl.l.deci = self.spl.l.deci_mod.copy()
        self.spl.l.hexa = self.spl.l.hexa_mod.copy()
        self.mer.l.bina = self.mer.l.bina_mod.copy()
        self.mer.l.deci = self.mer.l.deci_mod.copy()
        self.mer.l.hexa = self.mer.l.hexa_mod.copy()
        self.adr.l.bina = self.adr.l.bina_mod.copy()
        self.adr.l.hexa = self.adr.l.hexa_mod.copy()
        self.adr.l.hexa_per_pg = deepcopy(self.adr.l.hexa_per_pg_mod)

        self.reg_tab.reset_reg()
        self.eep_tab.reset_ed()

    def reset_gui(self):
        self.spl.l.bina = self.spl.l.bina_default.copy()
        self.spl.l.deci = self.spl.l.deci_default.copy()
        self.spl.l.hexa = self.spl.l.hexa_default.copy()
        self.mer.l.bina = self.mer.l.bina_default.copy()
        self.mer.l.deci = self.mer.l.deci_default.copy()
        self.mer.l.hexa = self.mer.l.hexa_default.copy()
        self.adr.l.bina = self.adr.l.bina_default.copy()
        self.adr.l.hexa = self.adr.l.hexa_default.copy()
        self.adr.l.hexa_per_pg = deepcopy(self.adr.l.hexa_per_pg_default)

        if len(self.reg_tab.name_tree.get_children()) != 0:
            self.reg_tab.reset_reg()
        if len(self.eep_tab.ed_name_tree.get_children()) != 0:
            self.eep_tab.reset_ed()
        self.eep_tab.reset_eep()

        self.reg_tab.name_tree.selection_clear()
        self.reg_tab.addr_tree.selection_clear()
        self.reg_tab.hid0_tree.selection_clear()
        self.reg_tab.hid1_tree.selection_clear()
        self.reg_tab.name_tree.yview_moveto(0)
        self.reg_tab.addr_tree.yview_moveto(0)
        self.reg_tab.hid0_tree.yview_moveto(0)
        self.reg_tab.hid1_tree.yview_moveto(0)
        self.reg_tab.search_entry.delete(0, END)

        self.reg.v.check0.set(0)
        self.reg.v.check1.set(0)
        self.reg_tab.reg_note.hide(self.reg_tab.hid0_frm)
        self.reg_tab.reg_note.hide(self.reg_tab.hid1_frm)
        self.eep.v.ed_check0.set(0)
        self.eep.v.ed_check1.set(0)
        self.eep_tab.edid_note.hide(self.eep_tab.ed_hid0)
        self.eep_tab.edid_note.hide(self.eep_tab.ed_hid1)

        for grp_iid in self.reg_tab.spl.groups_unique:
            if grp_iid != "EDID":
                self.reg_tab.name_tree.item(grp_iid, open=False)
                self.reg_tab.hid0_tree.item(grp_iid + "-split", open=False)
                self.reg_tab.name_tree.selection_remove(grp_iid)
                self.reg_tab.hid0_tree.selection_remove(grp_iid + "-split")
        for pg_iid in self.reg_tab.spl.pages_unique:
            if pg_iid != 237:
                self.reg_tab.addr_tree.item(str(pg_iid), open=False)
                self.reg_tab.hid1_tree.item(str(pg_iid), open=False)
                self.reg_tab.addr_tree.selection_remove(pg_iid)
                self.reg_tab.hid1_tree.selection_remove(pg_iid)

        self.tst_tab.regfile_summary_lists()
        self.tst_tab.summ_add_treeview()
        if "GPIO" in self.spl.l.groups_unique:
            self.tst_tab.test_gpio_tab.gpio_load()
            self.tst_tab.test_gpio_tab.set_defaults()
        if "EDID" in self.spl.l.groups_unique:
            self.eep_tab.ed_add_treeview()
            self.eep_tab.ed_load()
            self.eep_tab.set_defaults()

        for slave in self.eep_tab.idx_frm.grid_slaves():
            slave.destroy()
        for slave in self.eep_tab.file_frm.grid_slaves():
            slave.destroy()

        self.gui.v.logfilename.set("")
        self.gui.v.log_bool.set(False)
        self.gui.v.i2c_bool.set(False)
        self.gui.v.reg_bool.set(False)
        self.gui.v.log_check.set(0)
        self.gui.v.i2c_check.set(0)
        self.gui.v.reg_check.set(0)
        self.main.v.hres.set("")
        self.main.v.hblank.set("")
        self.main.v.hb_fp.set("")
        self.main.v.hb_bp.set("")
        self.main.v.vres.set("")
        self.main.v.vblank.set("")
        self.main.v.vb_fp.set("")
        self.main.v.vb_bp.set("")
        self.main.v.dic_no.set("4")
        self.main.v.dic_ch.set("960")
        self.main.v.dic_ofs.set("")
        [self.main.v.dic_lane[x].set("") for x in range(6)]
        [self.main.v.freq[x].set("") for x in range(7)]
        [self.main.v.mlt[x].set("") for x in range(3)]
        [self.main.v.div[x].set("") for x in range(14)]
        self.reg.v.search.set("")
        self.reg.v.curr_row.set("")
        self.i2c.v.slave_addr.set("54")
        self.i2c.v.access_addr.set("80 00")
        self.i2c.v.write.set("00")
        self.i2c.v.read_num.set("1")
        self.eep.v.slave_addr.set("51")
        self.eep.v.access_addr.set("00 00")
        self.eep.v.write.set("")
        self.eep.v.read_num.set("1")
        self.eep.v.pg_id.set("")
        self.eep.v.pg_len.set("")
        self.eep.v.crc_read.set("")
        self.eep.v.crc_sum.set("")
        self.eep.v.crc_ofs.set("FE")
        self.eep.v.next_pg.set("")
        self.eep.v.write_1.set("")
        self.eep.v.write_list.set("")
        self.eep.v.check_mod.set("")
        self.eep.v.pri_main.set("4A")
        self.eep.v.pri_core.set("ED 49 96 80 95")
        self.eep.v.pri_base.set("40 41 42 84 82 98 99 9A")
        self.eep.v.import_rom.set("")
        self.eep.v.conc.set("")
        self.eep.v.txt_main.set("")
        self.eep.v.txt_core.set("")
        self.eep.v.txt_base.set("")
        [self.eep.v.txtfile[x].set("") for x in range(2)]
        self.eep.v.sub20_pages.set("")
        self.eep.v.sub20_pg_num.set("")
        self.eep.v.sub20_total_len.set("")
        self.eep.v.check.set(0)
        self.eep.d.eep_imp_pg = {}
        self.eep.l.imported_txt = []
        self.eep.l.mod_by_eep_pg = []
        [self.tst.v.psm_var[x][y].set("") for x in range(5) for y in range(3)]
        self.tst.v.psm_var[5].set("")
        [self.tst.v.pss_var[x].set("") for x in range(5)]
        self.fls.v.flash_addr.set("")
        self.fls.v.w_24.set("")
        self.fls.v.r_24.set("")
        self.fls.v.flash_from.set("")
        self.fls.v.flash_to.set("")

        self.tkst_write(self.i2c_tab.tkst_read, delete=True)
        self.tkst_write(self.i2c_tab.tkst_read, text="-")

        messagebox.showinfo("RESET", "Complete")

    def launch(self):
        launch = FileCheck()

    # Globally Used Functions
    def get_val_by_name(self, name, col):
        iid = str(self.mer.l.names.index(name))
        if self.reg_tab.name_tree.exists(iid):
            return self.reg_tab.name_tree.set(iid, column=col)
        elif self.eep_tab.ed_name_tree.exists(iid):
            return self.eep_tab.ed_name_tree.set(iid, column=col)
        else:
            raise ValueError("Register Name Does Not Exist")

    def set_val_by_name(self, name, col, new, tag="modified"):
        row = str(self.mer.l.names.index(name))
        if self.reg_tab.name_tree.exists(row):
            val = self.reg_tab.name_tree.item(row, "value")
            self.reg_tab.modify0(col, row, name, val, new, mod_tag=tag)
        elif self.eep_tab.ed_name_tree.exists(row):
            val = self.eep_tab.ed_name_tree.item(row, "value")
            self.eep_tab.ed_modify0(col, row, name, val, new, mod_tag=tag)
        else:
            raise ValueError("Register Address Does Not Exist")

    def check_mod(self):
        self.eep.v.check_mod.set(" ".join([f"{int(pg):02x}".upper() for pg in sorted(self.reg.l.modified_pg, key=int)]))

    def imp_reg(self):
        try:
            txtfilename = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
            txt = open(txtfilename, "r")
            text = txt.readlines()
            txt.close()
        except FileNotFoundError:
            return

        format_err = []
        data_err0 = []
        data_err1 = []
        data_err2 = []
        for (i, line) in list(enumerate(map(str.strip, text), 1)):
            items = line.split(", ")

            if len(items) != 4:
                format_err.append((i, line))
                continue
            if items[0] not in self.spl.l.groups_unique:
                data_err0.append((i, items[0]))
                continue
            if items[1] not in self.spl.l.names_wo_width:
                data_err1.append((i, items[1]))
                continue
            if re.compile(r"[^0-9a-fA-F]").search(items[2]) is not None:
                data_err2.append((i, items[2]))
                continue
            if re.compile(r"[^0-9a-fA-F]").search(items[3]) is not None:
                data_err2.append((i, items[3]))
                continue

            if items[0] == "EDID":
                col = "#4"
                row = str(self.mer.l.names.index(items[1]))
                name = items[1]
                val = self.eep_tab.ed_name_tree.item(row, "value")
                new = items[3]
                self.eep_tab.ed_modify0(col, row, name, val, new)
            else:
                col = "#4"
                row = str(self.mer.l.names.index(items[1]))
                name = items[1]
                val = self.reg_tab.name_tree.item(row, "value")
                new = items[3]
                self.reg_tab.modify0(col, row, name, val, new)

        if len(format_err) > 0:
            err_str = ""
            for (i, line) in format_err:
                err_str += "Line " + str(i) + ": " + line + "\n"
            messagebox.showerror("IMPORT FORMAT ERROR", txtfilename + "\n" + "Wrong Import Format\n" + err_str[:-1])
        if len(data_err0) > 0:
            err_str = ""
            for (i, item) in data_err0:
                err_str += "Line " + str(i) + ": " + item + "\n"
            messagebox.showerror("IMPORT DATA ERROR", txtfilename + "\n" + "Nonexistent Group Name\n" + err_str[:-1])
        if len(data_err1) > 0:
            err_str = ""
            for (i, item) in data_err1:
                err_str += "Line " + str(i) + ": " + item + "\n"
            messagebox.showerror("IMPORT DATA ERROR", txtfilename + "\n" + "Nonexistent Register Name\n" + err_str[:-1])
        if len(data_err2) > 0:
            err_str = ""
            for (i, item) in data_err2:
                err_str += "Line " + str(i) + ": " + item + "\n"
            messagebox.showerror("IMPORT DATA ERROR", txtfilename + "\n" + "Invalid Hexadecimal Value\n" + err_str[:-1])

        if len(format_err + data_err0 + data_err1 + data_err2) > 0:
            print("Import Modified Register List Error: " + ", ".join(["Line " + str(x[0]) for x in format_err + data_err0 + data_err1 + data_err2]))

    def exp_reg(self):
        if len(self.reg_tab.hid1_tree.tag_has("modified") + self.reg_tab.hid1_tree.tag_has("eeprom") + self.reg_tab.hid1_tree.tag_has("gpio") +
               self.eep_tab.ed_hid1_tree.tag_has("modified") + self.eep_tab.ed_hid1_tree.tag_has("eeprom") + self.eep_tab.ed_hid1_tree.tag_has("edid")) == 0:
            messagebox.showinfo("EXPORT MODIFIED REGISTER LIST", "No Modified Register List")
            return

        txtfilename = filedialog.asksaveasfilename(filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if not txtfilename.lower().endswith(".txt"):
            txtfilename += ".txt"
        txt = open(txtfilename, "w")

        for iid in self.reg_tab.name_tree.tag_has("modified") + self.reg_tab.name_tree.tag_has("eeprom") + self.reg_tab.name_tree.tag_has("gpio"):
            if iid in self.spl.l.groups_unique:
                continue
            txt.write(self.spl.l.groups[int(iid)] + ", " + self.spl.l.names_wo_width[int(iid)] + ", " + self.mer.l.hexa[int(iid)] + ", " + self.mer.l.hexa_mod[int(iid)] + "\n")
        for iid in self.eep_tab.ed_name_tree.tag_has("modified") + self.eep_tab.ed_name_tree.tag_has("eeprom") + self.eep_tab.ed_name_tree.tag_has("edid"):
            txt.write(self.spl.l.groups[int(iid)] + ", " + self.spl.l.names_wo_width[int(iid)] + ", " + self.mer.l.hexa[int(iid)] + ", " + self.mer.l.hexa_mod[int(iid)] + "\n")

        txt.close()

    def imp_byte(self):
        try:
            txtfilename = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
            txt = open(txtfilename, "r")
            text = txt.readlines()
            txt.close()
        except FileNotFoundError:
            return

        format_err = []
        data_err0 = []
        data_err1 = []
        for (i, line) in list(enumerate(map(str.strip, text), 1)):
            items = line.split(", ")

            if len(items) != 3:
                format_err.append((i, line))
                continue

            pg_hex = items[0].split("-")[0]
            pg_dec = int(pg_hex, 16)
            pg_idx = self.spl.l.pages_unique.index(pg_dec)
            n = items[0].split("-")[1]

            if str(pg_dec) + "-" + n not in [x.split("(")[0] for x in self.spl.l.addr_total]:
                data_err0.append((i, items[0]))
                continue
            if re.compile(r"[^0-9a-fA-F]").search(items[1]) is not None:
                data_err1.append((i, items[1]))
                continue
            if re.compile(r"[^0-9a-fA-F]").search(items[2]) is not None:
                data_err1.append((i, items[2]))
                continue

            if pg_hex.upper() == "ED":
                row = "237 " + self.adr.l.num_range[pg_idx][int(n) // 16]
                pg = "237"
                num = int(n)
                new = items[2]
                self.eep_tab.ed_modify1(row, pg, num, new)
            else:
                row = str(pg_dec) + " " + self.adr.l.num_range[pg_idx][int(n) // 16]
                pg = str(pg_dec)
                num = int(n)
                new = items[2]
                self.reg_tab.modify1(row, pg, num, new)

        if len(format_err) > 0:
            err_str = ""
            for (i, line) in format_err:
                err_str += "Line " + str(i) + ": " + line + "\n"
            messagebox.showerror("IMPORT FORMAT ERROR", txtfilename + "\n" + "Wrong Import Format\n" + err_str[:-1])
        if len(data_err0) > 0:
            err_str = ""
            for (i, item) in data_err0:
                err_str += "Line " + str(i) + ": " + item + "\n"
            messagebox.showerror("IMPORT DATA ERROR", txtfilename + "\n" + "Nonexistent Address\n" + err_str[:-1])
        if len(data_err1) > 0:
            err_str = ""
            for (i, item) in data_err1:
                err_str += "Line " + str(i) + ": " + item + "\n"
            messagebox.showerror("IMPORT DATA ERROR", txtfilename + "\n" + "Invalid Hexadecimal Value\n" + err_str[:-1])

        if len(format_err + data_err0 + data_err1) > 0:
            print("Import Modified Byte List Error: " + ", ".join(["Line " + str(x[0]) for x in format_err + data_err0 + data_err1]))

    def exp_byte(self):
        if len(self.reg_tab.hid1_tree.tag_has("modified") + self.reg_tab.hid1_tree.tag_has("eeprom") + self.reg_tab.hid1_tree.tag_has("gpio") +
               self.eep_tab.ed_hid1_tree.tag_has("modified") + self.eep_tab.ed_hid1_tree.tag_has("eeprom") + self.eep_tab.ed_hid1_tree.tag_has("edid")) == 0:
            messagebox.showinfo("EXPORT MODIFIED BYTE LIST", "No Modified Byte List")
            return

        txtfilename = filedialog.asksaveasfilename(filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if not txtfilename.lower().endswith(".txt"):
            txtfilename += ".txt"
        txt = open(txtfilename, "w")

        for iid in self.reg_tab.hid1_tree.tag_has("modified") + self.reg_tab.hid1_tree.tag_has("eeprom") + self.reg_tab.hid1_tree.tag_has("gpio"):
            if iid in [str(x) for x in self.spl.l.pages_unique]:
                continue
            pg, num = iid.split("-")
            pg_idx = self.spl.l.pages_unique.index(int(pg))
            txt.write(f"{int(pg):02x}".upper() + "-" + num + ", " + self.adr.l.hexa_per_pg[pg_idx][int(num)] + ", " + self.adr.l.hexa_per_pg_mod[pg_idx][int(num)] + "\n")
        for iid in self.eep_tab.ed_hid1_tree.tag_has("modified") + self.eep_tab.ed_hid1_tree.tag_has("eeprom") + self.eep_tab.ed_hid1_tree.tag_has("edid"):
            pg, num = iid.split("-")
            pg_idx = self.spl.l.pages_unique.index(int(pg))
            txt.write("ED-" + num + ", " + self.adr.l.hexa_per_pg[pg_idx][int(num)] + ", " + self.adr.l.hexa_per_pg_mod[pg_idx][int(num)] + "\n")

        txt.close()

    def replace_text(self, start, end, replacement, text="00000000"):
        if end is not None:
            if end - start + 1 != len(replacement):
                raise IndexError("Invalid index replacement")
            return "%s%s%s" % (text[:len(text) - end - 1], replacement, text[len(text) - start:])
        elif end is None:
            if len(replacement) != 1:
                raise IndexError("Invalid index replacement")
            return "%s%s%s" % (text[:len(text) - start - 1], replacement, text[len(text) - start:])
    
    def tkst_write(self, tkst, text="", delete=False):
        tkst.configure(state=NORMAL)
        if delete:
            tkst.delete("1.0", END)
        else:
            tkst.insert(END, text + "\n")
        tkst.configure(state=DISABLED)


if __name__ == "__main__":
    app = HivicsGui()
    app.root.mainloop()