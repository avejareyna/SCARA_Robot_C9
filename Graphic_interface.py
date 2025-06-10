import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

L1 = 20
L2 = 20
L3 = 20
rmin = 20
rmax = 60
vel_lento = 30
vel_media = 60
vel_rapida = 90
start = 0
accion = 0
registro_acciones = {}

#----------Funciones del programa----------
def cambiar_modo_cinematica():
    if modo_cinematica.get() == "directa":
        entry_theta1.config(state='normal')
        entry_theta2.config(state='normal')
        entry_theta3.config(state='normal')
        entry_x.config(state='disabled')
        entry_y.config(state='disabled')
        entry_z.config(state='normal')
        boton_actualizar.config(command=entrada_cinematica_directa)
    else:
        entry_theta1.config(state='disabled')
        entry_theta2.config(state='disabled')
        entry_theta3.config(state='disabled')
        entry_x.config(state='normal')
        entry_y.config(state='normal')
        entry_z.config(state='normal')
        boton_actualizar.config(command=entrada_cinematica_inversa)

def cambiar_modo_electroiman():
    global estado_electroiman
    if modo_electroiman.get() == "activado":
        estado_electroiman = 1       
    else:
        estado_electroiman = 0

def entrada_cinematica_directa():
    global pos_X, pos_Y, pos_Z, start, t1, t2, t3
    if(start):
        try:
            t1 = float(entry_theta1.get())
            t2 = float(entry_theta2.get())
            t3 = float(entry_theta3.get())
            pos_Z = float(entry_z.get())
        except ValueError:
            label_resultado.config(text="Entrada inválida")
            return
    else:
        t1 = 0
        t2 = 0
        t3 = 0
        pos_Z = 0
        start = 1

    if((t1 < -90) or (t2 < -90) or (t3 < -90) or (t1 > 90) or (t3 > 90) or (t3 > 90) or (pos_Z < 0) or (pos_Z > 60)):
        label_resultado.config(text="Entrada inválida") 
        return

    puntos = cinematica_directa(t1, t2, t3)
    x_vals, y_vals = zip(*puntos)

    if(x_vals[-1] < 0):
        label_resultado.config(text="Entrada inválida")
        return

    if((x_vals[-1]**2 + y_vals[-1]**2) < 400):
        label_resultado.config(text="Entrada inválida")
        return

    ax1.clear()
    semicircle_outer = Wedge(center=(0, 0), r=rmax, theta1=-90, theta2=90, color="#a2d7ff", alpha=0.5, zorder=0)
    semicircle_inner = Wedge(center=(0, 0), r=rmin, theta1=-90, theta2=90, color='white', zorder=1)    
    ax1.add_artist(semicircle_inner)
    ax1.add_artist(semicircle_outer)
    ax1.plot(x_vals, y_vals, 'o-', linewidth=4, color="#2683c6")
    ax1.set_xlim(-70, 70)
    ax1.set_ylim(-70, 70)
    ax1.set_title("Brazo SCARA - rotacional", fontsize=13, color="#075985")
    ax1.set_aspect('equal')
    ax1.grid()
    canvas1.draw()

    ax2.clear()
    ax2.set_xlim(0, 4)
    ax2.set_ylim(0, 80)
    ax2.set_title("Brazo SCARA - traslacional", fontsize=13, color="#075985")
    ax2.set_aspect('auto')
    ax2.add_patch(plt.Rectangle((1.5, 0), 1, 70, edgecolor='#222', facecolor='#e0e7ef'))
    ax2.add_patch(plt.Rectangle((1.5, pos_Z), 1, 1, edgecolor='#222', facecolor='#2683c6'))
    ax2.text(2, pos_Z + 1.2, f"{pos_Z:.1f} cm", ha='center', fontsize=12, color='#075985')
    canvas2.draw()
        
    label_resultado.config(text=f"Posición X: {x_vals[-1]:.2f} | Y: {y_vals[-1]:.2f} | Z:{pos_Z:.2f}")

