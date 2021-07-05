"""
Created on Tue Mar  9 13:41:32 2021

@author: adrian
"""
import sys
from datetime import datetime
import documento
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi

informe=None #Iniciamos la variable que hará referencia al documento.
id_caso=None #Variable que ocntiene el ID del caso


def ventana_emergente(texto):
    #Metodo para crear ventana emergente. Se usa para errores y avisos
    mensaje = QMessageBox()
    mensaje.setText(texto)
    mensaje.exec()
    
          
class v_inicial(QMainWindow):
    #Clase de la ventana inicial
       
    def __init__(self):
        #inicializamos la ventana y cargamos el archivo que contiene los widgets
        super(v_inicial, self).__init__()
        loadUi('v_inicio.ui', self)
        self.bt_empezar.clicked.connect(self.escribir)#controlamos el  click del botón        
        
    def escribir(self):
        global id_caso #Con esto podremos modificar la variable global id_caso
        id_caso=self.tb_idCaso.text()#asignamos el valor de ID caso
        
        #creamos el documento
        try:
            informe= documento.crearDocumento(id_caso)
            if informe==-1:
                ventana_emergente("El ID del caso ya existe. Puedes modificarlo desde el archivo original.")
                sys.exit(app.exec())
        except Exception as e:
            ventana_emergente("Error al crear el documento. Código de Error: {}".format(e))
            sys.exit(app.exec())
            
        #Escribimos el nombre del analista   y la fecha del análisis         
        try:
            documento.escribirDocumento(informe, id_caso, "Nombre del Analista", self.tb_nombre.text())
            documento.escribirDocumento(informe, id_caso, "Fecha y hora del Análisis", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        except Exception as e:
            ventana_emergente("Error al escribir en el documento. Código de Error: {}".format(e))  
            
        #Abrimos la siguiente ventana
        self.hide()
        nuevaVentana=v1_AdmisionPruebas(self)
        nuevaVentana.show()

        
class v1_AdmisionPruebas(QMainWindow):
    #Clase Ventana Admision de pruebas (2ª ventana)
    global id_caso #Con esto podremos acceder al valor de la variable global id_caso
    
    def __init__(self, parent=None):
        #Mopstramos la ventana. Como es secundaria, necesitamos el parent.
        super(v1_AdmisionPruebas, self).__init__(parent)
        loadUi('v1_AdmisionPruebas.ui', self)
        self.bt_siguiente.clicked.connect(self.escribir) #Controlamos el click del boton
    
    def escribir (self):
        #Escribimos los resultados de cada una de las Text Box               
        try:                
            documento.escribirDocumento(informe, id_caso, "Nobre del acusado", self.tb_nombreAcusado.text())
            documento.escribirDocumento(informe, id_caso, "NIF del acusado", self.tb_nif.text())
            documento.escribirDocumento(informe, id_caso, "Ubicación", self.tb_ubicacion.text())
            documento.escribirDocumento(informe, id_caso, "Descripción del delito", self.tb_delito.toPlainText())
            documento.escribirDocumento(informe, id_caso, "Tipo de delito", self.tb_tipoIncidente.text())
            documento.escribirDocumento(informe, id_caso, "Tipo de dato/os a buscar", self.tb_tipoDatos.text())
        except Exception as e:
            ventana_emergente("Error al escribir en el documento. Código de Error: {}".format(e))
            print(e)
        
        #Abrimos la siguiente ventana
        self.hide()
        siguienteVentana=v2_Aviso(self)
        siguienteVentana.show()


class v2_Aviso(QMainWindow):
    def __init__(self, parent=None):
        #Mopstramos la ventana. Como es secundaria, necesitamos el parent.
        super(v2_Aviso, self).__init__(parent)
        loadUi('v2_Aviso.ui', self)
        self.bt_siguiente.clicked.connect(self.cambiarVentana) #Controlamos el click del boton
        
    def cambiarVentana(self):
        #Abrimos la siguiente ventana
        self.hide()
        siguienteVentana=v3_Identificacion(self)
        siguienteVentana.show()

        
class v3_Identificacion(QMainWindow):
    #Clase Ventana Identificacion (3ª ventana)
    global id_caso #Con esto podremos acceder al valor de la variable global id_caso
    
    def __init__(self, parent=None):
        #Mopstramos la ventana. Como es secundaria, necesitamos el parent.
        super(v3_Identificacion, self).__init__(parent)
        loadUi('v3_Identificacion.ui', self)
        self.bt_siguiente.clicked.connect(self.escribir) #Controlamos el click del boton
        
    def escribir (self):  
        #Solo se puede escribir si hemos analizado el dispositivo para toma huellas u otras evidencias
        if self.cb_analizado.isChecked():
            #Escribimos los datos necesarios
            documento.escribirDocumento(informe, id_caso, "Dispositivo incluido en la orden de registro", self.cb_registro.isChecked())
            documento.escribirDocumento(informe, id_caso, "El propietario ha dado su consentimiento para la extracción del dispositivo", self.cb_consentimiento.isChecked())
            documento.escribirDocumento(informe, id_caso, "Los datos que se requieren adquirir se especifican en la orden de registro",self.cb_datos.isChecked())
            if self.cb_persona.isChecked():
                documento.escribirDocumento(informe, id_caso, "Rol del propietario del dispositivo", "Dispositivo personal")
            elif self.cb_empleado.isChecked():
                documento.escribirDocumento(informe, id_caso, "Rol del propietario del dispositivo", "Dispositivo de una empresa")
            else:
                documento.escribirDocumento(informe, id_caso, "Rol del propietario del dispositivo", "Dispositivo personal")
            documento.escribirDocumento(informe, id_caso, "La politica corporativa permite la recopilación de datos y el posterior análisis", self.cb_permiso.isChecked())
            documento.escribirDocumento(informe, id_caso, "Lista de datos a recoger", self.tb_listaDatos.toPlainText())
            documento.escribirDocumento(informe, id_caso, "Marca del dispositivo", self.tb_marca.text())
            documento.escribirDocumento(informe, id_caso, "Modelo del dispositivo", self.tb_modelo.text())
            documento.escribirDocumento(informe, id_caso, "Número de serie del dispositivo", self.tb_numeroSerie.text())
            documento.escribirDocumento(informe, id_caso, "Color del dispositivo", self.tb_color.text())
            if self.cb_bloqueado.isChecked():
                documento.escribirDocumento(informe, id_caso, "Pantalla del dispositivo", "Bloqueada")
            else:
                documento.escribirDocumento(informe, id_caso, "Pantalla del dispositivo", "Desbloqueada")
            documento.escribirDocumento(informe, id_caso, "Hardware del dispositivo", self.tb_hardware.text())
            documento.escribirDocumento(informe, id_caso, "Estado del dispositivo", self.tb_estado.text())
            
            if self.cb_tarjetaSi.isChecked():
                documento.escribirDocumento(informe, id_caso, "Tarjetas de memoria del dispositivo", "El dispositivo contenía una trarjeta de memoria")
            elif self.cb_tarjetaNo.isChecked():
                documento.escribirDocumento(informe, id_caso, "Tarjetas de memoria del dispositivo", "El dispositivo NO contenía trarjeta de memoria")
                
            #Cambiamos a la siguiente ventana una vez se escriban todos los datos
            self.cambiarVentana()
            
        else:
            ventana_emergente("El dispositivo debe ser analizado previamente debido a que puede ser fuente de otras evidencias.\nCuando sea analizado, marque la opcion de la pestaña 'Otras Fuentes'")
            self.hide()
            ventanaActual=v3_Identificacion(self)
            ventanaActual.show()
       
    def cambiarVentana(self):
        #Abrimos la siguiente ventana
        self.hide()
        siguienteVentana=v4_Preparacion(self)
        siguienteVentana.show()
        

class v4_Preparacion(QMainWindow):
    def __init__(self, parent=None):
        #Mopstramos la ventana. Como es secundaria, necesitamos el parent.
        super(v4_Preparacion, self).__init__(parent)
        loadUi('v4_Preparacion.ui', self)
        self.bt_siguiente.clicked.connect(self.cambiarVentana) #Controlamos el click del boton
    def cambiarVentana(self):
        #Abrimos la siguiente ventana
        self.hide()
        siguienteVentana=v5_Aislamiento(self)
        siguienteVentana.show()
            

class v5_Aislamiento(QMainWindow):
    def __init__(self, parent=None):
        #Mopstramos la ventana. Como es secundaria, necesitamos el parent.
        super(v5_Aislamiento, self).__init__(parent)
        loadUi('v5_Aislamiento.ui', self)
        self.bt_siguiente.clicked.connect(self.cambiarVentana) #Controlamos el click del boton
    
    def cambiarVentana(self):
        #Abrimos la siguiente ventana
        self.hide()
        siguienteVentana=v6_Procesamiento(self)
        siguienteVentana.show()
    

class v6_Procesamiento(QMainWindow):
    def __init__(self, parent=None):
        #Mopstramos la ventana. Como es secundaria, necesitamos el parent.
        super(v6_Procesamiento, self).__init__(parent)
        loadUi('v6_Procesamiento.ui', self)
        self.bt_siguiente.clicked.connect(self.cambiarVentana) #Controlamos el click del boton
    
    def cambiarVentana(self):
        #Abrimos la siguiente ventana
        self.hide()
        siguienteVentana=v7_Proces_Paso0(self)
        siguienteVentana.show()
    

class v7_Proces_Paso0(QMainWindow):
    def __init__(self, parent=None):
        #Mopstramos la ventana. Como es secundaria, necesitamos el parent.
        super(v7_Proces_Paso0, self).__init__(parent)
        loadUi('v7_Proces_Paso0.ui', self)
        self.bt_siguiente.clicked.connect(self.cambiarVentana) #Controlamos el click del boton    
    
    def cambiarVentana(self):
        #Abrimos la siguiente ventana
        self.hide()
        siguienteVentana=v7_Proces_Paso1(self)
        siguienteVentana.show()
        

class v7_Proces_Paso1(QMainWindow):
    def __init__(self, parent=None):
        #Mopstramos la ventana. Como es secundaria, necesitamos el parent.
        super(v7_Proces_Paso1, self).__init__(parent)
        loadUi('v7_Proces_Paso1.ui', self)
        self.bt_siguiente.clicked.connect(self.cambiarVentanaAlante) #Controlamos el click del boton   
        self.bt_atras.clicked.connect(self.cambiarVentanaAtras) #Controlamos el click del boton 
    
    def cambiarVentanaAlante(self):
        #Abrimos la siguiente ventana
        self.hide()
        siguienteVentana=v7_Proces_Paso2(self)
        siguienteVentana.show()
    
    def cambiarVentanaAtras(self):
        #Abrimos la siguiente ventana
        self.hide()
        siguienteVentana=v7_Proces_Paso0(self)
        siguienteVentana.show()


class v7_Proces_Paso2(QMainWindow):
    def __init__(self, parent=None):
        #Mopstramos la ventana. Como es secundaria, necesitamos el parent.
        super(v7_Proces_Paso2, self).__init__(parent)
        loadUi('v7_Proces_Paso2.ui', self)
        self.bt_siguiente.clicked.connect(self.cambiarVentanaAlante) #Controlamos el click del boton   
        self.bt_atras.clicked.connect(self.cambiarVentanaAtras) #Controlamos el click del boton 
    
    def cambiarVentanaAlante(self):
        #Abrimos la siguiente ventana
        self.hide()
        siguienteVentana=v7_Proces_Paso3(self)
        siguienteVentana.show()
    
    def cambiarVentanaAtras(self):
        #Abrimos la siguiente ventana
        self.hide()
        siguienteVentana=v7_Proces_Paso1(self)
        siguienteVentana.show()


class v7_Proces_Paso3(QMainWindow):
    def __init__(self, parent=None):
        #Mopstramos la ventana. Como es secundaria, necesitamos el parent.
        super(v7_Proces_Paso3, self).__init__(parent)
        loadUi('v7_Proces_Paso3.ui', self)
        self.bt_siguiente.clicked.connect(self.cambiarVentanaAlante) #Controlamos el click del boton   
        self.bt_atras.clicked.connect(self.cambiarVentanaAtras) #Controlamos el click del boton 
    
    def cambiarVentanaAlante(self):
        #Abrimos la siguiente ventana
        self.hide()
        siguienteVentana=v7_Proces_Paso4(self)
        siguienteVentana.show()
    
    def cambiarVentanaAtras(self):
        #Abrimos la siguiente ventana
        self.hide()
        siguienteVentana=v7_Proces_Paso2(self)
        siguienteVentana.show()
        

class v7_Proces_Paso4(QMainWindow):
    def __init__(self, parent=None):
        #Mopstramos la ventana. Como es secundaria, necesitamos el parent.
        super(v7_Proces_Paso4, self).__init__(parent)
        loadUi('v7_Proces_Paso4.ui', self)
        self.bt_siguiente.clicked.connect(self.cambiarVentanaAlante) #Controlamos el click del boton   
        self.bt_atras.clicked.connect(self.cambiarVentanaAtras) #Controlamos el click del boton 
    
    def cambiarVentanaAlante(self):
        #Abrimos la siguiente ventana
        self.hide()
        siguienteVentana=v7_Proces_Paso5(self)
        siguienteVentana.show()
    
    def cambiarVentanaAtras(self):
        #Abrimos la siguiente ventana
        self.hide()
        siguienteVentana=v7_Proces_Paso3(self)
        siguienteVentana.show()


class v7_Proces_Paso5(QMainWindow):
    def __init__(self, parent=None):
        #Mopstramos la ventana. Como es secundaria, necesitamos el parent.
        super(v7_Proces_Paso5, self).__init__(parent)
        loadUi('v7_Proces_Paso5.ui', self)
        self.bt_siguiente.clicked.connect(self.cambiarVentanaAlante) #Controlamos el click del boton   
        self.bt_atras.clicked.connect(self.cambiarVentanaAtras) #Controlamos el click del boton 
    
    def cambiarVentanaAlante(self):
        #Abrimos la siguiente ventana
        self.hide()
        siguienteVentana=v7_Proces_Paso6(self)
        siguienteVentana.show()
    
    def cambiarVentanaAtras(self):
        #Abrimos la siguiente ventana
        self.hide()
        siguienteVentana=v7_Proces_Paso4(self)
        siguienteVentana.show()


class v7_Proces_Paso6(QMainWindow):
    def __init__(self, parent=None):
        #Mopstramos la ventana. Como es secundaria, necesitamos el parent.
        super(v7_Proces_Paso6, self).__init__(parent)
        loadUi('v7_Proces_Paso6.ui', self)
        self.bt_salir.clicked.connect(self.cerrarPrograma) #Controlamos el click del boton   
    
    def cerrarPrograma(self):
        #Abrimos la siguiente ventana
        self.hide()
        sys.exit(app.exec())
    



    
    

app = QApplication(sys.argv)
main = v_inicial()
main.show()
sys.exit(app.exec())