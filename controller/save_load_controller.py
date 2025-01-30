from PyQt5.QtWidgets import QFileDialog
import csv
from PyQt5.QtCore import QPointF

class SaveLoadController:
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Connect buttons to handlers
        self.main_window.save_filter_button.clicked.connect(self.save_filter)
        self.main_window.load_filter_button.clicked.connect(self.load_filter)

    def save_filter(self):
        """Save the current filter configuration to a CSV file"""
        # Get file path from user
        file_path, _ = QFileDialog.getSaveFileName(
            self.main_window,
            "Save Filter Configuration",
            "data/",  # Default to data directory
            "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow(['Type', 'Real', 'Imaginary'])
                
                # Write poles
                for pole in self.main_window.filter_model.poles:
                    writer.writerow(['pole', pole.real, pole.imag])
                
                # Write zeros
                for zero in self.main_window.filter_model.zeroes:
                    writer.writerow(['zero', zero.real, zero.imag])
                
                # Write conjugate poles
                for pole in self.main_window.filter_model.conj_poles:
                    writer.writerow(['conj_pole', pole.real, pole.imag])
                
                # Write conjugate zeros
                for zero in self.main_window.filter_model.conj_zeroes:
                    writer.writerow(['conj_zero', zero.real, zero.imag])
        except Exception as e:
            print(f"Error saving filter configuration: {e}")

    def load_filter(self):
        """Load a filter configuration from a CSV file"""
        # Get file path from user
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "Load Filter Configuration",
            "data/",  # Default to data directory
            "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            # Clear existing filter
            self.main_window.filter_model.clear_all_poles_and_zeroes()
            self.main_window.filter_z_plane.clear_all_graphical_items()

            with open(file_path, 'r', newline='') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header row
                
                for row in reader:
                    type_, real, imag = row
                    complex_value = complex(float(real), float(imag))
                    position = self.complex_to_position(complex_value)

                    if type_ == 'pole':
                        self.main_window.complex_type = "Pole"
                        self.main_window.filter_model.add_pole(complex_value)
                        self.main_window.filter_z_plane.add_graphical_item(position)
                    
                    elif type_ == 'zero':
                        self.main_window.complex_type = "Zero"
                        self.main_window.filter_model.add_zero(complex_value)
                        self.main_window.filter_z_plane.add_graphical_item(position)
                    
                    elif type_ == 'conj_pole':
                        self.main_window.complex_type = "Conj Poles"
                        self.main_window.filter_model.add_conj_poles(complex_value)
                        self.main_window.filter_z_plane.add_graphical_conjugate_items(position)
                    
                    elif type_ == 'conj_zero':
                        self.main_window.complex_type = "Conj Zeroes"
                        self.main_window.filter_model.add_conj_zeroes(complex_value)
                        self.main_window.filter_z_plane.add_graphical_conjugate_items(position)

        except Exception as e:
            print(f"Error loading filter configuration: {e}")

    def complex_to_position(self, complex_value):
        """Convert a complex number to a QPointF position for the z-plane"""
        x = complex_value.real * 100
        y = -complex_value.imag * 100
        return QPointF(x, y)