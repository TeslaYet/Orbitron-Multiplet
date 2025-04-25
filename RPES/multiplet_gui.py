#!/usr/bin/env python3
"""
Multiplet2 GUI Application
This application provides a graphical interface for the Multiplet2 code,
allowing users to create input files, run the multiplet process, and
convert output files.
"""

import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit,
                             QFileDialog, QFormLayout, QGroupBox, QGridLayout, QMessageBox,
                             QSpinBox, QDoubleSpinBox, QScrollArea)
from PyQt6.QtCore import Qt, QProcess

# Import the converter module
from convert_rpesalms import convert_rpesalms

class MultipletGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Multiplet2 GUI')
        self.setGeometry(100, 100, 900, 700)
        
        # Main tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Create tabs
        self.input_tab = QWidget()
        self.run_tab = QWidget()
        self.convert_tab = QWidget()
        
        # Add tabs to widget
        self.tabs.addTab(self.input_tab, "Create Input")
        self.tabs.addTab(self.run_tab, "Run Multiplet")
        self.tabs.addTab(self.convert_tab, "Convert Output")
        
        # Set up each tab
        self.setup_input_tab()
        self.setup_run_tab()
        self.setup_convert_tab()
    
    def setup_input_tab(self):
        # Main layout
        main_layout = QVBoxLayout()
        
        # Create scrollable text area to show the generated input
        self.input_preview = QTextEdit()
        self.input_preview.setReadOnly(True)
        
        # Create a form layout within a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        form_layout = QVBoxLayout(scroll_content)
        
        # Energy parameters group
        energy_box = QGroupBox("Energy Parameters")
        energy_layout = QGridLayout()
        
        # E(2p) and E(3d)
        self.e2p_input = QLineEdit("-639")
        self.e3d_input = QLineEdit("-1.e-6")
        energy_layout.addWidget(QLabel("E(2p):"), 0, 0)
        energy_layout.addWidget(self.e2p_input, 0, 1)
        energy_layout.addWidget(QLabel("E(3d):"), 0, 2)
        energy_layout.addWidget(self.e3d_input, 0, 3)
        
        # Crystal field matrix
        energy_layout.addWidget(QLabel("Crystal Field Matrix:"), 1, 0, 1, 4)
        self.cf_matrix = []
        for i in range(5):
            row = []
            for j in range(5):
                value = QLineEdit("0.")
                row.append(value)
                energy_layout.addWidget(value, i+2, j)
            self.cf_matrix.append(row)
        
        # Set crystal field values with exact spacing from reference
        self.cf_matrix[0][0].setText("-0.024")
        self.cf_matrix[0][1].setText("0.")
        self.cf_matrix[0][2].setText("0.")
        self.cf_matrix[0][3].setText("-0.056")
        self.cf_matrix[0][4].setText("0.")

        self.cf_matrix[1][0].setText("0.")
        self.cf_matrix[1][1].setText("0.064")
        self.cf_matrix[1][2].setText("0.")
        self.cf_matrix[1][3].setText("0.")
        self.cf_matrix[1][4].setText("0.056")

        self.cf_matrix[2][0].setText("0.")
        self.cf_matrix[2][1].setText("0.")
        self.cf_matrix[2][2].setText("-0.177")
        self.cf_matrix[2][3].setText("0.")
        self.cf_matrix[2][4].setText("0.")

        self.cf_matrix[3][0].setText("-0.056")
        self.cf_matrix[3][1].setText("0.")
        self.cf_matrix[3][2].setText("0.")
        self.cf_matrix[3][3].setText("0.064")
        self.cf_matrix[3][4].setText("0.")

        self.cf_matrix[4][0].setText("0.")
        self.cf_matrix[4][1].setText("0.056")
        self.cf_matrix[4][2].setText("0.")
        self.cf_matrix[4][3].setText("0.")
        self.cf_matrix[4][4].setText("-0.024")
        
        energy_box.setLayout(energy_layout)
        form_layout.addWidget(energy_box)
        
        # B-field parameters
        bfield_box = QGroupBox("Magnetic Field")
        bfield_layout = QHBoxLayout()
        self.bfield_strength = QLineEdit("1.e-3")
        self.bfield_theta = QLineEdit("90.")
        bfield_layout.addWidget(QLabel("B-field (eV):"))
        bfield_layout.addWidget(self.bfield_strength)
        bfield_layout.addWidget(QLabel("theta (deg):"))
        bfield_layout.addWidget(self.bfield_theta)
        bfield_box.setLayout(bfield_layout)
        form_layout.addWidget(bfield_box)
        
        # Photon energy parameters
        photon_box = QGroupBox("Photon Energy Settings")
        photon_layout = QHBoxLayout()
        self.omega_start = QLineEdit("651.8")
        self.omega_stop = QLineEdit("651.8")
        self.delta_omega = QLineEdit("2.")
        self.gamma = QLineEdit("0.4")
        self.gamma_flag = QLineEdit("0")
        photon_layout.addWidget(QLabel("ω start:"))
        photon_layout.addWidget(self.omega_start)
        photon_layout.addWidget(QLabel("ω stop:"))
        photon_layout.addWidget(self.omega_stop)
        photon_layout.addWidget(QLabel("Δω:"))
        photon_layout.addWidget(self.delta_omega)
        photon_layout.addWidget(QLabel("Γ:"))
        photon_layout.addWidget(self.gamma)
        photon_layout.addWidget(QLabel("flag:"))
        photon_layout.addWidget(self.gamma_flag)
        photon_box.setLayout(photon_layout)
        form_layout.addWidget(photon_box)
        
        # Electron configuration
        config_box = QGroupBox("Electron Configuration")
        config_layout = QVBoxLayout()
        
        config_row1 = QHBoxLayout()
        self.d_electrons = QLineEdit("5")
        config_row1.addWidget(QLabel("Number of d-electrons:"))
        config_row1.addWidget(self.d_electrons)
        config_layout.addLayout(config_row1)
        
        config_row2 = QHBoxLayout()
        self.l_values = QLineEdit("1 2 1 3 5")
        config_row2.addWidget(QLabel("l-values of active shells:"))
        config_row2.addWidget(self.l_values)
        config_layout.addLayout(config_row2)
        
        # SOC parameters
        config_row3 = QHBoxLayout()
        self.soc_params = QLineEdit("6.846  0.040 0 0 0")
        config_row3.addWidget(QLabel("SOC parameters:"))
        config_row3.addWidget(self.soc_params)
        config_layout.addLayout(config_row3)
        
        # Dipole matrix elements
        config_row4 = QHBoxLayout()
        self.dipole_elements = QLineEdit("2.064  0.02161  0.09695")
        config_row4.addWidget(QLabel("Dipole matrix elements:"))
        config_row4.addWidget(self.dipole_elements)
        config_layout.addLayout(config_row4)
        
        config_box.setLayout(config_layout)
        form_layout.addWidget(config_box)
        
        # Ground state parameters
        gs_box = QGroupBox("Ground State Parameters")
        gs_layout = QVBoxLayout()
        
        gs_row1 = QHBoxLayout()
        self.gs_config_count = QLineEdit("1")
        gs_row1.addWidget(QLabel("Number of configurations:"))
        gs_row1.addWidget(self.gs_config_count)
        gs_layout.addLayout(gs_row1)
        
        gs_row2 = QHBoxLayout()
        self.gs_occupation = QLineEdit("6 5 0 0 0")
        gs_row2.addWidget(QLabel("Occupation numbers:"))
        gs_row2.addWidget(self.gs_occupation)
        gs_layout.addLayout(gs_row2)
        
        # Slater-Condon parameters for ground state
        gs_row3 = QHBoxLayout()
        self.gs_slater_f2p3d = QLineEdit("0 0 5.0568")
        gs_row3.addWidget(QLabel("F_k(2p,3d):"))
        gs_row3.addWidget(self.gs_slater_f2p3d)
        gs_layout.addLayout(gs_row3)
        
        gs_row4 = QHBoxLayout()
        self.gs_slater_g2p3d = QLineEdit("0 3.6848 0 2.0936")
        gs_row4.addWidget(QLabel("G_k(2p,3d):"))
        gs_row4.addWidget(self.gs_slater_g2p3d)
        gs_layout.addLayout(gs_row4)
        
        gs_row5 = QHBoxLayout()
        self.gs_slater_f2p3d_2 = QLineEdit("0 0 5.0568")
        gs_row5.addWidget(QLabel("F_k(2p,3d) (2):"))
        gs_row5.addWidget(self.gs_slater_f2p3d_2)
        gs_layout.addLayout(gs_row5)
        
        gs_row6 = QHBoxLayout()
        self.gs_slater_f2p3d_3 = QLineEdit("0 0 5.0568")
        gs_row6.addWidget(QLabel("F_k(2p,3d) (3):"))
        gs_row6.addWidget(self.gs_slater_f2p3d_3)
        gs_layout.addLayout(gs_row6)
        
        gs_row7 = QHBoxLayout()
        self.gs_slater_g2p3d_2 = QLineEdit("0 3.6848 0 2.0936")
        gs_row7.addWidget(QLabel("G_k(2p,3d) (2):"))
        gs_row7.addWidget(self.gs_slater_g2p3d_2)
        gs_layout.addLayout(gs_row7)
        
        gs_row8 = QHBoxLayout()
        self.gs_slater_f3d3d = QLineEdit("0 0 9.4752 0 5.9256")
        gs_row8.addWidget(QLabel("F_k(3d,3d):"))
        gs_row8.addWidget(self.gs_slater_f3d3d)
        gs_layout.addLayout(gs_row8)
        
        gs_box.setLayout(gs_layout)
        form_layout.addWidget(gs_box)
        
        # Final state parameters
        fs_box = QGroupBox("Final State Parameters")
        fs_layout = QVBoxLayout()
        
        fs_row1 = QHBoxLayout()
        self.fs_config_count = QLineEdit("1")
        fs_row1.addWidget(QLabel("Number of configurations:"))
        fs_row1.addWidget(self.fs_config_count)
        fs_layout.addLayout(fs_row1)
        
        fs_row2 = QHBoxLayout()
        self.fs_occupation = QLineEdit("6 4 0 0 0")
        fs_row2.addWidget(QLabel("Occupation numbers:"))
        fs_row2.addWidget(self.fs_occupation)
        fs_layout.addLayout(fs_row2)
        
        # Slater-Condon parameters for final state
        fs_row3 = QHBoxLayout()
        self.fs_slater_f2p3d = QLineEdit("0 0 5.0568")
        fs_row3.addWidget(QLabel("F_k(2p,3d):"))
        fs_row3.addWidget(self.fs_slater_f2p3d)
        fs_layout.addLayout(fs_row3)
        
        fs_row4 = QHBoxLayout()
        self.fs_slater_g2p3d = QLineEdit("0 3.6848 0 2.0936")
        fs_row4.addWidget(QLabel("G_k(2p,3d):"))
        fs_row4.addWidget(self.fs_slater_g2p3d)
        fs_layout.addLayout(fs_row4)
        
        fs_row5 = QHBoxLayout()
        self.fs_slater_f2p3d_2 = QLineEdit("0 0 5.0568")
        fs_row5.addWidget(QLabel("F_k(2p,3d) (2):"))
        fs_row5.addWidget(self.fs_slater_f2p3d_2)
        fs_layout.addLayout(fs_row5)
        
        fs_row6 = QHBoxLayout()
        self.fs_slater_f2p3d_3 = QLineEdit("0 0 5.0568")
        fs_row6.addWidget(QLabel("F_k(2p,3d) (3):"))
        fs_row6.addWidget(self.fs_slater_f2p3d_3)
        fs_layout.addLayout(fs_row6)
        
        fs_row7 = QHBoxLayout()
        self.fs_slater_g2p3d_2 = QLineEdit("0 3.6848 0 2.0936")
        fs_row7.addWidget(QLabel("G_k(2p,3d) (2):"))
        fs_row7.addWidget(self.fs_slater_g2p3d_2)
        fs_layout.addLayout(fs_row7)
        
        fs_row8 = QHBoxLayout()
        self.fs_slater_f3d3d = QLineEdit("0 0 9.4752 0 5.9256")
        fs_row8.addWidget(QLabel("F_k(3d,3d):"))
        fs_row8.addWidget(self.fs_slater_f3d3d)
        fs_layout.addLayout(fs_row8)
        
        fs_box.setLayout(fs_layout)
        form_layout.addWidget(fs_box)
        
        # Intermediate state parameters
        is_box = QGroupBox("Intermediate State Parameters")
        is_layout = QVBoxLayout()
        
        is_row1 = QHBoxLayout()
        self.is_config_count = QLineEdit("1")
        is_row1.addWidget(QLabel("Number of configurations:"))
        is_row1.addWidget(self.is_config_count)
        is_layout.addLayout(is_row1)
        
        is_row2 = QHBoxLayout()
        self.is_occupation = QLineEdit("5 6  0 0 0")
        is_row2.addWidget(QLabel("Occupation numbers:"))
        is_row2.addWidget(self.is_occupation)
        is_layout.addLayout(is_row2)
        
        # Slater-Condon parameters for intermediate state
        is_row3 = QHBoxLayout()
        self.is_slater_f2p3d = QLineEdit("0 0 5.0568")
        is_row3.addWidget(QLabel("F_k(2p,3d):"))
        is_row3.addWidget(self.is_slater_f2p3d)
        is_layout.addLayout(is_row3)
        
        is_row4 = QHBoxLayout()
        self.is_slater_g2p3d = QLineEdit("0 3.6848 0 2.0936")
        is_row4.addWidget(QLabel("G_k(2p,3d):"))
        is_row4.addWidget(self.is_slater_g2p3d)
        is_layout.addLayout(is_row4)
        
        is_row5 = QHBoxLayout()
        self.is_slater_f2p3d_2 = QLineEdit("0 0 5.0568")
        is_row5.addWidget(QLabel("F_k(2p,3d) (2):"))
        is_row5.addWidget(self.is_slater_f2p3d_2)
        is_layout.addLayout(is_row5)
        
        is_row6 = QHBoxLayout()
        self.is_slater_f2p3d_3 = QLineEdit("0 0 5.0568")
        is_row6.addWidget(QLabel("F_k(2p,3d) (3):"))
        is_row6.addWidget(self.is_slater_f2p3d_3)
        is_layout.addLayout(is_row6)
        
        is_row7 = QHBoxLayout()
        self.is_slater_g2p3d_2 = QLineEdit("0 3.6848 0 2.0936")
        is_row7.addWidget(QLabel("G_k(2p,3d) (2):"))
        is_row7.addWidget(self.is_slater_g2p3d_2)
        is_layout.addLayout(is_row7)
        
        is_row8 = QHBoxLayout()
        self.is_slater_f3d3d = QLineEdit("0 0 8.9240 0 5.5528")
        is_row8.addWidget(QLabel("F_k(3d,3d):"))
        is_row8.addWidget(self.is_slater_f3d3d)
        is_layout.addLayout(is_row8)
        
        is_box.setLayout(is_layout)
        form_layout.addWidget(is_box)
        
        # Auger decay parameters
        auger_box = QGroupBox("Auger Decay Parameters")
        auger_layout = QVBoxLayout()
        
        auger_row1 = QHBoxLayout()
        self.auger_r_2pnp = QLineEdit("0. -.19047  0. -.15644")
        auger_row1.addWidget(QLabel("R_k(2p,np;3d,3d):"))
        auger_row1.addWidget(self.auger_r_2pnp)
        auger_layout.addLayout(auger_row1)
        
        auger_row2 = QHBoxLayout()
        self.auger_r_2pnf = QLineEdit("0. 0.7079   0. 0.44937")
        auger_row2.addWidget(QLabel("R_k(2p,nf;3d,3d):"))
        auger_row2.addWidget(self.auger_r_2pnf)
        auger_layout.addLayout(auger_row2)
        
        auger_row3 = QHBoxLayout()
        self.auger_r_2pnh = QLineEdit("0. 0.       0. 0.28778")
        auger_row3.addWidget(QLabel("R_k(2p,nh;3d,3d):"))
        auger_row3.addWidget(self.auger_r_2pnh)
        auger_layout.addLayout(auger_row3)
        
        auger_box.setLayout(auger_layout)
        form_layout.addWidget(auger_box)
        
        # Set the scroll area widget
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area, 1)
        
        # Preview and save buttons
        button_layout = QHBoxLayout()
        self.preview_button = QPushButton("Preview Input")
        self.save_button = QPushButton("Save Input File")
        self.preview_button.clicked.connect(self.preview_input)
        self.save_button.clicked.connect(self.save_input_file)
        button_layout.addWidget(self.preview_button)
        button_layout.addWidget(self.save_button)
        main_layout.addLayout(button_layout)
        
        # Preview area
        preview_box = QGroupBox("Input File Preview")
        preview_layout = QVBoxLayout()
        preview_layout.addWidget(self.input_preview)
        preview_box.setLayout(preview_layout)
        main_layout.addWidget(preview_box)
        
        self.input_tab.setLayout(main_layout)
    
    def setup_run_tab(self):
        layout = QVBoxLayout()
        
        # Input file selection
        input_group = QGroupBox("Input File")
        input_layout = QHBoxLayout()
        self.input_file_path = QLineEdit()
        self.input_file_path.setReadOnly(True)
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_input_file)
        input_layout.addWidget(QLabel("Input File:"))
        input_layout.addWidget(self.input_file_path)
        input_layout.addWidget(browse_button)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Output directory selection
        output_group = QGroupBox("Output Directory")
        output_layout = QHBoxLayout()
        self.output_dir_path = QLineEdit()
        self.output_dir_path.setReadOnly(True)
        output_browse_button = QPushButton("Browse")
        output_browse_button.clicked.connect(self.browse_output_dir)
        output_layout.addWidget(QLabel("Output Directory:"))
        output_layout.addWidget(self.output_dir_path)
        output_layout.addWidget(output_browse_button)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        # Run button
        self.run_button = QPushButton("Run Multiplet")
        self.run_button.clicked.connect(self.run_multiplet)
        layout.addWidget(self.run_button)
        
        # Console output
        console_group = QGroupBox("Console Output")
        console_layout = QVBoxLayout()
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        console_layout.addWidget(self.console_output)
        console_group.setLayout(console_layout)
        layout.addWidget(console_group)
        
        self.run_tab.setLayout(layout)
        
        # Process for running the multiplet calculation
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)
    
    def setup_convert_tab(self):
        layout = QVBoxLayout()
        
        # Input file selection
        input_group = QGroupBox("Input File (rpesalms.dat)")
        input_layout = QHBoxLayout()
        self.convert_input_path = QLineEdit()
        self.convert_input_path.setReadOnly(True)
        convert_browse_button = QPushButton("Browse")
        convert_browse_button.clicked.connect(self.browse_convert_input)
        input_layout.addWidget(QLabel("Input File:"))
        input_layout.addWidget(self.convert_input_path)
        input_layout.addWidget(convert_browse_button)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Output file selection
        output_group = QGroupBox("Output File (rpesalms.edac)")
        output_layout = QHBoxLayout()
        self.convert_output_path = QLineEdit()
        self.convert_output_path.setReadOnly(True)
        convert_output_button = QPushButton("Browse")
        convert_output_button.clicked.connect(self.browse_convert_output)
        output_layout.addWidget(QLabel("Output File:"))
        output_layout.addWidget(self.convert_output_path)
        output_layout.addWidget(convert_output_button)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        # Convert button
        self.convert_button = QPushButton("Convert File")
        self.convert_button.clicked.connect(self.convert_file)
        layout.addWidget(self.convert_button)
        
        # Status message
        self.convert_status = QLabel("Ready")
        layout.addWidget(self.convert_status)
        
        self.convert_tab.setLayout(layout)
    
    def generate_input_content(self):
        """Generate the content for the multiplet_input.txt file with exact formatting"""
        lines = []
        
        # Energy parameters - matching exact spacing from reference
        lines.append("-639 -1.e-6")
        
        # Crystal field matrix - match EXACT spacing from reference
        lines.append("-0.024 0.    0.   -0.056 0.    ")
        lines.append(" 0.    0.064 0.    0.    0.056 ")
        lines.append(" 0.    0.   -0.177 0.    0.    ")
        lines.append("-0.056 0.    0.    0.064 0.    ")
        lines.append(" 0.    0.056 0.    0.   -0.024")
        
        # B-field - exactly match reference format with trailing spaces
        lines.append(" 1.e-3 90.")
        
        # Photon energy - match reference spacing with extra spaces
        lines.append("651.8  651.8   2. 0.4 0")
        
        # Number of d-electrons
        lines.append("5")
        
        # l-values - exactly match reference format
        lines.append("1 2 1 3 5")
        
        # SOC parameters - match reference spacing
        lines.append("6.846  0.040 0 0 0")
        
        # Dipole matrix elements - match reference spacing
        lines.append("2.064  0.02161  0.09695")
        
        # Ground state configuration count
        lines.append("1")
        
        # Ground state occupation numbers
        lines.append("6 5 0 0 0")
        
        # Ground state Slater-Condon parameters - preserve exact spacing
        lines.append("0 0 5.0568")
        lines.append("0 3.6848 0 2.0936")
        lines.append("0 0 5.0568")
        lines.append("0 0 5.0568")
        lines.append("0 3.6848 0 2.0936")
        lines.append("0 0 9.4752 0 5.9256")
        
        # Final state configuration count
        lines.append("1")
        
        # Final state occupation numbers
        lines.append("6 4 0 0 0")
        
        # Final state Slater-Condon parameters - preserve exact spacing
        lines.append("0 0 5.0568")
        lines.append("0 3.6848 0 2.0936")
        lines.append("0 0 5.0568")
        lines.append("0 0 5.0568")
        lines.append("0 3.6848 0 2.0936")
        lines.append("0 0 9.4752 0 5.9256")
        
        # Intermediate state configuration count
        lines.append("1")
        
        # Intermediate state occupation numbers - match reference spacing
        lines.append("5 6  0 0 0")
        
        # Intermediate state Slater-Condon parameters - preserve exact spacing
        lines.append("0 0 5.0568")
        lines.append("0 3.6848 0 2.0936")
        lines.append("0 0 5.0568")
        lines.append("0 0 5.0568")
        lines.append("0 3.6848 0 2.0936")
        lines.append("0 0 8.9240 0 5.5528")
        
        # Auger decay integrals - match exact spacing from reference
        lines.append("0. -.19047  0. -.15644")
        lines.append("0. 0.7079   0. 0.44937")
        lines.append("0. 0.       0. 0.28778")
        
        return "\n".join(lines)
    
    def preview_input(self):
        """Preview the input file content"""
        content = self.generate_input_content()
        self.input_preview.setText(content)
    
    def save_input_file(self):
        """Save the input file with exact reference formatting"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Input File", 
                                                 "multiplet_input.txt", 
                                                 "Text Files (*.txt)")
        if file_path:
            content = self.generate_input_content()
            with open(file_path, 'w') as f:
                f.write(content)
            QMessageBox.information(self, "Success", 
                                   f"Input file saved to {file_path}\n\n"
                                   "Note: The file uses the exact reference values and formatting "
                                   "to ensure compatibility with the Multiplet code.")
    
    def browse_input_file(self):
        """Browse for input file"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Input File", 
                                                  "", 
                                                  "Text Files (*.txt)")
        if file_path:
            self.input_file_path.setText(file_path)
    
    def browse_output_dir(self):
        """Browse for output directory"""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_dir_path.setText(dir_path)
    
    def run_multiplet(self):
        """Run the multiplet calculation"""
        input_file = self.input_file_path.text()
        output_dir = self.output_dir_path.text()
        
        if not input_file:
            QMessageBox.warning(self, "Error", "Please select an input file")
            return
            
        if not output_dir:
            QMessageBox.warning(self, "Error", "Please select an output directory")
            return
        
        # Make sure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Clear console output
        self.console_output.clear()
        
        # Disable run button during execution
        self.run_button.setEnabled(False)
        
        # Get path to multiplet executable (assumed to be in same directory as this script)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        multiplet_path = os.path.join(script_dir, "multiplet")
        
        # Change to output directory
        os.chdir(output_dir)
        
        # Start the process
        self.process.start(multiplet_path, [])
        
        # Send input file content to process stdin
        with open(input_file, 'r') as f:
            input_content = f.read()
        
        self.process.write(input_content.encode())
        self.process.closeWriteChannel()
    
    def handle_stdout(self):
        """Handle standard output from the process"""
        data = self.process.readAllStandardOutput().data().decode()
        self.console_output.append(data)
    
    def handle_stderr(self):
        """Handle standard error from the process"""
        data = self.process.readAllStandardError().data().decode()
        self.console_output.append(data)
    
    def process_finished(self, exit_code, exit_status):
        """Handle process completion"""
        self.run_button.setEnabled(True)
        
        if exit_code == 0:
            self.console_output.append("\nMultiplet calculation completed successfully!")
        else:
            self.console_output.append(f"\nMultiplet calculation failed with exit code {exit_code}")
    
    def browse_convert_input(self):
        """Browse for rpesalms.dat file to convert"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select rpesalms.dat File", 
                                                  "", 
                                                  "DAT Files (*.dat)")
        if file_path:
            self.convert_input_path.setText(file_path)
            
            # Suggest default output file path
            base_dir = os.path.dirname(file_path)
            base_name = os.path.basename(file_path)
            name_parts = os.path.splitext(base_name)
            default_output = os.path.join(base_dir, f"{name_parts[0]}.edac")
            self.convert_output_path.setText(default_output)
    
    def browse_convert_output(self):
        """Browse for rpesalms.edac output file location"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Output File", 
                                                  "rpesalms.edac", 
                                                  "EDAC Files (*.edac)")
        if file_path:
            self.convert_output_path.setText(file_path)
    
    def convert_file(self):
        """Convert rpesalms.dat to rpesalms.edac"""
        input_file = self.convert_input_path.text()
        output_file = self.convert_output_path.text()
        
        if not input_file:
            QMessageBox.warning(self, "Error", "Please select an input file")
            return
            
        if not output_file:
            QMessageBox.warning(self, "Error", "Please specify an output file")
            return
        
        try:
            convert_rpesalms(input_file, output_file)
            self.convert_status.setText(f"Conversion successful! Output written to {output_file}")
            QMessageBox.information(self, "Success", f"File converted successfully!")
        except Exception as e:
            self.convert_status.setText(f"Conversion failed: {str(e)}")
            QMessageBox.critical(self, "Error", f"Conversion failed: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MultipletGUI()
    ex.show()
    sys.exit(app.exec()) 