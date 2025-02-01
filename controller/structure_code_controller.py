import numpy as np
from scipy.signal import tf2sos, zpk2tf, freqz
import matplotlib.pyplot as plt

class StructureCodeController:
    def __init__(self, filter_model):
        self.filter_model = filter_model

    def get_direct_form_ii(self):
        poles = self.filter_model.poles
        zeros = self.filter_model.zeroes
        numerator, denominator = self.direct_form_II(poles, zeros)
        return numerator, denominator

    def direct_form_II(self, poles, zeros):
        numerator = [1]
        denominator = [1]
        for pole in poles:
            denominator = np.convolve(denominator, [1, -complex(pole.real, pole.imag)])
        for zero in zeros:
            numerator = np.convolve(numerator, [1, -complex(zero.real, zero.imag)])
        return numerator, denominator

    def get_cascade_form(self):
        poles = self.filter_model.poles
        zeros = self.filter_model.zeroes
        sections = self.cascade_form(poles, zeros)
        return sections

    def cascade_form(self, poles, zeros):
        sections = []
        if len(poles) % 2 != 0 or len(zeros) % 2 != 0:
            raise ValueError("Number of poles and zeros must be even for cascade form.")

        for i in range(0, len(poles), 2):
            section_poles = poles[i:i+2]
            section_zeros = zeros[i:i+2]

            numerator = [1]
            denominator = [1]

            for pole in section_poles:
                denominator = np.convolve(denominator, [1, -complex(pole.real, pole.imag)])
            for zero in section_zeros:
                numerator = np.convolve(numerator, [1, -complex(zero.real, zero.imag)])

            sections.append((numerator, denominator))
        return sections

    def generate_c_code(self, filename, method="direct_form_II"):
        if method == "direct_form_II":
            numerator, denominator = self.get_direct_form_ii()
            self.generate_complex_filter_c(filename, method, b=numerator, a=denominator)
        else:
            sections = self.get_cascade_form()
            self.generate_complex_filter_c(filename, method, sections=sections)

    def generate_complex_filter_c(self, filename, method, sections=None, b=None, a=None):
        if method == "direct_form_II":
            if b is None or a is None:
                raise ValueError("Numerator and denominator coefficients must be provided for Direct Form II.")

            code = f"""
#include <stdio.h>
#include <complex.h>

// Filter coefficients
double complex b[] = {{{', '.join(f'{coef.real} + {coef.imag}*I' for coef in b)}}};
double complex a[] = {{{', '.join(f'{coef.real} + {coef.imag}*I' for coef in a[1:])}}};

double complex x[{len(b)}] = {{0}};  // Input buffer
double complex y[{len(a)}] = {{0}};  // Output buffer

double complex filter(double complex input) {{
    for (int i = {len(b) - 1}; i > 0; i--) {{
        x[i] = x[i-1];  // Shift input
        y[i] = y[i-1];  // Shift output
    }}

    x[0] = input;
    y[0] = 0 + 0*I;

    for (int i = 0; i < {len(b)}; i++) {{
        y[0] += b[i] * x[i];
    }}
    for (int i = 1; i < {len(a)}; i++) {{
        y[0] -= a[i] * y[i];
    }}

    return y[0];
}}

int main() {{
    double complex input_signal[] = {{1 + 0*I, 2 + 1*I, 3 - 1*I, 0 + 0*I}};
    int n = sizeof(input_signal) / sizeof(input_signal[0]);

    printf("Filtered output:\\n");
    for (int i = 0; i < n; i++) {{
        double complex output = filter(input_signal[i]);
        printf("Input: %.2f%+.2fi, Output: %.2f%+.2fi\\n",
            creal(input_signal[i]), cimag(input_signal[i]),
            creal(output), cimag(output));
    }}

    return 0;
}}
"""

        elif method == "cascade_form":
            if sections is None:
                raise ValueError("Sections must be provided for Cascade Form.")

            code = """
#include <stdio.h>
#include <complex.h>
"""

            for i, (b_sec, a_sec) in enumerate(sections):
                code += f"""
// Section {i + 1}
double complex b{i + 1}[] = {{{', '.join(f'{coef.real} + {coef.imag}*I' for coef in b_sec)}}};
double complex a{i + 1}[] = {{{', '.join(f'{coef.real} + {coef.imag}*I' for coef in a_sec[1:])}}};

double complex x{i + 1}[{len(b_sec)}] = {{0}};
double complex y{i + 1}[{len(a_sec)}] = {{0}};

double complex filter{i + 1}(double complex input) {{
    for (int j = {len(b_sec) - 1}; j > 0; j--) {{
        x{i + 1}[j] = x{i + 1}[j - 1];
        y{i + 1}[j] = y{i + 1}[j - 1];
    }}
    x{i + 1}[0] = input;
    y{i + 1}[0] = 0 + 0*I;

    for (int j = 0; j < {len(b_sec)}; j++) {{
        y{i + 1}[0] += b{i + 1}[j] * x{i + 1}[j];
    }}
    for (int j = 1; j < {len(a_sec)}; j++) {{
        y{i + 1}[0] -= a{i + 1}[j] * y{i + 1}[j];
    }}

    return y{i + 1}[0];
}}
"""

            code += """
int main() {
    double complex input_signal[] = {1 + 0*I, 2 + 1*I, 3 - 1*I, 0 + 0*I};
    int n = sizeof(input_signal) / sizeof(input_signal[0]);

    printf("Filtered output:\\n");
"""

            for i in range(len(sections)):
                code += f"""
    for (int j = 0; j < n; j++) {{
        input_signal[j] = filter{i + 1}(input_signal[j]);
    }}
"""

            code += """
    for (int j = 0; j < n; j++) {
        printf("Output: %.2f%+.2fi\\n", creal(input_signal[j]), cimag(input_signal[j]));
    }

    return 0;
}
"""

        else:
            raise ValueError("Invalid method. Choose 'direct_form_II' or 'cascade_form'.")

        with open(filename, 'w') as f:
            f.write(code)
        print(f"C code successfully written to {filename}")
