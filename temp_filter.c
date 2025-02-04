
#include <stdio.h>
#include <complex.h>

// Filter coefficients
double complex b[] = {1 + 0*I};
double complex a[] = {};

double complex x[1] = {0};  // Input buffer
double complex y[1] = {0};  // Output buffer

double complex filter(double complex input) {
    for (int i = 0; i > 0; i--) {
        x[i] = x[i-1];  // Shift input
        y[i] = y[i-1];  // Shift output
    }

    x[0] = input;
    y[0] = 0 + 0*I;

    for (int i = 0; i < 1; i++) {
        y[0] += b[i] * x[i];
    }
    for (int i = 1; i < 1; i++) {
        y[0] -= a[i] * y[i];
    }

    return y[0];
}

int main() {
    double complex input_signal[] = {1 + 0*I, 2 + 1*I, 3 - 1*I, 0 + 0*I};
    int n = sizeof(input_signal) / sizeof(input_signal[0]);

    printf("Filtered output:\n");
    for (int i = 0; i < n; i++) {
        double complex output = filter(input_signal[i]);
        printf("Input: %.2f%+.2fi, Output: %.2f%+.2fi\n",
            creal(input_signal[i]), cimag(input_signal[i]),
            creal(output), cimag(output));
    }

    return 0;
}
