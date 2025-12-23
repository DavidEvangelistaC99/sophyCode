#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: tx_file
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from modFreq import chirpUsrp
import numpy as np
import sip



class tx_file(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "tx_file", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("tx_file")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "tx_file")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 20000000
        self.f_central = f_central = 0
        self.bw = bw = 4000000
        self.amp = amp = 1
        self.IPP = IPP = 0.0004
        self.DC = DC = 15
        self.numSamples = numSamples = len(chirpUsrp(amp,IPP,DC,samp_rate,f_central,bw))
        self.chirp_param = chirp_param = 'chirp_amp_' + str(amp) + '_ipp_' + str(IPP) + '_dc_' + str(DC) + '_sr_' + str(samp_rate) + '_fc_' + str(f_central) + '_bw_' + str(bw)
        self.numSamples_Chirp = numSamples_Chirp = 15*numSamples/100
        self.chirp_file = chirp_file = '/home/idi/anaconda3/envs/sophy3.10/code/bin/gnuradio/' + chirp_param + '.bin'

        ##################################################
        # Blocks
        ##################################################

        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("addr=192.168.20.7", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_subdev_spec("A:AB", 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(70312500, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_gain(0, 0)
        self.qtgui_time_sink_x_0_0_1 = qtgui.time_sink_c(
            numSamples, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_1.enable_tags(True)
        self.qtgui_time_sink_x_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_1.enable_grid(False)
        self.qtgui_time_sink_x_0_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_1_win)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, numSamples)
        self.blocks_vector_source_x_0 = blocks.vector_source_c(chirpUsrp(amp,IPP,DC,samp_rate,f_central,bw), False, numSamples, [])
        self.blocks_skiphead_1 = blocks.skiphead(gr.sizeof_gr_complex*1, 0)
        self.blocks_head_1 = blocks.head(gr.sizeof_gr_complex*1, numSamples)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, chirp_file, False)
        self.blocks_file_sink_1.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_head_1, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.blocks_head_1, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_skiphead_1, 0), (self.blocks_head_1, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_skiphead_1, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.qtgui_time_sink_x_0_0_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "tx_file")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_chirp_param('chirp_amp_' + str(self.amp) + '_ipp_' + str(self.IPP) + '_dc_' + str(self.DC) + '_sr_' + str(self.samp_rate) + '_fc_' + str(self.f_central) + '_bw_' + str(self.bw))
        self.set_numSamples(len(chirpUsrp(self.amp,self.IPP,self.DC,self.samp_rate,self.f_central,self.bw)))
        self.blocks_vector_source_x_0.set_data(chirpUsrp(self.amp,self.IPP,self.DC,self.samp_rate,self.f_central,self.bw), [])
        self.qtgui_time_sink_x_0_0_1.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_f_central(self):
        return self.f_central

    def set_f_central(self, f_central):
        self.f_central = f_central
        self.set_chirp_param('chirp_amp_' + str(self.amp) + '_ipp_' + str(self.IPP) + '_dc_' + str(self.DC) + '_sr_' + str(self.samp_rate) + '_fc_' + str(self.f_central) + '_bw_' + str(self.bw))
        self.set_numSamples(len(chirpUsrp(self.amp,self.IPP,self.DC,self.samp_rate,self.f_central,self.bw)))
        self.blocks_vector_source_x_0.set_data(chirpUsrp(self.amp,self.IPP,self.DC,self.samp_rate,self.f_central,self.bw), [])

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.set_chirp_param('chirp_amp_' + str(self.amp) + '_ipp_' + str(self.IPP) + '_dc_' + str(self.DC) + '_sr_' + str(self.samp_rate) + '_fc_' + str(self.f_central) + '_bw_' + str(self.bw))
        self.set_numSamples(len(chirpUsrp(self.amp,self.IPP,self.DC,self.samp_rate,self.f_central,self.bw)))
        self.blocks_vector_source_x_0.set_data(chirpUsrp(self.amp,self.IPP,self.DC,self.samp_rate,self.f_central,self.bw), [])

    def get_amp(self):
        return self.amp

    def set_amp(self, amp):
        self.amp = amp
        self.set_chirp_param('chirp_amp_' + str(self.amp) + '_ipp_' + str(self.IPP) + '_dc_' + str(self.DC) + '_sr_' + str(self.samp_rate) + '_fc_' + str(self.f_central) + '_bw_' + str(self.bw))
        self.set_numSamples(len(chirpUsrp(self.amp,self.IPP,self.DC,self.samp_rate,self.f_central,self.bw)))
        self.blocks_vector_source_x_0.set_data(chirpUsrp(self.amp,self.IPP,self.DC,self.samp_rate,self.f_central,self.bw), [])

    def get_IPP(self):
        return self.IPP

    def set_IPP(self, IPP):
        self.IPP = IPP
        self.set_chirp_param('chirp_amp_' + str(self.amp) + '_ipp_' + str(self.IPP) + '_dc_' + str(self.DC) + '_sr_' + str(self.samp_rate) + '_fc_' + str(self.f_central) + '_bw_' + str(self.bw))
        self.set_numSamples(len(chirpUsrp(self.amp,self.IPP,self.DC,self.samp_rate,self.f_central,self.bw)))
        self.blocks_vector_source_x_0.set_data(chirpUsrp(self.amp,self.IPP,self.DC,self.samp_rate,self.f_central,self.bw), [])

    def get_DC(self):
        return self.DC

    def set_DC(self, DC):
        self.DC = DC
        self.set_chirp_param('chirp_amp_' + str(self.amp) + '_ipp_' + str(self.IPP) + '_dc_' + str(self.DC) + '_sr_' + str(self.samp_rate) + '_fc_' + str(self.f_central) + '_bw_' + str(self.bw))
        self.set_numSamples(len(chirpUsrp(self.amp,self.IPP,self.DC,self.samp_rate,self.f_central,self.bw)))
        self.blocks_vector_source_x_0.set_data(chirpUsrp(self.amp,self.IPP,self.DC,self.samp_rate,self.f_central,self.bw), [])

    def get_numSamples(self):
        return self.numSamples

    def set_numSamples(self, numSamples):
        self.numSamples = numSamples
        self.set_numSamples_Chirp(15*self.numSamples/100)
        self.blocks_head_1.set_length(self.numSamples)

    def get_chirp_param(self):
        return self.chirp_param

    def set_chirp_param(self, chirp_param):
        self.chirp_param = chirp_param
        self.set_chirp_file('/home/idi/anaconda3/envs/sophy3.10/code/bin/gnuradio/' + self.chirp_param + '.bin')

    def get_numSamples_Chirp(self):
        return self.numSamples_Chirp

    def set_numSamples_Chirp(self, numSamples_Chirp):
        self.numSamples_Chirp = numSamples_Chirp

    def get_chirp_file(self):
        return self.chirp_file

    def set_chirp_file(self, chirp_file):
        self.chirp_file = chirp_file
        self.blocks_file_sink_1.open(self.chirp_file)




def main(top_block_cls=tx_file, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
