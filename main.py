from tkinter import *
import tkinter.ttk as ttk
from funciones import*
import openpyxl
import os
import datetime

contador = 0

def grabar():
    """Esta funcion recoge la informacion del asiento"""

    data_operacion=operacion.get()
    data_fecha = fecha.get()
    data_proveedor=prov.get()
    data_n_fra=n_fra.get()
    try:
        if len(data_fecha) == 8:
            data_fecha = f'{data_fecha[:2]}/{data_fecha[2:4]}/{data_fecha[4:]}'
        data_total_fra = float(total_fra.get())
        data_tipo_iva = float(tipo_iva.get())
        
        # Validar y formatear la fecha
        fecha_formateada = datetime.datetime.strptime(data_fecha, "%d/%m/%Y").strftime("%d/%m/%Y")
    
    except ValueError as e:
        print(f"Error: {e}")
        return
    data_base_imponible = base_imponible(data_total_fra, data_tipo_iva)
    data_iva = iva(data_total_fra, data_tipo_iva)
    print(data_operacion)
    print(data_fecha)
    print(data_proveedor)
    print(data_n_fra)
    print(data_total_fra)

    #Creamos el directorio de excell y la cabecera
    filepath = r"C:\Users\ionac\python course\contabilidad\ data.xlsx"
    
    if not os.path.exists(filepath):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        heading = ["Operación", "Fecha", "Proveedor", "Nº Factura", "Base imponible", 
                    "Tipo IVA", "IVA", "Total Factura"]
        sheet.append(heading)
        workbook.save(filepath)
    workbook = openpyxl.load_workbook(filepath)
    sheet=workbook.active
    sheet.append([data_operacion, fecha_formateada, data_proveedor, data_n_fra, data_base_imponible,
                  data_tipo_iva, data_iva, data_total_fra])
    workbook.save(filepath)

    #Visualizamos el asiento grabado
    contador = contar_pulsos()
    my_tree.insert(parent="", index="end", iid=contador, text="", values=(contador, data_fecha, data_proveedor, data_n_fra, data_base_imponible, data_tipo_iva, data_iva, data_total_fra))
    
    #Limpiamos los campos de entrada
    operacion.set("Ingresos")
    fecha.set("")
    prov.set("")
    n_fra.set("")
    total_fra.set(0.0)
    tipo_iva.set(0.0)



root = Tk()
root.title("Programa de contabilidad")

#Marco principal
mainframe = ttk.Frame(root, padding="5 5 5 5")
mainframe.grid(column=0, row=0, sticky=(W, N, E, S))

#
#Marco donde mostrar los asientos contabilizados
#
showframe = ttk.Frame(mainframe)
showframe.grid(column=1, row=1, sticky=(W, N, E, S), pady="5 0")

#Tabla donde se muestran los asientos contabilizados
my_tree = ttk.Treeview(mainframe)

#Definimos las columnas
my_tree["columns"] = ("ASIENTO", "FECHA", "PROVEEDOR", "Nº FACTURA","BASE IMPONIBLE", "TIPO IVA", "IVA", "TOTAL" )
my_tree.grid(column=1, row=1, sticky=(W, N, E, S), pady="5 0")

#Formato columnas
my_tree.column("#0", width=0, minwidth=25)
my_tree.column("ASIENTO", anchor=CENTER, width=120, minwidth=25)
my_tree.column("FECHA", anchor=CENTER, width=120, minwidth=25)
my_tree.column("PROVEEDOR", anchor=W, width=120, minwidth=25)
my_tree.column("Nº FACTURA", anchor=E, width=120, minwidth=25)
my_tree.column("BASE IMPONIBLE", anchor=E, width=120, minwidth=25)
my_tree.column("TIPO IVA", anchor=CENTER, width=120, minwidth=25)
my_tree.column("IVA", anchor=E, width=120, minwidth=25)
my_tree.column("TOTAL", anchor=E, width=120, minwidth=25)

