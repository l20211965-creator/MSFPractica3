"""
Práctica 3: Sistema Musculoesquelético

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Escobedo Sandoval Pamela 
Número de control: 20211965
Correo institucional: l20211965@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0, t0, tend, dt, w, h = 0, 0, 10, 1E-3, 7, 3.5
N = int(tend/dt) + 1
t = np.linspace(t0, tend, N)
u2 = np.zeros(N); u2[round(1/dt):round(2/dt)] = 1  # Impulso

# Control
num_ctrl = [100*10e-6, 1-0.25]
den_ctrl = [100*(100e-6+10e-6), 1]
sys_ctrl = ctrl.tf(num_ctrl, den_ctrl)
print(f"FT Control: {sys_ctrl}\n")

# Caso
num_caso = [10e3*10e-6, 1-0.25]
den_caso = [10e3*(100e-6+10e-6), 1]
sys_caso = ctrl.tf(num_caso, den_caso)
print(f"FT Caso: {sys_caso}\n")

# Controlador
kP, kI = 0.22157, 3595.7467
Cr = 1E-6
Re = 1/(Cr*kI)
Rr = kP*Re
print(f"Cr = {Cr} F")
print(f"Re = {Re:.4f} Ω")
print(f"Rr = {Rr:.4f} Ω\n")
    
numPID = [Rr*Cr, 1]
denPID = [Re*Cr, 0]
PI = ctrl.tf(numPID, denPID)
print(f"FT Controlador PI: {PI}\n")

# Lazo cerrado
sys_caso_LC = ctrl.feedback(ctrl.series(PI, sys_caso), 1, sign=-1)
print(f"FT Caso LC: {sys_caso_LC}\n")

# RESPUESTAS
_, F_ctrl   = ctrl.forced_response(sys_ctrl, t, u2, x0)  # Control CE y FT
_, F_caso   = ctrl.forced_response(sys_caso, t, u2, x0)  # Caso CE y FT
_, PID_caso = ctrl.forced_response(sys_caso, t, u2, x0)  # PID(t): Caso

# COLORES 
clr1 = [0.7216, 0.8588, 0.5020]  # verde
clr2 = [0.9686, 0.9647, 0.8275]  # rojo
clr3 = [1.0000, 0.8941, 0.9373]  # azul

# Gráfica 1: Scope de Control
fig, axes = plt.subplots(2, 1, figsize=(w, h*2))
fig.patch.set_facecolor('white')

ax1 = axes[0]
ax1.plot(t, F_ctrl, '-',  color=clr1, linewidth=1.5, label=r'$F(t): Control\ CE$')
ax1.plot(t, F_ctrl, '--', color=clr2, linewidth=1.0, label=r'$F(t): Control\ FT$')
ax1.set_xlim(0, 10); ax1.set_xticks(np.arange(0, 11, 1))
ax1.set_ylim(-0.2, 0.9); ax1.set_yticks(np.arange(-0.2, 1.0, 0.2))
ax1.set_xlabel(r'$t\ [s]$', fontsize=11)
ax1.set_ylabel(r'$F(t)\ [V]$', fontsize=11)
ax1.set_title('Scope de Control', fontsize=10, fontweight='bold')
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.18), ncol=2,
           fontsize=9, frameon=False)

# Gráfica 2: Scope de Caso 
ax2 = axes[1]
ax2.plot(t, F_ctrl,   '-',  color=clr1, linewidth=1.0, label=r'$Control/2$')
ax2.plot(t, F_caso,   '-',  color=clr2, linewidth=1.0, label=r'$F(t): Caso\ CE$')
ax2.plot(t, F_caso,   '--', color=clr3, linewidth=1.5, label=r'$F(t): Caso\ FT$')
ax2.plot(t, PID_caso, ':',  color=clr2, linewidth=2.0, label=r'$PID(t): Caso$')
ax2.set_xlim(0, 10); ax2.set_xticks(np.arange(0, 11, 1))
ax2.set_ylim(-0.2, 0.9); ax2.set_yticks(np.arange(-0.2, 1.0, 0.2))
ax2.set_xlabel(r'$t\ [s]$', fontsize=11)
ax2.set_ylabel(r'$F(t)\ [V]$', fontsize=11)
ax2.set_title('Scope de Caso', fontsize=10, fontweight='bold')
ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.22), ncol=4,
           fontsize=9, frameon=False)

plt.tight_layout()
plt.savefig('musculoesqueletico.pdf', bbox_inches='tight')
plt.show()