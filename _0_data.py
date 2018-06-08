from tkinter import *


class GUIData:
    def __init__(self):
        self.v = self
        self.l = self

        self.v.version = StringVar(None, "rev0.170726")
        self.v.logfilename = StringVar()
        self.v.log_bool = BooleanVar(None, False)
        self.v.i2c_bool = BooleanVar(None, False)
        self.v.reg_bool = BooleanVar(None, False)
        self.v.log_check = IntVar(None, 0)
        self.v.i2c_check = IntVar(None, 0)
        self.v.reg_check = IntVar(None, 0)
        self.v.pad = IntVar()
        self.logo = b"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"


class MainTabData:
    def __init__(self):
        self.v = self
        self.l = self
        
        # Display Tab
        self.v.hres = StringVar()
        self.v.hblank = StringVar()
        self.v.hb_fp = StringVar()
        self.v.hb_bp = StringVar()
        self.v.vres = StringVar()
        self.v.vblank = StringVar()
        self.v.vb_fp = StringVar()
        self.v.vb_bp = StringVar()
        self.v.dic_no = StringVar(None, "4")
        self.v.dic_ch = StringVar(None, "960")
        self.v.dic_ofs = StringVar()
        self.v.dic_lane = (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar())

        self.l.dic_ch_list = (768, 804, 864, 960)

        # Frequency Tab
        self.v.freq = (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar())
        self.v.mlt = (StringVar(), StringVar(), StringVar())
        self.v.div = (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar())


class RegisterTabData:
    def __init__(self):
        self.v = self
        self.l = self
        
        self.v.xlsx_names = StringVar()
        self.v.search = StringVar()
        self.v.curr_row = IntVar()
        self.v.check0 = IntVar()
        self.v.check1 = IntVar()

        self.l.xlsx_list = []
        self.l.modified_pg = []
        self.l.children = []
        self.l.all_children = []
        self.l.hex_col = ["00", "01", "02", "03", "blank0", "04", "05", "06", "07", "blank1", "08", "09", "0A", "0B", "blank2", "0C", "0D", "0E", "0F"]


class I2CTabData:
    def __init__(self):
        self.v = self
        self.l = self
        
        self.v.slave_addr = StringVar(None, "54")
        self.v.access_addr = StringVar(None, "80 00")
        self.v.write = StringVar(None, "00")
        self.v.read_num = StringVar(None, "1")


class EEPROMTabData:
    def __init__(self):
        self.v = self
        self.l = self
        self.d = self
        
        self.v.slave_addr = StringVar(None, "51")
        self.v.access_addr = StringVar(None, "00 00")
        self.v.write = StringVar()
        self.v.read_num = StringVar(None, "1")
        self.v.pg_id = StringVar()
        self.v.pg_len = StringVar()
        self.v.crc_read = StringVar()
        self.v.crc_sum = StringVar()
        self.v.crc_ofs = StringVar(None, "FE")
        self.v.next_pg = StringVar()
        self.v.write_1 = StringVar()
        self.v.write_list = StringVar()
        self.v.check_mod = StringVar()
        self.v.pri_main = StringVar(None, "4A")
        self.v.pri_core = StringVar(None, "ED 49 96 80 95")
        self.v.pri_base = StringVar(None, "40 41 42 84 82 98 99 9A")
        self.v.import_rom = StringVar()
        self.v.conc = StringVar()
        self.v.txt_main = StringVar()
        self.v.txt_core = StringVar()
        self.v.txt_base = StringVar()
        self.v.txtfile = (StringVar(), StringVar())
        self.v.sub20_pages = StringVar()
        self.v.sub20_pg_num = StringVar()
        self.v.sub20_total_len = StringVar()
        self.v.check = IntVar()

        self.l.r_idx_vars = []

        self.d.eep_imp_pg = {}
        
        # Import Tab
        self.l.imported_txt = []
        self.l.mod_by_eep_pg = []

        # EDID Tab
        self.v.hac = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.hbl = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.hfp = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.hbp = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.hsy = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.vac = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.vbl = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.vfp = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.vbp = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.vsy = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.freq = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.rfsh = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.edid_checksum = StringVar()
        self.v.hac_default = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.hbl_default = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.hfp_default = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.hsy_default = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.vac_default = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.vbl_default = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.vfp_default = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.vsy_default = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.freq_default = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.rfsh_default = (StringVar(), StringVar(), StringVar(), StringVar())
        self.v.edid_checksum_default = StringVar()
        self.v.ed_check0 = IntVar()
        self.v.ed_check1 = IntVar()