def entrada_cinematica_inversa():
    global pos_X, pos_Y, pos_Z, start
    try:
        pos_X = float(entry_x.get())
        pos_Y = float(entry_y.get())
        pos_Z = float(entry_z.get())
    except ValueError:
        label_resultado.config(text="Entrada inválida")
        return

    if(pos_X < 0 or pos_X > 60):
        label_resultado.config(text="Entrada inválida")
        return    

    if((pos_X**2 + pos_Y**2) <= 3600 and (pos_X**2 + pos_Y**2) >= 3025):
        phi = np.arctan2(pos_Y,pos_X)
        phi2 = phi
        print(f"phi = {np.degrees(phi)}")
    elif((pos_X**2 + pos_Y**2) < 3025 and (pos_X**2 + pos_Y**2) >= 2500):
        phi = np.arctan2(pos_Y,pos_X) - 2*(np.pi/15)
        phi2 = np.arctan2(pos_Y,pos_X) + 2*(np.pi/15)
        print(f"phi = {np.degrees(phi)}")
    elif((pos_X**2 + pos_Y**2) < 2500 and (pos_X**2 + pos_Y**2) >= 2025):
        phi = np.arctan2(pos_Y,pos_X) - 3*(np.pi/15)
        phi2 = np.arctan2(pos_Y,pos_X) + 3*(np.pi/15)
        print(f"phi = {np.degrees(phi)}")
    elif((pos_X**2 + pos_Y**2) < 2025 and (pos_X**2 + pos_Y**2) >= 1600):
        phi = np.arctan2(pos_Y,pos_X) - 4*(np.pi/15)
        phi2 = np.arctan2(pos_Y,pos_X) + 4*(np.pi/15)
        print(f"phi = {np.degrees(phi)}")
    elif((pos_X**2 + pos_Y**2) < 1600 and (pos_X**2 + pos_Y**2) >= 1225):
        phi = np.arctan2(pos_Y,pos_X) - 5*(np.pi/15)
        phi2 = np.arctan2(pos_Y,pos_X) + 5*(np.pi/15)
        print(f"phi = {np.degrees(phi)}")
    elif((pos_X**2 + pos_Y**2) < 1225 and (pos_X**2 + pos_Y**2) >= 900):
        phi = np.arctan2(pos_Y,pos_X) - 6*(np.pi/15)
        phi2 = np.arctan2(pos_Y,pos_X) + 6*(np.pi/15)
        print(f"phi = {np.degrees(phi)}")
    elif((pos_X**2 + pos_Y**2) < 900 and (pos_X**2 + pos_Y**2) >= 625):
        phi = np.arctan2(pos_Y,pos_X) - 7*(np.pi/15)
        phi2 = np.arctan2(pos_Y,pos_X) + 7*(np.pi/15)
        print(f"phi = {np.degrees(phi)}")
    elif((pos_X**2 + pos_Y**2) < 625 and (pos_X**2 + pos_Y**2) >= 400):
        phi = np.arctan2(pos_Y,pos_X) - np.pi/2
        phi2 = np.arctan2(pos_Y,pos_X) + np.pi/2
        print(f"phi = {np.degrees(phi)}")
    else:
        label_resultado.config(text="Entrada inválida")
        return

    #phi = np.pi /3  #orientación del último eslabón con respecto a la horizontal

    soluciones = cinematica_inversa(pos_X, pos_Y, phi, L1, L2, L3)
    if not soluciones:
        label_resultado.config(text="No hay solución posible")
        return
    # Tomamos la primera solución
    theta1, theta2, theta3 = soluciones[0]

    t1_deg = np.degrees(theta1)
    t2_deg = np.degrees(theta2)
    t3_deg = np.degrees(theta3)

    print(f"Valores de la primera solución: theta1:{t1_deg},theta2:{t2_deg},theta3:{t3_deg}")

    if(t1_deg > 90 or t2_deg > 90 or t3_deg > 90 or t1_deg < -90 or t2_deg < -90 or t3_deg < -90 ):
        theta1, theta2, theta3 = soluciones[1]
        t1_deg = np.degrees(theta1)
        t2_deg = np.degrees(theta2)
        t3_deg = np.degrees(theta3)

        print(f"Valores de la segunda solución: theta1:{t1_deg},theta2:{t2_deg},theta3:{t3_deg}")

        if(t1_deg > 90 or t2_deg > 90 or t3_deg > 90 or t1_deg < -90 or t2_deg < -90 or t3_deg < -90 ):
            print("Cambiando el signo de phi")
            phi = -phi
            print(f"phi = {np.degrees(phi)}")

            soluciones = cinematica_inversa(pos_X, pos_Y, phi, L1, L2, L3)
            if not soluciones:
                label_resultado.config(text="No hay solución posible")
                return
            theta1, theta2, theta3 = soluciones[0]

            t1_deg = np.degrees(theta1)
            t2_deg = np.degrees(theta2)
            t3_deg = np.degrees(theta3)

            print(f"Valores de la tercera solución: theta1:{t1_deg},theta2:{t2_deg},theta3:{t3_deg}")

            if(t1_deg > 90 or t2_deg > 90 or t3_deg > 90 or t1_deg < -90 or t2_deg < -90 or t3_deg < -90 ):
                theta1, theta2, theta3 = soluciones[1]
                t1_deg = np.degrees(theta1)
                t2_deg = np.degrees(theta2)
                t3_deg = np.degrees(theta3)

                print(f"Valores de la cuarta solución: theta1:{t1_deg},theta2:{t2_deg},theta3:{t3_deg}")

                if(t1_deg > 90 or t2_deg > 90 or t3_deg > 90 or t1_deg < -90 or t2_deg < -90 or t3_deg < -90 ):
                    phi = phi2
                    print("Cambiando la orientacion de phi")
                    print(f"phi = {np.degrees(phi)}")
                    soluciones = cinematica_inversa(pos_X, pos_Y, phi, L1, L2, L3)
                    if not soluciones:
                        label_resultado.config(text="No hay solución posible")
                        return
                    
                    theta1, theta2, theta3 = soluciones[0]

                    t1_deg = np.degrees(theta1)
                    t2_deg = np.degrees(theta2)
                    t3_deg = np.degrees(theta3)

                    print(f"Valores de la quinta solución: theta1:{t1_deg},theta2:{t2_deg},theta3:{t3_deg}")

                    if(t1_deg > 90 or t2_deg > 90 or t3_deg > 90 or t1_deg < -90 or t2_deg < -90 or t3_deg < -90 ):
                        theta1, theta2, theta3 = soluciones[1]
                        t1_deg = np.degrees(theta1)
                        t2_deg = np.degrees(theta2)
                        t3_deg = np.degrees(theta3)

                        print(f"Valores de la sexta solución: theta1:{t1_deg},theta2:{t2_deg},theta3:{t3_deg}")

                        if(t1_deg > 90 or t2_deg > 90 or t3_deg > 90 or t1_deg < -90 or t2_deg < -90 or t3_deg < -90 ):
                            print("Cambiando el signo de phi")
                            phi = -phi
                            print(f"phi = {np.degrees(phi)}")

                            soluciones = cinematica_inversa(pos_X, pos_Y, phi, L1, L2, L3)
                            if not soluciones:
                                label_resultado.config(text="No hay solución posible")
                                return
                            theta1, theta2, theta3 = soluciones[0]

                            t1_deg = np.degrees(theta1)
                            t2_deg = np.degrees(theta2)
                            t3_deg = np.degrees(theta3)

                            print(f"Valores de la septima solución: theta1:{t1_deg},theta2:{t2_deg},theta3:{t3_deg}")

                            if(t1_deg > 90 or t2_deg > 90 or t3_deg > 90 or t1_deg < -90 or t2_deg < -90 or t3_deg < -90 ):
                                theta1, theta2, theta3 = soluciones[1]
                                t1_deg = np.degrees(theta1)
                                t2_deg = np.degrees(theta2)
                                t3_deg = np.degrees(theta3)

                                print(f"Valores de la octava solución: theta1:{t1_deg},theta2:{t2_deg},theta3:{t3_deg}")
                                if(t1_deg > 90 or t2_deg > 90 or t3_deg > 90 or t1_deg < -90 or t2_deg < -90 or t3_deg < -90 ):
                                    label_resultado.config(text="No hay solución posible")
                                    return

    # Tomamos la primera solución
    theta1, theta2, theta3 = soluciones[0]

    entry_theta1.delete(0, tk.END)
    entry_theta2.delete(0, tk.END)
    entry_theta3.delete(0, tk.END)
    entry_theta1.insert(0, f"{t1_deg:.2f}")
    entry_theta2.insert(0, f"{t2_deg:.2f}")
    entry_theta3.insert(0, f"{t3_deg:.2f}")

    puntos = cinematica_directa(t1_deg, t2_deg, t3_deg)
    x_vals, y_vals = zip(*puntos)

    ax1.clear()
    semicircle_outer = Wedge(center=(0, 0), r=rmax, theta1=-90, theta2=90, color="#a2d7ff", alpha=0.5, zorder=0)
    semicircle_inner = Wedge(center=(0, 0), r=rmin, theta1=-90, theta2=90, color='white', zorder=1)
    ax1.add_artist(semicircle_inner)
    ax1.add_artist(semicircle_outer)    
    ax1.plot(x_vals, y_vals, 'o-', linewidth=4, color="#2683c6")
    ax1.set_xlim(-70, 70)
    ax1.set_ylim(-70, 70)
    ax1.set_title("Brazo SCARA - rotacional", fontsize=13, color="#075985")
    ax1.set_aspect('equal')
    ax1.grid()
    canvas1.draw()

    ax2.clear()
    ax2.set_xlim(0, 4)
    ax2.set_ylim(0, 80)
    ax2.set_title("Brazo SCARA - traslacional", fontsize=13, color="#075985")
    ax2.set_aspect('auto')
    ax2.add_patch(plt.Rectangle((1.5, 0), 1, 70, edgecolor='#222', facecolor='#e0e7ef'))
    ax2.add_patch(plt.Rectangle((1.5, pos_Z), 1, 1, edgecolor='#222', facecolor='#2683c6'))
    ax2.text(2, pos_Z + 1.2, f"{pos_Z:.1f} cm", ha='center', fontsize=12, color='#075985')
    canvas2.draw()

    label_resultado.config(text=f"Ángulos: θ1={t1_deg:.2f}°, θ2={t2_deg:.2f}°, θ3={t3_deg:.2f}°")

