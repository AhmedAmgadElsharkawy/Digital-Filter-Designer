
#include <stdio.h>
#include <complex.h>

// Section 1
double complex b1[] = {1.0 + 0.0*I, 0.4750082125 + 0.0*I, 0.21174793700000002 + 0.0*I};
double complex a1[] = {0.953712634 + 0.0*I, 0.5656779368000001 + 0.0*I};

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
double complex b2[] = {1.0 + 0.0*I, 1.2635723273000001 + 0.0*I, 0.4247729524999999 + 0.0*I};
double complex a2[] = {-0.4361477111999999 + 0.0*I, 0.5634706981000001 + 0.0*I};

double complex x2[3] = {0};
double complex y2[3] = {0};

double complex filter2(double complex input) {
    for (int j = 2; j > 0; j--) {
        x2[j] = x2[j - 1];
        y2[j] = y2[j - 1];
    }
    x2[0] = input;
    y2[0] = 0 + 0*I;

    for (int j = 0; j < 3; j++) {
        y2[0] += b2[j] * x2[j];
    }
    for (int j = 1; j < 3; j++) {
        y2[0] -= a2[j] * y2[j];
    }

    return y2[0];
}

// Section 3
double complex b3[] = {1.0 + 0.0*I, 0.0 + 0.0*I, 0.0 + 0.0*I};
double complex a3[] = {-0.04686290779999991 + 0.0*I, 0.6119905060000002 + 0.0*I};

double complex x3[3] = {0};
double complex y3[3] = {0};

double complex filter3(double complex input) {
    for (int j = 2; j > 0; j--) {
        x3[j] = x3[j - 1];
        y3[j] = y3[j - 1];
    }
    x3[0] = input;
    y3[0] = 0 + 0*I;

    for (int j = 0; j < 3; j++) {
        y3[0] += b3[j] * x3[j];
    }
    for (int j = 1; j < 3; j++) {
        y3[0] -= a3[j] * y3[j];
    }

    return y3[0];
}

// Section 4
double complex b4[] = {1.0 + 0.0*I, 0.0 + 0.0*I, 0.0 + 0.0*I};
double complex a4[] = {0.540187138 + 0.0*I, 0.357404661 + 0.0*I};

double complex x4[3] = {0};
double complex y4[3] = {0};

double complex filter4(double complex input) {
    for (int j = 2; j > 0; j--) {
        x4[j] = x4[j - 1];
        y4[j] = y4[j - 1];
    }
    x4[0] = input;
    y4[0] = 0 + 0*I;

    for (int j = 0; j < 3; j++) {
        y4[0] += b4[j] * x4[j];
    }
    for (int j = 1; j < 3; j++) {
        y4[0] -= a4[j] * y4[j];
    }

    return y4[0];
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
        input_signal[j] = filter3(input_signal[j]);
    }

    for (int j = 0; j < n; j++) {
        input_signal[j] = filter4(input_signal[j]);
    }

    for (int j = 0; j < n; j++) {
        printf("Output: %.2f%+.2fi\n", creal(input_signal[j]), cimag(input_signal[j]));
    }

    return 0;
}