#Cabecera de las columnas
my_tree.heading("#0")
my_tree.heading("ASIENTO", text="ASIENTO", anchor= CENTER)
my_tree.heading("FECHA", text="FECHA", anchor= CENTER)
my_tree.heading("PROVEEDOR", text="PROVEEDOR", anchor= CENTER)
my_tree.heading("Nº FACTURA", text="Nº FACTURA", anchor= CENTER)
my_tree.heading("BASE IMPONIBLE", text="BASE IMPONIBLE", anchor= CENTER)
my_tree.heading("TIPO IVA", text="TIPO IVA", anchor= CENTER)
my_tree.heading("IVA", text="IVA", anchor= CENTER)
my_tree.heading("TOTAL", text="TOTAL", anchor= CENTER)

#Prueba de formato de datos
#my_tree.insert(parent="", index="end", iid=0, text="", values=("001", "15/02/2024", "Armarios Perez", "2024000028", 1000, "21%", 210, 1210))
#my_tree.insert(parent="", index="end", iid=1, text="", values=("002", "01/10/2024", "Maderas Romero", "16987", 100, "21%", 21, 121))
#my_tree.insert(parent="", index="end", iid=2, text="", values=("003", "23/02/2024", "Pomos Pomodoro", "FR000234", 60, "21%", 60*0.21, 72.60))

#
#Marco donde se contabiliza
#
ROW_CONTAFRAME = 8

contaframe = ttk.Frame(mainframe)
contaframe.grid(column=1, row=ROW_CONTAFRAME, sticky=(W, N, E, S), pady="5 0")

#Etiqueta
ttk.Label(contaframe, text="Operación").grid(column=1, row=ROW_CONTAFRAME)
ttk.Label(contaframe, text="Fecha").grid(column=2, row=ROW_CONTAFRAME)
ttk.Label(contaframe, text="Proveedor").grid(column=3, row=ROW_CONTAFRAME)
ttk.Label(contaframe, text="Nº factura").grid(column=4, row=ROW_CONTAFRAME)
ttk.Label(contaframe, text="Total factura").grid(column=5, row=ROW_CONTAFRAME)
ttk.Label(contaframe, text="Tipo IVA").grid(column=6, row=ROW_CONTAFRAME)

#Campo de entrada
operacion=StringVar(value="Ingresos")
fecha=StringVar()#Declaramos variable tipo string
prov=StringVar()
n_fra=StringVar()
total_fra=DoubleVar()#Declaramos variable tipo float
tipo_iva = DoubleVar()
entry_operacion = ttk.Combobox(contaframe, textvariable=operacion, values =["Ingresos", "Gastos"]).grid(column=1, row=ROW_CONTAFRAME+1)
entry_fecha = ttk.Entry(contaframe, textvariable=fecha, justify=CENTER).grid(column=2, row=ROW_CONTAFRAME+1)
entry_prov = ttk.Entry(contaframe, textvariable=prov).grid(column=3, row=ROW_CONTAFRAME+1)
entry_n_fra = ttk.Entry(contaframe, textvariable=n_fra).grid(column=4, row=ROW_CONTAFRAME+1)
entry_total_fra = ttk.Entry(contaframe, textvariable=total_fra, justify=RIGHT).grid(column=5, row=ROW_CONTAFRAME+1)
entry_tipo_iva = ttk.Entry(contaframe, textvariable=tipo_iva, justify=RIGHT).grid(column=6, row=ROW_CONTAFRAME+1)

#Botón grabar
button = ttk.Button(contaframe, text= "Grabar", command=grabar)
button.grid(row=ROW_CONTAFRAME+1, column= 10)

#Añade distancia entre todos los titulos y widgets que hay en el frame contaframe.
for widget in contaframe.winfo_children():
    widget.grid_configure(padx=5, pady=0)






root.mainloop() #Se lanza la interfaz