def cinematica_inversa(x, y, phi, L1, L2, L3):
    
    x_prime = x - L3 * np.cos(phi)
    y_prime = y - L3 * np.sin(phi)
    r = np.hypot(x_prime, y_prime)

    #ley de cosenos
    cos_theta2 = (r**2 - L1**2 - L2**2) / (2 * L1 * L2)
    if abs(cos_theta2) > 1:
        return None

    theta2_options = [np.arccos(cos_theta2), -np.arccos(cos_theta2)]  # Codo arriba/abajo
    soluciones = []
    for theta2 in theta2_options:
        alpha = np.arctan2(y_prime, x_prime)
        beta = np.arccos((L1**2 + r**2 - L2**2) / (2 * L1 * r))
        # La elección de suma/resta depende del signo de theta2
        if theta2 >= 0:
            theta1 = alpha - beta
        else:
            theta1 = alpha + beta
        theta3 = phi - theta1 - theta2
        soluciones.append((theta1, theta2, theta3))
    return soluciones
    
def cinematica_directa(theta1_deg, theta2_deg, theta3_deg):
    global pos_X, pos_Y
    theta1 = np.radians(theta1_deg)
    theta2 = np.radians(theta2_deg)
    theta3 = np.radians(theta3_deg)

    x1 = L1 * np.cos(theta1)
    y1 = L1 * np.sin(theta1)
    x2 = x1 + L2 * np.cos(theta1 + theta2)
    y2 = y1 + L2 * np.sin(theta1 + theta2)
    x3 = x2 + L3 * np.cos(theta1 + theta2 + theta3)
    y3 = y2 + L3 * np.sin(theta1 + theta2 + theta3)
    pos_X = x3
    pos_Y = y3
    return [(0, 0), (x1, y1), (x2, y2), (x3, y3)]

