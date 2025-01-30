import numpy as np

def calculate_response(poles, zeroes, num_points=1000):
    omega = np.linspace(-np.pi, np.pi, num_points)
    z = np.exp(1j * omega)  

    numerator = np.ones_like(z)
    for zero in zeroes:
        numerator *= (z - zero) 
    
    denominator = np.ones_like(z)
    for pole in poles:
        denominator *= (z - pole) 

    H = numerator / denominator

    magnitude = np.abs(H)
    phase = np.angle(H) 

    return omega, magnitude, phase
