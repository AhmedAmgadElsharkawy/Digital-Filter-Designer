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
        self.max_history = 50
        self._is_batch_operation = False
        
        # Save initial empty state
        self.save_empty_state()

        # Connect buttons to handlers
        self.main_window.save_filter_button.clicked.connect(self.save_filter)
        self.main_window.load_filter_button.clicked.connect(self.load_filter)
        self.main_window.undo_button.clicked.connect(self.undo)
        self.main_window.redo_button.clicked.connect(self.redo)

        # Initialize buttons state
        self.update_button_states()

    def save_empty_state(self):
        """Save an empty state to the undo stack"""
        empty_state = {
            'poles': [],
            'zeroes': [],
            'conj_poles': [],
            'conj_zeroes': []
        }
        self.undo_stack = [empty_state]
        self.redo_stack = []
        self.update_button_states()

    def save_current_state(self):
        """Save current filter state to history"""
        if hasattr(self, '_loading'):
            return

        current_state = {
            'poles': deepcopy(self.main_window.filter_model.poles),
            'zeroes': deepcopy(self.main_window.filter_model.zeroes),
            'conj_poles': deepcopy(self.main_window.filter_model.conj_poles),
            'conj_zeroes': deepcopy(self.main_window.filter_model.conj_zeroes)
        }

        if not self._is_batch_operation:
            # Don't add state if it's identical to the last one
            if self.undo_stack and self._states_are_equal(current_state, self.undo_stack[-1]):
                return
                
            self.undo_stack.append(current_state)
            self.redo_stack.clear()
            
            if len(self.undo_stack) > self.max_history:
                self.undo_stack.pop(0)
            
            self.update_button_states()

    def _states_are_equal(self, state1, state2):
        """Compare two states for equality"""
        return (state1['poles'] == state2['poles'] and
                state1['zeroes'] == state2['zeroes'] and
                state1['conj_poles'] == state2['conj_poles'] and
                state1['conj_zeroes'] == state2['conj_zeroes'])

    def update_button_states(self):
        """Update the enabled state of undo/redo buttons"""
        self.main_window.undo_button.setEnabled(len(self.undo_stack) > 1)
        self.main_window.redo_button.setEnabled(len(self.redo_stack) > 0)

    def apply_state(self, state):
        """Apply a saved state to the filter"""
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
            delattr(self, '_loading')

    def undo(self):
        """Undo the last action"""
        if len(self.undo_stack) <= 1:
            return

        current_state = self.undo_stack.pop()
        previous_state = self.undo_stack[-1]
        
        self.redo_stack.append(current_state)
        self.apply_state(previous_state)
        self.update_button_states()

    def redo(self):
        """Redo the last undone action"""
        if not self.redo_stack:
            return

        next_state = self.redo_stack.pop()
        self.undo_stack.append(next_state)
        self.apply_state(next_state)
        self.update_button_states()

    def load_filter(self):
        """Load a filter configuration from a CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "Load Filter Configuration",
            "data/",
            "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            # Save current state before loading
            current_state = {
                'poles': deepcopy(self.main_window.filter_model.poles),
                'zeroes': deepcopy(self.main_window.filter_model.zeroes),
                'conj_poles': deepcopy(self.main_window.filter_model.conj_poles),
                'conj_zeroes': deepcopy(self.main_window.filter_model.conj_zeroes)
            }

            self._loading = True

            # Clear current state
            self.main_window.filter_model.clear_all_poles_and_zeroes()
            self.main_window.filter_z_plane.clear_all_graphical_items()

            # Load new state from file
            loaded_state = {
                'poles': [],
                'zeroes': [],
                'conj_poles': [],
                'conj_zeroes': []
            }

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
                        loaded_state['poles'].append(complex_value)
                    
                    elif type_ == 'zero':
                        self.main_window.complex_type = "Zero"
                        self.main_window.filter_model.add_zero(complex_value)
                        self.main_window.filter_z_plane.add_graphical_item(position)
                        loaded_state['zeroes'].append(complex_value)
                    
                    elif type_ == 'conj_pole':
                        self.main_window.complex_type = "Conj Poles"
                        self.main_window.filter_model.add_conj_poles(complex_value)
                        self.main_window.filter_z_plane.add_graphical_conjugate_items(position)
                        loaded_state['conj_poles'].append(complex_value)
                    
                    elif type_ == 'conj_zero':
                        self.main_window.complex_type = "Conj Zeroes"
                        self.main_window.filter_model.add_conj_zeroes(complex_value)
                        self.main_window.filter_z_plane.add_graphical_conjugate_items(position)
                        loaded_state['conj_zeroes'].append(complex_value)

            # Update undo/redo stacks
            if not self._states_are_equal(current_state, loaded_state):
                self.undo_stack.append(loaded_state)
                self.redo_stack.clear()
                if len(self.undo_stack) > self.max_history:
                    self.undo_stack.pop(0)
            
        except Exception as e:
            print(f"Error loading filter configuration: {e}")
        finally:
            delattr(self, '_loading')
            self.update_button_states()

    def save_filter(self):
        """Save the current filter configuration to a CSV file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self.main_window,
            "Save Filter Configuration",
            "data/",
            "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Type', 'Real', 'Imaginary'])
                
                for pole in self.main_window.filter_model.poles:
                    writer.writerow(['pole', pole.real, pole.imag])
                
                for zero in self.main_window.filter_model.zeroes:
                    writer.writerow(['zero', zero.real, zero.imag])
                
                for pole in self.main_window.filter_model.conj_poles:
                    writer.writerow(['conj_pole', pole.real, pole.imag])
                
                for zero in self.main_window.filter_model.conj_zeroes:
                    writer.writerow(['conj_zero', zero.real, zero.imag])
        except Exception as e:
            print(f"Error saving filter configuration: {e}")

    def complex_to_position(self, complex_value):
        """Convert a complex number to a QPointF position for the z-plane"""
        from PyQt5.QtCore import QPointF
        x = complex_value.real * 100
        y = -complex_value.imag * 100
        return QPointF(x, y)