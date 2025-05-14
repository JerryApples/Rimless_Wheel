# -*- coding: utf-8 -*-
"""
Created on Mon May 12 18:29:38 2025

@author: jerry
"""

import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from impact_module import dynamic, impact_event, apply_impact, alpha


def simulate(initial_omega, steps=10):
    theta = -alpha  # Αρχική γωνία ίση με γωνία πρόσκρουσης
    omega = initial_omega
    t = 0.0

    times, thetas, omegas = [], [], []

    print(f"{'Step':<6}{'ω before':>12}{'ω after':>12}")
    print("-" * 30)

    for step in range(steps):
        # Επίλυση swing phase
        sol = solve_ivp(dynamic, [t, t + 10], [theta, omega],
                        events=impact_event, max_step=0.001, rtol=1e-6)
        
        # Αποθήκευση αποτελεσμάτων
        times.extend(sol.t)
        thetas.extend(sol.y[0])
        omegas.extend(sol.y[1])

        # Εκτύπωση πριν/μετά την κρούση
        omega_before = sol.y[1][-1]
        theta, omega = apply_impact(sol.y[0][-1], omega_before)

        print(f"{step + 1:<6}{omega_before:>12.4f}{omega:>12.4f}")

        t = sol.t[-1]

    return times, thetas, omegas

if __name__ == "__main__":
    # Παράμετροι προσομοίωσης
    initial_omega = 5.0  # rad/s

    times, thetas, omegas = simulate(initial_omega)

    # Γραφικές παραστάσεις
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(times, thetas, label='Γωνία (rad)')
    plt.xlabel("Χρόνος (s)")
    plt.ylabel("Θ (rad)")
    plt.title("Γωνιακή Μετατόπιση")
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(times, omegas, label='Γωνιακή ταχύτητα (rad/s)', color='orange')
    plt.xlabel("Χρόνος (s)")
    plt.ylabel("ω (rad/s)")
    plt.title("Γωνιακή Ταχύτητα")
    plt.grid()

    plt.tight_layout()
    plt.show()
