from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText as tkst
from math import floor, ceil
from copy import deepcopy
from ctypes import *
import time
import re


class EEPROMTab:
    def __init__(self, parent):
        self.p = parent
        self.gui = self.p.gui
        self.reg = self.p.reg
        self.tst = self.p.tst
        self.eep = self.p.eep
        self.spl = self.p.spl
        self.mer = self.p.mer
        self.adr = self.p.adr
        self.reg_tab = self.p.reg_tab
        self.i2c_tab = self.p.i2c_tab

        top_frm = ttk.Frame(self.p.eep_frm, padding=self.gui.v.pad.get())
        top_frm.pack(side=TOP, fill=X)
        eep_note = ttk.Notebook(self.p.eep_frm)
        eep_note.pack(side=TOP, fill=BOTH, expand=YES)

        read_frm = ttk.Frame(eep_note)
        write_frm = ttk.Frame(eep_note)
        export_frm = ttk.Frame(eep_note)
        import_frm = ttk.Frame(eep_note)
        edid_frm = ttk.Frame(eep_note)
        eep_note.add(read_frm, text=" Read ")
        eep_note.add(write_frm, text=" Write ")
        eep_note.add(export_frm, text=" Export ")
        eep_note.add(import_frm, text=" Import ")
        eep_note.add(edid_frm, text = " EDID ")

        read_note = ttk.Notebook(read_frm)
        read_note.pack(fill=BOTH, expand=YES)
        write_note = ttk.Notebook(write_frm)
        write_note.pack(fill=BOTH, expand=YES)
        export_note = ttk.Notebook(export_frm)
        export_note.pack(fill=BOTH, expand=YES)
        self.edid_note = ttk.Notebook(edid_frm)
        self.edid_note.pack(fill=BOTH, expand=YES)

        r_bytes = ttk.Frame(read_note, padding=self.gui.v.pad.get() * 2)
        r_page = ttk.Frame(read_note, padding=self.gui.v.pad.get() * 2)
        r_index = ttk.Frame(read_note, padding=self.gui.v.pad.get() * 2)
        r_file = ttk.Frame(read_note, padding=self.gui.v.pad.get() * 2)
        w_bytes = ttk.Frame(write_note, padding=self.gui.v.pad.get() * 2)
        w_page = ttk.Frame(write_note, padding=self.gui.v.pad.get() * 2)
        w_file = ttk.Frame(write_note, padding=self.gui.v.pad.get() * 2)
        exp_pri = ttk.Frame(export_note, padding=self.gui.v.pad.get() * 2)
        exp_txt = ttk.Frame(export_note, padding=self.gui.v.pad.get() * 2)
        exp_rom = ttk.Frame(export_note, padding=self.gui.v.pad.get() * 2)
        ed_data = ttk.Frame(self.edid_note, padding=self.gui.v.pad.get() * 1.8)
        ed_name = ttk.Frame(self.edid_note)
        self.ed_hid0 = ttk.Frame(self.edid_note)
        ed_addr = ttk.Frame(self.edid_note)
        self.ed_hid1 = ttk.Frame(self.edid_note)
        read_note.add(r_bytes, text=" Bytes ")
        read_note.add(r_page, text=" Page ")
        read_note.add(r_index, text=" Index ")
        read_note.add(r_file, text=" File ")
        write_note.add(w_bytes, text=" Bytes ")
        write_note.add(w_page, text=" Page ")
        write_note.add(w_file, text=" File ")
        export_note.add(exp_pri, text=" Priorities ")
        export_note.add(exp_txt, text=" Text File ")
        export_note.add(exp_rom, text=" ROM Maker ")
        self.edid_note.add(ed_data, text=" Data ")
        self.edid_note.add(ed_name, text=" Name ")
        self.edid_note.add(self.ed_hid0, text=" Name (hidden) ")
        self.edid_note.add(ed_addr, text=" Address ")
        self.edid_note.add(self.ed_hid1, text=" Address (hidden) ")
        self.edid_note.hide(self.ed_hid0)
        self.edid_note.hide(self.ed_hid1)

        ttk.Label(top_frm, text="I\u00b2C Slave Address (hex) ").grid(row=0, column=0, sticky=NE)
        ttk.Label(top_frm, text="I\u00b2C Access Address (hex, 2-byte) ").grid(row=1, column=0, sticky=NE)
        ttk.Entry(top_frm, textvariable=self.eep.v.slave_addr, width=2).grid(row=0, column=1, sticky=NW)
        ttk.Entry(top_frm, textvariable=self.eep.v.access_addr, width=5).grid(row=1, column=1, sticky=NW)

        ttk.Label(r_bytes, text="# of Reading Bytes (dec) ").grid(row=0, column=0, pady=(0, 5), sticky=NW)
        ttk.Label(r_bytes, text="I\u00b2C Access Data").grid(row=2, column=0, columnspan=2, ipadx=30, pady=(10, 5), sticky=N)
        ttk.Entry(r_bytes, textvariable=self.eep.v.read_num, width=5).grid(row=0, column=1, pady=(0, 5), sticky=NW)
        ttk.Entry(r_bytes, textvariable=self.eep.v.write, width=30).grid(row=3, column=1, sticky=W)
        ttk.Button(r_bytes, text="Read", command=self.eep_read).grid(row=1, column=0, padx=(0, 5), sticky=NE)
        ttk.Button(r_bytes, text="Write", command=self.eep_write).grid(row=3, column=0, padx=(0, 5), sticky=NE)
        self.tkst_r_read = tkst(r_bytes, width=30, height=12, state=DISABLED)
        self.tkst_r_read.grid(row=1, column=1, sticky=NW)

        r_pg0 = ttk.Frame(r_page)
        r_pg1 = ttk.Frame(r_page)
        r_pg2 = ttk.Frame(r_page)
        r_pg3 = ttk.Frame(r_page)
        r_pg0.pack(fill=X)
        r_pg1.pack(fill=X)
        r_pg2.pack(fill=X)
        r_pg3.pack(fill=X)
        ttk.Button(r_pg0, text="Read", command=self.eep_pg_read).grid(row=0, column=0, columnspan=4, pady=(0, 20), sticky=NW)
        ttk.Label(r_pg0, text="Page ID").grid(row=1, column=0, sticky=NW)
        ttk.Entry(r_pg0, textvariable=self.eep.v.pg_id, width=3, state="readonly").grid(row=1, column=1, padx=5, sticky=NW)
        ttk.Label(r_pg0, text=" Page length").grid(row=1, column=2, padx=5, sticky=NW)
        ttk.Entry(r_pg0, textvariable=self.eep.v.pg_len, width=3, state="readonly").grid(row=1, column=3, sticky=NW)
        ttk.Label(r_pg1, text="Page data").grid(row=0, column=0, padx=(0, 5), pady=10, sticky=NW)
        self.tkst_page = tkst(r_pg1, width=30, height=12, state=DISABLED)
        self.tkst_page.grid(row=0, column=1, pady=(10, 20), sticky=NW)
        ttk.Label(r_pg2, text="Page CRC (read)").grid(row=0, column=0, sticky=NW)
        ttk.Entry(r_pg2, textvariable=self.eep.v.crc_read, width=3, state="readonly").grid(row=0, column=1, padx=5, sticky=NW)
        ttk.Label(r_pg2, text=" Page CRC (sum)").grid(row=0, column=2, padx=5, sticky=NW)
        ttk.Entry(r_pg2, textvariable=self.eep.v.crc_sum, width=3, state="readonly").grid(row=0, column=3, padx=(0, 10), sticky=NW)
        ttk.Label(r_pg2, text=" Page CRC (offset) ").grid(row=0, column=4, sticky=NW)
        ttk.Entry(r_pg2, textvariable=self.eep.v.crc_ofs, width=3).grid(row=0, column=5, sticky=NW)
        ttk.Label(r_pg3, text="Next Page Start ").grid(row=0, column=0, pady=10)
        ttk.Entry(r_pg3, textvariable=self.eep.v.next_pg, width=5, state="readonly").grid(row=0, column=1, pady=10)

        idx_top = ttk.Frame(r_index)
        idx_top.pack(side=TOP, fill=X)
        ttk.Button(idx_top, text="Read Page Indices", width=15, command=self.eep_pg_idx_read).grid(row=0, column=0, padx=(0, 50), sticky=NW)
        ttk.Label(idx_top, text="EEPROM Checksum: ").grid(row=0, column=1, sticky=W)
        ttk.Entry(idx_top, textvariable=self.eep.v.crc_ofs, width=3).grid(row=0, column=2, sticky=W)
        self.idx_frm = ttk.Frame(r_index, padding=self.gui.v.pad.get())
        self.idx_frm.pack(side=TOP, fill=BOTH, expand=YES)

        file_top = ttk.Frame(r_file)
        file_top.pack(side=TOP, fill=X)
        ttk.Button(file_top, text="Read & Save", width=15, command=self.eep_read_save).grid(row=0, column=0, padx=(0, 50), sticky=NW)
        ttk.Label(file_top, text="EEPROM Checksum: ").grid(row=0, column=1, sticky=W)
        ttk.Entry(file_top, textvariable=self.eep.v.crc_ofs, width=3).grid(row=0, column=2, sticky=W)
        self.file_frm = ttk.Frame(r_file, padding=self.gui.v.pad.get() * 0.5)
        self.file_frm.pack(side=TOP, fill=BOTH, expand=YES)

        ttk.Label(w_bytes, text="I\u00b2C Access Data").grid(row=0, column=0, columnspan=2, ipadx=30, pady=(0, 5), sticky=N)
        ttk.Button(w_bytes, text="Write", command=self.eep_write).grid(row=1, column=0, padx=(0, 5), sticky=NE)
        ttk.Entry(w_bytes, textvariable=self.eep.v.write, width=30).grid(row=1, column=1, sticky=W)
        ttk.Label(w_bytes, text="# of Reading Bytes (dec) ").grid(row=2, column=0, pady=(10, 5), sticky=NW)
        ttk.Entry(w_bytes, textvariable=self.eep.v.read_num, width=5).grid(row=2, column=1, pady=(10, 5), sticky=NW)
        ttk.Button(w_bytes, text="Read", command=self.eep_read).grid(row=3, column=0, padx=(0, 5), sticky=NE)
        self.tkst_w_read = tkst(w_bytes, width=30, height=12, state=DISABLED)
        self.tkst_w_read.grid(row=3, column=1, sticky=NW)

        ttk.Label(w_page, text="Page CRC (offset) ").grid(row=0, column=0, sticky=NE)
        ttk.Entry(w_page, textvariable=self.eep.v.crc_ofs, width=3).grid(row=0, column=1, sticky=NW)
        ttk.Button(w_page, text="Write 1 Page", command=self.eep_write_1_pg).grid(row=1, column=0, padx=(0, 5), pady=(5, 0), sticky=NE)
        ttk.Entry(w_page, textvariable=self.eep.v.write_1, width=3).grid(row=1, column=1, pady=(7, 0), sticky=NW)
        ttk.Button(w_page, text="Write Listed Pages", command=self.eep_write_listed_pg).grid(row=2, column=0, padx=(0, 5), pady=(5, 0), sticky=NE)
        ttk.Entry(w_page, textvariable=self.eep.v.write_list, width=30).grid(row=2, column=1, pady=(7, 0), sticky=NW)
        ttk.Button(w_page, text="Write Modified Pages", command=self.eep_write_mod_pg).grid(row=3, column=0, padx=(0, 5), pady=(5, 0), sticky=NE)
        ttk.Entry(w_page, textvariable=self.eep.v.check_mod, width=30, state="readonly").grid(row=3, column=1, pady=(7, 0), sticky=NW)

        ttk.Button(w_file, text="Write", command=self.eep_file_write).grid(row=0, column=0)

        ttk.Label(exp_pri, text="Main Page ").grid(row=0, column=0, sticky=NE)
        ttk.Label(exp_pri, text="Core Page ").grid(row=1, column=0, pady=5, sticky=NE)
        ttk.Label(exp_pri, text="Base Page ").grid(row=2, column=0, sticky=NE)
        ttk.Entry(exp_pri, textvariable=self.eep.v.pri_main, width=5).grid(row=0, column=1, sticky=NW)
        ttk.Entry(exp_pri, textvariable=self.eep.v.pri_core, width=30).grid(row=1, column=1, pady=5, sticky=NW)
        ttk.Entry(exp_pri, textvariable=self.eep.v.pri_base, width=30).grid(row=2, column=1, sticky=NW)

        ttk.Label(exp_txt, text="Page CRC (offset) ").grid(row=0, column=0, columnspan=2, sticky=NE)
        ttk.Entry(exp_txt, textvariable=self.eep.v.crc_ofs, width=3).grid(row=0, column=2, sticky=NW)
        ttk.Label(exp_txt, text="Include EEPROM Control Page ").grid(row=1, column=0, columnspan=2, pady=(5, 0), sticky=NE)
        ttk.Checkbutton(exp_txt, variable=self.eep.v.check).grid(row=1, column=2, pady=(5, 0), sticky=NW)
        ttk.Label(exp_txt, text="").grid(row=2, column=0, columnspan=3)
        ttk.Button(exp_txt, text="Check\nModified Pages", width=12, style="Center.TButton", command=self.p.check_mod).grid(row=3, column=0, rowspan=2, padx=(0, 5), sticky=NE)
        ttk.Button(exp_txt, text="Remove\nDuplicated Pages", width=14, style="Center.TButton", command=self.remove_dup_mod).grid(row=3, column=1, rowspan=2, padx=(0, 5), sticky=NE)
        ttk.Entry(exp_txt, textvariable=self.eep.v.check_mod, width=30).grid(row=3, column=2, pady=(1, 0), sticky=NW)
        ttk.Button(exp_txt, text="Import Extra\nROM File", width=12, style="Center.TButton", command=self.import_rom).grid(row=5, column=0, rowspan=2, padx=(0, 5), pady=(5, 0), sticky=NE)
        ttk.Button(exp_txt, text="Remove\nDuplicated Pages", width=14, style="Center.TButton", command=self.remove_dup_imp).grid(row=5, column=1, rowspan=2, padx=(0, 5), pady=(5, 0), sticky=NE)
        ttk.Entry(exp_txt, textvariable=self.eep.v.import_rom, width=30).grid(row=5, column=2, pady=(6, 0), sticky=NW)
        self.exp_imported = ttk.Label(exp_txt, textvariable=self.eep.v.txtfile[0], foreground="gray50")
        ttk.Button(exp_txt, text="Concatenate Exporting Pages", command=self.concatenate).grid(row=7, column=0, columnspan=2, padx=(0, 5), pady=(5, 0), sticky=NE)
        ttk.Entry(exp_txt, textvariable=self.eep.v.conc, width=30, state="readonly").grid(row=7, column=2, pady=(5, 0), sticky=W)
        ttk.Button(exp_txt, text="Export as Plain Text", width=22, command=self.export_plain_txt).grid(row=8, column=0, columnspan=3, padx=(265, 0), pady=(5, 0), sticky=NW)
        ttk.Button(exp_txt, text="Export as TMD Command", width=22, command=self.export_tmd_cmd).grid(row=9, column=0, columnspan=3, padx=(265, 0), pady=(5, 0), sticky=NW)
        ttk.Label(exp_txt, text="\n").grid(row=10, column=0, columnspan=3)
        ttk.Label(exp_txt, text="Main Page ").grid(row=11, column=0, columnspan=2, sticky=NE)
        ttk.Label(exp_txt, text="Core Page ").grid(row=12, column=0, columnspan=2, pady=(5, 0), sticky=NE)
        ttk.Label(exp_txt, text="Base Page ").grid(row=13, column=0, columnspan=2, pady=(5, 0), sticky=NE)
        ttk.Label(exp_txt, text="Full Page ").grid(row=14, column=0, columnspan=2, pady=(5, 0), sticky=NE)
        ttk.Entry(exp_txt, textvariable=self.eep.v.txt_main, width=30, state="readonly").grid(row=11, column=2, sticky=NW)
        ttk.Entry(exp_txt, textvariable=self.eep.v.txt_core, width=30, state="readonly").grid(row=12, column=2, pady=(5, 0), sticky=NW)
        ttk.Entry(exp_txt, textvariable=self.eep.v.txt_base, width=30, state="readonly").grid(row=13, column=2, pady=(5, 0), sticky=NW)
        self.eep_txt_full = tkst(exp_txt, width=30, height=3, state=DISABLED)
        self.eep_txt_full.grid(row=14, column=2, columnspan=2, pady=(5, 0), sticky=NW)

        imp0 = ttk.Frame(import_frm, padding=self.gui.v.pad.get() * 2)
        imp1 = ttk.Frame(import_frm, padding=self.gui.v.pad.get() * 2)
        imp0.place(relx=0, rely=0, relwidth=0.7, relheight=1)
        imp1.place(relx=0.7, rely=0, relwidth=0.3, relheight=1)
        imp0_top = ttk.Frame(imp0)
        imp0_bot = ttk.Frame(imp0, height=18)
        imp0_top.pack(side=TOP, fill=BOTH, expand=YES)
        imp0_bot.pack(side=BOTTOM, fill=X)
        self.imp_tree = ttk.Treeview(imp0_top, columns=("col1", "col2", "col3", "col4", "col5"))
        imp_scrollbar = ttk.Scrollbar(imp0_top, orient=VERTICAL, command=self.imp_tree.yview)
        imp_scrollbar.pack(side=RIGHT, fill=Y)
        self.imp_tree["yscrollcommand"] = imp_scrollbar.set
        self.imp_tree.heading("#0", text="Address")
        self.imp_tree.heading("col1", text="BIN")
        self.imp_tree.heading("col2", text="HEX")
        self.imp_tree.column("#0", width=120)
        self.imp_tree.column("col1", width=150)
        self.imp_tree.column("col2", width=150)
        self.imp_tree.column("col3", width=20)
        self.imp_tree.column("col4", width=20)
        self.imp_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        self.imp_tree.tag_configure("check", background="DarkOliveGreen3")
        self.imp_tree.tag_configure("gray", background="gray80", foreground="gray50")
        self.imp_tree.bind("<Button-3>", self.check)
        ttk.Label(imp0_bot, textvariable=self.eep.v.txtfile[1], foreground="gray50").pack(side=BOTTOM, fill=X, anchor=W, pady=(2, 0))
        ttk.Button(imp1, text="Import EEPROM", width=20, command=self.eep_import).pack(side=TOP, anchor=CENTER, padx=(0, 15), pady=(20, 0), ipady=3)
        ttk.Button(imp1, text="Apply Values", width=20, command=self.apply_values).pack(side=TOP, anchor=CENTER, padx=(0, 15), pady=(15, 0), ipady=3)
        ttk.Button(imp1, text="Select All", width=20, command=self.select_all).pack(side=TOP, anchor=CENTER, padx=(0, 15), pady=(15, 0), ipady=3)
        ttk.Button(imp1, text="Clear All", width=20, command=self.clear_all).pack(side=TOP, anchor=CENTER, padx=(0, 15), pady=(15, 0), ipady=3)
        ttk.Button(imp1, text="Reset", width=20, command=self.reset_eep).pack(side=TOP, anchor=CENTER, padx=(0, 15), pady=(15, 0), ipady=3)

        data_l = ttk.Frame(ed_data)
        data_r = ttk.Frame(ed_data)
        data_l.place(relx=0, rely=0, relwidth=0.75, relheight=1)
        data_r.place(relx=0.75, rely=0, relwidth=0.25, relheight=1)
        self.data_cv = Canvas(data_l)
        self.data_cv.pack(side=LEFT, fill=BOTH, expand=YES)
        data_frm = ttk.Frame(self.data_cv)
        self.data_cv.create_window(0, 0, anchor=NW, window=data_frm)
        data_sb = Scrollbar(data_l, orient=VERTICAL, command=self.data_cv.yview)
        data_sb.pack(anchor=E, side=LEFT, fill=Y)
        self.data_cv.config(yscrollcommand=data_sb.set)
        data_l.bind("<Configure>", self.resize)

        for i in range(4):
            if i == 0:
                pad0 = 3
                pad1 = 0
            else:
                pad0 = self.gui.v.pad.get() * 2.7 + 3
                pad1 = self.gui.v.pad.get() * 2.7
            ttk.Label(data_frm, text="Descriptor " + str(i + 1) + "\n").grid(row=i * 4, column=0, columnspan=10, pady=(pad0, 0), sticky=SW)
            ttk.Button(data_frm, text="Calc Frequency", command=lambda num=i: self.calc_freq(num)).grid(row=i * 4, column=0, columnspan=10, padx=(80, 0), pady=(pad1, 0), sticky=NW)
            ttk.Button(data_frm, text="Calc Refresh", command=lambda num=i: self.calc_rfsh(num)).grid(row=i * 4, column=0, columnspan=10, padx=(180, 0), pady=(pad1, 0), sticky=NW)
            ttk.Label(data_frm, text="H active").grid(row=i * 4 + 1, column=0, padx=(30, 0), pady=(5, 0), sticky=NE)
            ttk.Label(data_frm, text="H blank").grid(row=i * 4 + 1, column=2, padx=(20, 0), pady=(5, 0), sticky=NE)
            ttk.Label(data_frm, text="H front-porch").grid(row=i * 4 + 1, column=4, padx=(20, 0), pady=(5, 0), sticky=NE)
            ttk.Label(data_frm, text="H back-porch").grid(row=i * 4 + 1, column=6, padx=(20, 0), pady=(5, 0), sticky=NE)
            ttk.Label(data_frm, text="H sync").grid(row=i * 4 + 1, column=8, padx=(20, 0), pady=(5, 0), sticky=NE)
            ttk.Label(data_frm, text="V active").grid(row=i * 4 + 2, column=0, padx=(30, 0), pady=(5, 0), sticky=NE)
            ttk.Label(data_frm, text="V blank").grid(row=i * 4 + 2, column=2, padx=(20, 0), pady=(5, 0), sticky=NE)
            ttk.Label(data_frm, text="V front-porch").grid(row=i * 4 + 2, column=4, padx=(20, 0), pady=(5, 0), sticky=NE)
            ttk.Label(data_frm, text="V back-porch").grid(row=i * 4 + 2, column=6, padx=(20, 0), pady=(5, 0), sticky=NE)
            ttk.Label(data_frm, text="V sync").grid(row=i * 4 + 2, column=8, padx=(20, 0), pady=(5, 0), sticky=NE)
            ttk.Label(data_frm, text="Frequency (MHz)").grid(row=i * 4 + 3, column=0, padx=(30, 0), pady=(5, 0), sticky=NE)
            ttk.Label(data_frm, text="Refresh (Hz)").grid(row=i * 4 + 3, column=2, padx=(20, 0), pady=(5, 0), sticky=NE)
            ttk.Entry(data_frm, textvariable=self.eep.v.hac[i], width=5).grid(row=i * 4 + 1, column=1, padx=(5, 0), pady=(5, 0), sticky=NW)
            ttk.Entry(data_frm, textvariable=self.eep.v.hbl[i], width=5).grid(row=i * 4 + 1, column=3, padx=(5, 0), pady=(5, 0), sticky=NW)
            ttk.Entry(data_frm, textvariable=self.eep.v.hfp[i], width=5).grid(row=i * 4 + 1, column=5, padx=(5, 0), pady=(5, 0), sticky=NW)
            ttk.Entry(data_frm, textvariable=self.eep.v.hbp[i], width=5, state="readonly").grid(row=i * 4 + 1, column=7, padx=(5, 0), pady=(5, 0), sticky=NW)
            ttk.Entry(data_frm, textvariable=self.eep.v.hsy[i], width=5).grid(row=i * 4 + 1, column=9, padx=(5, 0), pady=(5, 0), sticky=NW)
            ttk.Entry(data_frm, textvariable=self.eep.v.vac[i], width=5).grid(row=i * 4 + 2, column=1, padx=(5, 0), pady=(5, 0), sticky=NW)
            ttk.Entry(data_frm, textvariable=self.eep.v.vbl[i], width=5).grid(row=i * 4 + 2, column=3, padx=(5, 0), pady=(5, 0), sticky=NW)
            ttk.Entry(data_frm, textvariable=self.eep.v.vfp[i], width=5).grid(row=i * 4 + 2, column=5, padx=(5, 0), pady=(5, 0), sticky=NW)
            ttk.Entry(data_frm, textvariable=self.eep.v.vbp[i], width=5, state="readonly").grid(row=i * 4 + 2, column=7, padx=(5, 0), pady=(5, 0), sticky=NW)
            ttk.Entry(data_frm, textvariable=self.eep.v.vsy[i], width=5).grid(row=i * 4 + 2, column=9, padx=(5, 0), pady=(5, 0), sticky=NW)
            ttk.Entry(data_frm, textvariable=self.eep.v.freq[i], width=5).grid(row=i * 4 + 3, column=1, padx=(5, 0), pady=(5, 0), sticky=NW)
            ttk.Entry(data_frm, textvariable=self.eep.v.rfsh[i], width=5).grid(row=i * 4 + 3, column=3, padx=(5, 0), pady=(5, 0), sticky=NW)
            self.eep.v.hbl[i].trace("w", lambda name, index, mode, num=i, type="H": self.calc_bp(num, type))
            self.eep.v.hfp[i].trace("w", lambda name, index, mode, num=i, type="H": self.calc_bp(num, type))
            self.eep.v.hsy[i].trace("w", lambda name, index, mode, num=i, type="H": self.calc_bp(num, type))
            self.eep.v.vbl[i].trace("w", lambda name, index, mode, num=i, type="V": self.calc_bp(num, type))
            self.eep.v.vfp[i].trace("w", lambda name, index, mode, num=i, type="V": self.calc_bp(num, type))
            self.eep.v.vsy[i].trace("w", lambda name, index, mode, num=i, type="V": self.calc_bp(num, type))
        ttk.Label(data_frm, text="\n").grid(row=16, column=0, columnspan=10)
        ttk.Label(data_frm, text="Page Offset\n").grid(row=17, column=0, columnspan=10, pady=(3, 0), sticky=W)
        ttk.Button(data_frm, text="Calc EDID Checksum", command=self.calc_crc).grid(row=17, column=0, columnspan=10, padx=(80, 0), sticky=NW)
        ttk.Label(data_frm, text="Checksum", state="readonly").grid(row=18, column=0, padx=(30, 0), pady=(5, 0), sticky=NE)
        ttk.Entry(data_frm, textvariable=self.eep.v.edid_checksum, width=3, state="readonly").grid(row=18, column=1, padx=(5, 0), pady=(5, 0), sticky=NW)
        ttk.Button(data_r, text="Load Data", width=20, command=self.ed_load).pack(side=TOP, pady=(20, 0), ipady=3)
        ttk.Button(data_r, text="Set Data", width=20, command=self.ed_set).pack(side=TOP, pady=(15, 0), ipady=3)
        ttk.Button(data_r, text="Set Default", width=20, command=self.ed_set_default).pack(side=TOP, pady=(15, 0), ipady=3)
        ttk.Button(data_r, text="Reset to Default", width=20, command=self.reset_to_default).pack(side=TOP, pady=(15, 0), ipady=3)

        ed_name_tree_frm = ttk.Frame(ed_name)
        ed_name_ctrl_frm = ttk.Frame(ed_name)
        ed_name_tree_frm.place(relx=0, rely=0, relwidth=0.8, relheight=1)
        ed_name_ctrl_frm.place(relx=0.8, rely=0, relwidth=0.2, relheight=1)
        ttk.Label(ed_name_ctrl_frm, text="MAIN CONTROL\n", anchor=CENTER).pack(side=TOP, fill=X, pady=(20, 0))
        ttk.Button(ed_name_ctrl_frm, text="Reset Register Lists", width=23, command=self.reset_ed).pack(side=TOP, anchor=CENTER, pady=(0, 13), ipadx=3)
        ttk.Button(ed_name_ctrl_frm, text="Import Modified Register List", width=23, command=self.p.imp_reg).pack(side=TOP, anchor=CENTER, pady=(0, 3), ipadx=3)
        ttk.Button(ed_name_ctrl_frm, text="Export Modified Register List", width=23, command=self.p.exp_reg).pack(side=TOP, anchor=CENTER, pady=(0, 13), ipadx=3)
        ttk.Button(ed_name_ctrl_frm, text="Import Modified Byte List", width=23, command=self.p.imp_byte).pack(side=TOP, anchor=CENTER, pady=(0, 3), ipadx=3)
        ttk.Button(ed_name_ctrl_frm, text="Export Modified Byte List", width=23, command=self.p.exp_byte).pack(side=TOP, anchor=CENTER, pady=(0, 13), ipadx=3)
        ttk.Button(ed_name_ctrl_frm, text="Check Modified Pages", width=23, command=self.p.check_mod).pack(side=TOP, anchor=CENTER, pady=(0, 3), ipadx=3)
        ttk.Entry(ed_name_ctrl_frm, textvariable=self.eep.v.check_mod, width=23, state="readonly").pack(side=TOP, anchor=CENTER, ipadx=4)
        ttk.Label(ed_name_ctrl_frm, text="\n").pack(side=TOP, fill=X)
        ttk.Checkbutton(ed_name_ctrl_frm, text="Show Hidden Tab", variable=self.eep.v.ed_check0, command=lambda choice="name": self.show_hide(choice)).pack(side=TOP)
        self.ed_name_tree = ttk.Treeview(ed_name_tree_frm, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7"))
        edid_scrollbar = ttk.Scrollbar(ed_name_tree_frm, orient=VERTICAL, command=self.ed_name_tree.yview)
        edid_scrollbar.pack(side=RIGHT, fill=Y)
        self.ed_name_tree["yscrollcommand"] = edid_scrollbar.set
        self.ed_name_tree.heading("#0", text="Register Name")
        self.ed_name_tree.heading("col1", text="Width")
        self.ed_name_tree.heading("col2", text="BIN")
        self.ed_name_tree.heading("col3", text="DEC")
        self.ed_name_tree.heading("col4", text="HEX")
        self.ed_name_tree.column("col1", width=60)
        self.ed_name_tree.column("col2", width=150)
        self.ed_name_tree.column("col3", width=60)
        self.ed_name_tree.column("col4", width=60)
        self.ed_name_tree.column("col5", width=20)
        self.ed_name_tree.column("col6", width=20)
        self.ed_name_tree.column("col7", width=240)
        self.ed_name_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        self.ed_name_tree.bind("<Double-1>", lambda event, click_type=1: self.ed_popup0(event, click_type))
        self.ed_name_tree.bind("<Button-3>", lambda event, click_type=3: self.ed_popup0(event, click_type))
        self.ed_name_tree.tag_configure("modified", background="yellow")
        self.ed_name_tree.tag_configure("eeprom", background="DarkOliveGreen3")
        self.ed_name_tree.tag_configure("edid", background="orange")

        ed_addr_tree_frm = ttk.Frame(ed_addr)
        ed_addr_ctrl_frm = ttk.Frame(ed_addr)
        ed_addr_tree_frm.place(relx=0, rely=0, relwidth=0.8, relheight=1)
        ed_addr_ctrl_frm.place(relx=0.8, rely=0, relwidth=0.2, relheight=1)
        ttk.Label(ed_addr_ctrl_frm, text="MAIN CONTROL\n", anchor=CENTER).pack(side=TOP, fill=X, pady=(20, 0))
        ttk.Button(ed_addr_ctrl_frm, text="Reset Register Lists", width=23, command=self.reset_ed).pack(side=TOP, anchor=CENTER, pady=(0, 13), ipadx=3)
        ttk.Button(ed_addr_ctrl_frm, text="Import Modified Register List", width=23, command=self.p.imp_reg).pack(side=TOP, anchor=CENTER, pady=(0, 3), ipadx=3)
        ttk.Button(ed_addr_ctrl_frm, text="Export Modified Register List", width=23, command=self.p.exp_reg).pack(side=TOP, anchor=CENTER, pady=(0, 13), ipadx=3)
        ttk.Button(ed_addr_ctrl_frm, text="Import Modified Byte List", width=23, command=self.p.imp_byte).pack(side=TOP, anchor=CENTER, pady=(0, 3), ipadx=3)
        ttk.Button(ed_addr_ctrl_frm, text="Export Modified Byte List", width=23, command=self.p.exp_byte).pack(side=TOP, anchor=CENTER, pady=(0, 13), ipadx=3)
        ttk.Button(ed_addr_ctrl_frm, text="Check Modified Pages", width=23, command=self.p.check_mod).pack(side=TOP, anchor=CENTER, pady=(0, 3), ipadx=3)
        ttk.Entry(ed_addr_ctrl_frm, textvariable=self.eep.v.check_mod, width=23, state="readonly").pack(side=TOP, anchor=CENTER, ipadx=4)
        ttk.Label(ed_addr_ctrl_frm, text="\n").pack(side=TOP, fill=X)
        ttk.Checkbutton(ed_addr_ctrl_frm, text="Show Hidden Tab", variable=self.eep.v.ed_check1, command=lambda choice="addr": self.show_hide(choice)).pack(side=TOP)
        self.ed_addr_tree = ttk.Treeview(ed_addr_tree_frm, columns=tuple(self.reg.l.hex_col + ["last"]))
        addr_scrollbar = ttk.Scrollbar(ed_addr_tree_frm, orient=VERTICAL, command=self.ed_addr_tree.yview)
        addr_scrollbar.pack(side=RIGHT, fill=Y)
        self.ed_addr_tree["yscrollcommand"] = addr_scrollbar.set
        self.ed_addr_tree.heading("#0", text="Address")
        self.ed_addr_tree.column("#0", width=120)
        for (i, item) in list(enumerate(self.reg.l.hex_col)):
            if "blank" not in item:
                self.ed_addr_tree.heading(item, text=item)
                self.ed_addr_tree.column(item, width=20, anchor=CENTER)
            if "blank" in item:
                self.ed_addr_tree.heading(item, text="\u250a")
                self.ed_addr_tree.column(item, width=20, stretch=NO)
        self.ed_addr_tree.column("last", width=1, stretch=NO)
        self.ed_addr_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        self.ed_addr_tree.bind("<Double-1>", lambda event, click_type=1: self.ed_popup1(event, click_type))
        self.ed_addr_tree.bind("<Button-3>", lambda event, click_type=3: self.ed_popup1(event, click_type))
        self.ed_addr_tree.tag_configure("modified", background="yellow")
        self.ed_addr_tree.tag_configure("eeprom", background="DarkOliveGreen3")
        self.ed_addr_tree.tag_configure("edid", background="orange")

        ed_hid0_tree_frm = ttk.Frame(self.ed_hid0)
        ed_hid0_tree_frm.place(relx=0, rely=0, relwidth=0.8, relheight=1)
        self.ed_hid0_tree = ttk.Treeview(ed_hid0_tree_frm, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7"))
        hid0_scrollbar = ttk.Scrollbar(ed_hid0_tree_frm, orient=VERTICAL, command=self.ed_hid0_tree.yview)
        hid0_scrollbar.pack(side=RIGHT, fill=Y)
        self.ed_hid0_tree["yscrollcommand"] = hid0_scrollbar.set
        self.ed_hid0_tree.heading("#0", text="Register Name")
        self.ed_hid0_tree.heading("col1", text="Width")
        self.ed_hid0_tree.heading("col2", text="BIN")
        self.ed_hid0_tree.heading("col3", text="DEC")
        self.ed_hid0_tree.heading("col4", text="HEX")
        self.ed_hid0_tree.column("col1", width=60)
        self.ed_hid0_tree.column("col2", width=150)
        self.ed_hid0_tree.column("col3", width=60)
        self.ed_hid0_tree.column("col4", width=60)
        self.ed_hid0_tree.column("col5", width=20)
        self.ed_hid0_tree.column("col6", width=20)
        self.ed_hid0_tree.column("col7", width=240)
        self.ed_hid0_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        self.ed_hid0_tree.bind("<Button-3>", self.ed_popup_hid0)
        self.ed_hid0_tree.tag_configure("modified", background="yellow")
        self.ed_hid0_tree.tag_configure("eeprom", background="DarkOliveGreen3")
        self.ed_hid0_tree.tag_configure("edid", background="orange")

        ed_hid1_tree_frm = ttk.Frame(self.ed_hid1)
        ed_hid1_tree_frm.place(relx=0, rely=0, relwidth=0.8, relheight=1)
        self.ed_hid1_tree = ttk.Treeview(ed_hid1_tree_frm, columns=("col1", "col2", "col3", "col4"))
        ed_hid1_scrollbar = ttk.Scrollbar(ed_hid1_tree_frm, orient=VERTICAL, command=self.ed_hid1_tree.yview)
        ed_hid1_scrollbar.pack(side=RIGHT, fill=Y)
        self.ed_hid1_tree["yscrollcommand"] = ed_hid1_scrollbar.set
        self.ed_hid1_tree.heading("#0", text="Address")
        self.ed_hid1_tree.heading("col1", text="BIN")
        self.ed_hid1_tree.heading("col2", text="HEX")
        self.ed_hid1_tree.column("#0", width=120)
        self.ed_hid1_tree.column("col1", width=150)
        self.ed_hid1_tree.column("col2", width=150)
        self.ed_hid1_tree.column("col3", width=20)
        self.ed_hid1_tree.column("col4", width=350)
        self.ed_hid1_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        self.ed_hid1_tree.bind("<Button-3>", self.ed_popup_hid1)
        self.ed_hid1_tree.tag_configure("modified", background="yellow")
        self.ed_hid1_tree.tag_configure("eeprom", background="DarkOliveGreen3")
        self.ed_hid1_tree.tag_configure("edid", background="orange")

    def open_file(self):
        try:
            self.txtfilename = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("All Files", "*.*")))
            txt = open(self.txtfilename, "r")
            byte_text = txt.readlines()
            txt.close()
        except FileNotFoundError:
            return
        return list(map(str.strip, byte_text))

    # Read
    def eep_read(self):
        read_list, result = self.i2c_tab.sub20_i2c_read(int(self.eep.v.slave_addr.get(), 16), int("".join(self.eep.v.access_addr.get().split()), 16), int(self.eep.v.read_num.get()))
        time.sleep(0.1)
        try:
            len(read_list)
        except TypeError:
            messagebox.showerror("I\u00b2C Read Result", "Read Failed!\n" + result)
        else:
            read_str = " ".join([f"{ord(x):02X}" for x in read_list])
            self.p.tkst_write(self.tkst_r_read, delete=True)
            self.p.tkst_write(self.tkst_r_read, read_str)
            self.p.tkst_write(self.tkst_w_read, delete=True)
            self.p.tkst_write(self.tkst_w_read, read_str)

    def eep_pg_read(self):
        eep_addr = int("".join(self.eep.v.access_addr.get().split()), 16)
        id_list, result = self.i2c_tab.sub20_i2c_read(int(self.eep.v.slave_addr.get(), 16), eep_addr, 2)
        time.sleep(0.1)

        try:
            len(id_list)
        except TypeError:
            messagebox.showerror("I\u00b2C Read Result", "Read Failed!\n" + result)
            return
        else:
            self.eep.v.pg_id.set(f"{ord(id_list[0]):02X}")
            self.eep.v.pg_len.set(f"{ord(id_list[1]):02X}")
            page_len = int.from_bytes(id_list[1], byteorder="big", signed=False) + 1
            read_list, result = self.i2c_tab.sub20_i2c_read(int(self.eep.v.slave_addr.get(), 16), eep_addr + 2, page_len)
            time.sleep(0.1)
            try:
                len(read_list)
            except TypeError:
                messagebox.showerror("I\u00b2C Read Result", "Read Failed!\n" + result)
                return
            else:
                read_str = " ".join([f"{ord(x):02X}" for x in read_list])
                self.p.tkst_write(self.tkst_page, delete=True)
                self.p.tkst_write(self.tkst_page, read_str)

            crc_list, result = self.i2c_tab.sub20_i2c_read(int(self.eep.v.slave_addr.get(), 16), eep_addr + page_len + 2, 1)
            time.sleep(0.1)
            try:
                len(crc_list)
            except TypeError:
                messagebox.showerror("I\u00b2C Read Result", "Read Failed!\n" + result)
            else:
                read_str = " ".join([f"{ord(x):02X}" for x in crc_list])
                self.eep.v.crc_read.set(read_str)

                checksum = int.from_bytes(id_list[0], byteorder="big", signed=False) + page_len - 1
                for k in range(len(read_list)):
                    checksum += int.from_bytes(read_list[k], byteorder="big", signed=False)
                crc256q, crc256m = divmod(checksum, 256)
                crc_q, crc_v = divmod(256 + int(self.eep.v.crc_ofs.get(), 16) - crc256m, 256)
                self.eep.v.crc_sum.set(f"{crc_v:02X}")

                self.eep.v.next_pg.set(f"{(eep_addr + page_len + 3):04X}")

    def eep_pg_idx_read(self):
        for slave in self.idx_frm.grid_slaves():
            slave.destroy()

        self.eep.l.r_idx_vars = []
        n = 0
        eep_addr = 0

        while True:
            read_list, result = self.i2c_tab.sub20_i2c_read(int(self.eep.v.slave_addr.get(), 16), eep_addr, 259)
            time.sleep(0.1)
            try:
                len(read_list)
            except TypeError:
                messagebox.showerror("I\u00b2C Read Result", "Read Failed!\n" + result)
                return

            page_id = ord(read_list[0])
            page_len = ord(read_list[1])
            crc = 0
            for b in range(page_len + 1 + 3):
                crc = (crc + ord(read_list[b])) % 256

            self.eep.l.r_idx_vars.append(StringVar())
            self.eep.l.r_idx_vars[n].set(f"{eep_addr:04X}")
            row_div10, col_mod10 = divmod(n, 10)

            ttk.Label(self.idx_frm, text="Page ID:").grid(row=3 * row_div10, column=0, padx=(10, 20), pady=(30, 0), sticky=NW)
            ttk.Label(self.idx_frm, text="Address:").grid(row=3 * row_div10 + 1, column=0, padx=(10, 20), pady=(5, 0), sticky=NW)
            ttk.Label(self.idx_frm, text="Checksum:").grid(row=3 * row_div10 + 2, column=0, padx=(10, 20), pady=(5, 0), sticky=NW)
            ttk.Label(self.idx_frm, text=f"{page_id:02X}").grid(row=3 * row_div10, column=col_mod10 + 1, padx=(0, 5), pady=(30, 0), sticky=NW)
            ttk.Entry(self.idx_frm, textvariable=self.eep.l.r_idx_vars[n], width=5, state="readonly").grid(row=3 * row_div10 + 1, column=col_mod10 + 1, padx=(0, 5), pady=(5, 0), sticky=NW)
            ttk.Label(self.idx_frm, text=f"{crc:02X}").grid(row=3 * row_div10 + 2, column=col_mod10 + 1, padx=(0, 5), pady=(5, 0), sticky=NW)

            eep_addr = eep_addr + page_len + 4
            n += 1

            if crc != int(self.eep.v.crc_ofs.get(), 16):
                return

    def eep_read_save(self):
        for slave in self.file_frm.grid_slaves():
            slave.destroy()

        eep_pages = []
        eep_addr = 0
        while True:
            read_list, result = self.i2c_tab.sub20_i2c_read(int(self.eep.v.slave_addr.get(), 16), eep_addr, 259)
            time.sleep(0.1)
            try:
                len(read_list)
            except TypeError:
                messagebox.showerror("I\u00b2C Read Result", "Read Failed!\n" + result)
                return

            page_id = ord(read_list[0])
            page_len = ord(read_list[1])
            crc = 0
            for b in range(page_len + 1 + 3):
                crc = (crc + ord(read_list[b])) % 256

            if crc != int(self.eep.v.crc_ofs.get(), 16):
                read_num = eep_addr
                break

            eep_pages.append(f"{page_id:02X}")
            eep_addr = eep_addr + page_len + 4

        read_list, result = self.i2c_tab.sub20_i2c_read(int(self.eep.v.slave_addr.get(), 16), int("".join(self.eep.v.access_addr.get().split()), 16), read_num)
        time.sleep(0.1)
        try:
            len(read_list)
        except TypeError:
            messagebox.showerror("I\u00b2C Read Result", "Read Failed!\n" + result)
        else:
            txtfilename = filedialog.asksaveasfilename(filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
            if txtfilename == "":
                return
            if not txtfilename.lower().endswith(".txt"):
                txtfilename += ".txt"
            txt = open(txtfilename, "w")
            for hex in [f"{ord(x):02X}" for x in read_list]:
                txt.write(hex + "\n")
            txt.write("00" + "\n")
            txt.close()

            self.eep.v.sub20_pages.set(", ".join(eep_pages))
            self.eep.v.sub20_pg_num.set(str(len(eep_pages)))
            self.eep.v.sub20_total_len.set(str(len(read_list)))
            ttk.Label(self.file_frm, text=txtfilename + "\n", foreground="gray50").grid(row=0, column=0, columnspan=3, sticky=NW)
            ttk.Label(self.file_frm, text="Pages: ").grid(row=1, column=0, pady=(20, 0), sticky=NE)
            ttk.Entry(self.file_frm, textvariable=self.eep.v.sub20_pages, width=50, state="readonly").grid(row=1, column=1, pady=(20, 0), sticky=NW)
            ttk.Label(self.file_frm, text="# of Pages: ").grid(row=2, column=0, pady=(20, 0), sticky=NE)
            ttk.Entry(self.file_frm, textvariable=self.eep.v.sub20_pg_num, width=3).grid(row=2, column=1, pady=(20, 0), sticky=NW)
            ttk.Label(self.file_frm, text="Total Length: ").grid(row=3, column=0, pady=(20, 0), sticky=NE)
            ttk.Entry(self.file_frm, textvariable=self.eep.v.sub20_total_len, width=5).grid(row=3, column=1, pady=(20, 0), sticky=NW)

    # Write
    def eep_write(self):
        write_str = self.eep.v.write.get()
        n = len(write_str.split())
        byte_list = create_string_buffer(n)
        byte_list[0:n] = bytearray().fromhex(write_str)

        self.eep_32bytes_write(int(self.eep.v.slave_addr.get(), 16), int("".join(self.eep.v.access_addr.get().split()), 16), byte_list)

    def eep_pg_write(self, pg_hex):
        if len(self.spl.pages_unique) == 0:
            messagebox.showerror("ERROR", "Must Import Excel")
            return

        try:
            pg_dec = int(pg_hex, 16)
            pg_idx = self.spl.pages_unique.index(pg_dec)
        except ValueError:
            messagebox.showerror("EEPROM Write Result", "Page " + pg_hex + " Does Not Exist")
            return
        else:
            if self.tst.l.wo_cnt[pg_idx] < 0:
                messagebox.showerror("EEPROM Write Result", "No Re-writable Registers on Page " + pg_hex.upper())
                return

        sum = 0
        n = self.tst.l.wo_cnt[pg_idx] + 1
        byte_list = create_string_buffer(1)
        eep_addr = int("".join(self.eep.v.access_addr.get().split()), 16)
        byte_list[0:1] = bytearray().fromhex(pg_hex)
        sub_errno, result = self.i2c_tab.sub20_i2c_write(int(self.eep.v.slave_addr.get(), 16), eep_addr, byte_list)
        sum += pg_dec
        if sub_errno != 0:
            messagebox.showerror("EEPROM Write Result", "Write Failed!\n" + result)

        byte_list[0:1] = bytearray().fromhex(f"{(n - 1):02X}")
        sub_errno, result = self.i2c_tab.sub20_i2c_write(int(self.eep.v.slave_addr.get(), 16), eep_addr + 1, byte_list)
        sum += n - 1
        if sub_errno != 0:
            messagebox.showerror("EEPROM Write Result", "Write Failed!\n" + result)

        eep_addr_mod32 = divmod(eep_addr + 2, 32)[1]
        n1 = 0
        while True:
            nn = 32 - eep_addr_mod32
            if nn > n:
                nn = n

            byte_list = create_string_buffer(nn)
            byte_list[0:nn] = bytearray().fromhex(" ".join([x.zfill(2).upper() for x in [self.adr.hexa_per_pg_mod[pg_idx][i].replace("-", "00") for i in range(n1, n1 + nn)]]))
            sub_errno, result = self.i2c_tab.sub20_i2c_write(int(self.eep.v.slave_addr.get(), 16), eep_addr + 2 + n1, byte_list)
            for hex in [self.adr.hexa_per_pg_mod[pg_idx][i].replace("-", "00") for i in range(n1, n1 + nn)]:
                sum += int(hex, 16)
            if sub_errno != 0:
                messagebox.showerror("EEPROM Write Result", "Write Failed!\n" + result)

            n = n - nn
            if n <= 0:
                last = eep_addr + 2 + n1 + nn
                break
            n1 = n1 + nn
            eep_addr_mod32 = 0

        crc = (int(self.eep.v.crc_ofs.get(), 16) + 256 - sum) % 256
        byte_list = create_string_buffer(1)
        byte_list[0] = bytearray().fromhex(f"{crc:02X}")
        sub_errno, result = self.i2c_tab.sub20_i2c_write(int(self.eep.v.slave_addr.get(), 16), last, byte_list)
        if sub_errno != 0:
            messagebox.showerror("EEPROM Write Result", "Write Failed!\n" + result)

    def eep_write_1_pg(self):
        if re.compile(r"[^0-9a-fA-F]").search(self.eep.v.write_1.get()) is not None:
            messagebox.showerror("INPUT ERROR", "Invalid Input Format")
            return

        pg_hex = self.eep.v.write_1.get().upper()
        self.eep_pg_write(pg_hex)

    def eep_write_listed_pg(self):
        if re.compile(r"[^0-9a-fA-F ]").search(self.eep.v.write_list.get()) is not None:
            messagebox.showerror("INPUT ERROR", "Invalid Input Format")
            return

        pg_hexa = self.eep.v.write_list.get().upper().split()
        for pg_hex in pg_hexa:
            self.eep_pg_write(pg_hex)

    def eep_write_mod_pg(self):
        if re.compile(r"[^0-9a-fA-F ]").search(self.eep.v.check_mod.get()) is not None:
            messagebox.showerror("INPUT ERROR", "Invalid Input Format")
            return

        pg_hexa = self.eep.v.check_mod.get().upper().split()
        for pg_hex in pg_hexa:
            self.eep_pg_write(pg_hex)

    def eep_file_write(self):
        byte_text = self.open_file()

        n = len(byte_text)
        byte_list = create_string_buffer(n)
        byte_list[0:n] = bytearray().fromhex(" ".join(byte_text))

        self.eep_32bytes_write(int(self.eep.v.slave_addr.get(), 16), int("".join(self.eep.v.access_addr.get().split()), 16), byte_list)

    def eep_32bytes_write(self, slv_addr, mem_addr, byte_list):
        eep_addr_mod32 = mem_addr % 32
        n = len(byte_list)
        n1 = 0
        while n > 0:
            nn = 32 - eep_addr_mod32
            if nn > n:
                nn = n
            partial_byte_list = create_string_buffer(nn)
            partial_byte_list[0:nn] = byte_list[n1:n1 + nn]
            n_fail = 0
            while n_fail < 4:
                sub_errno, result = self.i2c_tab.sub20_i2c_write(slv_addr, mem_addr + n1, partial_byte_list)
                if sub_errno != 0:
                    messagebox.showerror("EEPROM Write Result", "Write Failed!\n" + result)
                else:
                    break
                n_fail = n_fail + 1
            if n_fail >= 4:
                print("EEPROM Write Error!")
                break
            n = n - nn
            n1 = n1 + nn
            eep_addr_mod32 = 0

            n_busy = 0
            while n_busy < 16 and n > 0:
                time.sleep(0.2)
                sub_errno = self.i2c_tab.sub20_i2c_busy(slv_addr, mem_addr + n1)
                n_busy = n_busy + 1
                if sub_errno == 0:
                    break
            if n_busy >= 16:
                messagebox.showwarning("EEPROM Busy", "Write Delayed")
            else:
                time.sleep(0.2 * n_busy)

        self.p.tkst_write(self.tkst_r_read, delete=True)
        self.p.tkst_write(self.tkst_r_read, text="-")
        self.p.tkst_write(self.tkst_w_read, delete=True)
        self.p.tkst_write(self.tkst_w_read, text="-")

    # Export - Text File Tab
    def import_rom(self):
        byte_text = self.open_file()
        self.eep.v.import_rom.set("")
        self.eep.v.txtfile[0].set("")
        self.eep.d.eep_imp_pg = {}

        if len(byte_text) == 0:
            return

        mod_page_list = []
        k = 0
        while k < len(byte_text):
            mod_page_list.append(byte_text[k])
            n = int(byte_text[k + 1], 16) + 4
            self.eep.d.eep_imp_pg[byte_text[k]] = " ".join(byte_text[k + 1:k + n])
            k += n

        self.eep.v.import_rom.set(" ".join(sorted([x.zfill(2) for x in mod_page_list])))
        self.eep.v.txtfile[0].set("Imported: " + self.txtfilename)

        self.exp_imported.grid(row=6, column=2, columnspan=2, sticky=E)

    def remove_dup_mod(self):
        mod_list = self.eep.v.check_mod.get().split()
        imp_list = self.eep.v.import_rom.get().split()
        mod_list = sorted(list(set(mod_list) - set(imp_list)))
        self.eep.v.check_mod.set(" ".join(mod_list))

    def remove_dup_imp(self):
        mod_list = self.eep.v.check_mod.get().split()
        imp_list = self.eep.v.import_rom.get().split()
        imp_list = sorted(list(set(imp_list) - set(mod_list)))
        self.eep.v.import_rom.set(" ".join(imp_list))

    def concatenate(self):
        mod_list = self.eep.v.check_mod.get().split()
        imp_list = self.eep.v.import_rom.get().split()
        c = [""]
        exp_list = sorted(list((set(mod_list) | set(imp_list)) - set(c)))
        self.eep.v.conc.set(" ".join(exp_list))

    def export_common(self):
        priority0 = self.eep.v.pri_main.get().split()
        priority1 = self.eep.v.pri_core.get().split()
        priority2 = self.eep.v.pri_base.get().split()

        self.eep.v.txt_main.set("")
        self.eep.v.txt_base.set("")
        self.eep.v.txt_core.set("")
        self.p.tkst_write(self.eep_txt_full, delete=True)
        self.p.tkst_write(self.eep_txt_full, text="-")

        if self.eep.v.conc.get() == "":
            return

        export_list = self.eep.v.conc.get().split()
        import_list = self.eep.v.import_rom.get().split()
        if self.eep.v.check.get() == 1:
            export_list.extend(self.eep.v.pri_main.get().split())
            export_list.extend(self.eep.v.pri_core.get().split())
            export_list.extend(self.eep.v.pri_base.get().split())
            export_list = sorted(list(set(export_list)))

        if len(self.eep.d.eep_imp_pg) == 0:
            sort_list = export_list.copy()
            for main in list(reversed(self.eep.v.pri_main.get().split())):
                if main in sort_list:
                    sort_list.insert(0, sort_list.pop(sort_list.index(main)))

            byte_list = []
            for pg in sort_list:
                try:
                    pg_idx = self.spl.pages_unique.index(int(pg, 16))
                except ValueError:
                    messagebox.showerror("ERROR", "Page " + pg + " Does Not Exist")
                    return []

                byte_list.append(pg)
                byte_list.append(f"{self.tst.l.wo_cnt[pg_idx]:02X}")

                sumcheck = int(pg, 16) + self.tst.l.wo_cnt[pg_idx]
                for i in range(self.tst.l.wo_cnt[pg_idx] + 1):
                    if self.adr.hexa_per_pg_mod[pg_idx][i] == "-":
                        byte_hex = "00"
                    else:
                        byte_hex = self.adr.hexa_per_pg_mod[pg_idx][i]
                    byte_list.append(byte_hex)
                    sumcheck = (sumcheck + int(byte_hex, 16)) % 256

                crc = (int(self.eep.v.crc_ofs.get(), 16) + 256 - sumcheck) % 256
                byte_list.append(f"{crc:02X}")

            root_list = []
            core_list = []
            base_list = []
            full_list = export_list.copy()
            rm_list0 = sorted(list(set(full_list) - set(priority0)))
            if rm_list0 is not full_list:
                root_list = sorted(list(set(full_list) - set(rm_list0)))
                full_list = rm_list0
            rm_list1 = sorted(list(set(full_list) - set(priority1)))
            if rm_list1 is not full_list:
                core_list = sorted(list(set(full_list) - set(rm_list1)))
                full_list = rm_list1
            rm_list2 = sorted(list(set(full_list) - set(priority2)))
            if rm_list2 is not full_list:
                base_list = sorted(list(set(full_list) - set(rm_list2)))
                full_list = rm_list2

            page_list1 = []
            page_list2 = []
            page_list3 = []

            if len(root_list) > 0:
                self.p.set_val_by_name("cfg_eeprom_total", "#4", f"{(1 + len(core_list) + len(base_list) + len(full_list)):X}")
                self.p.set_val_by_name("cfg_eeprom_base", "#4", f"{(1 + len(core_list) + len(base_list)):X}")
                self.p.set_val_by_name("cfg_eeprom_core", "#4", f"{(1 + len(core_list)):X}")
                page_list1.append(root_list[0])
                self.eep.v.txt_main.set(" ".join(root_list))

            if len(core_list) > 0:
                for page in core_list:
                    page_list1.append(page)
                page_list1 = list(set(page_list1) - set(self.eep.v.pri_main.get().split()))

            if len(base_list) > 0:
                for page in base_list:
                    page_list2.append(page)
                page_list2 = list(set(page_list2) - set(self.eep.v.pri_main.get().split()))

            if len(full_list) > 0:
                for page in full_list:
                    page_list3.append(page)
                page_list3 = list(set(page_list3) - set(self.eep.v.pri_main.get().split()))

            self.eep.v.txt_core.set(" ".join(sorted(page_list1)))
            self.eep.v.txt_base.set(" ".join(sorted(page_list2)))
            priority3 = " ".join(sorted(page_list3))
            self.p.tkst_write(self.eep_txt_full, delete=True)
            self.p.tkst_write(self.eep_txt_full, text=priority3)

            return byte_list

        root_list = []
        core_list = []
        base_list = []
        full_list = export_list.copy()
        rm_list0 = sorted(list(set(full_list) - set(priority0)))
        if rm_list0 is not full_list:
            root_list = sorted(list(set(full_list) - set(rm_list0)))
            full_list = rm_list0
        rm_list1 = sorted(list(set(full_list) - set(priority1)))
        if rm_list1 is not full_list:
            core_list = sorted(list(set(full_list) - set(rm_list1)))
            full_list = rm_list1
        rm_list2 = sorted(list(set(full_list) - set(priority2)))
        if rm_list2 is not full_list:
            base_list = sorted(list(set(full_list) - set(rm_list2)))
            full_list = rm_list2

        byte_list = []
        page_list1= []
        page_list2= []
        page_list3= []

        if len(root_list) > 0:
            self.p.set_val_by_name("cfg_eeprom_total", "#4", f"{(1 + len(core_list) + len(base_list) + len(full_list)):X}")
            self.p.set_val_by_name("cfg_eeprom_base", "#4", f"{(1 + len(core_list) + len(base_list)):X}")
            self.p.set_val_by_name("cfg_eeprom_core", "#4", f"{(1 + len(core_list)):X}")
            byte_list.extend(self.generate_page(root_list[0]))
            page_list1.append(root_list[0])
            self.eep.v.txt_main.set(" ".join(root_list))

        if len(core_list) > 0:
            for page in core_list:
                page_list1.append(page)
                if page in import_list:
                    byte_list.extend(self.page_reload(page))
                else:
                    byte_list.extend(self.generate_page(page))
            page_list1 = list(set(page_list1) - set(self.eep.v.pri_main.get().split()))

        if len(base_list) > 0:
            for page in base_list:
                page_list2.append(page)
                if page in import_list:
                    byte_list.extend(self.page_reload(page))
                else:
                    byte_list.extend(self.generate_page(page))
            page_list2 = list(set(page_list2) - set(self.eep.v.pri_main.get().split()))

        if len(full_list) > 0:
            for page in full_list:
                page_list3.append(page)
                if page in import_list:
                    byte_list.extend(self.page_reload(page))
                else:
                    byte_list.extend(self.generate_page(page))
            page_list3 = list(set(page_list3) - set(self.eep.v.pri_main.get().split()))

        self.eep.v.txt_core.set(" ".join(sorted(page_list1)))
        self.eep.v.txt_base.set(" ".join(sorted(page_list2)))
        priority3 = " ".join(sorted(page_list3))
        self.p.tkst_write(self.eep_txt_full, delete=True)
        self.p.tkst_write(self.eep_txt_full, text=priority3)

        return byte_list

    def export_plain_txt(self):
        byte_list = self.export_common()
        if len(byte_list) == 0:
            return

        txtfilename = filedialog.asksaveasfilename(filetypes=(("Text files", "*.txt"), ("All Files", "*.*")))
        if not txtfilename.lower().endswith(".txt"):
            txtfilename += ".txt"
        txt = open(txtfilename, "w")
        for b in byte_list:
            txt.write(b + "\n")
        txt.close()
    
    def export_tmd_cmd(self):
        byte_list = self.export_common()
        if len(byte_list) == 0:
            return

        byte_list_16 = []
        for sixteenth in range(0, len(byte_list), 16):
            byte_list_16.append(byte_list[sixteenth: sixteenth + 16] + [""] * (16 - len(byte_list[sixteenth:sixteenth + 16])))

        text = " MESSAGE  = \"EEPROM Write BEGIN\"\n I2C1_CFG = 0x51, 100000, 2, OFF ; 2byte regs ==> M\n EXT2_CFG = OUT\n EXT2  = L   ; EEP_WP disable\n\n"
        for (i, b_list) in list(enumerate(byte_list_16)):
            hex = f"{i:03X}"
            text += " DELAYMS = 20\nWREG3 = " + f"0x{hex}0 , "
            for (j, b) in list(enumerate(b_list)):
                if b == "":
                    continue
                text += f"0x{b},"
                if j in (3, 7, 11):
                    text += " "
            if text[-1] == " ":
                text = text[:-2] + "\n"
            elif text[-1] == ",":
                text = text[:-1] + "\n"
        text += "\n DELAYMS  = 100\n EXT2_CFG = IN\n MESSAGE  = \"EEPROM Write END\"\n"

        txtfilename = filedialog.asksaveasfilename(filetypes=(("Text files", "*.txt"), ("All Files", "*.*")))
        if not txtfilename.lower().endswith(".txt"):
            txtfilename += ".txt"
        txt = open(txtfilename, "w")
        txt.write(text)
        txt.close()

    def generate_page(self, pg_hex):
        byte_list = []
        pg_dec = int(pg_hex, 16)

        try:
            pg_idx = self.spl.pages_unique.index(pg_dec)
        except ValueError:
            messagebox.showerror("EEPROM Write Result", "Page " + pg_hex + " Does Not Exist")
            return byte_list
        else:
            if self.tst.l.wo_cnt[pg_idx] < 0:
                return byte_list

        pg_wo = self.tst.l.wo_cnt[pg_idx]
        sumcheck = pg_dec + pg_wo
        byte_list.append(pg_hex)
        byte_list.append(f"{pg_wo:02X}")

        for k in range(pg_wo + 1):
            if (pg_hex in self.eep.v.check_mod.get().split()) & (pg_hex not in self.eep.v.import_rom.get().split()):
                if pg_hex.upper() == "ED":
                    if self.ed_hid1_tree.tag_has("modified", "237-" + str(k)) | self.ed_hid1_tree.tag_has("eeprom", "237-" + str(k)) | self.ed_hid1_tree.tag_has("edid", "237-" + str(k)):
                        byte_hex = self.ed_hid1_tree.item(str(pg_dec) + "-" + str(k), "value")[1]
                    else:
                        if self.adr.hexa_per_pg_mod[pg_idx][k] == "-":
                            byte_hex = "00"
                        else:
                            byte_hex = self.eep.d.eep_imp_pg[pg_hex].split()[k + 1]
                else:
                    if self.reg_tab.hid1_tree.tag_has("modified", str(pg_dec) + "-" + str(k)) | self.reg_tab.hid1_tree.tag_has("eeprom", str(pg_dec) + "-" + str(k)):
                        byte_hex = self.reg_tab.hid1_tree.item(str(pg_dec) + "-" + str(k), "value")[1]
                    else:
                        if self.adr.hexa_per_pg_mod[pg_idx][k] == "-":
                            byte_hex = "00"
                        else:
                            byte_hex = self.eep.d.eep_imp_pg[pg_hex].split()[k + 1]
            else:
                if self.adr.hexa_per_pg_mod[pg_idx][k] == "-":
                    byte_hex = "00"
                else:
                    byte_hex = self.eep.d.eep_imp_pg[pg_hex].split()[k + 1]
            byte_dec = int(byte_hex, 16)
            byte_list.append(byte_hex)
            sumcheck = (sumcheck + byte_dec) % 256

        crc = (int(self.eep.v.crc_ofs.get(), 16) + 256 - sumcheck) % 256
        byte_list.append(f"{crc:02X}")

        return byte_list

    def page_reload(self, page):
        byte_list = self.eep.d.eep_imp_pg[page].split()
        byte_list.insert(0, page)
        return byte_list

    # Import Tab
    def eep_import(self):
        if len(self.spl.pages_unique) == 0:
            messagebox.showerror("ERROR", "Must Import Excel")
            return

        byte_text = self.open_file()

        if self.txtfilename == self.eep.v.txtfile[1].get()[10:]:
            return

        self.eep.v.txtfile[1].set("")

        if len(byte_text) == 0:
            return

        mod_pages = []
        imp_dict = {}
        k = 0
        while k < len(byte_text):
            pg_dec = str(int(byte_text[k], 16))
            if int(pg_dec) not in self.spl.pages_unique:
                break
            n = int(byte_text[k + 1], 16) + 4
            mod_pages.append(pg_dec)
            imp_dict[pg_dec] = " ".join(byte_text[k + 1:k + n])
            k += n
        mod_pages = sorted(mod_pages, key=int)

        self.imp_tree.delete(*self.imp_tree.get_children())

        for pg in mod_pages:
            eep_hexa = imp_dict[pg].split()[1:-1]
            self.imp_tree.insert("", END, iid=pg, text="Page " + f"{int(pg):02X}", values=("", "", "", "\u2610"))
            for (i, hex) in list(enumerate(eep_hexa)):
                self.imp_tree.insert(pg, i, iid=pg + "-" + str(i), text=str(i), values=(f"{int(hex, 16):08b}", hex.upper(), self.adr.desc_icon[self.adr.pg_and_num.index(pg + "-" + str(i))], "\u2610"))
                if pg + "-" + str(i) not in [x.split("(")[0] for x in self.spl.addr_total]:
                    self.imp_tree.item(pg + "-" + str(i), tag="gray")
                elif hex == self.adr.hexa[self.adr.pg_and_num.index(pg + "-" + str(i))]:
                    self.imp_tree.item(pg + "-" + str(i), tag="gray")
            if len(set(self.imp_tree.get_children(pg)) - set(self.imp_tree.tag_has("gray"))) == 0:
                self.imp_tree.item(pg, tag="gray")

        self.eep.v.txtfile[1].set("Imported: " + self.txtfilename)

    def check(self, event):
        col = self.imp_tree.identify_column(event.x)
        row = self.imp_tree.identify_row(event.y)
        val = self.imp_tree.item(row, "value")

        self.desc(col, row, val)

        if (row == "") | (col != "#4") | (row in self.imp_tree.tag_has("gray")):
            return

        if val[3] == "\u2610":
            if "-" not in row:
                self.imp_tree.set(row, column="#4", value="\u2611")
                self.imp_tree.item(row, tag="check")
                for child in list(set(self.imp_tree.get_children(row)) - set(self.imp_tree.tag_has("gray"))):
                    self.imp_tree.set(child, column="#4", value="\u2611")
                    self.imp_tree.item(child, tag="check")
            else:
                self.imp_tree.set(row, column="#4", value="\u2611")
                self.imp_tree.item(row, tag="check")
                self.imp_tree.item(self.imp_tree.parent(row), tag="check")
                if len(set(self.imp_tree.get_children(self.imp_tree.parent(row))) - set(self.imp_tree.tag_has("gray")) - set(self.imp_tree.tag_has("check"))) == 0:
                    self.imp_tree.set(self.imp_tree.parent(row), column="#4", value="\u2611")
                    self.imp_tree.item(self.imp_tree.parent(row), tag="check")
        elif val[3] == "\u2611":
            if "-" not in row:
                self.imp_tree.set(row, column="#4", value="\u2610")
                self.imp_tree.item(row, tag="")
                for child in list(set(self.imp_tree.get_children(row)) - set(self.imp_tree.tag_has("gray"))):
                    self.imp_tree.set(child, column="#4", value="\u2610")
                    self.imp_tree.item(child, tag="")
            else:
                self.imp_tree.set(row, column="#4", value="\u2610")
                self.imp_tree.item(row, tag="")
                self.imp_tree.set(self.imp_tree.parent(row), column="#4", value="\u2610")
                if set(self.imp_tree.get_children(self.imp_tree.parent(row))) - set(self.imp_tree.tag_has("check")) == set(self.imp_tree.get_children(self.imp_tree.parent(row))):
                    self.imp_tree.item(self.imp_tree.parent(row), tag="")

    def desc(self, col, row, val):
        if (row in [str(x) for x in self.spl.pages_unique]) | (row == ""):
            return
        if (col == "#3") & (val[2] != ""):
            messagebox.showinfo(row, self.adr.desc[self.adr.pg_and_num.index(row)])

    def apply_values(self):
        if len(self.imp_tree.get_children()) == 0:
            messagebox.showwarning("WARNING", "Must Import EEPROM")
            return
        if len(self.imp_tree.tag_has("check")) == 0:
            messagebox.showwarning("WARNING", "No Values to Apply")
            return

        not_exist = []
        cnt = 0
        for iid in self.imp_tree.tag_has("check"):
            if "-" not in iid:
                if iid not in self.reg.l.modified_pg:
                    self.reg.l.modified_pg.append(iid)
                if iid not in self.eep.l.mod_by_eep_pg:
                    self.eep.l.mod_by_eep_pg.append(iid)
                continue
            if iid not in [x.split("(")[0] for x in self.spl.addr_total]:
                not_exist.append(iid)
                continue

            new_val = self.imp_tree.item(iid, "value")[1]
            pg, num = iid.split("-")
            pg_idx = self.spl.pages_unique.index(int(pg))

            if pg != "237":
                self.reg_tab.modify1(pg + " " + self.adr.num_range[pg_idx][int(num) // 16], pg, int(num), new_val, mod_tag="eeprom")
            elif pg == "237":
                self.ed_modify1(pg + " " + self.adr.num_range[pg_idx][int(num) // 16], pg, int(num), new_val, mod_tag="eeprom")
            cnt += 1

        if (self.eep.v.txtfile[1].get()[10:] not in self.reg.l.xlsx_list) & (cnt != 0):
            self.eep.l.imported_txt.append(self.eep.v.txtfile[1].get()[10:])
            self.reg.l.xlsx_list.append(self.eep.v.txtfile[1].get()[10:])
            self.reg.v.xlsx_names.set("\n".join(self.reg.l.xlsx_list))

        if len(not_exist) > 0:
            messagebox.showwarning("WARNING", ", ".join(not_exist) + "Does Not Exist")

        messagebox.showinfo("Apply Values to Register Files", "Complete")

    def select_all(self):
        for parent in self.imp_tree.get_children():
            if self.imp_tree.tag_has("gray", parent):
                continue
            self.imp_tree.item(parent, tag="check")
            self.imp_tree.set(parent, column="#4", value="\u2611")
            for child in self.imp_tree.get_children(parent):
                if self.imp_tree.tag_has("gray", child):
                    continue
                self.imp_tree.item(child, tag="check")
                self.imp_tree.set(child, column="#4", value="\u2611")

    def clear_all(self):
        for iid in self.imp_tree.tag_has("check"):
            self.imp_tree.item(iid, tag="")
            self.imp_tree.set(iid, column="#4", value="\u2610")

    def reset_eep(self):
        self.imp_tree.delete(*self.imp_tree.get_children())
        self.eep.v.txtfile[1].set("")
    
    def show_hide(self, choice):
        if choice.lower() == "name":
            if self.eep.v.ed_check0.get() == 0:
                self.edid_note.hide(self.ed_hid0)
            elif self.eep.v.ed_check0.get() == 1:
                self.edid_note.add(self.ed_hid0)
        elif choice.lower() == "addr":
            if self.eep.v.ed_check1.get() == 0:
                self.edid_note.hide(self.ed_hid1)
            elif self.eep.v.ed_check1.get() == 1:
                self.edid_note.add(self.ed_hid1)

    # EDID - Data Tab
    def calc_bp(self, num, type):
        if num not in (0, 1, 2, 3):
            raise ValueError("Invalid argument value in calc_bp(): 'num'")

        if type.upper() == "H":
            bl = self.eep.v.hbl[num]
            fp = self.eep.v.hfp[num]
            bp = self.eep.v.hbp[num]
            sy = self.eep.v.hsy[num]
        elif type.upper() == "V":
            bl = self.eep.v.vbl[num]
            fp = self.eep.v.vfp[num]
            bp = self.eep.v.vbp[num]
            sy = self.eep.v.vsy[num]
        else:
            raise ValueError("Invalid argument value in calc_bp(): 'type'")

        if (bl.get() == "") | (fp.get() == "") | (sy.get() == ""):
            bp.set("")
        else:
            try:
                bp.set(int(bl.get()) - int(fp.get()) - int(sy.get()))
            except ValueError:
                bp.set("")

    def calc_freq(self, num):
        if num not in (0, 1, 2, 3):
            raise ValueError("Invalid argument value in calc_freq(): 'num'")

        missing = []
        if self.eep.v.rfsh[num].get() == "":
            missing.append("Refresh Rate")
        if self.eep.v.hac[num].get() == "":
            missing.append("H active")
        if self.eep.v.hbl[num].get() == "":
            missing.append("H blank")
        if self.eep.v.vac[num].get() == "":
            missing.append("V active")
        if self.eep.v.vbl[num].get() == "":
            missing.append("V blank")

        if len(missing) > 0:
            if len(missing) > 1:
                missing.insert(-1, "and")
            msg = "Missing " + ", ".join(missing).replace("and, ", "and ")
            messagebox.showerror("MISSING INPUT", msg)
            return

        try:
            self.eep.v.freq[num].set(round(float(self.eep.v.rfsh[num].get()) * (float(self.eep.v.hac[num].get()) + float(self.eep.v.hbl[num].get())) * (float(self.eep.v.vac[num].get()) + float(self.eep.v.vbl[num].get())) * (10 ** -6), 2))
        except ValueError:
            messagebox.showerror("INPUT ERROR", "Input a Valid Number")

    def calc_rfsh(self, num):
        if num not in (0, 1, 2, 3):
            raise ValueError("Invalid argument value in calc_rfsh(): 'num'")

        missing = []
        if self.eep.v.freq[num].get() == "":
            missing.append("Frequency")
        if self.eep.v.hac[num].get() == "":
            missing.append("H active")
        if self.eep.v.hbl[num].get() == "":
            missing.append("H blank")
        if self.eep.v.vac[num].get() == "":
            missing.append("V active")
        if self.eep.v.vbl[num].get() == "":
            missing.append("V blank")

        if len(missing) > 0:
            if len(missing) > 1:
                missing.insert(-1, "and")
            msg = "Missing " + ", ".join(missing).replace("and, ", "and ")
            messagebox.showerror("MISSING INPUT", msg)
            return

        try:
            self.eep.v.rfsh[num].set(round(float(self.eep.v.freq[num].get()) * (10 ** 6) / ((float(self.eep.v.hac[num].get()) + float(self.eep.v.hbl[num].get())) * (float(self.eep.v.vac[num].get()) + float(self.eep.v.vbl[num].get()))), 2))
        except ValueError:
            messagebox.showerror("INPUT ERROR", "Input a Valid Number")
        except ZeroDivisionError:
            messagebox.showerror("INPUT ERROR", "Zero in Denominator")

    def calc_crc(self):
        ed_bina = self.ed_update_bina()
        if len(ed_bina) == 0:
            messagebox.showwarning("WARNING", "Must Add Excel")
            return
        if ed_bina is False:
            messagebox.showwarning("WARNING", "Not Enough Data in EDID")
            return

        sum = 0
        for bin in ed_bina[:127]:
            sum += int(bin, 2)
        crc = 256 - int(f"{sum:02X}"[-2:], 16)
        self.eep.v.edid_checksum.set(f"{crc:02X}")

    def ed_load(self):
        for i in range(4):
            self.eep.v.rfsh[i].set("")
        for iid in self.ed_name_tree.get_children():
            name = self.ed_name_tree.item(iid, "text")
            val = self.ed_name_tree.item(iid, "value")
            if name == "EDID_checksum":
                self.eep.v.edid_checksum.set(val[3])
            for i in range(4):
                if name == f"EDID_desc{i + 1}_px_clk_10kHz":
                    self.eep.v.freq[i].set(round(int(val[2]) / 100, 2))
                elif name == f"EDID_desc{i + 1}_Hactive":
                    self.eep.v.hac[i].set(val[2])
                elif name == f"EDID_desc{i + 1}_Hblank":
                    self.eep.v.hbl[i].set(val[2])
                elif name == f"EDID_desc{i + 1}_HB_fp":
                    self.eep.v.hfp[i].set(val[2])
                elif name == f"EDID_desc{i + 1}_HB_sync":
                    self.eep.v.hsy[i].set(val[2])
                elif name == f"EDID_desc{i + 1}_Vactive":
                    self.eep.v.vac[i].set(val[2])
                elif name == f"EDID_desc{i + 1}_Vblank":
                    self.eep.v.vbl[i].set(val[2])
                elif name == f"EDID_desc{i + 1}_VB_fp":
                    self.eep.v.vfp[i].set(val[2])
                elif name == f"EDID_desc{i + 1}_VB_sync":
                    self.eep.v.vsy[i].set(val[2])

    def ed_set(self):
        new_bina = self.ed_update_bina()
        old_bina = self.adr.bina_mod[-128:]
        for (i, bin) in list(enumerate(new_bina)):
            if bin != old_bina[i]:
                self.ed_modify1("237 " + self.adr.num_range[self.spl.pages_unique.index(237)][i // 16], "237", i, f"{int(bin, 2):02X}", mod_tag="edid")

        self.ed_modified()

        messagebox.showinfo("Set Data to Register Files", "Complete")
    
    def ed_set_default(self):
        self.set_defaults()
        
        new_bina = self.ed_update_bina()
        old_bina = self.adr.bina_mod[-128:]
        for (num, bin) in list(enumerate(new_bina)):
            if bin != old_bina[num]:
                pg_idx = self.spl.pages_unique.index(237)
                self.ed_modify1("237 " + self.adr.num_range[pg_idx][num // 16], "237", num, f"{int(bin, 2):02X}", mod_tag="")
                spl_idx = []
                mer_idx = []
                adr_idx = self.adr.l.pg_and_num.index("237-" + str(num))
                for (i, pg_num) in list(enumerate([x.split("(")[0] for x in self.spl.addr_total])):
                    if pg_num == "237-" + str(num):
                        spl_idx.append(i)
                for j in spl_idx:
                    for (k, name) in self.mer.l.names:
                        if name == self.spl.l.names_wo_width[j]:
                            mer_idx.append(k)
                for s_idx in spl_idx:
                    self.spl.bina[s_idx] = self.spl.bina_mod[s_idx]
                    self.spl.deci[s_idx] = self.spl.deci_mod[s_idx]
                    self.spl.hexa[s_idx] = self.spl.hexa_mod[s_idx]
                for m_idx in mer_idx:
                    self.mer.bina[m_idx] = self.mer.bina_mod[m_idx]
                    self.mer.deci[m_idx] = self.mer.deci_mod[m_idx]
                    self.mer.hexa[m_idx] = self.mer.hexa_mod[m_idx]
                self.adr.bina[adr_idx] = self.adr.bina_mod[adr_idx]
                self.adr.hexa[adr_idx] = self.adr.hexa_mod[adr_idx]
                self.adr.hexa_per_pg[pg_idx][num] = self.adr.hexa_per_pg_mod[pg_idx][num]

    def reset_to_default(self):
        for i in range(4):
            self.eep.v.hac[i].set(self.eep.v.hac_default[i].get())
            self.eep.v.hbl[i].set(self.eep.v.hbl_default[i].get())
            self.eep.v.hfp[i].set(self.eep.v.hfp_default[i].get())
            self.eep.v.hsy[i].set(self.eep.v.hsy_default[i].get())
            self.eep.v.vac[i].set(self.eep.v.vac_default[i].get())
            self.eep.v.vbl[i].set(self.eep.v.vbl_default[i].get())
            self.eep.v.vfp[i].set(self.eep.v.vfp_default[i].get())
            self.eep.v.vsy[i].set(self.eep.v.vsy_default[i].get())
            self.eep.v.freq[i].set(self.eep.v.freq_default[i].get())
            self.eep.v.rfsh[i].set(self.eep.v.rfsh_default[i].get())
        self.eep.v.edid_checksum.set(self.eep.v.edid_checksum_default.get())

    def ed_update_bina(self):
        if len(self.ed_hid1_tree.get_children()) == 0:
            return []
        elif len(self.ed_hid1_tree.get_children()) != 128:
            return False

        ed_bina = []
        for n in self.ed_hid1_tree.get_children():
            ed_bina.append(self.ed_hid1_tree.item(n, "value")[0])

        inp_err = []
        for iid in self.ed_hid0_tree.get_children():
            name = self.ed_hid0_tree.item(iid, "text")
            val = self.ed_hid0_tree.item(iid, "value")
            for i in range(4):
                if self.eep.v.hac[i].get() != "":
                    if name == f"EDID_desc{i + 1}_Hactive":
                        try:
                            bin = f"{int(self.eep.v.hac[i].get()):b}".zfill(len(self.mer.bina[self.mer.names.index(name)]))
                            num = val[6].split("(")[0].split("-")[1]
                            bit = val[6].strip(")").split("(")[1]
                            if ":" in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0]):len(bin) - int(val[0].split(":")[1])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit.split(":")[1]), int(bit.split(":")[0]), new_bin, text=ed_bina[int(num)])
                            elif ":" not in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit), None, new_bin, text=ed_bina[int(num)])
                        except ValueError:
                            if f"hac{i + 1}" not in inp_err:
                                inp_err.append(f"hac{i + 1}")
                if self.eep.v.hbl[i].get() != "":
                    if name == f"EDID_desc{i + 1}_Hblank":
                        try:
                            bin = f"{int(self.eep.v.hbl[i].get()):b}".zfill(len(self.mer.bina[self.mer.names.index(name)]))
                            num = val[6].split("(")[0].split("-")[1]
                            bit = val[6].strip(")").split("(")[1]
                            if ":" in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0]):len(bin) - int(val[0].split(":")[1])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit.split(":")[1]), int(bit.split(":")[0]), new_bin, text=ed_bina[int(num)])
                            elif ":" not in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit), None, new_bin, text=ed_bina[int(num)])
                        except ValueError:
                            if f"hbl{i + 1}" not in inp_err:
                                inp_err.append(f"hbl{i + 1}")
                if self.eep.v.hfp[i].get() != "":
                    if name == f"EDID_desc{i + 1}_HB_fp":
                        try:
                            bin = f"{int(self.eep.v.hfp[i].get()):b}".zfill(len(self.mer.bina[self.mer.names.index(name)]))
                            num = val[6].split("(")[0].split("-")[1]
                            bit = val[6].strip(")").split("(")[1]
                            if ":" in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0]):len(bin) - int(val[0].split(":")[1])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit.split(":")[1]), int(bit.split(":")[0]), new_bin, text=ed_bina[int(num)])
                            elif ":" not in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit), None, new_bin, text=ed_bina[int(num)])
                        except ValueError:
                            if f"hfp{i + 1}" not in inp_err:
                                inp_err.append(f"hfp{i + 1}")
                if self.eep.v.hsy[i].get() != "":
                    if name == f"EDID_desc{i + 1}_HB_sync":
                        try:
                            bin = f"{int(self.eep.v.hsy[i].get()):b}".zfill(len(self.mer.bina[self.mer.names.index(name)]))
                            num = val[6].split("(")[0].split("-")[1]
                            bit = val[6].strip(")").split("(")[1]
                            if ":" in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0]):len(bin) - int(val[0].split(":")[1])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit.split(":")[1]), int(bit.split(":")[0]), new_bin, text=ed_bina[int(num)])
                            elif ":" not in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit), None, new_bin, text=ed_bina[int(num)])
                        except ValueError:
                            if f"hac{i + 1}" not in inp_err:
                                inp_err.append(f"hsy{i + 1}")
                if self.eep.v.vac[i].get() != "":
                    if name == f"EDID_desc{i + 1}_Vactive":
                        try:
                            bin = f"{int(self.eep.v.vac[i].get()):b}".zfill(len(self.mer.bina[self.mer.names.index(name)]))
                            num = val[6].split("(")[0].split("-")[1]
                            bit = val[6].strip(")").split("(")[1]
                            if ":" in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0]):len(bin) - int(val[0].split(":")[1])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit.split(":")[1]), int(bit.split(":")[0]), new_bin, text=ed_bina[int(num)])
                            elif ":" not in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit), None, new_bin, text=ed_bina[int(num)])
                        except ValueError:
                            if f"hac{i + 1}" not in inp_err:
                                inp_err.append(f"vac{i + 1}")
                if self.eep.v.vbl[i].get() != "":
                    if name == f"EDID_desc{i + 1}_Vblank":
                        try:
                            bin = f"{int(self.eep.v.vbl[i].get()):b}".zfill(len(self.mer.bina[self.mer.names.index(name)]))
                            num = val[6].split("(")[0].split("-")[1]
                            bit = val[6].strip(")").split("(")[1]
                            if ":" in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0]):len(bin) - int(val[0].split(":")[1])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit.split(":")[1]), int(bit.split(":")[0]), new_bin, text=ed_bina[int(num)])
                            elif ":" not in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit), None, new_bin, text=ed_bina[int(num)])
                        except ValueError:
                            if f"hac{i + 1}" not in inp_err:
                                inp_err.append(f"vbl{i + 1}")
                if self.eep.v.vfp[i].get() != "":
                    if name == f"EDID_desc{i + 1}_VB_fp":
                        try:
                            bin = f"{int(self.eep.v.vfp[i].get()):b}".zfill(len(self.mer.bina[self.mer.names.index(name)]))
                            num = val[6].split("(")[0].split("-")[1]
                            bit = val[6].strip(")").split("(")[1]
                            if ":" in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0]):len(bin) - int(val[0].split(":")[1])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit.split(":")[1]), int(bit.split(":")[0]), new_bin, text=ed_bina[int(num)])
                            elif ":" not in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit), None, new_bin, text=ed_bina[int(num)])
                        except ValueError:
                            if f"hac{i + 1}" not in inp_err:
                                inp_err.append(f"vfp{i + 1}")
                if self.eep.v.vsy[i].get() != "":
                    if name == f"EDID_desc{i + 1}_VB_sync":
                        try:
                            bin = f"{int(self.eep.v.vsy[i].get()):b}".zfill(len(self.mer.bina[self.mer.names.index(name)]))
                            num = val[6].split("(")[0].split("-")[1]
                            bit = val[6].strip(")").split("(")[1]
                            if ":" in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0]):len(bin) - int(val[0].split(":")[1])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit.split(":")[1]), int(bit.split(":")[0]), new_bin, text=ed_bina[int(num)])
                            elif ":" not in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit), None, new_bin, text=ed_bina[int(num)])
                        except ValueError:
                            if f"hac{i + 1}" not in inp_err:
                                inp_err.append(f"vsy{i + 1}")
                if self.eep.v.freq[i].get() != "":
                    if name == f"EDID_desc{i + 1}_px_clk_10kHz":
                        try:
                            bin = f"{floor(float(self.eep.v.freq[i].get()) * 100):b}".zfill(len(self.mer.bina[self.mer.names.index(name)]))
                            num = val[6].split("(")[0].split("-")[1]
                            bit = val[6].strip(")").split("(")[1]
                            if ":" in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0]):len(bin) - int(val[0].split(":")[1])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit.split(":")[1]), int(bit.split(":")[0]), new_bin, text=ed_bina[int(num)])
                            elif ":" not in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit), None, new_bin, text=ed_bina[int(num)])
                        except ValueError:
                            if f"freq{i + 1}" not in inp_err:
                                inp_err.append(f"freq{i + 1}")
            if self.eep.v.edid_checksum.get() != "":
                    if name == "EDID_checksum":
                        try:
                            bin = f"{int(self.eep.v.edid_checksum.get(), 16):b}".zfill(len(self.mer.bina[self.mer.names.index(name)]))
                            num = val[6].split("(")[0].split("-")[1]
                            bit = val[6].strip(")").split("(")[1]
                            if ":" in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0]):len(bin) - int(val[0].split(":")[1])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit.split(":")[1]), int(bit.split(":")[0]), new_bin, text=ed_bina[int(num)])
                            elif ":" not in val[0]:
                                new_bin = bin[len(bin) - 1 - int(val[0].split(":")[0])]
                                ed_bina[int(num)] = self.p.replace_text(int(bit), None, new_bin, text=ed_bina[int(num)])
                        except ValueError:
                            if "checksum" not in inp_err:
                                inp_err.append("checksum")
            
        for i in range(4):
            if f"hac{i + 1}" in inp_err:
                messagebox.showerror("INPUT ERROR", f"Invalid Entry: Descriptor {i + 1} H active")
            if f"hbl{i + 1}" in inp_err:
                messagebox.showerror("INPUT ERROR", f"Invalid Entry: Descriptor {i + 1} H blank")
            if f"hfp{i + 1}" in inp_err:
                messagebox.showerror("INPUT ERROR", f"Invalid Entry: Descriptor {i + 1} H front-porch")
            if f"hsy{i + 1}" in inp_err:
                messagebox.showerror("INPUT ERROR", f"Invalid Entry: Descriptor {i + 1} H sync")
            if f"vac{i + 1}" in inp_err:
                messagebox.showerror("INPUT ERROR", f"Invalid Entry: Descriptor {i + 1} V active")
            if f"vbl{i + 1}" in inp_err:
                messagebox.showerror("INPUT ERROR", f"Invalid Entry: Descriptor {i + 1} V blank")
            if f"vfp{i + 1}" in inp_err:
                messagebox.showerror("INPUT ERROR", f"Invalid Entry: Descriptor {i + 1} V front-porch")
            if f"vsy{i + 1}" in inp_err:
                messagebox.showerror("INPUT ERROR", f"Invalid Entry: Descriptor {i + 1} V sync")
            if f"freq{i + 1}" in inp_err:
                messagebox.showerror("INPUT ERROR", f"Invalid Entry: Descriptor {i + 1} Frequency")
        if "checksum" in inp_err:
            messagebox.showerror("INPUT ERROR", "Invalid Entry: Checksum")

        return ed_bina
    
    def set_defaults(self):
        for i in range(4):
            self.eep.v.hac_default[i].set(self.eep.v.hac[i].get())
            self.eep.v.hbl_default[i].set(self.eep.v.hbl[i].get())
            self.eep.v.hfp_default[i].set(self.eep.v.hfp[i].get())
            self.eep.v.hsy_default[i].set(self.eep.v.hsy[i].get())
            self.eep.v.vac_default[i].set(self.eep.v.vac[i].get())
            self.eep.v.vbl_default[i].set(self.eep.v.vbl[i].get())
            self.eep.v.vfp_default[i].set(self.eep.v.vfp[i].get())
            self.eep.v.vsy_default[i].set(self.eep.v.vsy[i].get())
            self.eep.v.freq_default[i].set(self.eep.v.freq[i].get())
            self.eep.v.rfsh_default[i].set(self.eep.v.rfsh[i].get())
        self.eep.v.edid_checksum_default.set(self.eep.v.edid_checksum.get())
    
    # ed_name_tree click event
    def ed_popup0(self, event, click_type):
        col = self.ed_name_tree.identify_column(event.x)
        row = self.ed_name_tree.identify_row(event.y)
        name = self.ed_name_tree.item(row, "text")
        val = self.ed_name_tree.item(row, "value")
        if (row in self.spl.groups_unique) | (row == ""):
            return
        if click_type == 1:
            self.ed_popup_entry0(col, row, name, val)
        elif click_type == 3:
            self.ed_popup_desc0(col, row, name, val)
        else:
            raise ValueError("Invalid argument value in ed_popup0(): 'click_type'")

    def ed_popup_entry0(self, col, row, name, val):
        bin_valid = re.compile(r"[^01]")
        dec_valid = re.compile(r"[^0-9]")
        hex_valid = re.compile(r"[^0-9a-fA-F]")

        if (col == "#2") & (val[1] != "-"):
            new_value = simpledialog.askstring(name, "Please enter a new BINARY value", initialvalue=val[1])
            if (new_value is None) | (new_value == ""):
                return
            if bin_valid.search(new_value) is not None:
                messagebox.showerror("INPUT ERROR", "Input a Valid BINARY Number!\n\"" + new_value + "\" is Not Valid")
                return
            if len(new_value) > len(val[1]):
                new_value = new_value[-len(val[1]):]
            if new_value.zfill(len(val[1])) != val[1]:
                self.ed_modify0(col, row, name, val, new_value)

        if (col == "#3") & (val[2] != "-"):
            new_value = simpledialog.askstring(name, "Please enter a new DECIMAL value", initialvalue=val[2])
            if (new_value is None) | (new_value == ""):
                return
            if dec_valid.search(new_value) is not None:
                messagebox.showerror("INPUT ERROR", "Input a Valid DECIMAL Number!\n\"" + new_value + "\" is Not Valid")
            elif new_value != val[2]:
                if int(new_value) > int("1" * len(self.mer.bina[int(row)]), 2):
                    new_value = str(int("1" * len(self.mer.bina[int(row)]), 2))
                    if new_value == val[2]:
                        return
                self.ed_modify0(col, row, name, val, new_value)

        if (col == "#4") & (val[3] != "-"):
            new_value = simpledialog.askstring(name, "Please enter a new HEXADECIMAL value", initialvalue=val[3])
            if (new_value is None) | (new_value == ""):
                return
            if hex_valid.search(new_value) is not None:
                messagebox.showerror("INPUT ERROR", "Input a Valid HEXADECIMAL Number!\n\"" + new_value + "\" is Not Valid")
                return
            if len(new_value) > len(val[3]):
                new_value = new_value[-len(val[3]):]
            if new_value.zfill(len(val[3])).upper() != val[3]:
                if int(new_value, 16) > int("1" * len(self.mer.bina[int(row)]), 2):
                    new_value = f"{int('1' * len(self.mer.bina[int(row)]), 2):X}".zfill(len(val[3]))
                    if new_value == val[3]:
                        return
                self.ed_modify0(col, row, name, val, new_value)

    def ed_popup_desc0(self, col, row, name, val):
        if (col == "#5") & (val[4] != ""):
            messagebox.showinfo(name, self.mer.desc[int(row)])

    def ed_modify0(self, col, row, name, val, new, mod_tag="modified"):
        if col == "#2":
            if val[1] == new.zfill(len(self.mer.bina[int(row)])):
                return
            self.mer.bina_mod[int(row)] = new.zfill(len(self.mer.bina[int(row)]))
            self.mer.deci_mod[int(row)] = int(new, 2)
            self.mer.hexa_mod[int(row)] = f"{int(new, 2):X}".zfill(len(val[3]))
        if col == "#3":
            if val[2] == new:
                return
            self.mer.bina_mod[int(row)] = f"{int(new):b}".zfill(len(self.mer.bina[int(row)]))
            self.mer.deci_mod[int(row)] = new
            self.mer.hexa_mod[int(row)] = f"{int(new):X}".zfill(len(val[3]))
        if col == "#4":
            if val[3] == new.upper().zfill(len(val[3])):
                return
            self.mer.bina_mod[int(row)] = f"{int(new, 16):b}".zfill(len(self.mer.bina[int(row)]))
            self.mer.deci_mod[int(row)] = int(new, 16)
            self.mer.hexa_mod[int(row)] = new.upper().zfill(len(val[3]))

        self.ed_name_tree.set(row, column="#2", value=self.mer.bina_mod[int(row)])
        self.ed_name_tree.set(row, column="#3", value=self.mer.deci_mod[int(row)])
        self.ed_name_tree.set(row, column="#4", value=self.mer.hexa_mod[int(row)])

        self.ed_name_tree.item(row, tag=mod_tag)

        self.ed_mod0_mg2sp(row, name, mod_tag)
        self.ed_mod0_sp2ad(name, mod_tag)
        self.ed_modified()
        self.ed_bin_over_20b(mod=True)

    def ed_mod0_mg2sp(self, row, name, mod_tag):
        spl_iid = []
        if self.spl.names_wo_width.count(name) == 1:
            spl_iid.append(int(row))
            self.spl.bina_mod[int(row)] = self.mer.bina_mod[int(row)]
            self.spl.deci_mod[int(row)] = int(self.spl.bina_mod[int(row)], 2)
            self.spl.hexa_mod[int(row)] = f"{int(self.spl.bina_mod[int(row)], 2):X}".zfill(len(self.spl.hexa_mod[int(row)]))
            self.ed_hid0_tree.item(row + "-split", tag=mod_tag)
        elif self.spl.names_wo_width.count(name) > 1:
            for (i, item) in list(enumerate(self.spl.names_wo_width)):
                if name == item:
                    spl_iid.append(int(row))
                    if ":" in self.spl.widths[i]:
                        large, small = [int(num) for num in self.spl.widths[i].split(":")]
                        self.spl.bina_mod[i] = self.mer.bina_mod[int(row)][len(self.mer.bina_mod[int(row)]) - 1 - large:len(self.mer.bina_mod[int(row)]) - small]
                    elif ":" not in self.spl.widths[i]:
                        self.spl.bina_mod[i] = self.mer.bina_mod[int(row)][len(self.mer.bina_mod[int(row)]) - 1 - int(self.spl.widths[i])]
                    self.spl.deci_mod[i] = int(self.spl.bina_mod[i], 2)
                    self.spl.hexa_mod[i] = f"{int(self.spl.bina_mod[i], 2):X}".zfill(len(self.spl.hexa_mod[i]))
                    self.ed_hid0_tree.item(str(i) + "-split", tag=mod_tag)

        for iid in spl_iid:
            self.ed_hid0_tree.set(str(iid) + "-split", column="#2", value=self.spl.bina_mod[iid])
            self.ed_hid0_tree.set(str(iid) + "-split", column="#3", value=self.spl.deci_mod[iid])
            self.ed_hid0_tree.set(str(iid) + "-split", column="#4", value=self.spl.hexa_mod[iid])

    def ed_mod0_sp2ad(self, name, mod_tag):
        adr_iid = []
        for (i, item) in list(enumerate(self.spl.names_wo_width)):
            if name == item:
                page_num, bit = self.spl.addr_total[i].strip(")").split("(")
                page, num = page_num.split("-")
                adr_iid.append(page_num)

                if ":" in bit:
                    if self.adr.bina_mod[self.adr.pg_and_num.index(page_num)] != self.p.replace_text(int(bit.split(":")[1]), int(bit.split(":")[0]), self.spl.bina_mod[i], text=self.adr.bina_mod[self.adr.pg_and_num.index(page_num)]):
                        self.adr.bina_mod[self.adr.pg_and_num.index(page_num)] = self.p.replace_text(int(bit.split(":")[1]), int(bit.split(":")[0]), self.spl.bina_mod[i], text=self.adr.bina_mod[self.adr.pg_and_num.index(page_num)])
                        self.adr.hexa_mod[self.adr.pg_and_num.index(page_num)] = f"{int(self.adr.bina_mod[self.adr.pg_and_num.index(page_num)], 2):02X}"
                        self.adr.hexa_per_pg_mod[self.spl.pages_unique.index(int(page))][int(num)] = self.adr.hexa_mod[self.adr.pg_and_num.index(page_num)]
                        self.ed_hid1_tree.item(page_num, tag=mod_tag)
                        self.ed_addr_tree.item((page + " " + self.adr.num_range[self.spl.pages_unique.index(int(page))][int(num) // 16]), tag=mod_tag)
                elif ":" not in bit:
                    if self.adr.bina_mod[self.adr.pg_and_num.index(page_num)] != self.p.replace_text(int(bit), None, self.spl.bina_mod[i], text=self.adr.bina_mod[self.adr.pg_and_num.index(page_num)]):
                        self.adr.bina_mod[self.adr.pg_and_num.index(page_num)] = self.p.replace_text(int(bit), None, self.spl.bina_mod[i], text=self.adr.bina_mod[self.adr.pg_and_num.index(page_num)])
                        self.adr.hexa_mod[self.adr.pg_and_num.index(page_num)] = f"{int(self.adr.bina_mod[self.adr.pg_and_num.index(page_num)], 2):02X}"
                        self.adr.hexa_per_pg_mod[self.spl.pages_unique.index(int(page))][int(num)] = self.adr.hexa_mod[self.adr.pg_and_num.index(page_num)]
                        self.ed_hid1_tree.item(page_num, tag=mod_tag)
                        self.ed_addr_tree.item((page + " " + self.adr.num_range[self.spl.pages_unique.index(int(page))][int(num) // 16]), tag=mod_tag)

        for iid in adr_iid:
            self.ed_hid1_tree.set(iid, column="#1", value=self.adr.bina_mod[self.adr.pg_and_num.index(iid)])
            self.ed_hid1_tree.set(iid, column="#2", value=self.adr.hexa_mod[self.adr.pg_and_num.index(iid)])

            pg, num = iid.split("-")
            pg_idx = self.spl.pages_unique.index(int(pg))
            row = pg + " " + self.adr.num_range[pg_idx][int(num) // 16]
            num_l, num_r = [int(x) for x in self.adr.num_range[pg_idx][int(num) // 16].split("~")]
            row_hexa = self.adr.hexa_per_pg_mod[pg_idx][num_l:num_r + 1]
            for i in (4, 9, 14):
                row_hexa.insert(i, "\u250a")
            for (i, hex) in list(enumerate(row_hexa, 1)):
                self.ed_addr_tree.set(row, column="#" + str(i), value=hex)

    # ed_addr_tree click event
    def ed_popup1(self, event, click_type):
        col = self.ed_addr_tree.identify_column(event.x)
        row = self.ed_addr_tree.identify_row(event.y)
        name = self.ed_addr_tree.item(row, "text")
        val = self.ed_addr_tree.item(row, "value")
        if (row in [str(item) for item in self.spl.pages_unique]) | (row == "") | (col == "") | (col == "#20"):
            return
        if val[int(col.strip("#")) - 1] in ("-", "", "\u250a"):
            return
        pg, rng = row.split()
        c = int(col.strip("#")) - 1
        num = self.adr.num_range[self.spl.pages_unique.index(int(pg))].index(rng) * 16 + int(self.reg.l.hex_col[c], 16)
        if click_type == 1:
            self.ed_popup_entry1(row, name, val, pg, c, num)
        elif click_type == 3:
            self.ed_popup_desc1(pg, num)
        else:
            raise ValueError("Invalid argument value in popup1(): 'click_type'")

    def ed_popup_entry1(self, row, name, val, pg, c, num):
        hex_valid = re.compile(r"[^0-9a-fA-F]")

        new_value = simpledialog.askstring(name, "Please enter a new HEXADECIMAL value", initialvalue=val[c])
        if (new_value is None) | (new_value == ""):
            return
        if hex_valid.search(new_value) is not None:
            messagebox.showerror("INPUT ERROR", "Input a Valid HEXADECIMAL Number!\n\"" + new_value + "\" is Not Valid")
            return

        bina_len = 0
        for (i, addr) in list(enumerate([x.split("(")[0] for x in self.spl.addr_total])):
            if addr == pg + "-" + str(num):
                bina_len += len(self.spl.bina[i])

        if len(new_value) > 2:
            new_value = new_value[-2:]
        if new_value.upper().zfill(2) != val[c]:
            if len(f"{int(new_value, 16):b}") > bina_len:
                new_value = f"{int('1' * bina_len, 2):02X}"
                if new_value == val[c]:
                    return
            self.ed_modify1(row, pg, num, new_value, mod_tag="modified")

    def ed_popup_desc1(self, pg, num):
        messagebox.showinfo(pg + "-" + str(num), self.adr.desc[self.adr.pg_and_num.index(pg + "-" + str(num))])

    def ed_modify1(self, row, pg, num, new, mod_tag="modified"):
        pg_idx = self.spl.pages_unique.index(int(pg))
        if new.upper().zfill(2) == self.adr.hexa_per_pg_mod[pg_idx][num]:
            return

        self.adr.hexa_per_pg_mod[self.spl.pages_unique.index(int(pg))][num] = new.upper().zfill(2)

        num_l, num_r = [int(x) for x in self.adr.num_range[pg_idx][int(num) // 16].split("~")]
        row_hexa = self.adr.hexa_per_pg_mod[pg_idx][num_l:num_r + 1]
        for i in (4, 9, 14):
            row_hexa.insert(i, "\u250a")
        for (i, hex) in list(enumerate(row_hexa, 1)):
            self.ed_addr_tree.set(row, column="#" + str(i), value=hex)

        self.ed_addr_tree.item(row, tag=mod_tag)

        self.ed_mod1_ad2sp(pg, num, mod_tag)
        self.ed_mod1_sp2mg(pg, num, mod_tag)
        self.ed_modified()
        self.ed_bin_over_20b(mod=True)

    def ed_mod1_ad2sp(self, pg, num, mod_tag):
        self.adr.hexa_mod[self.adr.pg_and_num.index(pg + "-" + str(num))] = self.adr.hexa_per_pg_mod[self.spl.pages_unique.index(int(pg))][num]
        self.adr.bina_mod[self.adr.pg_and_num.index(pg + "-" + str(num))] = f"{int(self.adr.hexa_per_pg_mod[self.spl.pages_unique.index(int(pg))][num], 16):08b}"

        spl_idx = []
        for (idx, addr) in list(enumerate([x.split("(")[0] for x in self.spl.addr_total])):
            if addr == pg + "-" + str(num):
                spl_idx.append(idx)

        for i in spl_idx:
            if ":" in self.spl.addr_bit[i]:
                self.spl.bina_mod[i] = self.adr.bina_mod[self.adr.pg_and_num.index(pg + "-" + str(num))][7 - int(self.spl.addr_bit[i].split(":")[0]):8 - int(self.spl.addr_bit[i].split(":")[1])]
            elif ":" not in self.spl.addr_bit[i]:
                self.spl.bina_mod[i] = self.adr.bina_mod[self.adr.pg_and_num.index(pg + "-" + str(num))][7 - int(self.spl.addr_bit[i])]
            self.spl.deci_mod[i] = int(self.spl.bina_mod[i], 2)
            self.spl.hexa_mod[i] = f"{int(self.spl.bina_mod[i], 2):X}".zfill(len(self.spl.hexa[i]))

        self.ed_hid1_tree.set(pg + "-" + str(num), column="#1", value=self.adr.bina_mod[self.adr.pg_and_num.index(pg + "-" + str(num))])
        self.ed_hid1_tree.set(pg + "-" + str(num), column="#2", value=self.adr.hexa_mod[self.adr.pg_and_num.index(pg + "-" + str(num))])
        
        for j in spl_idx:
            self.ed_hid0_tree.set(str(j) + "-split", column="#2", value=self.spl.bina_mod[j])
            self.ed_hid0_tree.set(str(j) + "-split", column="#3", value=self.spl.deci_mod[j])
            self.ed_hid0_tree.set(str(j) + "-split", column="#4", value=self.spl.hexa_mod[j])

        self.ed_hid1_tree.item(pg + "-" + str(num), tag=mod_tag)
        for k in spl_idx:
            if self.spl.bina_mod[k] != self.spl.bina[k]:
                self.ed_hid0_tree.item(str(k) + "-split", tag=mod_tag)

    def ed_mod1_sp2mg(self, pg, num, mod_tag):
        spl_idx = []
        for (idx, addr) in list(enumerate([x.split("(")[0] for x in self.spl.addr_total])):
            if addr == pg + "-" + str(num):
                spl_idx.append(idx)

        for i in spl_idx:
            mer_idx = self.mer.names.index(self.spl.names_wo_width[i])
            if self.spl.names_wo_width.count(self.spl.names_wo_width[i]) == 1:
                self.mer.bina_mod[mer_idx] = self.spl.bina_mod[i]
                self.mer.deci_mod[mer_idx] = self.spl.deci_mod[i]
                self.mer.hexa_mod[mer_idx] = self.spl.hexa_mod[i]
            elif self.spl.names_wo_width.count(self.spl.names_wo_width[i]) > 1:
                if ":" in self.spl.widths[i]:
                    self.mer.bina_mod[mer_idx] = self.p.replace_text(int(self.spl.widths[i].split(":")[1]), int(self.spl.widths[i].split(":")[0]), self.spl.bina_mod[i], self.mer.bina_mod[mer_idx])
                elif ":" not in self.spl.widths[i]:
                    self.mer.bina_mod[mer_idx] = self.p.replace_text(int(self.spl.widths[i]), None, self.spl.bina_mod[i], self.mer.bina_mod[mer_idx])
                self.mer.deci_mod[mer_idx] = int(self.mer.bina_mod[mer_idx], 2)
                self.mer.hexa_mod[mer_idx] = f"{self.mer.deci_mod[mer_idx]:X}".zfill(len(self.mer.hexa[mer_idx]))

        for j in spl_idx:
            mer_idx = self.mer.names.index(self.spl.names_wo_width[j])
            self.ed_name_tree.set(str(mer_idx), column="#2", value=self.mer.bina_mod[mer_idx])
            self.ed_name_tree.set(str(mer_idx), column="#3", value=self.mer.deci_mod[mer_idx])
            self.ed_name_tree.set(str(mer_idx), column="#4", value=self.mer.hexa_mod[mer_idx])
            if self.mer.bina_mod[mer_idx] != self.mer.bina[mer_idx]:
                self.ed_name_tree.item(mer_idx, tag=mod_tag)

    # hid0_tree (split name) click event
    def ed_popup_hid0(self, event):
        col = self.ed_hid0_tree.identify_column(event.x)
        row = self.ed_hid0_tree.identify_row(event.y)
        name = self.ed_hid0_tree.item(row, "text")
        val = self.ed_hid0_tree.item(row, "value")
        if (row in self.spl.groups_unique) | (row == ""):
            return
        if (col == "#5") & (val[4] != ""):
            messagebox.showinfo(name, self.spl.desc[int(row.split("-")[0])])

    # hid1_tree (address) click event
    def ed_popup_hid1(self, event):
        col = self.ed_hid1_tree.identify_column(event.x)
        row = self.ed_hid1_tree.identify_row(event.y)
        name = self.ed_hid1_tree.item(row, "text")
        val = self.ed_hid1_tree.item(row, "value")
        if (row in [str(item) for item in self.spl.pages_unique]) | (row == ""):
            return
        if (col == "#3") & (val[2] != ""):
            messagebox.showinfo(row, self.adr.desc[self.adr.pg_and_num.index(row)])

    # EDID Treeview etc
    def ed_add_treeview(self):
        self.ed_name_tree.delete(*self.ed_name_tree.get_children())
        self.ed_addr_tree.delete(*self.ed_addr_tree.get_children())
        self.ed_hid0_tree.delete(*self.ed_hid0_tree.get_children())
        self.ed_hid1_tree.delete(*self.ed_hid1_tree.get_children())

        for (i, item) in list(enumerate(self.spl.groups)):
            if (item == "EDID") & (self.mer.names[i] != "MERGED"):
                self.ed_name_tree.insert("", END, iid=str(i), text=self.mer.names[i], values=(self.mer.widths[i], self.mer.bina[i], self.mer.deci[i], self.mer.hexa[i], self.mer.desc_icon[i], self.spl.r_icon[i], self.mer.addr[i]))

        for (i, pg) in list(enumerate(self.spl.pages_unique)):
            if pg != 237:
                continue
            hex_val_list = []
            for (j, item) in list(enumerate(self.adr.num_range[i])):
                hex_val = []
                dec_from, dec_to = item.split("~")
                hex_from = f"{int(dec_from):02X}"
                hex_to = f"{int(dec_to):02X}"
                for k in range(16):
                    hex_val.append(self.adr.hexa_per_pg[i][j * 16 + k])
                for x in (4, 9, 14):
                    hex_val.insert(x, "\u250a")
                hex_val_list.append(hex_val)
                self.ed_addr_tree.insert("", END, iid=str(pg) + " " + item, text=hex_from + "~" + hex_to, values=tuple(hex_val_list[j]))

        for (i, item) in list(enumerate(self.spl.groups)):
            if item == "EDID":
                self.ed_hid0_tree.insert("", END, iid=str(i) + "-split", text=self.spl.names_wo_width[i], values=(self.spl.widths[i], self.spl.bina[i], self.spl.deci[i], self.spl.hexa[i], self.spl.desc_icon[i], self.spl.r_icon[i], self.spl.addr_total[i]))

        for (j, item) in list(enumerate(self.adr.pg_and_num)):
            if item.split("-")[0] == "237":
                self.ed_hid1_tree.insert("", END, iid=item, text=item.split("-")[1], values=(self.adr.bina[j], self.adr.hexa[j], self.adr.desc_icon[j]))

        self.ed_bin_over_20b()

    def ed_bin_over_20b(self, mod=False):
        if mod:
            for (i, item) in list(enumerate(self.mer.bina_mod)):
                if (len(item) > 20) & (i >= self.spl.groups.index("EDID")):
                    self.ed_name_tree.set(str(i), column="#2", value="-")
                    self.ed_name_tree.set(str(i), column="#3", value="-")
        else:
            for (i, item) in list(enumerate(self.mer.bina)):
                if (len(item) > 20) & (i >= self.spl.groups.index("EDID")):
                    self.ed_name_tree.set(str(i), column="#2", value="-")
                    self.ed_name_tree.set(str(i), column="#3", value="-")

    def reset_ed(self):
        for (i, item) in list(enumerate(self.mer.names)):
            if (item != "MERGED") & (i >= 5484):
                self.ed_name_tree.set(str(i), column="#2", value=self.mer.bina[i])
                self.ed_name_tree.set(str(i), column="#3", value=self.mer.deci[i])
                self.ed_name_tree.set(str(i), column="#4", value=self.mer.hexa[i])

        for j in range(len(self.spl.names_w_width)):
            if j >= 5484:
                self.ed_hid0_tree.set(str(j) + "-split", column="#2", value=self.spl.bina[j])
                self.ed_hid0_tree.set(str(j) + "-split", column="#3", value=self.spl.deci[j])
                self.ed_hid0_tree.set(str(j) + "-split", column="#4", value=self.spl.hexa[j])

        for (k, item) in list(enumerate(self.adr.pg_and_num)):
            if item.split("-")[0] == "237":
                self.ed_hid1_tree.set(item, column="#1", value=self.adr.bina[k])
                self.ed_hid1_tree.set(item, column="#2", value=self.adr.hexa[k])

        for (x, pg) in list(enumerate(self.spl.pages_unique)):
            if pg != 237:
                continue
            hex_val_list = []
            for (y, item) in list(enumerate(self.adr.num_range[x])):
                hex_val = []
                for z in range(16):
                    hex_val.append(self.adr.hexa_per_pg[x][y * 16 + z])
                for w in (4, 9, 14):
                    hex_val.insert(w, "\u250a")
                hex_val_list.append(hex_val)
            for (y, item) in list(enumerate(self.adr.num_range[x])):
                for col in range(19):
                    self.ed_addr_tree.set(str(pg) + " " + item, column="#" + str(col + 1), value=hex_val_list[y][col])

        self.mer.bina_mod[self.spl.pages.index(237):] = self.mer.bina[self.spl.pages.index(237):]
        self.mer.deci_mod[self.spl.pages.index(237):] = self.mer.deci[self.spl.pages.index(237):]
        self.mer.hexa_mod[self.spl.pages.index(237):] = self.mer.hexa[self.spl.pages.index(237):]
        self.spl.bina_mod[self.spl.pages.index(237):] = self.spl.bina[self.spl.pages.index(237):]
        self.spl.deci_mod[self.spl.pages.index(237):] = self.spl.deci[self.spl.pages.index(237):]
        self.spl.hexa_mod[self.spl.pages.index(237):] = self.spl.hexa[self.spl.pages.index(237):]
        self.adr.bina_mod[self.spl.pages.index(237):] = self.adr.bina[self.spl.pages.index(237):]
        self.adr.hexa_mod[self.spl.pages.index(237):] = self.adr.hexa[self.spl.pages.index(237):]
        self.adr.hexa_per_pg_mod[:self.spl.pages_unique.index(237)] = deepcopy(self.adr.hexa_per_pg[:self.spl.pages_unique.index(237)])
        self.reg.l.modified_pg = list(set(self.reg.l.modified_pg) - {"237"})
        self.eep.l.mod_by_eep_pg = list(set(self.eep.l.mod_by_eep_pg) - {"237"})

        for iid in self.ed_name_tree.tag_has("modified") + self.ed_name_tree.tag_has("eeprom") + self.ed_name_tree.tag_has("edid"):
            self.ed_name_tree.item(iid, tag="")
        for iid in self.ed_addr_tree.tag_has("modified") + self.ed_addr_tree.tag_has("eeprom") + self.ed_addr_tree.tag_has("edid"):
            self.ed_addr_tree.item(iid, tag="")
        for iid in self.ed_hid0_tree.tag_has("modified") + self.ed_hid0_tree.tag_has("eeprom") + self.ed_hid0_tree.tag_has("edid"):
            self.ed_hid0_tree.item(iid, tag="")
        for iid in self.ed_hid1_tree.tag_has("modified") + self.ed_hid1_tree.tag_has("eeprom") + self.ed_hid1_tree.tag_has("edid"):
            self.ed_hid1_tree.item(iid, tag="")

        if len(self.eep.l.mod_by_eep_pg) == 0:
            for file in self.eep.l.imported_txt:
                if file in self.reg.l.xlsx_list:
                    self.reg.l.xlsx_list.remove(file)
            self.reg.v.xlsx_names.set("\n".join(self.reg.l.xlsx_list))

        self.ed_bin_over_20b()
        self.p.check_mod()

    def ed_modified(self):
        if len(self.ed_name_tree.tag_has("modified") + self.ed_name_tree.tag_has("eeprom") + self.ed_name_tree.tag_has("edid")) != 0:
            if "237" not in self.reg.l.modified_pg:
                self.reg.l.modified_pg.append("237")

    # etc
    def resize(self, event):
        self.data_cv.configure(scrollregion=self.data_cv.bbox(ALL))