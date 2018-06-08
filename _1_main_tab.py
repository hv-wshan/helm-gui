from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from math import ceil, log2


class MainTab:
    def __init__(self, parent):
        self.p = parent
        self.gui = self.p.gui
        self.main = self.p.main
        self.spl = self.p.spl

        main_note = ttk.Notebook(self.p.main_frm)
        main_note.pack(fill=BOTH, expand=YES)

        disp_frm = ttk.Frame(main_note, padding=self.gui.v.pad.get() * 5)
        freq_frm = ttk.Frame(main_note, padding=self.gui.v.pad.get() * 5)
        ltps_frm = ttk.Frame(main_note, padding=self.gui.v.pad.get() * 5)
        main_note.add(disp_frm, text=" Display ")
        main_note.add(freq_frm, text=" Frequncy ")
        main_note.add(ltps_frm, text=" LTPS ")

        disp0 = ttk.Frame(disp_frm)
        disp1 = ttk.Frame(disp_frm)
        disp0.place(relx=0, rely=0, relwidth=0.6, relheight=1)
        disp1.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)
        ttk.Label(disp0, text="Resolution").grid(row=0, column=0, sticky=NW)
        ttk.Label(disp0, text="H active ").grid(row=1, column=0, sticky=NE)
        ttk.Label(disp0, text="H blank ").grid(row=2, column=0, sticky=NE)
        ttk.Label(disp0, text="H front-porch ").grid(row=3, column=0, sticky=NE)
        ttk.Label(disp0, text="H back-porch ").grid(row=4, column=0, sticky=NE)
        ttk.Label(disp0, text="V active ").grid(row=1, column=2, sticky=NE)
        ttk.Label(disp0, text="V blank ").grid(row=2, column=2, sticky=NE)
        ttk.Label(disp0, text="V front-porch ").grid(row=3, column=2, sticky=NE)
        ttk.Label(disp0, text="V back-porch ").grid(row=4, column=2, sticky=NE)
        ttk.Label(disp0, text="\n" + "Drive IC").grid(row=5, column=0, sticky=NW)
        ttk.Label(disp0, text="D-IC type ").grid(row=6, column=0, sticky=NE)
        ttk.Label(disp0, text="2:1 MUX").grid(row=6, column=1, sticky=NW)
        ttk.Label(disp0, text="# of D-IC ").grid(row=7, column=0, sticky=NE)
        ttk.Label(disp0, text="channels per D-IC ").grid(row=8, column=0, sticky=NE)
        ttk.Label(disp0, text="Starting offset ").grid(row=9, column=0, sticky=NE)
        ttk.Label(disp0, text="of 1st D-IC (px) ").grid(row=10, column=0, sticky=NE)
        for i in range(6):
            ttk.Label(disp0, text="Lane " + str(i) + " ").grid(row=i + 6, column=2, sticky=NE)
            ttk.Entry(disp0, textvariable=self.main.v.dic_lane[i], width=15, state="readonly").grid(row=i + 6, column=3, sticky=NW)
        ttk.Entry(disp0, textvariable=self.main.v.hres, width=5).grid(row=1, column=1, sticky=NW, padx=(0, 50))
        ttk.Entry(disp0, textvariable=self.main.v.hblank, width=5, state="readonly").grid(row=2, column=1, sticky=NW, padx=(0, 50))
        ttk.Entry(disp0, textvariable=self.main.v.hb_fp, width=5).grid(row=3, column=1, sticky=NW, padx=(0, 50))
        ttk.Entry(disp0, textvariable=self.main.v.hb_bp, width=5).grid(row=4, column=1, sticky=NW, padx=(0, 50))
        ttk.Entry(disp0, textvariable=self.main.v.vres, width=5).grid(row=1, column=3, sticky=NW)
        ttk.Entry(disp0, textvariable=self.main.v.vblank, width=5, state="readonly").grid(row=2, column=3, sticky=NW)
        ttk.Entry(disp0, textvariable=self.main.v.vb_fp, width=5).grid(row=3, column=3, sticky=NW)
        ttk.Entry(disp0, textvariable=self.main.v.vb_bp, width=5).grid(row=4, column=3, sticky=NW)
        ttk.Entry(disp0, textvariable=self.main.v.dic_ofs, width=5).grid(row=10, column=1, sticky=NW)
        ttk.Combobox(disp0, textvariable=self.main.v.dic_no, width=5, value=(1, 2, 3, 4, 5, 6), state="readonly").grid(row=7, column=1, sticky=NW)
        ttk.Combobox(disp0, textvariable=self.main.v.dic_ch, width=5, value=self.main.l.dic_ch_list, state="readonly").grid(row=8, column=1, sticky=NW)
        ttk.Button(disp1, text="Load Register Data", width=20, command=self.disp_load_reg).pack(side=TOP, pady=(15, 0), ipady=3)
        ttk.Button(disp1, text="Load IC Data", width=20, command=self.disp_load_ic, state=DISABLED).pack(side=TOP, pady=(15, 0), ipady=3)
        ttk.Button(disp1, text="Set Data", width=20, command=self.disp_set).pack(side=TOP, pady=(15, 0), ipady=3)

        self.main.v.hb_fp.trace0 = self.main.v.hb_fp.trace("w", lambda name, index, mode, type="H": self.calc_blank(type))
        self.main.v.hb_bp.trace1 = self.main.v.hb_bp.trace("w", lambda name, index, mode, type="H": self.calc_blank(type))
        self.main.v.vb_fp.trace2 = self.main.v.vb_fp.trace("w", lambda name, index, mode, type="V": self.calc_blank(type))
        self.main.v.vb_bp.trace3 = self.main.v.vb_bp.trace("w", lambda name, index, mode, type="V": self.calc_blank(type))

        freq0 = ttk.Frame(freq_frm)
        freq1 = ttk.Frame(freq_frm)
        freq0.place(relx=0, rely=0, relwidth=0.6, relheight=1)
        freq1.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)
        ttk.Button(freq1, text="Load Register Data", width=20, command=self.freq_load_reg).pack(side=TOP, pady=(15, 0), ipady=3)
        ttk.Button(freq1, text="Load IC Data", width=20, command=self.freq_load_ic, state=DISABLED).pack(side=TOP, pady=(15, 0), ipady=3)
        ttk.Button(freq1, text="Set Data", width=20, command=self.freq_set).pack(side=TOP, pady=(15, 0), ipady=3)
        ttk.Label(freq0, text="2-PX (MHz) = ").grid(row=3, column=0, pady=(5, 0), sticky=NE)
        ttk.Label(freq0, text="PSR (MHz) = ").grid(row=4, column=0, pady=(5, 0), sticky=NE)
        ttk.Label(freq0, text="UPI (MHz) = ").grid(row=5, column=0, pady=(5, 0), sticky=NE)
        ttk.Label(freq0, text="L/S (MHz) = ").grid(row=6, column=0, pady=(5, 0), sticky=NE)
        ttk.Label(freq0, text="QSPI (MHz) = ").grid(row=7, column=0, pady=(5, 0), sticky=NE)
        ttk.Label(freq0, text="QPI, init (MHz) = ").grid(row=8, column=0, pady=(5, 0), sticky=NE)
        ttk.Label(freq0, text="QPI, normal (MHz) = ").grid(row=9, column=0, pady=(5, 0), sticky=NE)
        for i in range(7):
            ttk.Label(freq0, text=" = 810 * ").grid(row=i + 3, column=2, pady=(5, 0), sticky=NE)
            ttk.Label(freq0, text=" / ").grid(row=i + 3, column=6, pady=(5, 0), sticky=NE)
            if i != 2:
                ttk.Label(freq0, text=" / ").grid(row=i + 3, column=4, pady=(5, 0), sticky=NE)
            if i >= 4:
                ttk.Label(freq0, text=" / ").grid(row=i + 3, column=8, pady=(5, 0), sticky=NE)
        ttk.Entry(freq0, textvariable=self.main.v.freq[0], width=8, state="readonly").grid(row=3, column=1, pady=(5, 0), sticky=NW)
        ttk.Entry(freq0, textvariable=self.main.v.freq[1], width=8, state="readonly").grid(row=4, column=1, pady=(5, 0), sticky=NW)
        ttk.Entry(freq0, textvariable=self.main.v.freq[2], width=8, state="readonly").grid(row=5, column=1, pady=(5, 0), sticky=NW)
        ttk.Entry(freq0, textvariable=self.main.v.freq[3], width=8, state="readonly").grid(row=6, column=1, pady=(5, 0), sticky=NW)
        ttk.Entry(freq0, textvariable=self.main.v.freq[4], width=8, state="readonly").grid(row=7, column=1, pady=(5, 0), sticky=NW)
        ttk.Entry(freq0, textvariable=self.main.v.freq[5], width=8, state="readonly").grid(row=8, column=1, pady=(5, 0), sticky=NW)
        ttk.Entry(freq0, textvariable=self.main.v.freq[6], width=8, state="readonly").grid(row=9, column=1, pady=(5, 0), sticky=NW)

        Spinbox(freq0, from_=0.5, to=4, increment=0.002, textvariable=self.main.v.mlt[0], width=6, command=lambda num=0: self.calc_freq(num)).grid(row=3, column=3, pady=(5, 0), sticky=NW)
        Spinbox(freq0, from_=0.5, to=4, increment=0.002, textvariable=self.main.v.mlt[0], width=6, command=lambda num=1: self.calc_freq(num)).grid(row=4, column=3, pady=(5, 0), sticky=NW)
        Spinbox(freq0, from_=0.5, to=4, increment=0.002, textvariable=self.main.v.mlt[1], width=6, command=lambda num=2: self.calc_freq(num)).grid(row=5, column=3, pady=(5, 0), sticky=NW)
        Spinbox(freq0, from_=0.5, to=4, increment=0.002, textvariable=self.main.v.mlt[2], width=6, command=lambda num=3: self.calc_freq(num)).grid(row=6, column=3, pady=(5, 0), sticky=NW)
        Spinbox(freq0, from_=0.5, to=4, increment=0.002, textvariable=self.main.v.mlt[2], width=6, command=lambda num=4: self.calc_freq(num)).grid(row=7, column=3, pady=(5, 0), sticky=NW)
        Spinbox(freq0, from_=0.5, to=4, increment=0.002, textvariable=self.main.v.mlt[2], width=6, command=lambda num=5: self.calc_freq(num)).grid(row=8, column=3, pady=(5, 0), sticky=NW)
        Spinbox(freq0, from_=0.5, to=4, increment=0.002, textvariable=self.main.v.mlt[2], width=6, command=lambda num=6: self.calc_freq(num)).grid(row=9, column=3, pady=(5, 0), sticky=NW)

        Spinbox(freq0, from_=4, to=31, increment=1, textvariable=self.main.v.div[0], width=6, command=lambda num=0: self.calc_freq(num)).grid(row=3, column=5, pady=(5, 0), sticky=NW)
        Spinbox(freq0, from_=4, to=31, increment=1, textvariable=self.main.v.div[1], width=6, command=lambda num=1: self.calc_freq(num)).grid(row=4, column=5, pady=(5, 0), sticky=NW)
        Spinbox(freq0, from_=4, to=31, increment=1, textvariable=self.main.v.div[2], width=6, command=lambda num=3: self.calc_freq(num)).grid(row=6, column=5, pady=(5, 0), sticky=NW)
        Spinbox(freq0, from_=4, to=31, increment=1, textvariable=self.main.v.div[3], width=6, command=lambda num=4: self.calc_freq(num)).grid(row=7, column=5, pady=(5, 0), sticky=NW)
        Spinbox(freq0, from_=4, to=31, increment=1, textvariable=self.main.v.div[4], width=6, command=lambda num=5: self.calc_freq(num)).grid(row=8, column=5, pady=(5, 0), sticky=NW)
        Spinbox(freq0, from_=4, to=31, increment=1, textvariable=self.main.v.div[4], width=6, command=lambda num=6: self.calc_freq(num)).grid(row=9, column=5, pady=(5, 0), sticky=NW)

        Spinbox(freq0, from_=1, to=4, increment=1, textvariable=self.main.v.div[5], width=6, command=lambda num=0: self.calc_freq(num)).grid(row=3, column=7, pady=(5, 0), sticky=NW)
        Spinbox(freq0, from_=1, to=4, increment=1, textvariable=self.main.v.div[6], width=6, command=lambda num=1: self.calc_freq(num)).grid(row=4, column=7, pady=(5, 0), sticky=NW)
        Spinbox(freq0, from_=1, to=4, increment=1, textvariable=self.main.v.div[7], width=6, command=lambda num=2: self.calc_freq(num)).grid(row=5, column=7, pady=(5, 0), sticky=NW)
        Spinbox(freq0, from_=1, to=4, increment=1, textvariable=self.main.v.div[8], width=6, command=lambda num=3: self.calc_freq(num)).grid(row=6, column=7, pady=(5, 0), sticky=NW)
        Spinbox(freq0, from_=1, to=4, increment=1, textvariable=self.main.v.div[9], width=6, command=lambda num=4: self.calc_freq(num)).grid(row=7, column=7, pady=(5, 0), sticky=NW)
        Spinbox(freq0, from_=1, to=4, increment=1, textvariable=self.main.v.div[10], width=6, command=lambda num=5: self.calc_freq(num)).grid(row=8, column=7, pady=(5, 0), sticky=NW)
        Spinbox(freq0, from_=1, to=4, increment=1, textvariable=self.main.v.div[10], width=6, command=lambda num=6: self.calc_freq(num)).grid(row=9, column=7, pady=(5, 0), sticky=NW)

        Spinbox(freq0, values=(1, 2), textvariable=self.main.v.div[11], width=6, command=lambda num=4: self.calc_freq(num)).grid(row=7, column=9, pady=(5, 0), sticky=NW)
        Spinbox(freq0, values=(1, 2, 4, 8), textvariable=self.main.v.div[12], width=6, command=lambda num=5: self.calc_freq(num)).grid(row=8, column=9, pady=(5, 0), sticky=NW)
        Spinbox(freq0, values=(1, 2, 4, 8), textvariable=self.main.v.div[13], width=6, command=lambda num=6: self.calc_freq(num)).grid(row=9, column=9, pady=(5, 0), sticky=NW)

        [self.main.v.mlt[x].set("") for x in range(3)]
        [self.main.v.div[x].set("") for x in range(14)]

    # Display Tab
    def calc_blank(self, type):
        if type.upper() == "H":
            fp = self.main.v.hb_fp.get()
            bp = self.main.v.hb_bp.get()
            blank = self.main.v.hblank
        elif type.upper() == "V":
            fp = self.main.v.vb_fp.get()
            bp = self.main.v.vb_bp.get()
            blank = self.main.v.vblank
        else:
            raise ValueError("Invalid argument value in calc_blank(): 'type'")

        if (fp == "") | (bp == ""):
            blank.set("")
        else:
            try:
                blank.set(int(fp) + int(bp))
            except ValueError:
                blank.set("")

    def disp_load_reg(self):
        if len(self.spl.l.names_wo_width) == 0:
            messagebox.showerror("ERROR", "Must Import Excel")
            return
        if "TCON" not in self.spl.l.groups_unique:
            messagebox.showwarning("WARNING", "Must Add Excel")
            return

        self.main.v.hb_fp.trace_vdelete("w", self.main.v.hb_fp.trace0)
        self.main.v.hb_bp.trace_vdelete("w", self.main.v.hb_bp.trace1)
        self.main.v.vb_fp.trace_vdelete("w", self.main.v.vb_fp.trace2)
        self.main.v.vb_bp.trace_vdelete("w", self.main.v.vb_bp.trace3)

        hres = self.p.get_val_by_name("HRES", "#3")
        hb = self.p.get_val_by_name("HB", "#3")
        hb_fp = self.p.get_val_by_name("HB_FP", "#3")
        vres = self.p.get_val_by_name("VRES", "#3")
        vb = self.p.get_val_by_name("VB", "#3")
        vb_fp = self.p.get_val_by_name("VB_FP", "#3")
        dic_no = self.p.get_val_by_name("DIC_NO", "#3")
        dic_ch = self.p.get_val_by_name("DIC_LEN", "#3")
        dic_ofs = self.p.get_val_by_name("DIC_OFS", "#3")

        self.main.v.hres.set(hres)
        self.main.v.hblank.set(hb)
        self.main.v.hb_fp.set(hb_fp)
        self.main.v.hb_bp.set(int(self.main.v.hblank.get()) - int(self.main.v.hb_fp.get()))
        self.main.v.vres.set(vres)
        self.main.v.vblank.set(vb)
        self.main.v.vb_fp.set(vb_fp)
        self.main.v.vb_bp.set(int(self.main.v.vblank.get()) - int(self.main.v.vb_fp.get()))
        self.main.v.dic_no.set(dic_no)
        self.main.v.dic_ch.set(int(dic_ch) * 3)
        self.main.v.dic_ofs.set(dic_ofs)

        dic_start = 2 - (int(dic_no) - 1) // 2
        px_start = 1
        for ic in range(6):
            self.main.v.dic_lane[ic].set("")
        for ic in range(int(dic_no)):
            if ic == 0:
                px_len = int(dic_ch) * 2 - int(dic_ofs)
            else:
                px_len = int(dic_ch) * 2
            px_end = px_start - 1 + px_len
            if px_end > int(hres):
                px_end = int(hres)
            self.main.v.dic_lane[dic_start + ic].set(f"{px_start:4d}px ~ {px_end:4d}px")
            px_start = px_end + 1

        self.main.v.hb_fp.trace0 = self.main.v.hb_fp.trace("w", lambda name, index, mode, type="H": self.calc_blank(type))
        self.main.v.hb_bp.trace1 = self.main.v.hb_bp.trace("w", lambda name, index, mode, type="H": self.calc_blank(type))
        self.main.v.vb_fp.trace2 = self.main.v.vb_fp.trace("w", lambda name, index, mode, type="V": self.calc_blank(type))
        self.main.v.vb_bp.trace3 = self.main.v.vb_bp.trace("w", lambda name, index, mode, type="V": self.calc_blank(type))

    def disp_load_ic(self):
        return

    def disp_set(self):
        if len(self.spl.l.names_wo_width) == 0:
            messagebox.showerror("ERROR", "Must Import Excel")
            return
        if "TCON" not in self.spl.l.groups_unique:
            messagebox.showwarning("WARNING", "Must Add Excel")
            return

        hres = int(self.main.v.hres.get())
        hb = int(self.main.v.hblank.get())
        hb_fp = int(self.main.v.hb_fp.get())
        vres = int(self.main.v.vres.get())
        vb = int(self.main.v.vblank.get())
        vb_fp = int(self.main.v.vb_fp.get())
        vb_bp = int(self.main.v.vb_bp.get())
        dic_no = int(self.main.v.dic_no.get())
        dic_ch = int(self.main.v.dic_ch.get())
        dic_ofs = int(self.main.v.dic_ofs.get())

        self.p.set_val_by_name("HRES", "#3", hres)
        self.p.set_val_by_name("HB", "#3", hb)
        self.p.set_val_by_name("HB_FP", "#3", hb_fp)
        self.p.set_val_by_name("VRES", "#3", vres)
        self.p.set_val_by_name("VB", "#3", vb)
        self.p.set_val_by_name("VB_FP", "#3", vb_fp)
        self.p.set_val_by_name("BIST_HRES", "#3", hres)
        self.p.set_val_by_name("BIST_HB", "#3", hb)
        self.p.set_val_by_name("BIST_HB_FP", "#3", hb_fp)
        self.p.set_val_by_name("BIST_VRES", "#3", vres)
        self.p.set_val_by_name("BIST_VB", "#3", vb)
        self.p.set_val_by_name("BIST_VB_FP", "#3", vb_fp)
        self.p.set_val_by_name("cfg_rx_vback_porch", "#3", vb_bp - 1)
        self.p.set_val_by_name("cfg_poc_hres", "#3", hres)
        self.p.set_val_by_name("cfg_poc_vres", "#3", vres)
        self.p.set_val_by_name("cfg_poc_total_num", "#3", 270 + ((hres - 1) // 8 + 1 + 1) * ((vres - 1) // 4 + 1 + 1) * 4)
        self.p.set_val_by_name("cfg_poc_lite_total_num", "#3", 20 + ((hres - 1) // 64 + 1 + 1) * ((vres - 1)//32 + 1 + 1) * 4)
        self.p.set_val_by_name('PPS_pic_height', "#3", vres)
        self.p.set_val_by_name('PPS_pic_width', "#3", hres)
        self.p.set_val_by_name('PPS_slice_width', "#3", hres // 2)
        self.p.set_val_by_name('PPS_chunk_size', "#3", hres // 2 * 8 // 8)

        initial_scale_value = int(self.p.get_val_by_name("PPS_initial_scale_value", "#3"))
        if initial_scale_value > (hres // 2 + 2) // 3 + 8:
            initial_scale_value = (hres // 2 + 2) // 3 + 8 + 8
        self.p.set_val_by_name("PPS_initial_scale_value", "#3", initial_scale_value)

        slice_height = int(self.p.get_val_by_name("PPS_slice_height", "#3"))
        bpg_ofs = 12 + int(0.09 * (slice_height - 8))
        if bpg_ofs > 21:
            bpg_ofs = 21
        self.p.set_val_by_name("PPS_first_line_bpg_offset", "#3", bpg_ofs)
        self.p.set_val_by_name("PPS_nfl_bpg_offset", "#3", ceil(bpg_ofs * 2 ** 16 / (slice_height - 1)))

        self.p.set_val_by_name("DIC_NO", "#3", dic_no)
        self.p.set_val_by_name("DIC_LEN", "#3", dic_ch // 3)
        self.p.set_val_by_name("DIC_OFS", "#3", dic_ofs)

        upi_sel = self.main.l.dic_ch_list.index(dic_ch)
        for ic in range(6):
            self.p.set_val_by_name(f"UPI_SEL_{ic}", "#3", upi_sel)

        messagebox.showinfo("Set Data to Register Files", "Complete")

    # Frequency Tab
    def freq_load_reg(self):
        if len(self.spl.l.names_wo_width) == 0:
            messagebox.showerror("ERROR", "Must Import Excel")
            return
        if "mithril" not in self.spl.l.groups_unique:
            messagebox.showwarning("WARNING", "Must Add Excel")
            return

        frac0 = int(self.p.get_val_by_name("mn_t", "#3")) / 512
        frac1 = int(self.p.get_val_by_name("mn_u", "#3")) / 512
        frac2 = int(self.p.get_val_by_name("mn_m", "#3")) / 512
        div0 = int(self.p.get_val_by_name("mt_dv2", "#3"))
        div1 = int(self.p.get_val_by_name("mt_dv1", "#3"))
        div2 = int(self.p.get_val_by_name("mm_dv1", "#3"))
        div3 = int(self.p.get_val_by_name("mm_dv2", "#3"))
        div4 = int(self.p.get_val_by_name("mm_dv3", "#3"))
        div5 = int(self.p.get_val_by_name("mt_post_dv2", "#3"))
        div6 = int(self.p.get_val_by_name("mt_post_dv1", "#3"))
        div7 = int(self.p.get_val_by_name("f_dv", "#3"))
        div8 = int(self.p.get_val_by_name("mm_post_dv1", "#3"))
        div9 = int(self.p.get_val_by_name("mm_post_dv2", "#3"))
        div10 = int(self.p.get_val_by_name("mm_post_dv3", "#3"))
        div11 = int(self.p.get_val_by_name("mm_post2_dv2", "#3"))
        div12 = int(self.p.get_val_by_name("mm_post2a_dv3", "#3"))
        div13 = int(self.p.get_val_by_name("mm_post2b_dv3", "#3"))

        self.main.v.mlt[0].set(f"{frac0:.3f}")
        self.main.v.mlt[1].set(f"{frac1:.3f}")
        self.main.v.mlt[2].set(f"{frac2:.3f}")
        self.main.v.div[0].set(div0)
        self.main.v.div[1].set(div1)
        self.main.v.div[2].set(div2)
        self.main.v.div[3].set(div3)
        self.main.v.div[4].set(div4)
        self.main.v.div[5].set(div5 + 1)
        self.main.v.div[6].set(div6 + 1)
        self.main.v.div[7].set(div7 + 1)
        self.main.v.div[8].set(div8 + 1)
        self.main.v.div[9].set(div9 + 1)
        self.main.v.div[10].set(div10 + 1)
        self.main.v.div[11].set(div11 + 1)
        self.main.v.div[12].set(2 ** div12)
        self.main.v.div[13].set(2 ** div13)
        self.main.v.freq[0].set(f"{810 * frac0 / div0 / (div5 + 1):.2f}")
        self.main.v.freq[1].set(f"{810 * frac0 / div1 / (div6 + 1):.2f}")
        self.main.v.freq[2].set(f"{810 * frac1 / (div7 + 1):.2f}")
        self.main.v.freq[3].set(f"{810 * frac2 / div2 / (div8 + 1):.2f}")
        self.main.v.freq[4].set(f"{810 * frac2 / div3 / (div9 + 1) / (2 ** div11):.2f}")
        self.main.v.freq[5].set(f"{810 * frac2 / [lambda: div4, lambda: 1][div4 == 0]() / (div10 + 1) / (2 ** div12):.2f}")
        self.main.v.freq[6].set(f"{810 * frac2 / [lambda: div4, lambda: 1][div4 == 0]() / (div10 + 1) / (2 ** div13):.2f}")

    def freq_load_ic(self):
        return

    def freq_set(self):
        if len(self.spl.l.names_wo_width) == 0:
            messagebox.showerror("ERROR", "Must Import Excel")
            return
        if "mithril" not in self.spl.l.groups_unique:
            messagebox.showwarning("WARNING", "Must Add Excel")
            return

        mlt0 = round(float(self.main.v.mlt[0].get()) * 512)
        mlt1 = round(float(self.main.v.mlt[1].get()) * 512)
        mlt2 = round(float(self.main.v.mlt[2].get()) * 512)
        div0 = int(self.main.v.div[0].get())
        div1 = int(self.main.v.div[1].get())
        div2 = int(self.main.v.div[2].get())
        div3 = int(self.main.v.div[3].get())
        div4 = int(self.main.v.div[4].get())
        div5 = int(self.main.v.div[5].get())
        div6 = int(self.main.v.div[6].get())
        div7 = int(self.main.v.div[7].get())
        div8 = int(self.main.v.div[8].get())
        div9 = int(self.main.v.div[9].get())
        div10 = int(self.main.v.div[10].get())
        div11 = int(self.main.v.div[11].get())
        div12 = int(self.main.v.div[12].get())
        div13 = int(self.main.v.div[13].get())

        self.p.set_val_by_name("mn_t", "#3", mlt0)
        self.p.set_val_by_name("mt_dv2", "#3", div0)
        self.p.set_val_by_name("mt_post_dv2", "#3", div5 - 1)
        self.p.set_val_by_name("mt_dv1", "#3", div1)
        self.p.set_val_by_name("mt_post_dv1", "#3", div6 - 1)
        self.p.set_val_by_name("mn_u", "#3", mlt1)
        self.p.set_val_by_name("f_dv", "#3", div7 - 1)
        self.p.set_val_by_name("mn_m", "#3", mlt2)
        self.p.set_val_by_name("mm_dv1", "#3", div2)
        self.p.set_val_by_name("mm_post_dv1", "#3", div8 - 1)
        self.p.set_val_by_name("mm_dv2", "#3", div3)
        self.p.set_val_by_name("mm_post_dv2", "#3", div9 - 1)
        self.p.set_val_by_name("mm_post2_dv2", "#3", div11 - 1)
        self.p.set_val_by_name("mm_dv3", "#3", div4)
        self.p.set_val_by_name("mm_post_dv3", "#3", div10 - 1)
        self.p.set_val_by_name("mm_post2a_dv3", "#3", round(log2(div12)))
        self.p.set_val_by_name("mm_post2b_dv3", "#3", round(log2(div13)))

        messagebox.showinfo("Set Data to Register Files", "Complete")

    def calc_freq(self, num):
        if num == 0:
            f = 810 * float(self.main.v.mlt[0].get()) / int(self.main.v.div[0].get()) / int(self.main.v.div[5].get())
        elif num == 1:
            f = 810 * float(self.main.v.mlt[0].get()) / int(self.main.v.div[1].get()) / int(self.main.v.div[6].get())
        elif num == 2:
            f = 810 * float(self.main.v.mlt[1].get()) / int(self.main.v.div[7].get())
        elif num == 3:
            f = 810 * float(self.main.v.mlt[2].get()) / int(self.main.v.div[2].get()) / int(self.main.v.div[8].get())
        elif num == 4:
            f = 810 * float(self.main.v.mlt[2].get()) / int(self.main.v.div[3].get()) / int(self.main.v.div[9].get()) / int(self.main.v.div[11].get())
        elif num == 5:
            f = 810 * float(self.main.v.mlt[2].get()) / int(self.main.v.div[4].get()) / int(self.main.v.div[10].get()) / int(self.main.v.div[12].get())
        elif num == 6:
            f = 810 * float(self.main.v.mlt[2].get()) / int(self.main.v.div[4].get()) / int(self.main.v.div[10].get()) / int(self.main.v.div[13].get())
        else:
            return
        self.main.v.freq[num].set(f"{f:.2f}")