
#include <stdio.h>
#include <complex.h>

// Section 1
double complex b1[] = {1.0 + 0.0*I, 0.07697000000000001 + -0.7976700000000001*I, -0.2001464842 + -0.033586075800000004*I};
double complex a1[] = {-0.58776 + -0.80467*I, -0.26560412590000004 + 0.3542221805*I};

double complex x1[3] = {0};
double complex y1[3] = {0};

double complex filter1(double complex input) {
    for (int j = 2; j > 0; j--) {
        x1[j] = x1[j - 1];
        y1[j] = y1[j - 1];
    }
    x1[0] = input;
    y1[0] = 0 + 0*I;

    for (int j = 0; j < 3; j++) {
        y1[0] += b1[j] * x1[j];
    }
    for (int j = 1; j < 3; j++) {
        y1[0] -= a1[j] * y1[j];
    }

    return y1[0];
}

// Section 2
double complex b2[] = {1 + 0*I};
double complex a2[] = {-0.4898 + -0.048980000000000024*I, 0.0889095356 + -0.0845013556*I};

double complex x2[1] = {0};
double complex y2[3] = {0};

double complex filter2(double complex input) {
    for (int j = 0; j > 0; j--) {
        x2[j] = x2[j - 1];
        y2[j] = y2[j - 1];
    }
    x2[0] = input;
    y2[0] = 0 + 0*I;

    for (int j = 0; j < 1; j++) {
        y2[0] += b2[j] * x2[j];
    }
    for (int j = 1; j < 3; j++) {
        y2[0] -= a2[j] * y2[j];
    }

    return y2[0];
}

int main() {
    double complex input_signal[] = {1 + 0*I, 2 + 1*I, 3 - 1*I, 0 + 0*I};
    int n = sizeof(input_signal) / sizeof(input_signal[0]);

    printf("Filtered output:\n");

    for (int j = 0; j < n; j++) {
        input_signal[j] = filter1(input_signal[j]);
    }

    for (int j = 0; j < n; j++) {
        input_signal[j] = filter2(input_signal[j]);
    }

    for (int j = 0; j < n; j++) {
        printf("Output: %.2f%+.2fi\n", creal(input_signal[j]), cimag(input_signal[j]));
    }

    return 0;
}