class TestTabData:
    def __init__(self):
        self.v = self
        self.l = self
        self.d = self

        # RegFile Summary Tab
        self.l.pages_hex = []
        self.l.grp_per_pg = []
        self.l.wo_cnt = []
        self.l.rw_cnt = []
        self.l.pg_not_used = []

        # GPIO Tab
        self.v.grp_sel = (StringVar(None, "OFF"), StringVar(None, "OFF"), StringVar(None, "OFF"), StringVar(None, "OFF"), StringVar(None, "OFF"), StringVar(None, "OFF"), StringVar(None, "OFF"), StringVar(None, "OFF"))
        self.v.bit_sel = (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar())
        self.v.clk_sel = (StringVar(None, "OFF"), StringVar(None, "OFF"))
        self.v.txt_sel = (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar())
        self.v.grp_sel_default = (StringVar(None, "OFF"), StringVar(None, "OFF"), StringVar(None, "OFF"), StringVar(None, "OFF"), StringVar(None, "OFF"), StringVar(None, "OFF"), StringVar(None, "OFF"), StringVar(None, "OFF"))
        self.v.bit_sel_default = (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar())
        self.v.clk_sel_default = (StringVar(), StringVar())
        self.v.gpio_sel = (StringVar(None, "0"), StringVar(None, "0"), StringVar(None, "0"), StringVar(None, "0"), StringVar(None, "0"), StringVar(None, "0"), StringVar(None, "0"), StringVar(None, "0"), StringVar(None, "-"))
        self.v.gpio_sel_default = (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar())
        self.v.type_sel = (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar())
        self.v.amnt_sel = (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar())
        self.v.type_sel_default = (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar())
        self.v.amnt_sel_default = (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar())
        self.v.tcn_new = StringVar(None, "0")
        self.v.cdc_new = StringVar(None, "0")
        self.v.gpio_cell = [(StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()), (StringVar(), StringVar(), StringVar(), StringVar()),
                            (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()), (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()),
                            (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()), (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()),
                            (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()), (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()),
                            (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar())]
        self.v.prev_sel = (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar())

        self.d.clk_num = {0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 12:10, 13:11, 15:12, 16:13, 17:14, 18:15, 19:16, 20:17, 21:18, 24:19, 25:20, 26:21, 27:22, 28:23, 29:24, 32:25, 33:26}
        self.d.tcn_num = {0:0, 1:1, 2:2, 3:3, 8:4, 9:5, 10:6, 11:7, 12:8, 13:9, 14:10}
        self.d.cdc_num = {0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 8:6, 9:7, 10:8, 11:9, 12:10, 13:11, 14:12, 15:13}
        self.d.inv_clk = {y:x for x, y in self.d.clk_num.items()}

        self.l.gpio_grps = ("OFF", "Mithrill", "SAM", "eDP", "TCON", "CDC", "UPI", "PSR", "CORE")
        self.l.gpio_bits = ("0", "1", "2", "3", "4", "5", "6", "7")
        self.l.gpio_clks = ("OFF", "sam54", "ext54", "ck54", "ls0/4", "ls1/4", "ls2/4", "ls3/4", "link/4", "LTPS", "2px", "4px", "PSR", "upi0", "upi1", "upi2", "upi3", "upi4", "upi5", "upi0/4", "upi1/4", "upi2/4", "upi3/4", "upi4/4", "upi5/4", "sam_test", "mit_test")
        self.l.gpio_vals = ((0, 1, 2, 3, 4, 5, 6, 7), (0, 1, 2, 3), (0, 1, 2, 3, 4, 5, 6, 7), tuple(i for i in range(22)), (0, 1, 2, 3, 8, 9, 10, 11, 12, 13, 14), (0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15), (0, 1, 2, 3, 4, 5), (0, 1, 2, 3, 4, 5, 6, 7), ("-"))
        self.l.ext_types = ("Bypass", "Active-Low", "Active-High")
        self.l.ext_amnts = tuple(str(i) for i in range(16))

        self.l.gpio_reg_names = [("GPIO0_group_sel", "GPIO0_bit_sel"), ("GPIO1_group_sel", "GPIO1_bit_sel"), ("GPIO2_group_sel", "GPIO2_bit_sel"), ("GPIO3_group_sel", "GPIO3_bit_sel"), ("GPIO4_group_sel", "GPIO4_bit_sel"), ("GPIO5_group_sel", "GPIO5_bit_sel"), ("GPIO6_group_sel", "GPIO6_bit_sel"), ("GPIO7_group_sel", "GPIO7_bit_sel"), "GPIO8_clk_sel", "GPIO9_clk_sel"]
        self.l.gpio_ext_reg_names = [("GPIO0_extend_type", "GPIO0_extend_amount"), ("GPIO1_extend_type", "GPIO1_extend_amount"), ("GPIO2_extend_type", "GPIO2_extend_amount"), ("GPIO3_extend_type", "GPIO3_extend_amount"), ("GPIO4_extend_type", "GPIO4_extend_amount"), ("GPIO5_extend_type", "GPIO5_extend_amount"), ("GPIO6_extend_type", "GPIO6_extend_amount"), ("GPIO7_extend_type", "GPIO7_extend_amount")]
        self.l.gpio_grp_reg_names_w_width = ["mit_test_mode[2:0]", "test_ch[1:0]", "test_mode[2:0]", "cfg_rx_user_test[7:0]", "GPIO_TCON_sel[3:0]", "GPIO_CDC_sel[3:0]", "GPIO_CDC_sel[3:0]", "test_out_sel[2:0]", "N/A", "GPIO_group7_sel"]
        self.l.gpio_grp_reg_names_wo_width = ["mit_test_mode", "test_ch", "test_mode", "cfg_rx_user_test", "GPIO_TCON_sel", "GPIO_CDC_sel", "GPIO_CDC_sel", "test_out_sel", "N/A", "GPIO_group7_sel"]
        self.l.gpio_grp_widths = ["2:0", "1:0", "2:0", "7:0", "3:0", "3:0", "3:0", "2:0"]
        self.l.gpio_grp_bits = ["2:0", "1:0", "2:0", "7:0", "3:0", "3:0", "3:0", "2:0"]

        self.l.mit_choice = ["ccode_t_o[7:0]", "fcode_t_o[9:2]", "ccode_u_o[7:0]", "fcode_u_o[9:2]", "ccode_m_o[7:0]", "fcode_m_o[9:2]", "fd_idx[11:4]",
                           "phy_cal_done", "fd_idx_change", "0", "0", "ck25_t_o", "ck25_u_o", "ck25_m_o", "ck_ss_10_o"]

        self.l.sam_choice0 = ["ch#0", "ch#1", "ch#2", "ch#3"]
        self.l.sam_choice1 = ["ccode_phy[7:0]", "fcode_phy[9:2]", "eq_code_phy[3:0]", "ref_sw_phy[3:0]", "fd_idx_clk[11:4]", "ml_state_lnk[3:0]", "ct_state[3:0]", "os_ds[4:0]", "ft_state[2:0]", "mat_num[3:0]", "swg_large[3:0]",
                            "os_cal", "0", "0", "0", "fd1_phy[1:0]", "es_pol_int", "prbs_err_io"]

        self.l.eDP_choice = ["phy_lane_en_o[3:0]", "phy_link_bw_o[1:0]", "eq_en_o", "cr_en_o",
                           "phy_eq_done_i[3:0]", "phy_cr_done_i[3:0]", "link_eq_done[3:0]", "link_cr_done[3:0]",
                           "symbol_locked[3:0]", "go_to_stdby", "go_to_psr_stdby", "go_to_psr_sleep", "phy_ready",
                           "edid_sda", "edid_scl", "edid_sda_oen", "eeprom_loading", "go_to_phy_stdby", "go_to_phy_sleep", "go_to_sleep_o", "vid_power_down_o",
                           "mon_link_tr_done[3:0]", "kCFG_RX_PHY_EQUALIZATION_DONE[3:0]",
                           "kTRAINING_STATUS1_SYMBOL_LOCKED", "kTRAINING_STATUS1_CHANNEL_EQ_DONE", "kTRAINING_STATUS1_CR_DONE", "kTRAINING_STATUS1_TRAINING_LOST", "kTRAINING_STATUS0_SYMBOL_LOCKED", "kTRAINING_STATUS0_CHANNEL_EQ_DONE",
                           "kTRAINING_STATUS0_CR_DONE", "kTRAINING_STATUS0_TRAINING_LOST",
                           "kTRAINING_STATUS3_SYMBOL_LOCKED", "kTRAINING_STATUS3_CHANNEL_EQ_DONE", "kTRAINING_STATUS3_CR_DONE", "kTRAINING_STATUS3_TRAINING_LOST", "kTRAINING_STATUS2_SYMBOL_LOCKED", "kTRAINING_STATUS2_CHANNEL_EQ_DONE",
                           "kTRAINING_STATUS2_CR_DONE", "kTRAINING_STATUS2_TRAINING_LOST",
                           "vid_vblank", "vid_enable", "vid_hsync", "vid_vsync", "vid_display_on", "vid_msa", "mon_sr_done", "link_status",
                           "CFG_RX_USER_STATUS_FIFO_OVERFLOW", "BE_detected", "BS_detected", "mon_dec_err[3:0]", "mon_training_lost",
                           "init_cor_done", "black_video_enable", "hot_plug_detect", "top_assert_hpd", "load_fail", "init_load_done", "init_base_done", "eeprom_loading",
                           "local_vres[7:0]", "local_vres[15:8]", "local_vtotal[7:0]", "local_vtotal[15:8]", "local_hres[7:0]", "local_hres[15:8]", "local_htotal[7:0]", "local_htotal[15:8]",
                           "frame_capture OR psr_off_ack", "phy_wake_detected", "aux_wakeup", "i_power_down", "tx_off_timeout", "edp_mux_sel[2:0]",
                           "lt_cr_done", "lt_eq_done", "lt_symbol_locked", "w_phy_ready", "self_ana_train", "self_dig_train", "align_start", "link_recovered",
                           "w_cr_done[3:0]", "w_symbol_locked[3:0]"]

        self.l.tcn_choice = ["0", "0", "0", "0", "0", "de_i", "hsync_i", "vsync_i",
                           "seed_de", "mDNIe_de", "sp_de", "acl_bgc_de", "sp_de", "cor1_de", "cor2_de", "cor3_de",
                           "seed_hsync", "mDNIe_hsync", "sp_hsync", "acl_bgc_hsync", "sp_hsync", "cor1_hsync", "cor2_hsync", "cor3_hsync",
                           "seed_vsync", "mDNIe_vsync", "sp_vsync", "acl_bgc_vsync", "sp_vsync", "cor1_vsync", "cor2_vsync", "cor3_vsync",
                           "vsync_i", "elon2_start", "elon_dc_en", "elon_frame_start", "avdd_start", "avdd_dc_start", "MPS_REF", "vmux_change_flag",
                           "update_key", "GMA_MODE", "0", "0", "0", "0", "0", "0",
                           "SP_monitor[7:0]",
                           "CLK1", "CLK2", "EM_CLK1", "EM_CLK2", "ACL_FLM", "FLM", "FLM2", "EM_FLM",
                           "INT1", "INT2", "EM_CLK1", "EM_CLK2", "ACL_FLM", "FLM", "CLK1", "CLK2",
                           "EM_INT1", "EM_INT2", "EM_CLK1", "EM_CLK2", "ACL_FLM", "FLM", "FLM2", "CLK1",
                           "EM_INT1", "EM_CLK1", "CLK1", "INT1", "ACL_FLM", "FLM", "FLM2", "ltps_hsync"]

        self.l.cdc_choice = ["upi0_mon[1]", "upi0_lchop_evod", "upi0_mon[2]", "upi0_valid", "upi0_mon[0]", "upi0_de_flag", "upi0_hsync", "upi0_vsync",
                           "upi0_mon[1]", "upi1_lchop_evod", "upi0_mon[2]", "upi1_valid", "upi0_mon[0]", "upi1_de_flag", "upi1_hsync", "upi1_vsync",
                           "upi0_mon[1]", "upi2_lchop_evod", "upi0_mon[2]", "upi2_valid", "upi0_mon[0]", "upi2_de_flag", "upi2_hsync", "upi2_vsync",
                           "upi0_mon[1]", "upi3_lchop_evod", "upi0_mon[2]", "upi3_valid", "upi0_mon[0]", "upi3_de_flag", "upi3_hsync", "upi3_vsync",
                           "upi0_mon[1]", "upi4_lchop_evod", "upi0_mon[2]", "upi4_valid", "upi0_mon[0]", "upi4_de_flag", "upi4_hsync", "upi4_vsync",
                           "upi0_mon[1]", "upi5_lchop_evod", "upi0_mon[2]", "upi5_valid", "upi0_mon[0]", "upi5_de_flag", "upi5_hsync", "upi5_vsync",
                           "0", "0", "upi1_hsync", "upi1_vsync", "0", "0", "upi0_hsync", "upi0_vsync",
                           "0", "0", "upi3_hsync", "upi3_vsync", "0", "0", "upi2_hsync", "upi2_vsync",
                           "0", "0", "upi5_hsync", "upi5_vsync", "0", "0", "upi4_hsync", "upi4_vsync",
                           "upi4_lchop_evod", "upi4_de_flag", "upi4_hsync", "upi4_vsync", "line_chop_evod", "de_i", "hsync_i", "vsync_i",
                           "upi3_lchop_evod", "upi3_de_flag", "upi3_hsync", "upi3_vsync", "line_chop_evod", "de_i", "hsync_i", "vsync_i",
                           "upi2_lchop_evod", "upi2_de_flag", "upi2_hsync", "upi2_vsync", "line_chop_evod", "de_i", "hsync_i", "vsync_i",
                           "0", "0", "upi5_de_flag", "upi4_de_flag", "upi3_de_flag", "upi2_de_flag", "upi1_de_flag", "upi0_de_flag",
                           "0", "0", "upi5_vsync", "upi4_vsync", "upi3_vsync", "upi2_vsync", "upi1_vsync", "upi0_vsync"]

        self.l.upi_choice = ["upi0_de_scr", "upi0_VBLANK", "upi0_FPRO", "upi0_FSYNC", "upi0_upi_ck_train", "upi0_UPI_ren", "upi0_read_start", "upi0_de_tgdp",
                           "upi1_de_scr", "upi1_VBLANK", "upi1_FPRO", "upi1_FSYNC", "upi1_upi_ck_train", "upi1_UPI_ren", "upi1_read_start", "upi1_de_tgdp",
                           "upi2_de_scr", "upi2_VBLANK", "upi2_FPRO", "upi2_FSYNC", "upi2_upi_ck_train", "upi2_UPI_ren", "upi2_read_start", "upi2_de_tgdp",
                           "upi3_de_scr", "upi3_VBLANK", "upi3_FPRO", "upi3_FSYNC", "upi3_upi_ck_train", "upi3_UPI_ren", "upi3_read_start", "upi3_de_tgdp",
                           "upi4_de_scr", "upi4_VBLANK", "upi4_FPRO", "upi4_FSYNC", "upi4_upi_ck_train", "upi4_UPI_ren", "upi4_read_start", "upi4_de_tgdp",
                           "upi5_de_scr", "upi5_VBLANK", "upi5_FPRO", "upi5_FSYNC", "upi5_upi_ck_train", "upi5_UPI_ren", "upi5_read_start", "upi5_de_tgdp"]

        self.l.psr_choice = ["recon_px_valid_h0_o", "psr_pre_load_i_h0", "decoder_de_i_h0", "decoder_en_i_h0", "encoder_en_i", "dsc_mode_i", "psr_mode_i", "pps_valid",
                           "dsc_vsync_o", "dsc_hsync_o", "dsc_vsync_i", "dsc_hsync_i", "local_vsync_i", "local_hsync_i", "vid_vsync_i", "vid_hsync_i",
                           "recon_px_valid_h1_o", "recon_px_valid_h0_o", "b128_word_valid_vsc_i_1bit", "dsc_mode_i", "su_de_valid_i", "su_mode_i", "vid_vsync_i", "vid_hsync_i",
                           "recon_px_valid_h1_o", "recon_px_valid_h0_o", "psr_pre_load_i_h1", "psr_pre_load_i_h0", "decoder_de_i_h1", "decoder_de_i_h0", "decoder_en_i_h1", "decoder_en_i_h0",
                           "su_mode_i_psr_d", "dec_b128_word_valid_h0_pre3", "edram_req_b128_word_h0", "dec_sync_rstb_psr", "enc_b128_zpad_valid_h0", "enc_b128_word_valid_h0", "enc_b128_word_valid_pre_h0", "enc_sync_rstb_psr",
                           "dec_b128_word_valid_h1_pre3", "dec_b128_word_valid_h0_pre3", "edram_req_b128_wrod_h1", "edram_req_b128_wrod_h0", "enc_b128_word_valid_h1", "enc_b128_word_valid_h0", "enc_b128_word_valid_pre_h1", "enc_b128_word_valid_pre_h0",
                           "dec0_sync_rst", "enc0_b128_word_sending_done", "enc0_slice_proc_done", "enc0_slice_sending_done", "psr_pre_load_i_h0", "decoder_de_i_h0", "decoder_en_i_h0", "encoder_en_i",
                           "dec1_sync_rst", "enc1_b128_word_sending_done", "enc1_slice_proc_done", "enc1_slice_sending_done", "dec0_sync_rst", "enc0_b128_word_sending_done", "enc0_slice_proc_done", "enc0_slice_sending_done"]

        self.l.cor_choice = ["PNL_ON", "EL_ON", "ELS_ON", "GLS_ON", "TCON_RDY", "TCON_INT", "LS_EN", "EL_ON2"]

        self.l.mit0 = ["ccode_t_o[0]", "ccode_t_o[1]", "ccode_t_o[2]", "ccode_t_o[3]", "ccode_t_o[4]", "ccode_t_o[5]", "ccode_t_o[6]", "ccode_t_o[7]"]
        self.l.mit1 = ["fcode_t_o[2]", "fcode_t_o[3]", "fcode_t_o[4]", "fcode_t_o[5]", "fcode_t_o[6]", "fcode_t_o[7]", "fcode_t_o[8]", "fcode_t_o[9]"]
        self.l.mit2 = ["ccode_u_o[0]", "ccode_u_o[1]", "ccode_u_o[2]", "ccode_u_o[3]", "ccode_u_o[4]", "ccode_u_o[5]", "ccode_u_o[6]", "ccode_u_o[7]"]
        self.l.mit3 = ["fcode_u_o[2]", "fcode_u_o[3]", "fcode_u_o[4]", "fcode_u_o[5]", "fcode_u_o[6]", "fcode_u_o[7]", "fcode_u_o[8]", "fcode_u_o[9]"]
        self.l.mit4 = ["ccode_m_o[0]", "ccode_m_o[1]", "ccode_m_o[2]", "ccode_m_o[3]", "ccode_m_o[4]", "ccode_m_o[5]", "ccode_m_o[6]", "ccode_m_o[7]"]
        self.l.mit5 = ["fcode_m_o[2]", "fcode_m_o[3]", "fcode_m_o[4]", "fcode_m_o[5]", "fcode_m_o[6]", "fcode_m_o[7]", "fcode_m_o[8]", "fcode_m_o[9]"]
        self.l.mit6 = ["fd_idx[4]", "fd_idx[5]", "fd_idx[6]", "fd_idx[7]", "fd_idx[8]", "fd_idx[9]", "fd_idx[10]", "fd_idx[11]"]
        self.l.mit7 = ["ck_ss_10_o", "ck25_m_o", "ck25_u_o", "ck25_t_o", "0", "0", "fd_idx_change", "phy_cal_done"]

        self.l.sam0 = ["ccode_phy[0]", "ccode_phy[1]", "ccode_phy[2]", "ccode_phy[3]", "ccode_phy[4]", "ccode_phy[5]", "ccode_phy[6]", "ccode_phy[7]"]
        self.l.sam1 = ["fcode_phy[2]", "fcode_phy[3]", "fcode_phy[4]", "fcode_phy[5]", "fcode_phy[6]", "fcode_phy[7]", "fcode_phy[8]", "fcode_phy[9]"]
        self.l.sam2 = ["ref_sw_phy[0]", "ref_sw_phy[1]", "ref_sw_phy[2]", "ref_sw_phy[3]", "eq_code_phy[0]", "eq_code_phy[1]", "eq_code_phy[2]", "eq_code_phy[3]"]
        self.l.sam3 = ["fd_idx_clk[4]", "fd_idx_clk[5]", "fd_idx_clk[6]", "fd_idx_clk[7]", "fd_idx_clk[8]", "fd_idx_clk[9]", "fd_idx_clk[10]", "fd_idx_clk[11]"]
        self.l.sam4 = ["ct_state[0]", "ct_state[1]", "ct_state[2]", "ct_state[3]", "ml_state_lnk[0]", "ml_state_lnk[1]", "ml_state_lnk[2]", "ml_state_lnk[3]"]
        self.l.sam5 = ["ft_state[0]", "ft_state[1]", "ft_state[2]", "os_ds[0]", "os_ds[1]", "os_ds[2]", "os_ds[3]", "os_ds[4]"]
        self.l.sam6 = ["swg_large[0]", "swg_large[1]", "swg_large[2]", "swg_large[3]", "mat_num[0]", "mat_num[1]", "mat_num[2]", "mat_num[3]"]
        self.l.sam7 = ["prbs_err_io", "es_pol_int", "fd1_phy[0]", "fd1_phy[1]", "0", "0", "0", "os_cal"]

        self.l.eDP0 = ["cr_en_o", "eq_en_o", "phy_link_bw_o[0]", "phy_link_bw_o[1]", "phy_lane_en_o[0]", "phy_lane_en_o[1]", "phy_lane_en_o[2]", "phy_lane_en_o[3]"]
        self.l.eDP1 = ["phy_cr_done_i[0]", "phy_cr_done_i[1]", "phy_cr_done_i[2]", "phy_cr_done_i[3]", "phy_eq_done_i[0]", "phy_eq_done_i[1]", "phy_eq_done_i[2]", "phy_eq_done_i[3]"]
        self.l.eDP2 = ["link_cr_done[0]", "link_cr_done[1]", "link_cr_done[2]", "link_cr_done[3]", "link_eq_done[0]", "link_eq_done[1]", "link_eq_done[2]", "link_eq_done[3]"]
        self.l.eDP3 = ["phy_ready", "go_to_psr_sleep", "go_to_psr_stdby", "go_to_stdby", "symbol_locked[0]", "symbol_locked[1]", "symbol_locked[2]", "symbol_locked[3]"]
        self.l.eDP4 = ["vid_power_down_o", "go_to_sleep_o", "go_to_phy_sleep", "go_to_phy_stdby", "eeprom_loading", "edid_sda_oen", "edid_scl", "edid_sda"]
        self.l.eDP5 = ["kCFG_RX_PHY_EQUALIZATION_DONE[0]", "kCFG_RX_PHY_EQUALIZATION_DONE[1]", "kCFG_RX_PHY_EQUALIZATION_DONE[2]", "kCFG_RX_PHY_EQUALIZATION_DONE[3]", "mon_link_tr_done[0]", "mon_link_tr_done[1]", "mon_link_tr_done[2]", "mon_link_tr_done[3]"]
        self.l.eDP6 = ["kTRAINING_STATUS0_TRAINING_LOST", "kTRAINING_STATUS0_CR_DONE", "kTRAINING_STATUS0_CHANNEL_EQ_DONE", "kTRAINING_STATUS0_SYMBOL_LOCKED", "kTRAINING_STATUS1_TRAINING_LOST", "kTRAINING_STATUS1_CR_DONE",
                     "kTRAINING_STATUS1_CHANNEL_EQ_DONE", "kTRAINING_STATUS1_SYMBOL_LOCKED"]
        self.l.eDP7 = ["kTRAINING_STATUS2_TRAINING_LOST", "kTRAINING_STATUS2_CR_DONE", "kTRAINING_STATUS2_CHANNEL_EQ_DONE", "kTRAINING_STATUS2_SYMBOL_LOCKED", "kTRAINING_STATUS3_TRAINING_LOST", "kTRAINING_STATUS3_CR_DONE",
                     "kTRAINING_STATUS3_CHANNEL_EQ_DONE", "kTRAINING_STATUS3_SYMBOL_LOCKED"]
        self.l.eDP8 = ["link_status", "mon_sr_done", "vid_msa", "vid_display_on", "vid_vsync", "vid_hsync", "vid_enable", "vid_vblank"]
        self.l.eDP9 = ["mon_training_lost", "mon_dec_err[0]", "mon_dec_err[1]", "mon_dec_err[2]", "mon_dec_err[3]", "BS_detected", "BE_detected", "CFG_RX_USER_STATUS_FIFO_OVERFLOW"]
        self.l.eDP10 = ["eeprom_loading", "init_base_done", "init_load_done", "load_fail", "top_assert_hpd", "hot_plug_detect", "black_video_enable", "init_cor_done"]
        self.l.eDP11 = ["local_vres[0]", "local_vres[1]", "local_vres[2]", "local_vres[3]", "local_vres[4]", "local_vres[5]", "local_vres[6]", "local_vres[7]"]
        self.l.eDP12 = ["local_vres[8]", "local_vres[9]", "local_vres[10]", "local_vres[11]", "local_vres[12]", "local_vres[13]", "local_vres[14]", "local_vres[15]"]
        self.l.eDP13 = ["local_vtotal[0]", "local_vtotal[1]", "local_vtotal[2]", "local_vtotal[3]", "local_vtotal[4]", "local_vtotal[5]", "local_vtotal[6]", "local_vtotal[7]"]
        self.l.eDP14 = ["local_vtotal[8]", "local_vtotal[9]", "local_vtotal[10]", "local_vtotal[11]", "local_vtotal[12]", "local_vtotal[13]", "local_vtotal[14]", "local_vtotal[15]"]
        self.l.eDP15 = ["local_hres[0]", "local_hres[1]", "local_hres[2]", "local_hres[3]", "local_hres[4]", "local_hres[5]", "local_hres[6]", "local_hres[7]"]
        self.l.eDP16 = ["local_hres[8]", "local_hres[9]", "local_hres[10]", "local_hres[11]", "local_hres[12]", "local_hres[13]", "local_hres[14]", "local_hres[15]"]
        self.l.eDP17 = ["local_htotal[0]", "local_htotal[1]", "local_htotal[2]", "local_htotal[3]", "local_htotal[4]", "local_htotal[5]", "local_htotal[6]", "local_htotal[7]"]
        self.l.eDP18 = ["local_htotal[8]", "local_htotal[9]", "local_htotal[10]", "local_htotal[11]", "local_htotal[12]", "local_htotal[13]", "local_htotal[14]", "local_htotal[15]"]
        self.l.eDP19 = ["edp_mux_sel[0]", "edp_mux_sel[1]", "edp_mux_sel[2]", "tx_off_timeout", "i_power_down", "aux_wakeup", "phy_wake_detected", "frame_capture OR psr_off_ack"]
        self.l.eDP20 = ["link_recovered", "align_start", "self_dig_train", "self_ana_train", "w_phy_ready", "lt_symbol_locked", "lt_eq_done", "lt_cr_done"]
        self.l.eDP21 = ["w_symbol_locked[0]", "w_symbol_locked[1]", "w_symbol_locked[2]", "w_symbol_locked[3]", "w_cr_done[0]", "w_cr_done[1]", "w_cr_done[2]", "w_cr_done[3]"]

        self.l.tcn0 = ["vsync_i", "hsync_i", "de_i", "0", "0", "0", "0", "0"]
        self.l.tcn1 = ["cor3_de", "cor2_de", "cor1_de", "sp_de", "acl_bgc_de", "sp_de", "mDNIe_de", "seed_de"]
        self.l.tcn2 = ["cor3_hsync", "cor2_hsync", "cor1_hsync", "sp_hsync", "acl_bgc_hsync", "sp_hsync", "mDNIe_hsync", "seed_hsync"]
        self.l.tcn3 = ["cor3_vsync", "cor2_vsync", "cor1_vsync", "sp_vsync", "acl_bgc_vsync", "sp_vsync", "mDNIe_vsync", "seed_vsync"]
        self.l.tcn8 = ["vmux_change_flag", "MPS_REF", "avdd_dc_start", "avdd_start", "elon_frame_start", "elon_dc_en", "elon2_start", "vsync_i"]
        self.l.tcn9 = ["0", "0", "0", "0", "0", "0", "GMA_MODE", "update_key"]
        self.l.tcn10 = ["SP_monitor[0]", "SP_monitor[1]", "SP_monitor[2]", "SP_monitor[3]", "SP_monitor[4]", "SP_monitor[5]", "SP_monitor[6]", "SP_monitor[7]"]
        self.l.tcn11 = ["EM_FLM", "FLM2", "FLM", "ACL_FLM", "EM_CLK2", "EM_CLK1", "CLK2", "CLK1"]
        self.l.tcn12 = ["CLK2", "CLK1", "FLM", "ACL_FLM", "EM_CLK2", "EM_CLK1", "INT2", "INT1"]
        self.l.tcn13 = ["CLK1", "FLM2", "FLM", "ACL_FLM", "EM_CLK2", "EM_CLK1", "EM_INT2", "EM_INT1"]
        self.l.tcn14 = ["ltps_hsync", "FLM2", "FLM", "ACL_FLM", "INT1", "CLK1", "EM_CLK1", "EM_INT1"]

        self.l.cdc0 = ["upi0_vsync", "upi0_hsync", "upi0_de_flag", "upi0_mon[0]", "upi0_valid", "upi0_mon[2]", "upi0_lchop_evod", "upi0_mon[1]"]
        self.l.cdc1 = ["upi1_vsync", "upi1_hsync", "upi1_de_flag", "upi0_mon[0]", "upi1_valid", "upi0_mon[2]", "upi1_lchop_evod", "upi0_mon[1]"]
        self.l.cdc2 = ["upi2_vsync", "upi2_hsync", "upi2_de_flag", "upi0_mon[0]", "upi2_valid", "upi0_mon[2]", "upi2_lchop_evod", "upi0_mon[1]"]
        self.l.cdc3 = ["upi3_vsync", "upi3_hsync", "upi3_de_flag", "upi0_mon[0]", "upi3_valid", "upi0_mon[2]", "upi3_lchop_evod", "upi0_mon[1]"]
        self.l.cdc4 = ["upi4_vsync", "upi4_hsync", "upi4_de_flag", "upi0_mon[0]", "upi4_valid", "upi0_mon[2]", "upi4_lchop_evod", "upi0_mon[1]"]
        self.l.cdc5 = ["upi5_vsync", "upi5_hsync", "upi5_de_flag", "upi0_mon[0]", "upi5_valid", "upi0_mon[2]", "upi5_lchop_evod", "upi0_mon[1]"]
        self.l.cdc8 = ["upi0_vsync", "upi0_hsync", "0", "0", "upi1_vsync", "upi1_hsync", "0", "0"]
        self.l.cdc9 = ["upi2_vsync", "upi2_hsync", "0", "0", "upi3_vsync", "upi3_hsync", "0", "0"]
        self.l.cdc10 = ["upi4_vsync", "upi4_hsync", "0", "0", "upi5_vsync", "upi5_hsync", "0", "0"]
        self.l.cdc11 = ["vsync_i", "hsync_i", "de_i", "line_chop_evod", "upi4_vsync", "upi4_hsync", "upi4_de_flag", "upi4_lchop_evod"]
        self.l.cdc12 = ["vsync_i", "hsync_i", "de_i", "line_chop_evod", "upi3_vsync", "upi3_hsync", "upi3_de_flag", "upi3_lchop_evod"]
        self.l.cdc13 = ["vsync_i", "hsync_i", "de_i", "line_chop_evod", "upi2_vsync", "upi2_hsync", "upi2_de_flag", "upi2_lchop_evod"]
        self.l.cdc14 = ["upi0_de_flag", "upi1_de_flag", "upi2_de_flag", "upi3_de_flag", "upi4_de_flag", "upi5_de_flag", "0", "0"]
        self.l.cdc15 = ["upi0_vsync", "upi1_vsync", "upi2_vsync", "upi3_vsync", "upi4_vsync", "upi5_vsync", "0", "0"]

        self.l.upi0 = ["upi0_de_tgdp", "upi0_read_start", "upi0_UPI_ren", "upi0_upi_ck_train", "upi0_FSYNC", "upi0_FPRO", "upi0_VBLANK", "upi0_de_scr"]
        self.l.upi1 = ["upi1_de_tgdp", "upi1_read_start", "upi1_UPI_ren", "upi1_upi_ck_train", "upi1_FSYNC", "upi1_FPRO", "upi1_VBLANK", "upi1_de_scr"]
        self.l.upi2 = ["upi2_de_tgdp", "upi2_read_start", "upi2_UPI_ren", "upi2_upi_ck_train", "upi2_FSYNC", "upi2_FPRO", "upi2_VBLANK", "upi2_de_scr"]
        self.l.upi3 = ["upi3_de_tgdp", "upi3_read_start", "upi3_UPI_ren", "upi3_upi_ck_train", "upi3_FSYNC", "upi3_FPRO", "upi3_VBLANK", "upi3_de_scr"]
        self.l.upi4 = ["upi4_de_tgdp", "upi4_read_start", "upi4_UPI_ren", "upi4_upi_ck_train", "upi4_FSYNC", "upi4_FPRO", "upi4_VBLANK", "upi4_de_scr"]
        self.l.upi5 = ["upi5_de_tgdp", "upi5_read_start", "upi5_UPI_ren", "upi5_upi_ck_train", "upi5_FSYNC", "upi5_FPRO", "upi5_VBLANK", "upi5_de_scr"]

        self.l.psr0 = ["pps_valid", "psr_mode_i", "dsc_mode_i", "encoder_en_i", "decoder_en_i_h0", "decoder_de_i_h0", "psr_pre_load_i_h0", "recon_px_valid_h0_o"]
        self.l.psr1 = ["vid_hsync_i", "vid_vsync_i", "local_hsync_i", "local_vsync_i", "dsc_hsync_i", "dsc_vsync_i", "dsc_hsync_o", "dsc_vsync_o"]
        self.l.psr2 = ["vid_hsync_i", "vid_vsync_i", "su_mode_i", "su_de_valid_i", "dsc_mode_i", "b128_word_valid_vsc_i_1bit", "recon_px_valid_h0_o", "recon_px_valid_h1_o"]
        self.l.psr3 = ["decoder_en_i_h0", "decoder_en_i_h1", "decoder_de_i_h0", "decoder_de_i_h1", "psr_pre_load_i_h0", "psr_pre_load_i_h1", "recon_px_valid_h0_o", "recon_px_valid_h1_o"]
        self.l.psr4 = ["enc_sync_rstb_psr", "enc_b128_word_valid_pre_h0", "enc_b128_word_valid_h0", "enc_b128_zpad_valid_h0", "dec_sync_rstb_psr", "edram_req_b128_word_h0", "dec_b128_word_valid_h0_pre3", "su_mode_i_psr_d"]
        self.l.psr5 = ["enc_b128_word_valid_pre_h0", "enc_b128_word_valid_pre_h1", "enc_b128_word_valid_h0", "enc_b128_word_valid_h1", "edram_req_b128_wrod_h0", "edram_req_b128_wrod_h1", "dec_b128_word_valid_h0_pre3", "dec_b128_word_valid_h1_pre3"]
        self.l.psr6 = ["encoder_en_i", "decoder_en_i_h0", "decoder_de_i_h0", "psr_pre_load_i_h0", "enc0_slice_sending_done", "enc0_slice_proc_done", "enc0_b128_word_sending_done", "dec0_sync_rst"]
        self.l.psr7 = ["enc0_slice_sending_done", "enc0_slice_proc_done", "enc0_b128_word_sending_done", "dec0_sync_rst", "enc1_slice_sending_done", "enc1_slice_proc_done", "enc1_b128_word_sending_done", "dec1_sync_rst"]

        self.l.cor0 = ["EL_ON2", "LS_EN", "TCON_INT", "TCON_RDY", "GLS_ON", "ELS_ON", "EL_ON", "PNL_ON"]

        self.l.mit_row = [self.l.mit0, self.l.mit1, self.l.mit2, self.l.mit3, self.l.mit4, self.l.mit5, self.l.mit6, self.l.mit7]
        self.l.sam_row = [self.l.sam0, self.l.sam1, self.l.sam2, self.l.sam3, self.l.sam4, self.l.sam5, self.l.sam6, self.l.sam7]
        self.l.eDP_row = [self.l.eDP0, self.l.eDP1, self.l.eDP2, self.l.eDP3, self.l.eDP4, self.l.eDP5, self.l.eDP6, self.l.eDP7, self.l.eDP8, self.l.eDP9, self.l.eDP10, self.l.eDP11, self.l.eDP12, self.l.eDP13, self.l.eDP14, self.l.eDP15, self.l.eDP16, self.l.eDP17, self.l.eDP18, self.l.eDP19, self.l.eDP20, self.l.eDP21]
        self.l.tcn_row = [self.l.tcn0, self.l.tcn1, self.l.tcn2, self.l.tcn3, self.l.tcn8, self.l.tcn9, self.l.tcn10, self.l.tcn11, self.l.tcn12, self.l.tcn13, self.l.tcn14]
        self.l.cdc_row = [self.l.cdc0, self.l.cdc1, self.l.cdc2, self.l.cdc3, self.l.cdc4, self.l.cdc5, self.l.cdc8, self.l.cdc9, self.l.cdc10, self.l.cdc11, self.l.cdc12, self.l.cdc13, self.l.cdc14, self.l.cdc15]
        self.l.upi_row = [self.l.upi0, self.l.upi1, self.l.upi2, self.l.upi3, self.l.upi4, self.l.upi5]
        self.l.psr_row = [self.l.psr0, self.l.psr1, self.l.psr2, self.l.psr3, self.l.psr4, self.l.psr5, self.l.psr6, self.l.psr7]
        self.l.cor_row = [self.l.cor0]

        self.l.name_list = [self.l.mit_row, self.l.sam_row, self.l.eDP_row, self.l.tcn_row, self.l.cdc_row, self.l.upi_row, self.l.psr_row, self.l.cor_row]

        # Power Tab
        self.v.psm_var = ((StringVar(), StringVar(), StringVar()), (StringVar(), StringVar(), StringVar()), (StringVar(), StringVar(), StringVar()), (StringVar(), StringVar(), StringVar()), (StringVar(), StringVar(), StringVar()), StringVar())
        self.v.pss_var = (StringVar(), StringVar(), StringVar(), StringVar(), StringVar())


