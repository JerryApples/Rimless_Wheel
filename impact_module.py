# -*- coding: utf-8 -*-
"""
Created on Mon May 12 18:29:17 2025

@author: jerry
"""


import numpy as np

# Σταθερές συστήματος
g = 9.81
l = 1.0
number_of_legs = 10
alpha = (2*np.pi) / number_of_legs  # Γωνία μεταξύ ποδιών
gamma = 0.15  # Γωνία κλίσης εδάφους 
omega_treshold = ( ((2*g)/l) * (1 - np.cos(gamma - alpha)) ) ** 0.5

def dynamic(t, y):
    """Εξίσωση stance phase: d²θ/dt² = (g/l) * sin(θ)"""
    theta = y[0]
    dtheta_dt = y[1]
    # το y είναι διάνυσμα το οποίο τροφοδοτείται από την solve_ivp 
    # και είναι [θ, ω]
    domega_dt = (g / l) * np.sin(theta) 
    return [dtheta_dt, domega_dt]


def impact_event(t, y):
    theta, omega = y # είναι ισοδύναμο με theta = y[0] και omega = y[1]
    
    return theta + alpha  # Event when θ = -α (leg touches ground)

impact_event.direction = -1  # Only trigger when decreasing (θ → -α)
impact_event.terminal = True

def apply_impact(theta, omega):
    """
    Υπολογισμός ταχύτητας μετά την κρούση.
    """
    if (omega > omega_treshold) :
        theta_dot_new =  np.cos(2 * alpha) * ( ( omega**2 + ((4*g)/l)*np.sin(alpha)*np.sin(gamma) ) ** 0.5)
    
    elif (-omega_treshold < omega and  omega < omega_treshold):
        theta_dot_new = (-theta) * np.cos(2*alpha)
    
    elif (omega < (-omega_treshold)):
        theta_dot_new =  - (np.cos(2 * alpha) * ( ( omega**2 + ((4*g)/l)*np.sin(alpha)*np.sin(gamma) ) ** 0.5) )
        
    
    return -alpha, theta_dot_new