def guardar_accion():
    global accion, pos_X, pos_Y, pos_Z
    accion += 1
    registro_acciones[accion] = {
        'numero_accion': accion,
        'movimientoX': pos_X,
        'movimientoY': pos_Y,
        'movimientoZ': pos_Z,
        'electroiman': estado_electroiman
    }
    actualizar_historial()

def borrar_accion():
    global accion
    if registro_acciones:
        registro_acciones.popitem()
        accion -= 1
        if accion < 0:
            accion = 0
        actualizar_historial()

def borrar_todo():
    global accion
    registro_acciones.clear()
    accion = 0
    label_resultado.config(text="Posición X: -- | Y: -- | Z: --")
    actualizar_historial()

def actualizar_historial():
    listbox_historial.delete(0, tk.END)
    for numero, datos in registro_acciones.items():
        texto = f"Acción {numero}: X={datos['movimientoX']:.2f},Y={datos['movimientoY']:.2f}, Z={datos['movimientoZ']:.2f}, Electroiman = {datos['electroiman']}"
        listbox_historial.insert(tk.END, texto)

def reproducir_secuencia():
    if(registro_acciones):
        print("Reproduciendo secuencia")

    else:
        print("No hay acciones registradas para reproducir")
        return

def homing():
    print("Moviendo a home")
    #poner algún tipo de espera

