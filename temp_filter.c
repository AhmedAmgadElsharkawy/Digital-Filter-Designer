
#include <stdio.h>
#include <complex.h>

// Filter coefficients
double complex b[] = {1.0 + 0.0*I, 4.0002200484 + 0.0*I, 6.000220048389353 + 0.0*I, 3.999780048378704 + 0.0*I, 0.9995600484 + 0.0*I};
double complex a[] = {-1.5416656796000003 + 0.0*I, 1.427576516390528 + 0.0*I, -0.061462933831600175 + 0.0*I, 0.5558253857 + 0.0*I};

double complex x[5] = {0};  // Input buffer
double complex y[5] = {0};  // Output buffer

double complex filter(double complex input) {
    for (int i = 4; i > 0; i--) {
        x[i] = x[i-1];  // Shift input
        y[i] = y[i-1];  // Shift output
    }

    x[0] = input;
    y[0] = 0 + 0*I;

    for (int i = 0; i < 5; i++) {
        y[0] += b[i] * x[i];
    }
    for (int i = 1; i < 5; i++) {
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
