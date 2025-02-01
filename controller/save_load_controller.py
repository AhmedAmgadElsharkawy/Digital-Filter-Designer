from PyQt5.QtWidgets import QFileDialog
import csv
from copy import deepcopy

class SaveLoadController:
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Initialize undo/redo stacks
        self.undo_stack = []
        self.redo_stack = []
        self.max_history = 20  # Maximum number of states to keep in history

        # Connect buttons to handlers
        self.main_window.save_filter_button.clicked.connect(self.save_filter)
        self.main_window.load_filter_button.clicked.connect(self.load_filter)
        self.main_window.undo_button.clicked.connect(self.undo)
        self.main_window.redo_button.clicked.connect(self.redo)

        # Connect to filter model's updated signal to track changes
        self.main_window.filter_model.updated.connect(self.on_filter_updated)

        # Initialize buttons state
        self.update_button_states()

    def save_current_state(self):
        """Save current filter state to history"""
        # Don't save state if we're in the middle of a load operation
        if hasattr(self, '_loading'):
            return
            
        current_state = {
            'poles': deepcopy(self.main_window.filter_model.poles),
            'zeroes': deepcopy(self.main_window.filter_model.zeroes),
            'conj_poles': deepcopy(self.main_window.filter_model.conj_poles),
            'conj_zeroes': deepcopy(self.main_window.filter_model.conj_zeroes)
        }
        
        # Save state and clear redo stack
        self.undo_stack.append(current_state)
        self.redo_stack.clear()
        
        # Limit the size of undo stack
        if len(self.undo_stack) > self.max_history:
            self.undo_stack.pop(0)
        
        self.update_button_states()

    def on_filter_updated(self):
        """Called when filter model is updated"""
        # Save state for all operations except load
        if not hasattr(self, '_loading'):
            self.save_current_state()

    def update_button_states(self):
        """Update the enabled state of undo/redo buttons"""
        self.main_window.undo_button.setEnabled(len(self.undo_stack) > 1)  # Enable only if we have more than one state
        self.main_window.redo_button.setEnabled(len(self.redo_stack) > 0)

    def apply_state(self, state):
        """Apply a saved state to the filter"""
        # Set flag to prevent state saving during state application
        self._loading = True
        
        try:
            # Clear current state
            self.main_window.filter_model.clear_all_poles_and_zeroes()
            self.main_window.filter_z_plane.clear_all_graphical_items()

            # Restore poles
            for pole in state['poles']:
                self.main_window.complex_type = "Pole"
                self.main_window.filter_model.add_pole(pole)
                position = self.complex_to_position(pole)
                self.main_window.filter_z_plane.add_graphical_item(position)

            # Restore zeros
            for zero in state['zeroes']:
                self.main_window.complex_type = "Zero"
                self.main_window.filter_model.add_zero(zero)
                position = self.complex_to_position(zero)
                self.main_window.filter_z_plane.add_graphical_item(position)

            # Restore conjugate poles
            for pole in state['conj_poles']:
                self.main_window.complex_type = "Conj Poles"
                self.main_window.filter_model.add_conj_poles(pole)
                position = self.complex_to_position(pole)
                self.main_window.filter_z_plane.add_graphical_conjugate_items(position)

            # Restore conjugate zeros
            for zero in state['conj_zeroes']:
                self.main_window.complex_type = "Conj Zeroes"
                self.main_window.filter_model.add_conj_zeroes(zero)
                position = self.complex_to_position(zero)
                self.main_window.filter_z_plane.add_graphical_conjugate_items(position)
        
        finally:
            # Remove loading flag
            delattr(self, '_loading')

    def undo(self):
        """Undo the last action"""
        if len(self.undo_stack) <= 1:  # Need at least 2 states to undo
            return

        # Get current state and previous state
        current_state = self.undo_stack.pop()
        previous_state = self.undo_stack[-1]  # Get previous state without removing it
        
        # Save current state to redo stack
        self.redo_stack.append(current_state)
        
        # Apply the previous state
        self.apply_state(previous_state)
        
        self.update_button_states()

    def redo(self):
        """Redo the last undone action"""
        if not self.redo_stack:
            return

        # Get next state from redo stack
        next_state = self.redo_stack.pop()
        
        # Save it to undo stack
        self.undo_stack.append(next_state)
        
        # Apply the next state
        self.apply_state(next_state)
        
        self.update_button_states()

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
            # Set loading flag to prevent state saving
            self._loading = True

            # Clear existing filter
            self.main_window.filter_model.clear_all_poles_and_zeroes()
            self.main_window.filter_z_plane.clear_all_graphical_items()

            # Clear undo/redo stacks since we're loading a new file
            self.undo_stack.clear()
            self.redo_stack.clear()

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

            # Save initial state after loading
            self.save_current_state()
            
        except Exception as e:
            print(f"Error loading filter configuration: {e}")
        finally:
            # Remove loading flag
            delattr(self, '_loading')
            self.update_button_states()

    def complex_to_position(self, complex_value):
        """Convert a complex number to a QPointF position for the z-plane"""
        from PyQt5.QtCore import QPointF
        x = complex_value.real * 100
        y = -complex_value.imag * 100
        return QPointF(x, y)