def pausa():
    print("Pausa")

def paro_emergencia():
    print("PARO DE EMERGENCIA ACCIONADO")

# --------- Interfaz gráfica ---------
ventana = tk.Tk()
ventana.title("Robot SCARA - Cinemática Directa")
ventana.resizable(False, False)
ventana.configure(bg="#DCDAD5")

bigfont = ("Segoe UI", 13)
titlefont = ("Segoe UI", 20, "bold")

style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', font=bigfont, background="#DCDAD5")
style.configure('TButton', font=bigfont, background="#2683c6", foreground="white")
style.configure('EButton.TButton', font=bigfont, background="#c62626", foreground="white")
style.map('TButton', background=[('active', '#176fa2')])
style.map('EButton.TButton', background=[('active', "#a11f1f")])

# Título
label_titulo = ttk.Label(ventana, text="Robot SCARA", font=titlefont, foreground="#075985")
label_titulo.grid(row=0, column=1, columnspan=1, pady=(12,10))

# FRAME IZQUIERDO
frame_izq = ttk.Frame(ventana, padding=10, style='TFrame')
frame_izq.grid(row=1, column=0, sticky="n")
frame_izq.grid_rowconfigure(1, minsize=50) #Pequeño espacio al inicio 

ttk.Label(frame_izq, text="Ángulo θ1 (°):").grid(column=0, row=3, sticky="w", pady=2)
entry_theta1 = ttk.Entry(frame_izq, width=12, font=bigfont)
entry_theta1.grid(column=1, row=3, pady=2)

ttk.Label(frame_izq, text="Ángulo θ2 (°):").grid(column=0, row=4, sticky="w", pady=2)
entry_theta2 = ttk.Entry(frame_izq, width=12, font=bigfont)
entry_theta2.grid(column=1, row=4, pady=2)

ttk.Label(frame_izq, text="Ángulo θ3 (°):").grid(column=0, row=5, sticky="w", pady=2)
entry_theta3 = ttk.Entry(frame_izq, width=12, font=bigfont)
entry_theta3.grid(column=1, row=5, pady=2)

ttk.Label(frame_izq, text="Posición en Z").grid(column=0, row=6, sticky="w", pady=2)
entry_z = ttk.Entry(frame_izq, width=12, font=bigfont)
entry_z.grid(column=1, row=6, pady=2)

ttk.Label(frame_izq, text="Posición en X").grid(column=0, row=7, sticky="w", pady=2)
entry_x = ttk.Entry(frame_izq, width=12, font=bigfont)
entry_x.grid(column=1, row=7, pady=2)

ttk.Label(frame_izq, text="Posición en Y").grid(column=0, row=8, sticky="w", pady=2)
entry_y = ttk.Entry(frame_izq, width=12, font=bigfont)
entry_y.grid(column=1, row=8, pady=2)

# SELECCIÓN DEL MODO DE INGRESO DE DATOS
modo_cinematica = tk.StringVar(value="directa")
rb_directa = ttk.Radiobutton(frame_izq, text="Cinemática directa", variable=modo_cinematica, value="directa", command=cambiar_modo_cinematica)
rb_inversa = ttk.Radiobutton(frame_izq, text="Cinemática inversa", variable=modo_cinematica, value="inversa", command=cambiar_modo_cinematica)
rb_directa.grid(row=9, column=0)
rb_inversa.grid(row=9, column=1)

