import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle


class StructureController:
    def __init__(self, filter=None):
        self.circle_radius = 0.3
        self.box_width = 0.6
        self.box_height = 0.6
        self.arrow_head_width = 0.2
        self.arrow_head_length = 0.2
        self.center_x = 4
        self.current_fig = None
        self.current_ax = None
        self.filter = filter

    def cleanup_figure(self, fig):
        """Clean up matplotlib figure after use"""
        plt.close(fig)

    def _create_figure(self, figsize=(12, 8)):
        """Create new figure and axis or clear existing one"""
        plt.close('all')  # Close all existing figures
        self.current_fig, self.current_ax = plt.subplots(figsize=figsize)
        return self.current_fig, self.current_ax

    def _calculate_delays(self, transfer_function=None):
        """Calculate number of delay elements needed"""
        denominator_coeffs = transfer_function[1]
        numerator_coeffs = transfer_function[0]
        if len(denominator_coeffs) >= len(numerator_coeffs) - 1:
            if denominator_coeffs[-1] == 0:
                return len(denominator_coeffs) - 1
            return len(denominator_coeffs)
        else:
            if numerator_coeffs[-1] == 0:
                return len(numerator_coeffs) - 2
            return len(numerator_coeffs) - 1

    def _setup_plot(self, width, height, title):
        """Common plot setup logic"""
        ax = self.current_ax
        ax.set_xlim(-2, width)
        ax.set_ylim(-2 * height - 1, 2)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal')

        # Draw input arrow
        ax.arrow(-1, 0, 2.5, 0,
                 head_width=self.arrow_head_width, head_length=self.arrow_head_length)
        ax.text(-1.5, 0.3, 'x(n)', fontsize=12)

        plt.title(title)

    def _draw_elements(self, ax, transfer_function=None, offset_x=0):
        """Draw a single Direct Form II section at the specified x offset"""
        # Determine the number of delay elements needed
        denominator_coeffs = transfer_function[1]
        numerator_coeffs = transfer_function[0]
        if len(denominator_coeffs) > len(numerator_coeffs) - 1:
            # is_denominator_max_order = True  # Denominator has higher order so it determines the number of delays
            if denominator_coeffs[-1] == 0:  # Check if the last coefficient is zero so no need for the extra delay
                n_delays = len(denominator_coeffs) - 1
            else:
                n_delays = len(denominator_coeffs)
        elif len(denominator_coeffs) == len(numerator_coeffs) - 1:
            if denominator_coeffs[-1] == 0 and numerator_coeffs[-1] == 0:
                n_delays = len(denominator_coeffs) - 1
            else:
                n_delays = len(denominator_coeffs)
        else:
            if numerator_coeffs[-1] == 0:
                n_delays = len(numerator_coeffs) - 2
            else:
                n_delays = len(numerator_coeffs) - 1

        center_x = self.center_x + offset_x

        # Draw delay elements
        for i in range(n_delays):
            y_pos = -2 * (i + 1) - 0.3

            # Draw delay element box
            z_box = Rectangle((center_x - self.box_width / 2, y_pos),
                              self.box_width, self.box_height, fill=False)
            ax.add_patch(z_box)
            ax.text(center_x - 0.2, y_pos + 0.2, r'$z^{-1}$', fontsize=12)

            # Vertical connections for delay elements
            if i == 0:
                ax.arrow(center_x, 0, 0, y_pos + self.box_height + 0.2,
                         head_width=self.arrow_head_width, head_length=self.arrow_head_length)
            else:
                ax.arrow(center_x, y_pos + self.box_height + 1.4, 0, -1.2,
                         head_width=self.arrow_head_width, head_length=self.arrow_head_length)

            # Feedback paths
            if i < len(denominator_coeffs):
                ax.arrow(center_x - self.box_width / 2, y_pos + self.box_height / 2,
                         -1.5 + self.circle_radius, 0,
                         head_width=self.arrow_head_width, head_length=self.arrow_head_length)
                ax.text(center_x - 1.3, y_pos + self.box_height,
                        f'-{round(denominator_coeffs[i], 3)}', fontsize=12)
                ax.arrow(center_x - 2, y_pos + self.box_height, 0, 1.2,
                         head_width=self.arrow_head_width, head_length=self.arrow_head_length)

            # Feedforward paths
            if i + 1 < len(numerator_coeffs):
                ax.arrow(center_x + self.box_width / 2, y_pos + self.box_height / 2,
                         2.2, 0, head_width=self.arrow_head_width, head_length=self.arrow_head_length)
                ax.text(center_x + 1.5, y_pos + self.box_height,
                        f'{round(numerator_coeffs[i + 1], 3)}', fontsize=12)
                ax.arrow(center_x + 3, y_pos + self.box_height, 0, 1.2,
                         head_width=self.arrow_head_width, head_length=self.arrow_head_length)

        # Draw feedback summing junctions
        feedback_sum = Circle((center_x - 2, 0), self.circle_radius, fill=False)
        ax.add_patch(feedback_sum)
        ax.text(center_x - 2, 0, '+', ha='center', va='center', fontsize=12)
        for i in range(0, len(denominator_coeffs)):
            if i == len(denominator_coeffs) - 1 and denominator_coeffs[-1] == 0:
                continue
            y_pos = -2 * (i + 1)
            feedback_sum = Circle((center_x - 2, y_pos), self.circle_radius, fill=False)
            ax.add_patch(feedback_sum)
            ax.text(center_x - 2, y_pos, '+', ha='center', va='center', fontsize=12)

        # Draw output summing junctions
        for i in range(len(numerator_coeffs)):
            if i == len(numerator_coeffs) - 1 and numerator_coeffs[-1] == 0:
                continue
            y_pos = -2 * i
            output_sum = Circle((center_x + 3, y_pos), self.circle_radius, fill=False)
            ax.add_patch(output_sum)
            ax.text(center_x + 3, y_pos, '+', ha='center', va='center', fontsize=12)

        # Draw main path
        ax.arrow(center_x - 1.7, 0, 4.2, 0,
                 head_width=self.arrow_head_width, head_length=self.arrow_head_length)
        ax.text(center_x + 1.5, 0.3, f'{round(numerator_coeffs[0], 3)}', fontsize=12)

        return center_x + 3  # Return the x-coordinate of the output

    def _draw_output_arrow(self, start_x):
        """Draw the final output arrow and label"""
        self.current_ax.arrow(start_x + 0.3, 0, 1.5, 0,
                              head_width=self.arrow_head_width, head_length=self.arrow_head_length)
        self.current_ax.text(start_x + 1.2, 0.3, 'y(n)', fontsize=12)

    def draw_direct_form_2(self, figsize=(12, 12)):
        """Create Direct Form II structure from filter coefficients"""
        self._create_figure(figsize)

        # Calculate number of delays and plot dimensions
        tf = self.filter.get_transfer_function(self)
        # Remove leading 1 from denominator
        tf = (tf[0], tf[1][1:])
        n_delays = self._calculate_delays(tf)
        self._setup_plot(10, n_delays + 1, 'Filter Structure in Direct Form II ')

        # Draw the section and output
        output_x = self._draw_elements(self.current_ax, tf)
        self._draw_output_arrow(output_x)

        return self.current_fig

    def draw_cascade_form(self, figsize=(20, 20)):
        """Create Cascade Form structure from multiple sections"""
        self._create_figure(figsize)

        # Calculate plot dimensions
        _tf_sections = self.filter.get_cascade_form()  # shape(n_sections, 6)
        tf_sections = []
        for section in _tf_sections:
            numerator = section[:3]
            denominator = section[4:]
            if denominator[-1] == 0:
                denominator = denominator[:-1]
            if denominator[-1] == 0:
                denominator = denominator[:-1]
            if numerator[-1] == 0:
                numerator = numerator[:-1]
            if numerator[-1] == 0:
                numerator = numerator[:-1]
            tf_sections.append((numerator, denominator))

        max_delays = 2
        width = len(tf_sections) * 8 + 2
        self._setup_plot(width, max_delays + 1, 'Filter Structure in Cascade Form')

        # Draw each section
        last_offset = 0
        for i, tf in enumerate(tf_sections):
            last_offset = self._draw_elements(self.current_ax, tf, last_offset)

            # Connection to next section
            if i < len(tf_sections) - 1:
                self.current_ax.arrow(last_offset + self.circle_radius, 0,
                                      2.2, 0, head_width=self.arrow_head_width,
                                      head_length=self.arrow_head_length)

        # Draw final output
        if last_offset is not None:
            self._draw_output_arrow(last_offset)

        return self.current_fig, self.current_ax

    def show(self):
        """Display the current figure"""
        if self.current_fig is not None:
            plt.show()
            self.current_fig = None
            self.current_ax = None
        else:
            print("No figure to display")