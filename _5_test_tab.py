from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from ctypes import *


class TestTab:
    def __init__(self, parent):
        self.p = parent
        self.gui = self.p.gui
        self.reg = self.p.reg
        self.tst = self.p.tst
        self.spl = self.p.spl
        self.mer = self.p.mer
        self.adr = self.p.adr
        self.reg_tab = self.p.reg_tab
        self.i2c_tab = self.p.i2c_tab

        test_note = ttk.Notebook(self.p.test_frm)
        test_note.pack(fill=BOTH, expand=YES)

        summ_frm = ttk.Frame(test_note)
        BIST_frm = ttk.Frame(test_note)
        self.gpio_frm = ttk.Frame(test_note)
        powr_frm = ttk.Frame(test_note, padding=self.gui.v.pad.get() * 5)
        test_note.add(summ_frm, text=" Reg. File Summary ")
        test_note.add(BIST_frm, text=" BIST ")
        test_note.add(self.gpio_frm, text=" GPIO ")
        test_note.add(powr_frm, text=" Power ")

        self.test_tree = ttk.Treeview(summ_frm, columns=("col1", "col2", "col3", "col4", "col5"))
        test_scrollbar = ttk.Scrollbar(summ_frm, orient=VERTICAL, command=self.test_tree.yview)
        test_scrollbar.pack(side=RIGHT, fill=Y)
        self.test_tree["yscrollcommand"] = test_scrollbar.set
        self.test_tree.heading("#0", text="Page")
        self.test_tree.heading("col1", text="Group")
        self.test_tree.heading("col2", text="W-only count")
        self.test_tree.heading("col3", text="R/W count")
        self.test_tree.heading("col4", text="N/A")
        self.test_tree.column("#0", width=30)
        self.test_tree.column("col1", width=410)
        self.test_tree.column("col2", width=50)
        self.test_tree.column("col3", width=50)
        self.test_tree.column("col4", width=10)
        self.test_tree.column("col5", width=60)
        self.test_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        self.test_tree.bind("<Button-3>", self.summary_check)

        # Power Tab
        psm_frm = ttk.Frame(powr_frm)
        pss_frm = ttk.Frame(powr_frm)
        psm_frm.pack(side=TOP, fill=X)
        pss_frm.pack(side=TOP, fill=X)
        powr_frms = [psm_frm, pss_frm]

        ttk.Label(psm_frm, text="Power Supply Measurement").grid(row=0, column=0, columnspan=6, pady=(0, 5), sticky=NW)
        ttk.Label(pss_frm, text="\nPower Supply Setting").grid(row=0, column=0, columnspan=7, pady=5, sticky=NW)
        for i in range(2):
            ttk.Label(powr_frms[i], text="", width=5).grid(row=1, column=0, rowspan=5, sticky=NSEW)
            ttk.Label(powr_frms[i], text="Digital").grid(row=1, column=1, sticky=NW)
            ttk.Label(powr_frms[i], text="eDRAM").grid(row=2, column=1, sticky=NW)
            ttk.Label(powr_frms[i], text="Mithrill").grid(row=3, column=1, sticky=NW)
            ttk.Label(powr_frms[i], text="SAM").grid(row=4, column=1, sticky=NW)
            ttk.Label(powr_frms[i], text="I/O").grid(row=5, column=1, sticky=NW)
        for r in range(5):
            for c in range(3):
                ttk.Entry(psm_frm, width=6 + 2 * (c // 2), textvariable=self.tst.v.psm_var[r][c], state="readonly").grid(row=r + 1, column=c + 2, sticky=NW)
            ttk.Button(psm_frm, text="Measure", command=lambda num=r: self.measure(num)).grid(row=r + 1, column=5, padx=10, sticky=NW)
            ttk.Entry(pss_frm, width=6, textvariable=self.tst.v.pss_var[r], state="readonly").grid(row=r + 1, column=5, sticky=NW)
            ttk.Button(pss_frm, text="\u25B2", width=2, command=lambda num=r, type="inc": self.inc_dec(num, type)).grid(row=r + 1, column=2, padx=(5, 0), sticky=NW)
            ttk.Button(pss_frm, text="\u25BC", width=2, command=lambda num=r, type="dec": self.inc_dec(num, type)).grid(row=r + 1, column=3, sticky=NW)
            ttk.Button(pss_frm, text="Measure", command=lambda num=r: self.measure(num)).grid(row=r + 1, column=4, padx=10, sticky=NW)
            ttk.Button(pss_frm, text="Read", command=lambda num=r: self.read_pot(num)).grid(row=r + 1, column=6, padx=10, sticky=NW)
        ttk.Entry(psm_frm, width=8, textvariable=self.tst.v.psm_var[5], state="readonly").grid(row=6, column=4, sticky=NW)
        ttk.Button(psm_frm, text="Measure ALL", command=self.measure_all).grid(row=6, column=5, padx=10, sticky=NW)

        # GPIO Tab
        self.test_gpio_tab = GPIOTab(self)

    # Summary Tab
    def regfile_summary_lists(self):
        self.tst.l.pages_hex = []
        self.tst.l.grp_per_pg = []
        self.tst.l.wo_cnt = []
        self.tst.l.rw_cnt = []
        self.tst.l.pg_not_used = []
        
        for (i, pg_dec) in list(enumerate(self.spl.pages_unique)):
            self.tst.l.pages_hex.append(f"{pg_dec:02X}")

            grp_str = ""
            wonly = []
            wandr = []
            for (j, page) in list(enumerate(self.spl.pages)):
                if page == pg_dec:
                    if self.spl.groups[j] not in grp_str.split(", "):
                        grp_str = grp_str + ", " + self.spl.groups[j]

                    wandr.append([int(x) for x in self.spl.addr_num][j])
                    if self.spl.defaults[j] != "R":
                        wonly.append([int(x) for x in self.spl.addr_num][j])
            grp_str = grp_str[2:]
            wonly.sort()
            wandr.sort()

            self.tst.l.grp_per_pg.append(grp_str)
            if len(wonly) == 0:
                self.tst.l.wo_cnt.append(-1)
            else:
                self.tst.l.wo_cnt.append(wonly[-1])
            self.tst.l.rw_cnt.append(wandr[-1])

        for i in self.tst.l.pages_hex:
            self.tst.l.pg_not_used.append(1)

    def summ_add_treeview(self):
        self.test_tree.delete(*self.test_tree.get_children())

        for (i, pg_hex) in list(enumerate(self.tst.l.pages_hex)):
            self.test_tree.insert("", i, iid=pg_hex, text=pg_hex, values=(self.tst.l.grp_per_pg[i], self.tst.l.wo_cnt[i], self.tst.l.rw_cnt[i], "\u2713"))

    def summary_check(self, event):
        col = self.test_tree.identify_column(event.x)
        row = self.test_tree.identify_row(event.y)
        val = self.test_tree.item(row, "value")

        if (col != "#4") | (row == ""):
            return

        if val[3] == "":
            self.test_tree.set(row, column="#4", value="\u2713")
            self.tst.l.pg_not_used[self.tst.l.pages_hex.index(row)] = 1
        elif val[3] == "\u2713":
            self.test_tree.set(row, column="#4", value="")
            self.tst.l.pg_not_used[self.tst.l.pages_hex.index(row)] = 0

    # Power Tab
    def measure_volt(self, ch):
        byte_list = create_string_buffer(2)
        byte_list[0:2] = bytearray().fromhex(f"D2 {2 ** 5 + 1 + ch * 2:02X}")

        sub_errno, result = self.i2c_tab.sub20_i2c_direct_write(int("35", 16), byte_list)
        if sub_errno != 0:
            return 0

        read_list, result = self.i2c_tab.sub20_i2c_direct_read(int("35", 16), 2)
        if result == "":
            return 0

        return (ord(read_list[0]) % 16) * 256 + ord(read_list[1])

    def volt_set(self, ch):
        v1 = self.measure_volt(2 * ch)
        v2 = self.measure_volt(2 * ch + 1)
        if (v1 == 0) | (v2 == 0):
            return 0, 0
        else:
            return v2, v1 - v2

    def measure(self, num):
        v, i = self.volt_set([lambda: num, lambda: 5][num == 4]())
        p = v * i * 0.0005
        if v == 0:
            self.tst.v.psm_var[num][0].set("ERROR")
        else:
            self.tst.v.psm_var[num][0].set(f"{v * 0.0005:.2f}V")
        self.tst.v.psm_var[num][1].set(f"{i:3d}mA")
        self.tst.v.psm_var[num][2].set(f"{p:5.1f}mW")
        self.pwr_sum()

    def measure_all(self):
        for num in range(5):
            self.measure(num)

    def pwr_sum(self):
        pwr0 = self.tst.v.psm_var[0][2].get()
        pwr1 = self.tst.v.psm_var[1][2].get()
        pwr2 = self.tst.v.psm_var[2][2].get()
        pwr3 = self.tst.v.psm_var[3][2].get()
        mw = re.compile(r"mW")

        if mw.search(pwr0):
            p0 = float(mw.sub("", pwr0))
        else:
            p0 = 0
        if mw.search(pwr1):
            p1 = float(mw.sub("", pwr1))
        else:
            p1 = 0
        if mw.search(pwr2):
            p2 = float(mw.sub("", pwr2))
        else:
            p2 = 0
        if mw.search(pwr3):
            p3 = float(mw.sub("", pwr3))
        else:
            p3 = 0

        p = p0 + p1 + p2 + p3
        self.tst.v.psm_var[5].set(f"{p:5.1f}mW")

    def read_pot(self, num):
        ch_pot, ch01 = divmod([lambda: num, lambda: 5][num == 4](), 2)
        read_list, result = self.i2c_tab.sub20_i2c_direct_read(40 + ch_pot, 2)
        if result == "":
            pot = -1
        else:
            pot = (ord(read_list[0]) % 2) * 256 + ord(read_list[1])
        self.tst.v.pss_var[num].set(pot)

    def inc_dec(self, num, type):
        if type.lower() == "inc":
            dir = 1
        elif type.lower() == "dec":
            dir = -1
        else:
            return

        ch_pot, ch01 = divmod([lambda: num, lambda: 5][num == 4](), 2)
        dec = 6 + 2 * dir
        byte_list = create_string_buffer(1)
        byte_list[0:1] = bytearray().fromhex(f"{ch01:d}{dec:X}")
        sub_errno, result = self.i2c_tab.sub20_i2c_direct_write(40 + ch_pot, byte_list)


class GPIOTab:
    def __init__(self, parent):
        self.p = parent
        self.gui = self.p.gui
        self.reg = self.p.reg
        self.tst = self.p.tst
        self.spl = self.p.spl
        self.mer = self.p.mer
        self.adr = self.p.adr
        self.reg_tab = self.p.reg_tab
        self.i2c_tab = self.p.i2c_tab

        gpio_tabs = ttk.Notebook(self.p.gpio_frm)
        gpio_tabs.pack(fill=BOTH, expand=YES)
        tabs = {}
        for i in range(10):
            tabs[i] = ttk.Frame(gpio_tabs)
            if i == 0:
                gpio_tabs.add(tabs[i], text=" Main Data ")
            elif i == 1:
                gpio_tabs.add(tabs[i], text=" Pulse Extend ")
            else:
                gpio_tabs.add(tabs[i], text=" " + self.tst.l.gpio_grps[i - 1] + " ")

# --------------------Main Data-----------------------------------------------------------------------------------------

        self.main_l = ttk.Frame(tabs[0], padding=self.gui.v.pad.get() * 5)
        self.main_l.place(relx=0, rely=0, relwidth=0.7, relheight=0.6)
        main_r = ttk.Frame(tabs[0])
        main_r.place(relx=0.7, rely=0, relwidth=0.3, relheight=0.6)
        main_b = ttk.Frame(tabs[0])
        main_b.place(relx=0, rely=0.6, relwidth=1, relheight=0.4)

        ttk.Label(self.main_l, text="Data").grid(row=0, column=0, padx=(20, 0), pady=5, sticky=W)
        ttk.Label(self.main_l, text="\nClock").grid(row=9, column=0, padx=(20, 0), pady=5, sticky=W)
        ttk.Label(self.main_l, text="GPIO 8").grid(row=10, column=0, padx=(30, 5), pady=3)
        ttk.Label(self.main_l, text="GPIO 9").grid(row=11, column=0, padx=(30, 5), pady=3)

        self.widgets = {}
        self.widgets["c0"] = ttk.Combobox(self.main_l, value=self.tst.l.gpio_clks, textvariable=self.tst.v.clk_sel[0], width=20, state="readonly")
        self.widgets["c1"] = ttk.Combobox(self.main_l, value=self.tst.l.gpio_clks, textvariable=self.tst.v.clk_sel[1], width=20, state="readonly")
        self.widgets["c0"].grid(row=10, column=1, padx=5, pady=3)
        self.widgets["c1"].grid(row=11, column=1, padx=5, pady=3)
        
        for i in range(8):
            ttk.Label(self.main_l, text="GPIO " + str(i)).grid(row=1 + i, column=0, padx=(30, 5), pady=3)
            self.widgets["g" + str(i)] = ttk.Combobox(self.main_l, value=self.tst.l.gpio_grps, textvariable=self.tst.v.grp_sel[i], width=20, state="readonly")
            self.widgets["b" + str(i)] = ttk.Combobox(self.main_l, value=self.tst.l.gpio_bits, textvariable=self.tst.v.bit_sel[i], width=10, state="readonly")
            self.widgets["g" + str(i)].grid(row=1 + i, column=1, padx=5, pady=3)
            self.widgets["b" + str(i)].grid(row=1 + i, column=2, padx=5, pady=3)
            self.widgets["g" + str(i)].bind("<<ComboboxSelected>>", lambda event, num=i: self.label_data_event(event, num))
            self.widgets["b" + str(i)].bind("<<ComboboxSelected>>", lambda event, num=i: self.label_data_event(event, num))

        ttk.Button(main_r, text="Load Data", width=20, command=self.gpio_load).pack(side=TOP, padx=(0, 130), pady=(65, 0), ipady=3, anchor=E)
        ttk.Button(main_r, text="Set Data", width=20, command=self.gpio_set).pack(side=TOP, padx=(0, 130), pady=(15, 0), ipady=3, anchor=E)
        ttk.Button(main_r, text="Set I\u00b2C", width=20, command=self.gpio_i2c).pack(side=TOP, padx=(0, 130), pady=(15, 0), ipady=3, anchor=E)
        ttk.Button(main_r, text="Set Default", width=20, command=self.gpio_set_default).pack(side=TOP, padx=(0, 130), pady=(15, 0), ipady=3, anchor=E)
        ttk.Button(main_r, text="Reset to Default", width=20, command=self.gpio_reset).pack(side=TOP, padx=(0, 130), pady=(15, 0), ipady=3, anchor=E)
        ttk.Button(main_r, text="Clear Data", width=20, command=self.gpio_clear).pack(side=TOP, padx=(0, 130), pady=(15, 0), ipady=3, anchor=E)

        for i in range(1, 9):
            if i == 2:
                ttk.Label(main_b, text=self.tst.l.gpio_grps[i] + ": ").grid(row=1, column=0, padx=(70, 0), pady=(8, 0), sticky=NW)
                ttk.Label(main_b, text=self.tst.l.gpio_grps[i] + ": ").grid(row=2, column=0, padx=(70, 0), pady=(8, 0), sticky=NW)
                continue
            ttk.Label(main_b, text=self.tst.l.gpio_grps[i] + ": ").grid(row=[lambda: i, lambda: i - 1][i == 1](), column=0, padx=(70, 0), pady=(8, 0), sticky=NW)
        for j in range(9):
            ttk.Label(main_b, text=self.tst.l.gpio_grp_reg_names_w_width[j]).grid(row=j, column=1, padx=(0, 10), pady=(8, 0), sticky=NW)

        for i in range(9):
            self.widgets["cb" + str(i)] = ttk.Combobox(main_b, value=self.tst.l.gpio_vals[i], textvariable=self.tst.v.gpio_sel[i], width=5, state="readonly")
            self.widgets["cb" + str(i)].grid(row=i, column=2, pady=4, sticky=NW)
            self.widgets[i] = ttk.Frame(main_b, width=600, relief=SOLID)
            self.widgets[i].grid(row=i, column=3, padx=(10, 0), sticky=NSEW)
            for j in range(8):
                if i == 1:
                    w = 150
                    if j > 3:
                        continue
                else:
                    w = 75
                self.widgets[str(i) + str(j)] = ttk.Frame(self.widgets[i], relief=SOLID, width=w, padding=1)
                self.widgets[str(i) + str(j)].pack(side=LEFT, fill=Y)
                self.widgets[str(i) + str(j)].pack_propagate(False)
                self.widgets["lb" + str(i) + str(j)] = ttk.Label(self.widgets[str(i) + str(j)], textvariable=self.tst.v.gpio_cell[i][j], font=("Consolas", 8), anchor=NW, wraplength=70)
                self.widgets["lb" + str(i) + str(j)].pack(fill=BOTH, expand=YES)

        for r in range(9):
            if r == 1:
                for i in range(4):
                    self.tst.v.gpio_cell[r][i].set(self.tst.l.sam_choice0[i])
                continue

            grp = [lambda: r - 1, lambda: r][r == 0]()
            for c in range(8):
                if self.tst.v.gpio_sel[r].get() == "-":
                    grp_row = 0
                else:
                    grp_row = int(self.tst.v.gpio_sel[r].get())
                self.tst.v.gpio_cell[r][c].set(list(reversed(self.tst.l.name_list[grp][grp_row]))[c])

# ------------------Pulse Extend----------------------------------------------------------------------------------------

        ext_frm = ttk.Frame(tabs[1], padding=self.gui.v.pad.get() * 3)
        btn_frm = ttk.Frame(tabs[1])
        ext_frm.place(relx=0, rely=0, relwidth=0.7, relheight=1)
        btn_frm.place(relx=0.7, rely=0, relwidth=0.3, relheight=1)

        ttk.Label(ext_frm, text="Pulse Width Adjustment").grid(row=0, column=0, columnspan=5, padx=(50, 0), pady=(0, self.gui.v.pad.get()))
        for i in range(8):
            ttk.Label(ext_frm, text="GPIO " + str(i)).grid(row=1 + 2 * i, column=0, padx=(70, 0), pady=(self.gui.v.pad.get() * 2, 0), sticky=NW)
            ttk.Label(ext_frm, text="Extend Type:").grid(row=2 + 2 * i, column=0, padx=(100, 5), pady=self.gui.v.pad.get(), sticky=NW)
            ttk.Label(ext_frm, text="Extend Amount:").grid(row=2 + 2 * i, column=2, padx=(20, 5), pady=self.gui.v.pad.get(), sticky=NW)
            ttk.Label(ext_frm, text="2 ^").grid(row=2 + 2 * i, column=3, padx=(5, 0), pady=self.gui.v.pad.get(), sticky=NW)
            self.widgets["t" + str(i)] = ttk.Combobox(ext_frm, value=self.tst.l.ext_types, textvariable=self.tst.v.type_sel[i], width=20, state="readonly")
            self.widgets["a" + str(i)] = ttk.Combobox(ext_frm, value=self.tst.l.ext_amnts, textvariable=self.tst.v.amnt_sel[i], width=10, state="readonly")
            self.widgets["t" + str(i)].grid(row=2 + 2 * i, column=1, padx=5, pady=self.gui.v.pad.get(), sticky=NW)
            self.widgets["a" + str(i)].grid(row=2 + 2 * i, column=4, padx=5, pady=self.gui.v.pad.get(), sticky=NW)

        ttk.Button(btn_frm, text="Load Data", width=20, command=self.gpio_load).pack(side=TOP, padx=(0, 130), pady=(15 + self.gui.v.pad.get() * 5, 0), ipady=3, anchor=E)
        ttk.Button(btn_frm, text="Set Data", width=20, command=self.gpio_set).pack(side=TOP, padx=(0, 130), pady=(15, 0), ipady=3, anchor=E)
        ttk.Button(btn_frm, text="Set I\u00b2C", width=20, command=self.gpio_i2c).pack(side=TOP, padx=(0, 130), pady=(15, 0), ipady=3, anchor=E)
        ttk.Button(btn_frm, text="Set Default", width=20, command=self.gpio_set_default).pack(side=TOP, padx=(0, 130), pady=(15, 0), ipady=3, anchor=E)
        ttk.Button(btn_frm, text="Reset to Default", width=20, command=self.gpio_reset).pack(side=TOP, padx=(0, 130), pady=(15, 0), ipady=3, anchor=E)
        ttk.Button(btn_frm, text="Clear Data", width=20, command=self.gpio_clear).pack(side=TOP, padx=(0, 130), pady=(15, 0), ipady=3, anchor=E)

# --------------------Mithrill------------------------------------------------------------------------------------------

        self.mit_frm = Frame(tabs[2], height=50)
        self.mit_frm.pack(side=TOP, fill=X)
        self.mit_cv = Canvas(tabs[2])
        self.mit_cv.pack(fill=BOTH, side=TOP, expand=YES)
        self.mit_cv_frm = Frame(self.mit_cv, padx=10)
        self.mit_cv.create_window(0, 0, anchor=NW, window=self.mit_cv_frm)

        ttk.Label(self.mit_frm, text=self.tst.l.gpio_grp_reg_names_w_width[0], font=("Helvetica", 10, "bold")).place(relx=0.49, rely=0.35, anchor=NE)
        self.widgets["mit"] = ttk.Combobox(self.mit_frm, value=self.tst.l.gpio_vals[0], textvariable=self.tst.v.gpio_sel[0], width=10, state="readonly")
        self.widgets["mit"].bind("<<ComboboxSelected>>", lambda event, frame=self.mit_cv_frm, txt=self.tst.v.gpio_sel[0], num=23, r=0: self.cell_event(event, frame, txt, num, r))
        self.widgets["cb0"].bind("<<ComboboxSelected>>", lambda event, frame=self.mit_cv_frm, txt=self.tst.v.gpio_sel[0], num=23, r=0: self.cell_event(event, frame, txt, num, r))
        self.widgets["mit"].place(relx=0.51, rely=0.35, anchor=NW)

        for i in range(8):
            ttk.Label(self.mit_cv_frm, text=i, width=5, relief=SOLID, anchor=CENTER, font=("Arial", 10, "normal")).grid(row=i, column=0, ipady=15, sticky=NSEW)

        for (i, x) in list(enumerate(self.tst.l.mit_choice)):
            if i <= 6:
                ttk.Label(self.mit_cv_frm, text=x, relief=SOLID, anchor=CENTER).grid(row=i, column=1, columnspan=8, sticky=NSEW)
            elif i > 6:
                ttk.Label(self.mit_cv_frm, text=x, width=15, relief=SOLID, anchor=CENTER).grid(row=7, column=i - 6, sticky=NSEW)

        mit_slave = self.mit_cv_frm.grid_slaves()
        for i in range(23):
            mit_info = mit_slave[i].grid_info()
            if mit_info["row"] == 0:
                mit_slave[i].configure(background="yellow")

# --------------------SAM-----------------------------------------------------------------------------------------------

        self.sam_frm0 = Frame(tabs[3], height=50)
        self.sam_frm0.pack(side=TOP, fill=X)
        self.sam_cv0 = Canvas(tabs[3], height=47)
        self.sam_cv0.pack(fill=X, anchor=NW, side=TOP)
        self.sam_cv0_frm = Frame(self.sam_cv0, padx=10)
        self.sam_cv0.create_window(0, 0, anchor=NW, window=self.sam_cv0_frm)
        self.sam_frm1 = Frame(tabs[3], height=50)
        self.sam_frm1.pack(side=TOP, fill=X, anchor=N)
        self.sam_cv1 = Canvas(tabs[3])
        self.sam_cv1.pack(fill=BOTH, anchor=NW, side=TOP, expand=YES)
        self.sam_cv1_frm = Frame(self.sam_cv1, padx=10)
        self.sam_cv1.create_window(0, 0, anchor=NW, window=self.sam_cv1_frm)

        ttk.Label(self.sam_frm0, text=self.tst.l.gpio_grp_reg_names_w_width[1], font=("Helvetica", 10, "bold")).place(relx=0.49, rely=0.35, anchor=NE)
        ttk.Label(self.sam_frm1, text=self.tst.l.gpio_grp_reg_names_w_width[2], font=("Helvetica", 10, "bold")).place(relx=0.49, rely=0.35, anchor=NE)
        self.widgets["sm0"] = ttk.Combobox(self.sam_frm0, value=self.tst.l.gpio_vals[1], textvariable=self.tst.v.gpio_sel[1], width=10, state="readonly")
        self.widgets["sm1"] = ttk.Combobox(self.sam_frm1, value=self.tst.l.gpio_vals[2], textvariable=self.tst.v.gpio_sel[2], width=10, state="readonly")
        self.widgets["sm0"].place(relx=0.51, rely=0.35, anchor=NW)
        self.widgets["sm1"].place(relx=0.51, rely=0.35, anchor=NW)
        self.widgets["sm0"].bind("<<ComboboxSelected>>", self.sam_sel_event)
        self.widgets["sm1"].bind("<<ComboboxSelected>>", lambda event, frame=self.sam_cv1_frm, txt=self.tst.v.gpio_sel[2], num=26, r=2: self.cell_event(event, frame, txt, num, r))
        self.widgets["cb1"].bind("<<ComboboxSelected>>", lambda event, frame=None, txt=None, num=None, r=1: self.cell_event(event, frame, txt, num, r))
        self.widgets["cb2"].bind("<<ComboboxSelected>>", lambda event, frame=self.sam_cv1_frm, txt=self.tst.v.gpio_sel[2], num=26, r=2: self.cell_event(event, frame, txt, num, r))

        for i in range(4):
            ttk.Label(self.sam_cv0_frm, text=i, width=5, relief=SOLID, anchor=CENTER, font=("Arial", 10, "normal")).grid(row=0, column=2 * i, ipady=15, sticky=NSEW)
        for i in range(8):
            ttk.Label(self.sam_cv1_frm, text=i, width=5, relief=SOLID, anchor=CENTER, font=("Arial", 10, "normal")).grid(row=i, column=0, ipady=15, sticky=NSEW)

        for (i, x0) in list(enumerate(self.tst.l.sam_choice0)):
            ttk.Label(self.sam_cv0_frm, text=x0, width=26, relief=SOLID, anchor=CENTER).grid(row=0, column=2 * i + 1, ipadx=1, sticky=NSEW)
        for (i, x1) in list(enumerate(self.tst.l.sam_choice1)):
            if i <= 1:
                ttk.Label(self.sam_cv1_frm, text=x1, relief=SOLID, anchor=CENTER).grid(row=0 + i, column=1, columnspan=8, sticky=NSEW)
            elif i <= 3:
                ttk.Label(self.sam_cv1_frm, text=x1, relief=SOLID, anchor=CENTER).grid(row=2, column=(i % 2) * 4 + 1, columnspan=4, sticky=NSEW)
            elif i == 4:
                ttk.Label(self.sam_cv1_frm, text=x1, relief=SOLID, anchor=CENTER).grid(row=3, column=1, columnspan=8, sticky=NSEW)
            elif i <= 6:
                ttk.Label(self.sam_cv1_frm, text=x1, relief=SOLID, anchor=CENTER).grid(row=4, column=(i % 5) * 4 + 1, columnspan=4, sticky=NSEW)
            elif i <= 8:
                ttk.Label(self.sam_cv1_frm, text=x1, relief=SOLID, anchor=CENTER).grid(row=5, column=(i % 7) * 5 + 1, columnspan=(i % 2) * 2 + 3, sticky=NSEW)
            elif i <= 10:
                ttk.Label(self.sam_cv1_frm, text=x1, relief=SOLID, anchor=CENTER).grid(row=6, column=(i % 9) * 4 + 1, columnspan=4, sticky=NSEW)
            elif i <= 14:
                ttk.Label(self.sam_cv1_frm, text=x1, width=15, relief=SOLID, anchor=CENTER).grid(row=7, column=i - 10, sticky=NSEW)
            elif i == 15:
                ttk.Label(self.sam_cv1_frm, text=x1, width=30, relief=SOLID, anchor=CENTER).grid(row=7, column=5, columnspan=2, sticky=NSEW)
            elif i <= 17:
                ttk.Label(self.sam_cv1_frm, text=x1, width=15, relief=SOLID, anchor=CENTER).grid(row=7, column=i - 9, sticky=NSEW)

        sam_slave0 = self.sam_cv0_frm.grid_slaves()
        for i in range(8):
            sam_info0 = sam_slave0[i].grid_info()
            if (sam_info0["column"] == 0) | (sam_info0["column"] == 1):
                sam_slave0[i].configure(background="yellow")

        sam_slave1 = self.sam_cv1_frm.grid_slaves()
        for i in range(26):
            sam_info1 = sam_slave1[i].grid_info()
            if sam_info1["row"] == 0:
                sam_slave1[i].configure(background="yellow")

# --------------------eDP-----------------------------------------------------------------------------------------------

        self.eDP_frm = Frame(tabs[4], height=50)
        self.eDP_frm.pack(side=TOP, fill=X)
        self.eDP_cv = Canvas(tabs[4])
        self.eDP_cv.pack(fill=BOTH, anchor=W, side=LEFT, expand=YES)
        self.eDP_cv_frm = Frame(self.eDP_cv, padx=10)
        self.eDP_cv.create_window(0, 0, anchor=NW, window=self.eDP_cv_frm)
        self.scrollbar = Scrollbar(tabs[4], orient=VERTICAL, command=self.eDP_cv.yview)
        self.scrollbar.pack(anchor=E, side=LEFT, fill=Y)
        self.eDP_cv.config(yscrollcommand=self.scrollbar.set)
        tabs[4].bind("<Configure>", self.resize)

        ttk.Label(self.eDP_frm, text=self.tst.l.gpio_grp_reg_names_w_width[3], font=("Helvetica", 10, "bold")).place(relx=0.49, rely=0.35, anchor=NE)
        self.widgets["edp"] = ttk.Combobox(self.eDP_frm, value=self.tst.l.gpio_vals[3], textvariable=self.tst.v.gpio_sel[3], width=10, state="readonly")
        self.widgets["edp"].bind("<<ComboboxSelected>>", lambda event, frame=self.eDP_cv_frm, txt=self.tst.v.gpio_sel[3], num=106, r=3: self.cell_event(event, frame, txt, num, r))
        self.widgets["cb3"].bind("<<ComboboxSelected>>", lambda event, frame=self.eDP_cv_frm, txt=self.tst.v.gpio_sel[3], num=106, r=3: self.cell_event(event, frame, txt, num, r))
        self.widgets["edp"].place(relx=0.51, rely=0.35, anchor=NW)

        for i in range(22):
            ttk.Label(self.eDP_cv_frm, text=i, width=5, relief=SOLID, anchor=CENTER, font=("Arial", 10, "normal")).grid(row=i, column=0, ipady=15, sticky=NSEW)

        for (i, x) in list(enumerate(self.tst.l.eDP_choice)):
            if i <= 1:
                ttk.Label(self.eDP_cv_frm, text=x, width=60 - (30 * i), relief=SOLID, anchor=CENTER).grid(row=0, column=i * 4 + 1, columnspan=4 - (i * 2), sticky=NSEW)
            elif i <= 3:
                ttk.Label(self.eDP_cv_frm, text=x, width=15, relief=SOLID, anchor=CENTER, wraplength=100).grid(row=0, column=i + 5, sticky=NSEW)
            elif (i == 4) | (i == 6) | (i == 8):
                ttk.Label(self.eDP_cv_frm, text=x, width=60, relief=SOLID, anchor=CENTER).grid(row=i // 2 - 1, column=1, columnspan=4, sticky=NSEW)
            elif (i == 5) | (i == 7):
                ttk.Label(self.eDP_cv_frm, text=x, width=60, relief=SOLID, anchor=CENTER).grid(row=i // 3, column=5, columnspan=4, sticky=NSEW)
            elif i <= 12:
                ttk.Label(self.eDP_cv_frm, text=x, width=15, relief=SOLID, anchor=CENTER, wraplength=100).grid(row=3, column=i - 4, sticky=NSEW)
            elif i <= 20:
                ttk.Label(self.eDP_cv_frm, text=x, width=15, relief=SOLID, anchor=CENTER, wraplength=100).grid(row=4, column=i - 12, sticky=NSEW)
            elif i <= 22:
                ttk.Label(self.eDP_cv_frm, text=x, width=60, relief=SOLID, anchor=CENTER).grid(row=5, column=(i - 21) * 4 + 1, columnspan=4, sticky=NSEW)
            elif i <= 30:
                ttk.Label(self.eDP_cv_frm, text=x, width=15, relief=SOLID, anchor=CENTER, wraplength=100).grid(row=6, column=i - 22, sticky=NSEW)
            elif i <= 38:
                ttk.Label(self.eDP_cv_frm, text=x, width=15, relief=SOLID, anchor=CENTER, wraplength=100).grid(row=7, column=i - 30, sticky=NSEW)
            elif i <= 46:
                ttk.Label(self.eDP_cv_frm, text=x, width=15, relief=SOLID, anchor=CENTER, wraplength=100).grid(row=8, column=i - 38, sticky=NSEW)
            elif i <= 49:
                ttk.Label(self.eDP_cv_frm, text=x, width=15, relief=SOLID, anchor=CENTER, wraplength=100).grid(row=9, column=i - 46, sticky=NSEW)
            elif i == 50:
                ttk.Label(self.eDP_cv_frm, text=x, width=60, relief=SOLID, anchor=CENTER).grid(row=9, column=4, columnspan=4, sticky=NSEW)
            elif i == 51:
                ttk.Label(self.eDP_cv_frm, text=x, width=15, relief=SOLID, anchor=CENTER, wraplength=100).grid(row=9, column=8, sticky=NSEW)
            elif i <= 59:
                ttk.Label(self.eDP_cv_frm, text=x, width=15, relief=SOLID, anchor=CENTER, wraplength=100).grid(row=10, column=i - 51, sticky=NSEW)
            elif i <= 67:
                ttk.Label(self.eDP_cv_frm, text=x, width=120, relief=SOLID, anchor=CENTER).grid(row=i - 49, column=1, columnspan=8, sticky=NSEW)
            elif i <= 72:
                ttk.Label(self.eDP_cv_frm, text=x, width=15, relief=SOLID, anchor=CENTER, wraplength=100).grid(row=19, column=i - 67, sticky=NSEW)
            elif i == 73:
                ttk.Label(self.eDP_cv_frm, text=x, width=45, relief=SOLID, anchor=CENTER).grid(row=19, column=i - 67, columnspan=3, sticky=NSEW)
            elif i <= 81:
                ttk.Label(self.eDP_cv_frm, text=x, width=15, relief=SOLID, anchor=CENTER, wraplength=100).grid(row=20, column=i - 73, sticky=NSEW)
            elif i <= 83:
                ttk.Label(self.eDP_cv_frm, text=x, width=60, relief=SOLID, anchor=CENTER).grid(row=21, column=(i - 82) * 4 + 1, columnspan=4, sticky=NSEW)

        eDP_slave = self.eDP_cv_frm.grid_slaves()
        for i in range(106):
            eDP_info = eDP_slave[i].grid_info()
            if eDP_info["row"] == 0:
                eDP_slave[i].configure(background="yellow")

# --------------------TCON----------------------------------------------------------------------------------------------

        self.tcn_frm = Frame(tabs[5], height=50)
        self.tcn_frm.pack(side=TOP, fill=X)
        self.tcn_cv = Canvas(tabs[5])
        self.tcn_cv.pack(fill=BOTH, anchor=W, side=LEFT, expand=YES)
        self.tcn_cv_frm = Frame(self.tcn_cv, padx=10)
        self.tcn_cv.create_window(0, 0, anchor=NW, window=self.tcn_cv_frm)

        ttk.Label(self.tcn_frm, text=self.tst.l.gpio_grp_reg_names_w_width[4], font=("Helvetica", 10, "bold")).place(relx=0.49, rely=0.35, anchor=NE)
        self.widgets["tcn"] = ttk.Combobox(self.tcn_frm, value=self.tst.l.gpio_vals[4], textvariable=self.tst.v.gpio_sel[4], width=10, state="readonly")
        self.widgets["tcn"].bind("<<ComboboxSelected>>", lambda event, frame=self.tcn_cv_frm, txt=self.tst.v.tcn_new, num=92, r=4: self.cell_event(event, frame, txt, num, r))
        self.widgets["cb4"].bind("<<ComboboxSelected>>", lambda event, frame=self.tcn_cv_frm, txt=self.tst.v.tcn_new, num=92, r=4: self.cell_event(event, frame, txt, num, r))
        self.widgets["tcn"].place(relx=0.51, rely=0.35, anchor=NW)

        for i in range(4):
            ttk.Label(self.tcn_cv_frm, text=i, width=5, relief=SOLID, anchor=CENTER, font=("Arial", 10, "normal")).grid(row=i, column=0, ipady=15, sticky=NSEW)
        for i in range(8, 15):
            ttk.Label(self.tcn_cv_frm, text=i, width=5, relief=SOLID, anchor=CENTER, font=("Arial", 10, "normal")).grid(row=i - 4, column=0, ipady=15, sticky=NSEW)

        for (i, x) in list(enumerate(self.tst.l.tcn_choice)):
            if i != 48:
                if i <= 47:
                    ttk.Label(self.tcn_cv_frm, text=x, width=15, relief=SOLID, anchor=CENTER).grid(row=i // 8, column=i % 8 + 1, sticky=NSEW)
                elif i <= 80:
                    ttk.Label(self.tcn_cv_frm, text=x, width=15, relief=SOLID, anchor=CENTER).grid(row=(i - 1) // 8 + 1, column=(i - 1) % 8 + 1, sticky=NSEW)
            elif i == 48:
                ttk.Label(self.tcn_cv_frm, text=x, width=120, relief=SOLID, anchor=CENTER).grid(row=6, column=1, columnspan=8, sticky=NSEW)

        tcn_slave = self.tcn_cv_frm.grid_slaves()
        for i in range(92):
            tcn_info = tcn_slave[i].grid_info()
            if tcn_info["row"] == 0:
                tcn_slave[i].configure(background="yellow")

# --------------------TCON2UPI------------------------------------------------------------------------------------------

        self.cdc_frm = Frame(tabs[6], height=50)
        self.cdc_frm.pack(side=TOP, fill=X)
        self.cdc_cv = Canvas(tabs[6])
        self.cdc_cv.pack(fill=BOTH, anchor=W, side=LEFT, expand=YES)
        self.cdc_cv_frm = Frame(self.cdc_cv, padx=10)
        self.cdc_cv.create_window(0, 0, anchor=NW, window=self.cdc_cv_frm)

        ttk.Label(self.cdc_frm, text=self.tst.l.gpio_grp_reg_names_w_width[5], font=("Helvetica", 10, "bold")).place(relx=0.49, rely=0.35, anchor=NE)
        self.widgets["cdc"] = ttk.Combobox(self.cdc_frm, value=self.tst.l.gpio_vals[5], textvariable=self.tst.v.gpio_sel[5], width=10, state="readonly")
        self.widgets["cdc"].bind("<<ComboboxSelected>>", lambda event, frame=self.cdc_cv_frm, txt=self.tst.v.cdc_new, num=126, r=5: self.cell_event(event, frame, txt, num, r))
        self.widgets["cb5"].bind("<<ComboboxSelected>>", lambda event, frame=self.cdc_cv_frm, txt=self.tst.v.cdc_new, num=126, r=5: self.cell_event(event, frame, txt, num, r))
        self.widgets["cdc"].place(relx=0.51, rely=0.35, anchor=NW)

        for i in range(6):
            ttk.Label(self.cdc_cv_frm, text=i, width=5, relief=SOLID, anchor=CENTER, font=("Arial", 10, "normal")).grid(row=i, column=0, ipady=15, sticky=NSEW)
        for i in range(8, 16):
            ttk.Label(self.cdc_cv_frm, text=i, width=5, relief=SOLID, anchor=CENTER, font=("Arial", 10, "normal")).grid(row=i - 2, column=0, ipady=15, sticky=NSEW)

        for (i, x) in list(enumerate(self.tst.l.cdc_choice)):
            r = i // 8
            c = i % 8 + 1
            ttk.Label(self.cdc_cv_frm, text=x, width=15, relief=SOLID, anchor=CENTER).grid(row=r, column=c, sticky=NSEW)

        cdc_slave = self.cdc_cv_frm.grid_slaves()
        for i in range(126):
            cdc_info = cdc_slave[i].grid_info()
            if cdc_info["row"] == 0:
                cdc_slave[i].configure(background="yellow")

# --------------------UPI-----------------------------------------------------------------------------------------------

        self.upi_frm = Frame(tabs[7], height=50)
        self.upi_frm.pack(side=TOP, fill=X)
        self.upi_cv = Canvas(tabs[7])
        self.upi_cv.pack(fill=BOTH, anchor=W, side=LEFT, expand=YES)
        self.upi_cv_frm = Frame(self.upi_cv, padx=10)
        self.upi_cv.create_window(0, 0, anchor=NW, window=self.upi_cv_frm)

        ttk.Label(self.upi_frm, text=self.tst.l.gpio_grp_reg_names_w_width[6], font=("Helvetica", 10, "bold")).place(relx=0.49, rely=0.35, anchor=NE)
        self.widgets["upi"] = ttk.Combobox(self.upi_frm, value=self.tst.l.gpio_vals[6], textvariable=self.tst.v.gpio_sel[6], width=10, state="readonly")
        self.widgets["upi"].bind("<<ComboboxSelected>>", lambda event, frame=self.upi_cv_frm, txt=self.tst.v.gpio_sel[6], num=54, r=6: self.cell_event(event, frame, txt, num, r))
        self.widgets["cb6"].bind("<<ComboboxSelected>>", lambda event, frame=self.upi_cv_frm, txt=self.tst.v.gpio_sel[6], num=54, r=6: self.cell_event(event, frame, txt, num, r))
        self.widgets["upi"].place(relx=0.51, rely=0.35, anchor=NW)

        for i in range(6):
            ttk.Label(self.upi_cv_frm, text=i, width=5, relief=SOLID, anchor=CENTER, font=("Arial", 10, "normal")).grid(row=i, column=0, ipady=15, sticky=NSEW)

        for (i, x) in list(enumerate(self.tst.l.upi_choice)):
            r = i // 8
            c = i % 8 + 1
            ttk.Label(self.upi_cv_frm, text=x, width=15, relief=SOLID, anchor=CENTER).grid(row=r, column=c, sticky=NSEW)

        upi_slave = self.upi_cv_frm.grid_slaves()
        for i in range(54):
            upi_info = upi_slave[i].grid_info()
            if upi_info["row"] == 0:
                upi_slave[i].configure(background="yellow")

# --------------------PSR-----------------------------------------------------------------------------------------------

        self.psr_frm = Frame(tabs[8], height=50)
        self.psr_frm.pack(side=TOP, fill=X)
        self.psr_cv = Canvas(tabs[8])
        self.psr_cv.pack(fill=BOTH, anchor=W, side=LEFT, expand=YES)
        self.psr_cv_frm = Frame(self.psr_cv, padx=10)
        self.psr_cv.create_window(0, 0, anchor=NW, window=self.psr_cv_frm)

        ttk.Label(self.psr_frm, text=self.tst.l.gpio_grp_reg_names_w_width[7], font=("Helvetica", 10, "bold")).place(relx=0.49, rely=0.35, anchor=NE)
        self.widgets["psr"] = ttk.Combobox(self.psr_frm, value=self.tst.l.gpio_vals[7], textvariable=self.tst.v.gpio_sel[7], width=10, state="readonly")
        self.widgets["psr"].bind("<<ComboboxSelected>>", lambda event, frame=self.psr_cv_frm, txt=self.tst.v.gpio_sel[7], num=72, r=7: self.cell_event(event, frame, txt, num, r))
        self.widgets["cb7"].bind("<<ComboboxSelected>>", lambda event, frame=self.psr_cv_frm, txt=self.tst.v.gpio_sel[7], num=72, r=7: self.cell_event(event, frame, txt, num, r))
        self.widgets["psr"].place(relx=0.51, rely=0.35, anchor=NW)

        for i in range(8):
            ttk.Label(self.psr_cv_frm, text=i, width=5, relief=SOLID, anchor=CENTER, font=("Arial", 10, "normal")).grid(row=i, column=0, ipady=15, sticky=NSEW)

        for (i, x) in list(enumerate(self.tst.l.psr_choice)):
            r = i // 8
            c = i % 8 + 1
            ttk.Label(self.psr_cv_frm, text=x, width=15, relief=SOLID, anchor=CENTER, wraplength=100).grid(row=r, column=c, sticky=NSEW)

        psr_slave = self.psr_cv_frm.grid_slaves()
        for i in range(72):
            psr_info = psr_slave[i].grid_info()
            if psr_info["row"] == 0:
                psr_slave[i].configure(background="yellow")

# --------------------CORE----------------------------------------------------------------------------------------------

        self.cor_frm = Frame(tabs[9], height=50)
        self.cor_frm.pack(side=TOP, fill=X)
        self.cor_cv = Canvas(tabs[9])
        self.cor_cv.pack(fill=BOTH, anchor=W, side=LEFT, expand=YES)
        self.cor_cv_frm = Frame(self.cor_cv, padx=10)
        self.cor_cv.create_window(0, 0, anchor=NW, window=self.cor_cv_frm)

        ttk.Label(self.cor_frm, text=self.tst.l.gpio_grp_reg_names_w_width[8], font=("Helvetica", 10, "bold")).place(relx=0.49, rely=0.35, anchor=NE)
        self.widgets["cor"] = ttk.Combobox(self.cor_frm, value=self.tst.l.gpio_vals[8], textvariable=self.tst.v.gpio_sel[8], width=10, state="readonly")
        self.widgets["cor"].bind("<<ComboboxSelected>>", self.cor_sel_event)
        self.widgets["cb8"].bind("<<ComboboxSelected>>", lambda event, frame=None, txt=None, num=None, r=8: self.cell_event(event, frame, txt, num, r))
        self.widgets["cor"].place(relx=0.51, rely=0.35, anchor=NW)

        ttk.Label(self.cor_cv_frm, text="-", width=5, relief=SOLID, anchor=CENTER, font=("Arial", 10, "normal"), background="yellow").grid(row=0, column=0, ipady=15, sticky=NSEW)

        for (i, x) in list(enumerate(self.tst.l.cor_choice, 1)):
            ttk.Label(self.cor_cv_frm, text=x, width=15, relief=SOLID, anchor=CENTER, background="yellow").grid(row=0, column=i, sticky=NSEW)

    # Combobox Select Event
    def label_data_event(self, event, num):
        if self.tst.v.bit_sel[num].get() not in [str(x) for x in range(8)]:
            return
        if self.tst.v.grp_sel[num].get() == self.tst.l.gpio_grps[0]:
            self.tst.v.txt_sel[num].set("")
            if self.tst.v.prev_sel[num].get() != "":
                for rc in self.tst.v.prev_sel[num].get().split():
                    if rc not in [x.get() for x in self.tst.v.prev_sel[:num] + self.tst.v.prev_sel[num + 1:]]:
                        self.widgets["lb" + rc].configure(background="gray95")
            self.remove_highlight()
            return

        grp_r = [lambda: self.tst.l.gpio_grps.index(self.tst.l.grp_sel[num].get()), lambda: self.tst.l.gpio_grps.index(self.tst.l.grp_sel[num].get()) - 1][self.tst.l.gpio_grps.index(self.tst.l.grp_sel[num].get()) == 1]()
        if self.tst.v.gpio_sel[grp_r].get() == "OFF":
            self.tst.v.txt_sel[num].set("0")
        else:
            i = self.tst.l.gpio_grps.index(self.tst.v.grp_sel[num].get()) - 1
            txt_list = [self.tst.v.gpio_sel[0], self.tst.v.gpio_sel[2], self.tst.v.gpio_sel[3], self.tst.v.tcn_new, self.tst.v.cdc_new, self.tst.v.gpio_sel[6], self.tst.v.gpio_sel[7], self.tst.v.gpio_sel[8]]
            r_num = [lambda: int(txt_list[i].get()), lambda: 0][txt_list[i].get() == "-"]()
            c_num = int(self.tst.v.bit_sel[num].get())

            if i == 1:
                self.tst.v.txt_sel[num].set(self.tst.l.sam_choice0[int(self.tst.v.gpio_sel[1].get())] + ": " + self.tst.l.name_list[i][r_num][c_num])
            else:
                self.tst.v.txt_sel[num].set(self.tst.l.name_list[i][r_num][c_num])
        ttk.Label(self.main_l, textvariable=self.tst.v.txt_sel[num], anchor=W).grid(row=num + 1, column=3, padx=3, sticky=W)

        self.cell_highlight_event(event, num)

    def select_event(self, event, frame, txt, num):
        slave = list(reversed(frame.grid_slaves()))
        for i in range(num):
            info = slave[i].grid_info()
            slave[i].configure(background="gray95")
            if info["column"] == 0:
                slave[i].configure(font=("Arial", 10, "normal"))
            if int(txt.get()) == info["row"]:
                slave[i].configure(background="yellow")
                if info["column"] == 0:
                    slave[i].configure(font=("Arial", 10, "bold"))

        for x in range(8):
            self.label_data(x)

    def sam_sel_event(self, event):
        slave = list(reversed(self.sam_cv0_frm.grid_slaves()))
        for i in range(4):
            slave[i].configure(background="gray95", font=("Arial", 10, "normal"))
            if self.tst.v.gpio_sel[1].get() == str(i):
                slave[i].configure(background="yellow", font=("Arial", 10, "bold"))
        for i in range(4, 8):
            slave[i].configure(background="gray95")
            if self.tst.v.gpio_sel[1].get() == str(i - 4):
                slave[i].configure(background="yellow")

        for k in range(8):
            self.label_data(k)

    def tcn_sel_event(self, event, frame, txt, num):
        if int(self.tst.v.gpio_sel[4].get()) <= 3:
            self.tst.v.tcn_new.set(self.tst.v.gpio_sel[4].get())
        elif int(self.tst.v.gpio_sel[4].get()) >= 8:
            self.tst.v.tcn_new.set(int(self.tst.v.gpio_sel[4].get()) - 4)
        self.select_event(event, frame, txt, num)

    def cdc_sel_event(self, event, frame, txt, num):
        if int(self.tst.v.gpio_sel[5].get()) <= 5:
            self.tst.v.cdc_new.set(self.tst.v.gpio_sel[5].get())
        elif int(self.tst.v.gpio_sel[5].get()) >= 8:
            self.tst.v.cdc_new.set(int(self.tst.v.gpio_sel[5].get()) - 2)
        self.select_event(event, frame, txt, num)

    def cor_sel_event(self, event):
        slave = self.cor_cv_frm.grid_slaves()
        if self.tst.v.gpio_sel[8].get() != "":
            slave[8].configure(font=("Arial", 10, "bold"))
            for i in range(9):
                slave[i].configure(background="yellow")

    def cell_event(self, event, frame, txt, num, r):
        if r == 1:
            self.sam_sel_event(event)
            return
        elif r == 8:
            self.cor_sel_event(event)
            return

        if r == 4:
            self.tcn_sel_event(event, frame, txt, num)
            grp_r = [lambda: int(self.tst.v.gpio_sel[r].get()), lambda: int(self.tst.v.gpio_sel[r].get()) - 4][int(self.tst.v.gpio_sel[r].get()) >= 8]()
        elif r == 5:
            self.cdc_sel_event(event, frame, txt, num)
            grp_r = [lambda: int(self.tst.v.gpio_sel[r].get()), lambda: int(self.tst.v.gpio_sel[r].get()) - 2][int(self.tst.v.gpio_sel[r].get()) >= 8]()
        else:
            self.select_event(event, frame, txt, num)
            grp_r = int(self.tst.v.gpio_sel[r].get())

        grp = [lambda: r - 1, lambda: r][r == 0]()
        for c in range(8):
            cell_txt = [lambda: list(reversed(self.tst.l.name_list[grp][grp_r]))[c], lambda: list(reversed(self.tst.l.name_list[grp][grp_r]))[c][:19] + "..."][len(list(reversed(self.tst.l.name_list[grp][grp_r]))[c]) > 22]()
            self.tst.v.gpio_cell[r][c].set(cell_txt)

    def cell_highlight_event(self, event, num):
        if self.tst.v.prev_sel[num].get() != "":
            for rc in self.tst.v.prev_sel[num].get().split():
                if rc not in [x.get() for x in self.tst.v.prev_sel[:num] + self.tst.v.prev_sel[num + 1:]]:
                    self.widgets["lb" + rc].configure(background="gray95")

        r = [lambda: self.tst.l.gpio_grps.index(self.tst.v.grp_sel[num].get()), lambda: self.tst.l.gpio_grps.index(self.tst.v.grp_sel[num].get()) - 1][self.tst.l.gpio_grps.index(self.tst.v.grp_sel[num].get()) == 1]()
        c = 7 - int(self.tst.v.bit_sel[num].get())
        self.widgets["lb" + str(r) + str(c)].configure(background="yellow")
        self.tst.v.prev_sel[num].set(str(r) + str(c))
        if r == 2:
            self.widgets["lb1" + self.tst.v.gpio_sel[1].get()].configure(background="yellow")
            self.tst.v.prev_sel[num].set(self.tst.v.prev_sel[num].get() + " 1" + self.tst.v.gpio_sel[1].get())

    # Combobox Select Function
    def label_data(self, num):
        if self.tst.v.bit_sel[num].get() not in [str(x) for x in range(8)]:
            return
        if self.tst.v.grp_sel[num].get() == self.tst.l.gpio_grps[0]:
            self.tst.v.txt_sel[num].set("")
            if self.tst.v.prev_sel[num].get() != "":
                for rc in self.tst.v.prev_sel[num].get().split():
                    if rc not in [x.get() for x in self.tst.v.prev_sel[:num] + self.tst.v.prev_sel[num + 1:]]:
                        self.widgets["lb" + rc].configure(background="gray95")
            self.remove_highlight()
            return

        i = self.tst.l.gpio_grps.index(self.tst.v.grp_sel[num].get()) - 1
        txt_list = [self.tst.v.gpio_sel[0], self.tst.v.gpio_sel[2], self.tst.v.gpio_sel[3], self.tst.v.tcn_new, self.tst.v.cdc_new, self.tst.v.gpio_sel[6], self.tst.v.gpio_sel[7], self.tst.v.gpio_sel[8]]
        r_num = [lambda: int(txt_list[i].get()), lambda: 0][txt_list[i].get() == "-"]()
        c_num = int(self.tst.v.bit_sel[num].get())

        if i == 1:
            self.tst.v.txt_sel[num].set(self.tst.l.sam_choice0[int(self.tst.v.gpio_sel[1].get())] + ": " + self.tst.l.name_list[i][r_num][c_num])
        else:
            self.tst.v.txt_sel[num].set(self.tst.l.name_list[i][r_num][c_num])
        ttk.Label(self.main_l, textvariable=self.tst.v.txt_sel[num], anchor=W).grid(row=num + 1, column=3, padx=3, sticky=W)

        self.cell_highlight(num)

    def select(self, frame, txt, num, deselect=False):
        slave = list(reversed(frame.grid_slaves()))
        for i in range(num):
            info = slave[i].grid_info()
            slave[i].configure(background="gray95")
            if info["column"] == 0:
                slave[i].configure(font=("Arial", 10, "normal"))
            if deselect:
                continue
            if int(txt.get()) == info["row"]:
                slave[i].configure(background="yellow")
                if info["column"] == 0:
                    slave[i].configure(font=("Arial", 10, "bold"))

    def sam_sel(self):
        slave = list(reversed(self.sam_cv0_frm.grid_slaves()))
        for i in range(4):
            slave[i].configure(background="gray95", font=("Arial", 10, "normal"))
            if self.tst.v.gpio_sel[1].get() == str(i):
                slave[i].configure(background="yellow", font=("Arial", 10, "bold"))
        for i in range(4, 8):
            slave[i].configure(background="gray95")
            if self.tst.v.gpio_sel[1].get() == str(i - 4):
                slave[i].configure(background="yellow")

    def tcn_sel(self, frame, txt, num):
        if int(self.tst.v.gpio_sel[4].get()) <= 3:
            self.tst.v.tcn_new.set(self.tst.v.gpio_sel[4].get())
        elif int(self.tst.v.gpio_sel[4].get()) >= 8:
            self.tst.v.tcn_new.set(int(self.tst.v.gpio_sel[4].get()) - 4)
        self.select(frame, txt, num)

    def cdc_sel(self, frame, txt, num):
        if int(self.tst.v.gpio_sel[5].get()) <= 5:
            self.tst.v.cdc_new.set(self.tst.v.gpio_sel[5].get())
        elif int(self.tst.v.gpio_sel[5].get()) >= 8:
            self.tst.v.cdc_new.set(int(self.tst.v.gpio_sel[5].get()) - 2)
        self.select(frame, txt, num)

    def cor_sel(self):
        slave = self.cor_cv_frm.grid_slaves()
        if self.tst.v.gpio_sel[8].get() != "":
            slave[8].configure(font=("Arial", 10, "bold"))
            for i in range(9):
                slave[i].configure(background="yellow")

    def cell(self, frame, txt, num, r):
        if r == 1:
            self.sam_sel()
            return
        elif r == 8:
            return

        if self.tst.v.gpio_sel[r].get() == "OFF":
            for c in range(8):
                self.tst.v.gpio_cell[r][c].set("0")
            self.select(frame, txt, num, deselect=True)
            return

        if r == 4:
            self.tcn_sel(frame, txt, num)
            grp_r = [lambda: int(self.tst.v.gpio_sel[r].get()), lambda: int(self.tst.v.gpio_sel[r].get()) - 4][int(self.tst.v.gpio_sel[r].get()) >= 8]()
        elif r == 5:
            self.cdc_sel(frame, txt, num)
            grp_r = [lambda: int(self.tst.v.gpio_sel[r].get()), lambda: int(self.tst.v.gpio_sel[r].get()) - 2][int(self.tst.v.gpio_sel[r].get()) >= 8]()
        else:
            self.select(frame, txt, num)
            grp_r = int(self.tst.v.gpio_sel[r].get())

        grp = [lambda: r - 1, lambda: r][r == 0]()
        for c in range(8):
            cell_txt = [lambda: list(reversed(self.tst.l.name_list[grp][grp_r]))[c], lambda: list(reversed(self.tst.l.name_list[grp][grp_r]))[c][:19] + "..."][len(list(reversed(self.tst.l.name_list[grp][grp_r]))[c]) > 22]()
            self.tst.v.gpio_cell[r][c].set(cell_txt)

    def cell_highlight(self, num):
        if self.tst.v.prev_sel[num].get() != "":
            for rc in self.tst.v.prev_sel[num].get().split():
                if rc not in [x.get() for x in self.tst.v.prev_sel[:num] + self.tst.v.prev_sel[num + 1:]]:
                    self.widgets["lb" + rc].configure(background="gray95")

        r = [lambda: self.tst.l.gpio_grps.index(self.tst.v.grp_sel[num].get()), lambda: self.tst.l.gpio_grps.index(self.tst.v.grp_sel[num].get()) - 1][self.tst.l.gpio_grps.index(self.tst.v.grp_sel[num].get()) == 1]()
        c = 7 - int(self.tst.v.bit_sel[num].get())
        self.widgets["lb" + str(r) + str(c)].configure(background="yellow")
        self.tst.v.prev_sel[num].set(str(r) + str(c))
        if r == 2:
            self.widgets["lb1" + self.tst.v.gpio_sel[1].get()].configure(background="yellow")
            self.tst.v.prev_sel[num].set(self.tst.v.prev_sel[num].get() + " 1" + self.tst.v.gpio_sel[1].get())

    def remove_highlight(self):
        for i in range(1, 9):
            if i == 1:
                rows = [0]
            elif i == 2:
                rows = [1, 2]
            else:
                rows = [i]

            if self.tst.l.gpio_grps[i] not in [x.get() for x in self.tst.v.grp_sel]:
                for rc in [str(r) + str(c) for r in rows for c in range([lambda: 8, lambda: 4][r == 1]())]:
                    self.widgets["lb" + rc].configure(background="gray95")

    # Button Functions
    def gpio_load(self):
        if "GPIO" not in self.spl.l.groups_unique:
            messagebox.showwarning("WARNING", "Must Add Excel")
            return

        for iid in [x[0] for x in self.reg.l.children]:
            name = self.reg_tab.name_tree.item(iid, "text")
            val = self.reg_tab.name_tree.item(iid, "value")
            if name == self.tst.l.gpio_grp_reg_names_wo_width[0]:
                self.widgets["mit"].current(int(val[1][len(val[1]) - 3:len(val[1])], 2))
            elif name == self.tst.l.gpio_grp_reg_names_wo_width[1]:
                self.widgets["sm0"].current(int(val[1][len(val[1]) - 2:len(val[1])], 2))
            elif name == self.tst.l.gpio_grp_reg_names_wo_width[2]:
                self.widgets["sm1"].current(int(val[1][len(val[1]) - 3:len(val[1])], 2))
            elif name == self.tst.l.gpio_grp_reg_names_wo_width[3]:
                if int(val[1][len(val[1]) - 8:len(val[1])], 2) > 21:
                    self.tst.v.gpio_sel[3].set("OFF")
                else:
                    self.widgets["edp"].current(int(val[1][len(val[1]) - 8:len(val[1])], 2))
            elif name == self.tst.l.gpio_grp_reg_names_wo_width[4]:
                if int(val[1][len(val[1]) - 4:len(val[1])], 2) in (4, 5, 6, 7, 15):
                    self.tst.v.gpio_sel[4].set("OFF")
                else:
                    self.widgets["tcn"].current(self.tst.d.tcn_num[int(val[1][len(val[1]) - 4:len(val[1])], 2)])
            elif name == self.tst.l.gpio_grp_reg_names_wo_width[5]:
                if int(val[1][len(val[1]) - 4:len(val[1])], 2) in (6, 7):
                    self.tst.v.gpio_sel[5].set("OFF")
                else:
                    self.widgets["cdc"].current(self.tst.d.cdc_num[int(val[1][len(val[1]) - 4:len(val[1])], 2)])
            elif name == self.tst.l.gpio_grp_reg_names_wo_width[6]:
                if int(val[1][len(val[1]) - 4:len(val[1])], 2) > 5:
                    self.widgets["upi"].current(5)
                else:
                    self.widgets["upi"].current(int(val[1][len(val[1]) - 4:len(val[1])], 2))
            elif name == self.tst.l.gpio_grp_reg_names_wo_width[7]:
                self.widgets["psr"].current(int(val[1][len(val[1]) - 3:len(val[1])], 2))
            else:
                for i in range(8):
                    if name == self.tst.l.gpio_reg_names[i][1]:
                        self.widgets["b" + str(i)].current(int(val[2]))
                    elif name == self.tst.l.gpio_reg_names[i][0]:
                        if int(val[2]) == 7:
                            self.widgets["g" + str(i)].current(int(val[2]) + int(self.reg_tab.name_tree.item(str(self.mer.l.names.index(self.tst.l.gpio_grp_reg_names_wo_width[9])), "value")[2]))
                        else:
                            self.widgets["g" + str(i)].current(int(val[2]))
                for j in range(2):
                    if name == self.tst.l.gpio_reg_names[8 + j]:
                        if (int(val[2]) in (10, 11, 14, 22, 23, 30, 31)) | (int(val[2]) > 33):
                            self.widgets["c" + str(j)].current(0)
                        else:
                            self.widgets["c" + str(j)].current(self.tst.d.clk_num[int(val[2])])
                for k in range(8):
                    if name == self.tst.l.gpio_ext_reg_names[k][0]:
                        if int(val[2]) == 3:
                            self.tst.v.type_sel[k].set("ERROR")
                        else:
                            self.widgets["t" + str(k)].current(int(val[2]))
                    elif name == self.tst.l.gpio_ext_reg_names[k][1]:
                        self.widgets["a" + str(k)].current(int(val[2]))
        
        for k in range(8):
            self.label_data(k)

        self.cell(self.mit_cv_frm, self.tst.v.gpio_sel[0], 23, 0)
        self.cell(None, None, None, 1)
        self.cell(self.sam_cv1_frm, self.tst.v.gpio_sel[2], 26, 2)
        self.cell(self.eDP_cv_frm, self.tst.v.gpio_sel[3], 106, 3)
        self.cell(self.tcn_cv_frm, self.tst.v.tcn_new, 92, 4)
        self.cell(self.cdc_cv_frm, self.tst.v.cdc_new, 126, 5)
        self.cell(self.upi_cv_frm, self.tst.v.gpio_sel[6], 54, 6)
        self.cell(self.psr_cv_frm, self.tst.v.gpio_sel[7], 72, 7)
        self.cell(None, None, None, 8)

    def gpio_set(self):
        gpio_hexa = self.gpio_update_hexa()

        if len(gpio_hexa) == 0:
            return

        for nested_list in gpio_hexa:
            for (news, pgs, nums, bits) in nested_list:
                if news != "":
                    new = news.split()
                    pg = pgs.split()
                    num = nums.split()
                    for i in range(len(new)):
                        pg_idx = self.spl.pages_unique.index(int(pg[i]))
                        if new[i] != self.adr.hexa_per_pg_mod[pg_idx][int(num[i])]:
                            self.reg_tab.modify1(pg[i] + " " + self.adr.num_range[pg_idx][int(num[i]) // 16], pg[i], int(num[i]), new[i], mod_tag="gpio")

        messagebox.showinfo("Set Data to Register Files", "Complete")

    def gpio_i2c(self):
        gpio_hexa = self.gpio_update_hexa()

        if len(gpio_hexa) == 0:
            return

        write_list = []
        first_pg = ""
        first_num = ""
        last_num = ""

        for pg in [x[1] for x in gpio_hexa[0]]:
            if pg != "":
                first_pg = pg
                for page in [x[1] for x in gpio_hexa[0]]:
                    if page != "":
                        if page != first_pg:
                            messagebox.showerror("ERROR", "GPIO Selection Register Not In GPIO Page")
                            return
                break
        for num in [x[2] for x in gpio_hexa[0]]:
            if num != "":
                first_num = num
                break
        for rev_num in list(reversed([x[2] for x in gpio_hexa[0]])):
            if rev_num != "":
                last_num = rev_num
                break

        if (first_pg != "") & (first_num != "") & (last_num != ""):
            new_hexa = self.adr.hexa_per_pg_mod[self.spl.pages_unique.index(first_pg)]
            for (new, pg, num) in gpio_hexa[0]:
                if new != "":
                    new_hexa[num] = new
            new_hexa = new_hexa[first_num:int(last_num) + 1]
            write_list.append((int(f"{first_pg:02X}" + f"{first_num:02X}", 16), " ".join(new_hexa)))

        for (i, (news, pgs, nums, bits)) in list(enumerate(gpio_hexa[1])):
            new = news.split()
            pg = pgs.split()
            num = nums.split()
            bit = bits.split()
            for j in range(len(new)):
                if new[j] != "":
                    bin = f"{int(new[j], 16):08b}"
                    if ":" in bit[j]:
                        bit_l, bit_r = [int(x) for x in bit[j].split(":")]
                        bin_part = bin[8 - bit_l - 1:8 - bit_r]
                    else:
                        bit_l, bit_r = None, int(bit[j])
                        bin_part = bin[8 - bit_r - 1]
                    new_bin = self.p.p.replace_text(bit_r, bit_l, bin_part, self.i2c_tab.read_one_addr(pg[j] + "-" + num[j]))
                    new_hex = f"{int(new_bin, 2):02X}"
                    write_list.append((int(f"{int(pg[j]):02X}" + f"{int(num[j]):02X}", 16), new_hex))

        self.i2c_tab.write_byte_list(write_list)

        messagebox.showinfo("Set I\u00b2C", "Complete")

    def gpio_set_default(self):
        self.set_defaults()
        
        gpio_hexa = self.gpio_update_hexa()

        if len(gpio_hexa) == 0:
            return

        for nested_list in gpio_hexa:
            for (news, pgs, nums, bits) in nested_list:
                new = news.split()
                pg = pgs.split()
                num = nums.split()
                for i in range(len(new)):
                    if new[i] != "":
                        pg_idx = self.spl.pages_unique.index(int(pg[i]))
                        if new[i] != self.adr.hexa_per_pg_mod[pg_idx][int(num[i])]:
                            self.reg_tab.modify1(pg[i] + " " + self.adr.num_range[pg_idx][int(num[i]) // 16], pg[i], int(num[i]), new[i], mod_tag="")
                            spl_idx = []
                            mer_idx = []
                            adr_idx = self.adr.l.pg_and_num.index(pg[i] + "-" + str(num))
                            for (i, pg_num) in list(enumerate([x.split("(")[0] for x in self.spl.addr_total])):
                                if pg_num == pg[i] + "-" + num[i]:
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
                            self.adr.hexa_per_pg[pg_idx][int(num[i])] = self.adr.hexa_per_pg_mod[pg_idx][int(num[i])]

        messagebox.showinfo("Set GPIO Defaults", "Complete")

    def gpio_reset(self):
        if "GPIO" not in self.spl.l.groups_unique:
            messagebox.showwarning("WARNING", "Must Add Excel")
            return

        for i in range(8):
            self.tst.v.grp_sel[i].set(self.tst.v.grp_sel_default[i].get())
            self.tst.v.bit_sel[i].set(self.tst.v.bit_sel_default[i].get())
            self.tst.v.type_sel[i].set(self.tst.v.type_sel_default[i].get())
            self.tst.v.amnt_sel[i].set(self.tst.v.amnt_sel_default[i].get())
        for j in range(2):
            self.tst.v.clk_sel[j].set(self.tst.v.clk_sel_default[j].get())
        for k in range(9):
            self.tst.v.gpio_sel[k].set(self.tst.v.gpio_sel_default[k].get())
        for x in range(8):
            self.label_data(x)

        self.cell(self.mit_cv_frm, self.tst.v.gpio_sel[0], 23, 0)
        self.cell(None, None, None, 1)
        self.cell(self.sam_cv1_frm, self.tst.v.gpio_sel[2], 26, 2)
        self.cell(self.eDP_cv_frm, self.tst.v.gpio_sel[3], 106, 3)
        self.cell(self.tcn_cv_frm, self.tst.v.tcn_new, 92, 4)
        self.cell(self.cdc_cv_frm, self.tst.v.cdc_new, 126, 5)
        self.cell(self.upi_cv_frm, self.tst.v.gpio_sel[6], 54, 6)
        self.cell(self.psr_cv_frm, self.tst.v.gpio_sel[7], 72, 7)
        self.cell(None, None, None, 8)

    def gpio_clear(self):
        for i in range(8):
            self.tst.v.grp_sel[i].set(self.tst.l.gpio_grps[0])
            self.tst.v.bit_sel[i].set("")
            self.tst.v.txt_sel[i].set("")
            self.tst.v.type_sel[i].set("")
            self.tst.v.amnt_sel[i].set("")
        for j in range(2):
            self.tst.v.clk_sel[j].set("OFF")
        for r in range(9):
            self.widgets["cb" + str(r)].current(0)
            for c in range(8):
                if (r == 1) & (c > 3):
                    continue
                self.widgets["lb" + str(r) + str(c)].configure(background="gray95")

        self.cell(self.mit_cv_frm, self.tst.v.gpio_sel[0], 23, 0)
        self.cell(None, None, None, 1)
        self.cell(self.sam_cv1_frm, self.tst.v.gpio_sel[2], 26, 2)
        self.cell(self.eDP_cv_frm, self.tst.v.gpio_sel[3], 106, 3)
        self.cell(self.tcn_cv_frm, self.tst.v.tcn_new, 92, 4)
        self.cell(self.cdc_cv_frm, self.tst.v.cdc_new, 126, 5)
        self.cell(self.upi_cv_frm, self.tst.v.gpio_sel[6], 54, 6)
        self.cell(self.psr_cv_frm, self.tst.v.gpio_sel[7], 72, 7)
        self.cell(None, None, None, 8)

    # etc
    def resize(self, event):
        self.eDP_cv.configure(scrollregion=self.eDP_cv.bbox(ALL))

    def set_defaults(self):
        for i in range(8):
            self.tst.v.grp_sel_default[i].set(self.tst.v.grp_sel[i].get())
            self.tst.v.bit_sel_default[i].set(self.tst.v.bit_sel[i].get())
            self.tst.v.type_sel_default[i].set(self.tst.v.type_sel[i].get())
            self.tst.v.amnt_sel_default[i].set(self.tst.v.amnt_sel[i].get())
        for j in range(2):
            self.tst.v.clk_sel_default[j].set(self.tst.v.clk_sel[j].get())
        for k in range(9):
            self.tst.v.gpio_sel_default[k].set(self.tst.v.gpio_sel[k].get())

    def gpio_update_hexa(self):
        if "GPIO" not in self.spl.l.groups_unique:
            messagebox.showwarning("WARNING", "Must Add Excel")
            return []

        grps = [x.get() for x in self.tst.v.grp_sel]
        bits = [x.get() for x in self.tst.v.bit_sel]
        types = [x.get() for x in self.tst.v.type_sel]
        amnts = [x.get() for x in self.tst.v.amnt_sel]
        hexa = [
                [["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""],                    # grp & bit selection                "consecutive address
                 ["", "", "", ""], ["", "", "", ""],                                                                                                                                # clk selection                       from
                 ["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""]],                   # extend type & amount selection      141-70 to 141-87"
                [["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""]]  # group reg name                     "address scattered throughout reg"
                ]

        if (self.tst.l.gpio_grps[7] in grps) & (self.tst.l.gpio_grps[8] in grps):
            messagebox.showerror("ERROR", "Cannot Set Both PSR & CORE")
            return []

        for i in range(8):
            if grps[i] != "":
                choice = [lambda: self.tst.l.gpio_grps.index(grps[i]), lambda: self.tst.l.gpio_grps.index(grps[i]) - 1][self.tst.l.gpio_grps.index(grps[i]) == 8]()
                idx = self.spl.l.names_wo_width.index(self.tst.l.gpio_reg_names[i][0])
                pg, num = [int(x) for x in self.spl.l.addr_total[idx].split("(")[0].split("-")]
                pg_idx = self.spl.pages_unique.index(pg)
                if ":" in self.spl.addr_bit[idx]:
                    bit_l, bit_r = [int(x) for x in self.spl.addr_bit[idx].split(":")]
                else:
                    bit_l, bit_r = None, int(self.spl.addr_bit[idx])
                if hexa[0][i][0] == "":
                    bin = self.p.p.replace_text(bit_r, bit_l, f"{choice:03b}", text=f"{int(self.adr.l.hexa_per_pg_mod[pg_idx][num], 16):08b}")
                else:
                    bin = self.p.p.replace_text(bit_r, bit_l, f"{choice:03b}", text=f"{int(hexa[0][i][0], 16):08b}")
                hexa[0][i][0] = f"{int(str(bin), 2):02X}"
                for n in (1, 2):
                    if hexa[0][i][n] == "":
                        hexa[0][i][n] = (pg, num)[n - 1]
                    else:
                        if hexa[0][i][n] != (pg, num)[n - 1]:
                            messagebox.showerror("ERROR", "Wrong Address for " + self.tst.l.gpio_reg_names[i][0])
                            return []
            if bits[i] != "":
                choice = self.tst.l.gpio_bits.index(bits[i])
                idx = self.spl.l.names_wo_width.index(self.tst.l.gpio_reg_names[i][1])
                pg, num = [int(x) for x in self.spl.l.addr_total[idx].split("(")[0].split("-")]
                pg_idx = self.spl.pages_unique.index(pg)
                if ":" in self.spl.addr_bit[idx]:
                    bit_l, bit_r = [int(x) for x in self.spl.addr_bit[idx].split(":")]
                else:
                    bit_l, bit_r = None, int(self.spl.addr_bit[idx])
                if hexa[0][i][0] == "":
                    bin = self.p.p.replace_text(bit_r, bit_l, f"{choice:03b}", text=f"{int(self.adr.l.hexa_per_pg_mod[pg_idx][num], 16):08b}")
                else:
                    bin = self.p.p.replace_text(bit_r, bit_l, f"{choice:03b}", text=f"{int(hexa[0][i][0], 16):08b}")
                hexa[0][i][0] = f"{int(str(bin), 2):02X}"
                for n in (1, 2):
                    if hexa[0][i][n] == "":
                        hexa[0][i][n] = (pg, num)[n - 1]
                    else:
                        if hexa[0][i][n] != (pg, num)[n - 1]:
                            messagebox.showerror("ERROR", "Wrong Address for " + self.tst.l.gpio_reg_names[i][1])
                            return []
            if types[i] not in ("", "ERROR"):
                choice = self.tst.l.ext_types.index(types[i])
                idx = self.spl.l.names_wo_width.index(self.tst.l.gpio_ext_reg_names[i][0])
                pg, num = [int(x) for x in self.spl.l.addr_total[idx].split("(")[0].split("-")]
                pg_idx = self.spl.pages_unique.index(pg)
                if ":" in self.spl.addr_bit[idx]:
                    bit_l, bit_r = [int(x) for x in self.spl.addr_bit[idx].split(":")]
                else:
                    bit_l, bit_r = None, int(self.spl.addr_bit[idx])
                if hexa[0][i + 10][0] == "":
                    bin = self.p.p.replace_text(bit_r, bit_l, f"{choice:02b}", text=f"{int(self.adr.l.hexa_per_pg_mod[pg_idx][num], 16):08b}")
                else:
                    bin = self.p.p.replace_text(bit_r, bit_l, f"{choice:02b}", text=f"{int(hexa[0][i + 10][0], 16):08b}")
                hexa[0][i + 10][0] = f"{int(str(bin), 2):02X}"
                for n in (1, 2):
                    if hexa[0][i + 10][n] == "":
                        hexa[0][i + 10][n] = (pg, num)[n - 1]
                    else:
                        if hexa[0][i + 10][n] != (pg, num)[n - 1]:
                            messagebox.showerror("ERROR", "Wrong Address for " + self.tst.l.gpio_ext_reg_names[i][0])
                            return []
            if amnts[i] != "":
                choice = int(amnts[i])
                idx = self.spl.l.names_wo_width.index(self.tst.l.gpio_ext_reg_names[i][1])
                pg, num = [int(x) for x in self.spl.l.addr_total[idx].split("(")[0].split("-")]
                pg_idx = self.spl.pages_unique.index(pg)
                if ":" in self.spl.addr_bit[idx]:
                    bit_l, bit_r = [int(x) for x in self.spl.addr_bit[idx].split(":")]
                else:
                    bit_l, bit_r = None, int(self.spl.addr_bit[idx])
                if hexa[0][i + 10][0] == "":
                    bin = self.p.p.replace_text(bit_r, bit_l, f"{choice:04b}", text=f"{int(self.adr.l.hexa_per_pg_mod[pg_idx][num], 16):08b}")
                else:
                    bin = self.p.p.replace_text(bit_r, bit_l, f"{choice:04b}", text=f"{int(hexa[0][i + 10][0], 16):08b}")
                hexa[0][i + 10][0] = f"{int(str(bin), 2):02X}"
                for n in (1, 2):
                    if hexa[0][i + 10][n] == "":
                        hexa[0][i + 10][n] = (pg, num)[n - 1]
                    else:
                        if hexa[0][i + 10][n] != (pg, num)[n - 1]:
                            messagebox.showerror("ERROR", "Wrong Address for " + self.tst.l.gpio_ext_reg_names[i][1])
                            return []

        for j in range(2):
            if self.tst.v.clk_sel[j].get() != "":
                choice = self.tst.d.inv_clk[self.tst.l.gpio_clks.index(self.tst.v.clk_sel[j].get())]
                idx = self.spl.l.names_wo_width.index(self.tst.l.gpio_reg_names[8 + j])
                pg, num = [int(x) for x in self.spl.l.addr_total[idx].split("(")[0].split("-")]
                pg_idx = self.spl.pages_unique.index(pg)
                if ":" in self.spl.addr_bit[idx]:
                    bit_l, bit_r = [int(x) for x in self.spl.addr_bit[idx].split(":")]
                else:
                    bit_l, bit_r = None, int(self.spl.addr_bit[idx])
                if hexa[0][8 + j][0] == "":
                    bin = self.p.p.replace_text(bit_r, bit_l, f"{choice:06b}", text=f"{int(self.adr.l.hexa_per_pg_mod[pg_idx][num], 16):08b}")
                else:
                    bin = self.p.p.replace_text(bit_r, bit_l, f"{choice:06b}", text=f"{int(hexa[0][8 + j][0], 16):08b}")
                hexa[0][8 + j][0] = f"{int(str(bin), 2):02X}"
                for n in (1, 2):
                    hexa[0][8 + j][n] = (pg, num)[n - 1]

        for k in range(8):
            if self.tst.v.gpio_sel[k].get() != "OFF":
                choice = int(self.tst.v.gpio_sel[k].get())
                indices = [i for i, x in enumerate(self.spl.l.names_wo_width) if x == self.tst.l.gpio_grp_reg_names_wo_width[k]]
                hex_list = []
                pg_list = []
                num_list = []
                bit_list = []
                for idx in indices:
                    pg, num = [int(x) for x in self.spl.l.addr_total[idx].split("(")[0].split("-")]
                    pg_idx = self.spl.pages_unique.index(pg)
                    bit_l, bit_r = [int(x) for x in self.tst.l.gpio_grp_widths[k].split(":")]
                    bin = self.p.p.replace_text(bit_r, bit_l, f"{choice:b}".zfill(bit_l - bit_r + 1), text=f"{int(self.adr.l.hexa_per_pg_mod[pg_idx][num], 16):08b}")
                    hex_list.append(f"{int(str(bin), 2):02X}")
                    pg_list.append(str(pg))
                    num_list.append(str(num))
                    bit_list.append(self.spl.l.addr_bit[idx])
                hexa[1][k][0] = " ".join(hex_list)
                hexa[1][k][1] = " ".join(pg_list)
                hexa[1][k][2] = " ".join(num_list)
                hexa[1][k][3] = " ".join(bit_list)

        if self.tst.l.gpio_grps[7] in grps:
            idx = self.spl.l.names_wo_width.index(self.tst.l.gpio_grp_reg_names_wo_width[9])
            pg, num = [int(x) for x in self.spl.l.addr_total[idx].split("(")[0].split("-")]
            pg_idx = self.spl.pages_unique.index(pg)
            bit_l, bit_r = None, int(self.spl.addr_bit[idx])
            bin = self.p.p.replace_text(bit_r, bit_l, "1", text=f"{int(self.adr.l.hexa_per_pg_mod[pg_idx][num], 16):08b}")
            hexa[1][8][0] = f"{int(str(bin), 2):02X}"
            for n in (1, 2):
                hexa[1][8][n] = (pg, num)[n - 1]
            hexa[1][8][3] = self.spl.l.addr_bit[idx]
        elif self.tst.l.gpio_grps[8] in grps:
            idx = self.spl.l.names_wo_width.index(self.tst.l.gpio_grp_reg_names_wo_width[9])
            pg, num = [int(x) for x in self.spl.l.addr_total[idx].split("(")[0].split("-")]
            pg_idx = self.spl.pages_unique.index(pg)
            bit_l, bit_r = None, int(self.spl.addr_bit[idx])
            bin = self.p.p.replace_text(bit_r, bit_l, "1", text=f"{int(self.adr.l.hexa_per_pg_mod[pg_idx][num], 16):08b}")
            hexa[1][8][0] = f"{int(str(bin), 2):02X}"
            for n in (1, 2):
                hexa[1][8][n] = (pg, num)[n - 1]
            hexa[1][8][3] = self.spl.l.addr_bit[idx]

        return hexa