boton_actualizar = ttk.Button(frame_izq, text="Calcular y Dibujar", command=entrada_cinematica_directa)
boton_actualizar.grid(column=0, row=10, columnspan=2, pady=10)

label_resultado = ttk.Label(frame_izq, text="Posición X: -- | Y: -- | Z: --", font=("Segoe UI", 12, "bold"))
label_resultado.grid(column=0, row=11, columnspan=2, pady=(10, 8))

frame_izq.grid_rowconfigure(12, minsize=20) 

boton_registro = ttk.Button(frame_izq, text="Registrar acción", command=guardar_accion)
boton_registro.grid(column=0, row=13, pady=8)

boton_borrar = ttk.Button(frame_izq, text="Borrar última acción", command=borrar_accion)
boton_borrar.grid(column=1, row=13, columnspan=2, pady=8)

boton_borrar_todo = ttk.Button(frame_izq, text="Borrar todo", command=borrar_todo)
boton_borrar_todo.grid(column=0, row=14, columnspan=2, pady=8)

#ACTIVAR/DESACTIVAR ELECTROIMÁN
modo_electroiman = tk.StringVar(value="desactivado")
rb_activado = ttk.Radiobutton(frame_izq, text="Electroimán activado", variable=modo_electroiman, value="activado", command=cambiar_modo_electroiman)
rb_desactivado = ttk.Radiobutton(frame_izq, text="Electroimán desactivado", variable=modo_electroiman, value="desactivado", command=cambiar_modo_electroiman)
rb_activado.grid(row=15, column=0)
rb_desactivado.grid(row=15, column=1)

frame_izq.grid_rowconfigure(16, minsize=20) 

boton_reproducir = ttk.Button(frame_izq, text="Reproducir secuencia", command=reproducir_secuencia)
boton_reproducir.grid(column=0, row=17)

boton_pausa = ttk.Button(frame_izq, text="Pausa", command=pausa)
boton_pausa.grid(column=1, row=17)

boton_home = ttk.Button(frame_izq, text="Home", command=homing)
boton_home.grid(column=0, row=18, columnspan=2, pady=8)

frame_izq.grid_rowconfigure(19, minsize=100) 

boton_paro = ttk.Button(frame_izq, text="PARO", style='EButton.TButton',command=paro_emergencia)
boton_paro.grid(column=0, row=20, pady=8)

# FRAME DERECHO: Historial
frame_der = ttk.Frame(ventana, padding=10, style='TFrame')
frame_der.grid(row=1, column=2, sticky="n")

# --- Historial (Listbox)
ttk.Label(frame_der, text="Historial de acciones:").grid(column=3, row=1, columnspan=2, pady=(10,0))
listbox_historial = tk.Listbox(frame_der, width=54, height=38, font=("Consolas", 11), bg="#ffffff", bd=0, highlightthickness=0, fg="#176fa2")
listbox_historial.grid(column=3, row=2, columnspan=2, pady=(0,10))

# FRAME MEDIO: Gráficas
frame_med = ttk.Frame(ventana, padding=10, style='TFrame')
frame_med.grid(row=1, column=1, sticky="n")

fig1, ax1 = plt.subplots(figsize=(4, 4))
fig1.patch.set_facecolor('#DCDAD5')
canvas1 = FigureCanvasTkAgg(fig1, master=frame_med)
canvas1.get_tk_widget().grid(row=0, column=0, padx=5, pady=5)

fig2, ax2 = plt.subplots(figsize=(4, 4))
fig2.patch.set_facecolor('#DCDAD5')
canvas2 = FigureCanvasTkAgg(fig2, master=frame_med)
canvas2.get_tk_widget().grid(row=1, column=0, padx=5, pady=5)

# Inicializa la interfaz en un estado predeterminado
actualizar_historial()
entrada_cinematica_directa()
cambiar_modo_cinematica()
cambiar_modo_electroiman()

ventana.mainloop()
