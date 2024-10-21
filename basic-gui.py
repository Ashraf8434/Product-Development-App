from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox,
    QCheckBox, QGroupBox, QSlider, QGridLayout, QTabWidget, QFileDialog, QTextEdit, QTableWidget, QTableWidgetItem, QInputDialog, QMessageBox
)
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon
from PyQt5.QtCore import Qt
import sys
import lasio
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import seaborn as sns

class PetroAnalysis(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PetroAnalysis')
        self.setGeometry(100, 100, 1000, 650)

        # Set main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        ######################
        # Add a bold title label for the app name "Petro"
        title_label = QLabel("PetroAnalysis")
        title_label.setFont(QFont('Arial', 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(
            "background-color: skyblue; "
            "border: 2px solid black; "
            "padding: 10px; "
            "border-radius: 5px;"
        )
        main_layout.addWidget(title_label)
        
        ######################

        # Tabs for Data Loading and Basic Visualization
        tab_widget = QTabWidget()
        tab_widget.addTab(self.create_data_loading_tab(), "Data Loading")
        tab_widget.addTab(self.create_visualization_tab(), "Basic Visualization")
        tab_widget.addTab(self.create_formation_evaluation_tab(), "Formation Evaluation")
        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)

        # Set custom styling for the app
        self.setStyle()

    def setStyle(self):
        # Set the palette for custom colors
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#f2f5f9"))  # Light grey background
        palette.setColor(QPalette.Button, QColor("#007BFF"))  # Blue buttons
        palette.setColor(QPalette.ButtonText, QColor("#FFFFFF"))  # White text on buttons
        self.setPalette(palette)

    def create_data_loading_tab(self):
        # Create Data Loading Tab Layout
        data_loading_tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # LAS File Upload section
        las_group = self.create_group_box("Upload LAS/CSV File", "#D6EAF8")
        las_layout = QVBoxLayout()
        las_upload_layout = QHBoxLayout()
        self.las_file_input = QLineEdit()
        self.las_file_input.setPlaceholderText("Drag and drop file here or browse...")
        browse_button = QPushButton("Browse files")
        browse_button.clicked.connect(self.browse_files)
        las_upload_layout.addWidget(self.las_file_input)
        las_upload_layout.addWidget(browse_button)
        las_layout.addLayout(las_upload_layout)
        self.use_demo_checkbox = QCheckBox("Use demo file")
        las_layout.addWidget(self.use_demo_checkbox)
        las_group.setLayout(las_layout)

        # Formation Tops and Core Data section
        formation_core_group = self.create_group_box("Formation Tops & Core Data", "#E8F8F5")
        formation_core_layout = QHBoxLayout()
        formation_combo = QComboBox()
        formation_combo.addItems(["Upload Formation Tops"])
        formation_core_layout.addWidget(formation_combo)

        core_combo = QComboBox()
        core_combo.addItems(["Upload Core Data"])
        formation_core_layout.addWidget(core_combo)
        formation_core_group.setLayout(formation_core_layout)

        # LAS File Header Information
        header_info_group = self.create_group_box("LAS File Header Information", "#FDEDEC")
        header_layout = QVBoxLayout()
        self.header_text = QTextEdit()
        self.header_text.setReadOnly(True)
        self.header_text.setPlaceholderText("LAS file header information will appear here after loading.")
        header_layout.addWidget(self.header_text)
        header_info_group.setLayout(header_layout)
        
        ###############tabular form for well header info#######
        
        
        ############### 

        # Well Log Unit Conversion
        unit_conversion_group = self.create_group_box("Well Log Unit Conversion", "#FDEDEC")
        unit_conversion_layout = QVBoxLayout()
        unit_conversion_layout.addWidget(QPushButton("Unit Conversion"))
        unit_conversion_group.setLayout(unit_conversion_layout)

        # Well Data and Statistics
        well_data_group = self.create_group_box("Well Data", "#FCF3CF")
        well_data_layout = QVBoxLayout()

        # Create Table Widget for Well Data
        self.well_data_table = QTableWidget()
        self.well_data_table.setColumnCount(0)  # Initial column count
        self.well_data_table.setRowCount(0)      # Initial row count
        well_data_layout.addWidget(self.well_data_table)
        well_data_group.setLayout(well_data_layout)

        # Statistics Table
        statistics_group = self.create_group_box("Statistics", "#FCF3CF")
        statistics_layout = QVBoxLayout()

        # Table Widget for Statistics
        self.statistics_table = QTableWidget()
        self.statistics_table.setColumnCount(0)  # Initial column count for statistics
        self.statistics_table.setRowCount(0)      # Initial row count
        statistics_layout.addWidget(self.statistics_table)
        statistics_group.setLayout(statistics_layout)

        # Add groups to layout
        layout.addWidget(las_group)
        layout.addWidget(formation_core_group)
        layout.addWidget(header_info_group)
        layout.addWidget(unit_conversion_group)
        layout.addWidget(well_data_group)
        layout.addWidget(statistics_group)

        data_loading_tab.setLayout(layout)
        return data_loading_tab
    ############Customizing the button style################
    def style_button(self, button):
        
        button.setStyleSheet("""QPushButton {
            background-color: purple;  
            color: white;                /* White text */
            border: none;                /* No border */
            border-radius: 5px;         /* Rounded corners */
            padding: 10px;               /* Padding */
            font-size: 14px;             /* Font size */
            transition: background-color 0.3s; /* Smooth transition */
        }
        QPushButton:hover {
            background-color: yellow; 
        }
        QPushButton:pressed {
            background-color: red; 
        }
        """)
    #######################################################

    def create_visualization_tab(self):
        # Placeholder for the Basic Visualization tab content
        visualization_tab = QWidget()
        layout = QVBoxLayout()
        # Add buttons for different plots
        self.plot_buttons_layout = QHBoxLayout()
        self.plot_buttons_layout.setSpacing(10)
        self.histogram_button = QPushButton("Histogram")
        self.style_button(self.histogram_button)
        self.histogram_button.clicked.connect(self.plot_histogram)
        self.histogram_button.setStyleSheet("background-color: #3498db; color: white;")
        self.scatter_plot_button = QPushButton("Scatter Plot")
        self.style_button(self.scatter_plot_button)
        self.scatter_plot_button.clicked.connect(self.plot_scatter)
        self.scatter_plot_button.setStyleSheet("background-color: #3498db; color: white;")
        self.cross_plot_button = QPushButton("Cross Plot")
        self.cross_plot_button.clicked.connect(self.plot_cross)
        self.cross_plot_button.setStyleSheet("background-color: #3498db; color: white;")
        self.plot_buttons_layout.addWidget(self.histogram_button)
        self.plot_buttons_layout.addWidget(self.scatter_plot_button)
        self.plot_buttons_layout.addWidget(self.cross_plot_button)
        layout.addLayout(self.plot_buttons_layout)
        
        ########Triple compo plot#####
        self.plot_buttons_layout = QHBoxLayout()
        self.plot_buttons_layout.setSpacing(10)
        self.triple_combo_plot_button = QPushButton("Triple Combo Plot")
        self.triple_combo_plot_button.clicked.connect(self.plot_triple_combo)
        self.triple_combo_plot_button.setStyleSheet("background-color: #3498db; color: white;")
        self.plot_buttons_layout.addWidget(self.triple_combo_plot_button)
        layout.addLayout(self.plot_buttons_layout)
    ###############################
    # Formation Top Plot Section
    ###############################
        self.plot_buttons_layout = QHBoxLayout()
        self.plot_buttons_layout.setSpacing(10)
        self.formation_top_plot_button = QPushButton("Formation Top Plot")
        self.formation_top_plot_button.clicked.connect(self.plot_formation_top)
        self.formation_top_plot_button.setStyleSheet("background-color: #3498db; color: white;")
        self.plot_buttons_layout.addWidget(self.formation_top_plot_button)
        layout.addLayout(self.plot_buttons_layout)
        # Create a canvas for matplotlib
        self.canvas = FigureCanvas(plt.Figure())
        layout.addWidget(self.canvas)
        visualization_tab.setLayout(layout)
        return visualization_tab
    
    ################################### ###################
#############   Create formation evaluation tab   #################
    def create_formation_evaluation_tab(self):
        # Formation Evaluation Tab Setup
        formation_evaluation_tab = QWidget()
    
    # Main layout for Formation Evaluation tab
        main_layout = QVBoxLayout()
        #title_label = QLabel("Petrophysical properties Evaluation")
        title_label=QLabel("Vshale calculation and Plot")
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
####Input for min and max gr
        input_label = QLabel("Select Data:")

        self.data_combobox = QComboBox()

        load_button = QPushButton("Load Data")

        load_button.clicked.connect(self.load_evaluation_data)
        
        gr_input_layout=QGridLayout()
        min_gr_label=QLabel("Enter the minimum GR value (Percentile):")
        self.min_gr_input=QLineEdit()
        max_gr_label=QLabel("Enter the maximum GR value (Percentile):")
        self.max_gr_input=QLineEdit()
        gr_input_layout.addWidget(min_gr_label,0,0)
        gr_input_layout.addWidget(self.min_gr_input,0,1)
        gr_input_layout.addWidget(max_gr_label,1,0)
        gr_input_layout.addWidget(self.max_gr_input,1,1)
        main_layout.addLayout(gr_input_layout)
        
        #Vshape type#############
        
        
        
    # Slider for Depth Range
        slider_label = QLabel("Adjust the Depth Range:")
        self.depth_slider = QSlider(Qt.Horizontal)
        self.depth_slider.setMinimum(0)
        self.depth_slider.setMaximum(100)  # Adjust based on your data
        self.depth_slider.setValue(50)
        self.depth_slider.setTickPosition(QSlider.TicksBelow)
        self.depth_slider.setTickInterval(10)
    
    # Display selected depth range
        self.depth_range_label = QLabel("Selected Depth Range: 0 - 100")
        self.depth_slider.valueChanged.connect(self.update_depth_range)

    # Evaluation Results Display
        self.evaluation_results = QTextEdit()
        self.evaluation_results.setReadOnly(True)
        self.evaluation_results.setPlaceholderText("Evaluation results will appear here...")

    # Plot Area
        self.evaluation_canvas = FigureCanvas(plt.Figure())
    
    # Add all widgets to the layout
        main_layout.addWidget(input_label)
        main_layout.addWidget(self.data_combobox)
        main_layout.addWidget(load_button)
        main_layout.addWidget(slider_label)
        main_layout.addWidget(self.depth_slider)
        main_layout.addWidget(self.depth_range_label)
        main_layout.addWidget(self.evaluation_results)
        main_layout.addWidget(self.evaluation_canvas)

        formation_evaluation_tab.setLayout(main_layout)
        return formation_evaluation_tab

    def update_depth_range(self):
        # Update the label to show the current depth range selected by the slider
        current_value = self.depth_slider.value()
        self.depth_range_label.setText(f"Selected Depth Range: 0 - {current_value}")

    def load_evaluation_data(self):
        # Load the selected data for evaluation
        selected_data = self.data_combobox.currentText()
        if selected_data == "Select Data":
            QMessageBox.warning(self, "Warning", "Please select a valid dataset.")
            return
    
    # Example: Load data based on the selection (implement your logic)
    # self.load_data(selected_data)

    # For demonstration, we'll simulate evaluation results
        self.evaluation_results.setText(f"Evaluation results for {selected_data}...\nDepth Range: 0 - {self.depth_slider.value()}")

    # Example of plotting results
        self.plot_evaluation_results(selected_data)

    def plot_evaluation_results(self, selected_data):
        # Placeholder for plotting logic based on the selected data
        self.evaluation_canvas.figure.clf()  # Clear previous plots
        ax = self.evaluation_canvas.figure.add_subplot(111)
    
    # Simulated data for plotting
        depths = np.linspace(0, self.depth_slider.value(), 100)
        values = np.random.rand(100) * 100  # Example random values for demonstration

        ax.plot(values, depths, color='blue')
        ax.set_title(f'Evaluation Plot for {selected_data}')
        ax.set_xlabel('Values')
        ax.set_ylabel('Depth')
        ax.invert_yaxis()  # Depth increases downward
        ax.grid(True)
    
        self.evaluation_canvas.draw()  # Redraw the canvas
        
########################################################     
###########################################################
    def plot_histogram(self):
        # Plot a histogram for selected logs
        if hasattr(self, 'las_data'):
            selected_log, ok = QInputDialog.getItem(self, "Select Log for Histogram", "Select Log:", self.las_data.columns.tolist(), 0, False)
            if ok:
                # Plot the histogram
                data = self.las_data[selected_log].dropna()  # Drop NaN values for cleaner plot
                self.canvas.figure.clf()  # Clear the previous plot
                ax = self.canvas.figure.add_subplot(111)
                sns.histplot(data, bins=30, ax=ax, kde=True, color='blue')  # Add KDE for smooth distribution
                ax.set_title(f'Histogram of {selected_log}')
                ax.set_xlabel(selected_log)
                ax.set_ylabel('Counts')
                self.canvas.draw()  # Redraw the canvas

    def plot_scatter(self):
        # Plot a scatter plot for two selected logs
        if hasattr(self, 'las_data'):
            log_x, ok_x = QInputDialog.getItem(self, "Select X Log for Scatter Plot", "Log X Name:", self.las_data.columns.tolist(), 0, False)
            if ok_x:
                log_y, ok_y = QInputDialog.getItem(self, "Select Y Log for Scatter Plot", "Log Y Name:", self.las_data.columns.tolist(), 0, False)
                if ok_y:
                    x_data = self.las_data[log_x].dropna()
                    y_data = self.las_data[log_y].dropna()
                    plt_data = pd.concat([x_data, las['Depth']], axis=1).dropna()  # Combine and drop NaN
                    self.canvas.figure.clf()  # Clear the previous plot
                    ax = self.canvas.figure.add_subplot(111)
                    ax.scatter(plt_data[log_x], plt_data[log_y], color='green', cmap='viridis', alpha=0.5)
                    ax.set_title(f'Scatter Plot: {log_x} vs {log_y}')
                    ax.set_xlabel(log_x)
                    ax.set_ylabel(log_y)
                    self.canvas.draw()  # Redraw the canvas

    def plot_cross(self):
        # Plot a cross plot for two selected logs
        if hasattr(self, 'las_data'):
            log_x, ok_x = QInputDialog.getItem(self, "Select X Log for Cross Plot", "Log X Name:", self.las_data.columns.tolist(), 0, False)
            if ok_x:
                # Select Y Log 1 for the Combo Plot
                log_y1, ok_y1 = QInputDialog.getItem(self, "Select Y Log 1 for Combo Plot", "Log Y1 Name:", self.las_data.columns.tolist(), 0, False)
                if ok_y1:
                    # Select Y Log 2 for the Combo Plot
                    log_y2, ok_y2 = QInputDialog.getItem(self, "Select Y Log 2 for Combo Plot", "Log Y2 Name:", self.las_data.columns.tolist(), 0, False)
                    if ok_y2:
                        log_y3, ok_y3 = QInputDialog.getItem(self, "Select Y Log 3 for Combo Plot", "Log Y3 Name:", self.las_data.columns.tolist(), 0, False)
                        if ok_y3:
                            x_data = self.las_data[log_x].dropna()
                            y_data1 = self.las_data[log_y1].dropna()
                            y_data2= self.las_data[log_y2].dropna()
                            y_data3 = self.las_data[log_y3].dropna()
                            plt_data = pd.concat([x_data, y_data1,y_data2,y_data3], axis=1).dropna()  # Combine and drop NaN
                            
                            if plt_data.empty:
                                QMessageBox.warning(self, "Error", "Selected logs have no data. Please select other logs.")
                                return
                            self.canvas.figure.clf()  # Clear the previous plot
                            fig,axs=plt.subplots(3,1,figsize=(15,5),sharex=True)
                            # Plot each log on a different subplot
                            axs[0].plot(plt_data[log_x], plt_data[log_y1], color='blue', label=log_y1)
                            axs[0].set_ylabel(log_y1)
                            axs[0].legend(loc='upper right')
                            axs[0].grid(True)

                            axs[1].plot(plt_data[log_x], plt_data[log_y2], color='orange', label=log_y2)
                            axs[1].set_ylabel(log_y2)
                            axs[1].legend(loc='upper right')
                            axs[1].grid(True)

                            axs[2].plot(plt_data[log_x], plt_data[log_y3], color='green', label=log_y3)
                            axs[2].set_ylabel(log_y3)
                            axs[2].set_xlabel(log_x)
                            axs[2].legend(loc='upper right')
                            axs[2].grid(True)
                            # Set a title for the entire figure
                            fig.suptitle(f'Triple Combo Plot: {log_x} vs {log_y1}, {log_y2}, {log_y3}', fontsize=16)

                        # Redraw the canvas to display the new plot
                            self.canvas.draw()
                            
#########COde for triple combo plot########
    def plot_triple_combo(self):
        """plot for triple combo"""
        if hasattr(self,'las_data'):
            #Selecting the logs
            log_x, ok_x = QInputDialog.getItem(self, "Select X Log for Triple Combo Plot", "Log X Name:", self.las_data.columns.tolist(), 0, False)
            if ok_x:
                log_y, ok_y = QInputDialog.getItem(self, "Select Y Log for Triple Combo Plot", "Log Y Name:", self.las_data.columns.tolist(), 0, False)
                if ok_y:
                    log_z, ok_z = QInputDialog.getItem(self, "Select Z Log for Triple Combo Plot", "Log Z Name:", self.las_data.columns.tolist(), 0, False)
                    if ok_z:
                        x_data = self.las_data[log_x].dropna()
                        y_data = self.las_data[log_y].dropna()
                        z_data = self.las_data[log_z].dropna()
                        plt_data = pd.concat([x_data, y_data, z_data], axis=1).dropna()
#######################PLOT FORMATION TOP CODE#################
    def plot_formation_top(self):
        """plot for formation top"""
        if hasattr(self,'las_data'):
            #Prompt the user to select the logs for depth
            depth_log, ok_depth = QInputDialog.getItem(self, "Select Depth Log for Formation Top Plot", "Depth log:", self.las_data.columns.tolist(), 0, False)
            if not ok_depth:
                return
            #Prompt the user to select the logs for formation top
            formation_log, ok_formation = QInputDialog.getItem(self, "Select Formation Top Log for Formation Top Plot", "Formation Top log:", self.las_data.columns.tolist(), 0, False)
            if not ok_formation:
                return
            depth_data=self.las_data[depth_log].dropna()
            formation_data=self.las_data[formation_log].dropna()
            #drop nun value
            plot_data=pd.concat([depth_data,formation_data],axis=1).dropna()
            #clear the previous plot and create a new formation plot
            self.canvas.figure.clf()
            ax=self.canvas.figure.add_subplot(111)
            ax.plot(plot_data[formation_log],plot_data[depth_log],color='red',lw=2)
            ax.set_title(f'Formation Top Plot: {formation_log} vs {depth_log}') 
            ax.set_xlabel(formation_log)
            ax.set_ylabel(depth_log)
            ax.invert_yaxis()  #####It means depth increases downward
            ax.grid(True)
            self.canvas.draw()

################################################################3

##########################################
    def browse_files(self):
        # Functionality for file browsing
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open LAS or CSV File", "", "LAS Files (*.las);;CSV Files (*.csv)", options=options)
        if file_name:
            self.las_file_input.setText(file_name)
            if file_name.endswith('.las'):
                self.load_las_data(file_name)
            elif file_name.endswith('.csv'):
                self.load_csv_data(file_name)

    def load_las_data(self, file_path):
        try:
            las=lasio.read(file_path)
            self.header_text.setText(str(las.header))
            self.las_data=las.df()
            self.update_well_data_table(self.las_data)
            self.update_statistics_table(self.las_data)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error loading LAS file: {str(e)}")

    def load_csv_data(self, file_path):
        # Function to load CSV data
        df = pd.read_csv(file_path)
        self.las_data = df
        self.update_well_data_table(self.las_data)
        self.update_statistics_table(self.las_data)

    def update_well_data_table(self, df):
        # Update the table with well data
        self.well_data_table.setRowCount(df.shape[0])
        self.well_data_table.setColumnCount(df.shape[1])
        self.well_data_table.setHorizontalHeaderLabels(df.columns)
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.well_data_table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))

    def update_statistics_table(self, df):
        # Update the statistics table with data statistics
        stats = df.describe().T
        self.statistics_table.setRowCount(stats.shape[0])
        self.statistics_table.setColumnCount(stats.shape[1])
        self.statistics_table.setHorizontalHeaderLabels(stats.columns)
        self.statistics_table.setVerticalHeaderLabels(stats.index)
        for i in range(stats.shape[0]):
            for j in range(stats.shape[1]):
                self.statistics_table.setItem(i, j, QTableWidgetItem(str(stats.iloc[i, j])))

    def create_group_box(self, title, color):
        # Create a styled group box for sections
        group_box = QGroupBox(title)
        group_box.setStyleSheet(f"QGroupBox {{ background-color: {color}; border: 1px solid #000; border-radius: 5px; padding: 10px; font-size: 14px; font-weight: bold; }}")
        return group_box

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("1.png"))
    window = PetroAnalysis()
    window.show()
    sys.exit(app.exec_())