class FlashTabData:
    def __init__(self):
        self.v = self
        self.l = self
        
        self.v.flash_addr = StringVar()
        self.v.w_24 = StringVar()
        self.v.r_24 = StringVar()
        self.v.flash_from = StringVar()
        self.v.flash_to = StringVar()


class SplitRegData:
    def __init__(self):
        self.v = self
        self.l = self
        
        self.l.pages = []
        self.l.pages_unique = []
        self.l.groups = []
        self.l.groups_unique = []
        self.l.names_w_width = []
        self.l.names_wo_width = []
        self.l.widths = []
        self.l.addr_raw = []
        self.l.addr_num = []
        self.l.addr_bit = []
        self.l.addr_total = []
        self.l.defaults = []
        self.l.desc = []
        self.l.desc_icon = []
        self.l.merge_check = []
        self.l.ronly_check = []
        self.l.r_icon = []
        self.l.bina = []
        self.l.bina_mod = []
        self.l.bina_default = []
        self.l.deci = []
        self.l.deci_mod = []
        self.l.deci_default = []
        self.l.hexa = []
        self.l.hexa_mod = []
        self.l.hexa_default = []


class MergedRegData:
    def __init__(self):
        self.v = self
        self.l = self
        
        self.l.names = []
        self.l.widths = []
        self.l.addr = []
        self.l.bina = []
        self.l.bina_mod = []
        self.l.bina_default = []
        self.l.deci = []
        self.l.deci_mod = []
        self.l.deci_default = []
        self.l.hexa = []
        self.l.hexa_mod = []
        self.l.hexa_default = []
        self.l.desc = []
        self.l.desc_icon = []


class AddressRegData:
    def __init__(self):
        self.v = self
        self.l = self
        
        self.l.pg_and_num = []         # ["pg-num", "pg-num", ...]
        self.l.num_per_pg = []         # [[nums in pg 64], [nums in pg 65], [nums in pg 66], ...]
        self.l.num_range = []          # [num~num, num~num, ...]
        self.l.bina = []
        self.l.bina_mod = []
        self.l.bina_default = []
        self.l.hexa = []
        self.l.hexa_mod = []
        self.l.hexa_default = []
        self.l.hexa_per_pg = []        # [[hexa in pg 64], [hexa in pg 65], [hexa in pg 66], ...]
        self.l.hexa_per_pg_mod = []
        self.l.hexa_per_pg_default = []
        self.l.desc = []
        self.l.desc_icon = []