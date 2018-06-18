# --------------- LIBRERIAS -------------------------------------------------------------
import sys, re, paramiko, logging, os, socket
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5 import uic
from main import *
var1 = 0
var2 = False
hola = False
var = ""
ssh_ip_url =""
ssh_user = ""
#rsa = ""
#rsa_file = "Public_key-cert.pub"
#----------------------- INICIALIZACION -------------------------------------------------
class Dialog(QDialog):
    #f = open(rsa_file,'w')
    #f.close()
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("Login2.ui",self) #cargando archivo.ui
        self.IP_URL.textChanged.connect(self.validar_IP_URL) # llamada a validar IP_URL
        self.USER.textChanged.connect(self.validar_USER) #llamada a lavidar USER
        self.Login_Button.clicked.connect(self.Validar_Login) # llamada cuand se presiona Login
        self.Cancel_Button.clicked.connect(self.salir) # llamada cuando se presiona cancel
        #self.Pkey_Button.clicked.connect(self.Rsa_pkey)

#------------------------------ INICIALIZANDO COMUNICACION SSH ---------------------------------

    def ssh (Self, A,B,C):

        #f = os.stat(D).st_size
        #global hola
        #f = open(D,'r')
        #f .read() != ""

    #    try:
            #paramiko.util.log_to_file('ssh.log')
            #ssh_cliente = paramiko.SSHClient()
            #ssh_cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #ssh_cliente.connect(hostname = A, port = 22, username = B, password = C)
            #K = paramiko.RSAKey.from_private_key_file(filename = D, password = None)
            #f = open("Public_key.txt",'w')
            #K = str(K).encode("utf-8")
            #print(K)
            #f.close()
            #stdin, stdout, stderr = ssh_cliente.exec_command("python /home/kzin/python/Add_key/" + "Add_key.pyw " + K.exportKey() )
            #x = stderr.readlines()
            #print(x)
    #    except (paramiko.BadHostKeyException, paramiko.AuthenticationException, paramiko.SSHException,paramiko.ssh_exception.NoValidConnectionsError) as e:

            #return False
        #if (f != 0) and (E == False):
        #    try:

        #        K = paramiko.RSAKey.from_private_key_file(filename = D, password = None)
        #        paramiko.util.log_to_file('ssh.log')
        #        ssh_cliente = paramiko.SSHClient()
        #        ssh_cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #        ssh_cliente.connect(hostname = A, port = 22, username = B, pkey = K)
        #        ssh_cliente.close()

        #    except (paramiko.BadHostKeyException, paramiko.AuthenticationException, paramiko.SSHException,paramiko.ssh_exception.NoValidConnectionsError) as e:

        #        return False
        #if (f == 0 ) and (E == True):
        try:
            v = socket.gethostbyname(A)
            paramiko.util.log_to_file('ssh.log')
            ssh_cliente = paramiko.SSHClient()
            ssh_cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_cliente.connect(hostname = v, port = 22, username = B, password = C)
            ssh_cliente.close()


        except (paramiko.BadHostKeyException, paramiko.AuthenticationException, paramiko.SSHException,paramiko.ssh_exception.NoValidConnectionsError) as e:
            return False

    #------------------------------VALIDACION DE IP Y URL ------------------------------------------
    def validar_IP_URL(self):
        ip_url = self.IP_URL.text()
        validar = re.match("(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))",ip_url)
        validar2 = re.match("(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})",ip_url)
        if ip_url == "":
            self.IP_URL.setStyleSheet("no border")
            return False
        elif (not validar) and (not validar2):
            self.IP_URL.setStyleSheet("border: 1px solid red")
            return False
        else:
            self.IP_URL.setStyleSheet("border: 1px solid #00b300")
            return True
#------------------------------- VALIDACION DE USER -------------------------------------------------
    def validar_USER(self):
        user = self.USER.text()
        validar = re.match("^[a-z]+$",user,re.I)
        if user == "":
            self.USER.setStyleSheet("no border")
            return False
        elif not validar:
            self.USER.setStyleSheet("border: 1px solid red")
            return False
        else:
            self.USER.setStyleSheet("border: 1px solid #00b300")
            return True
#--------------------------- COMPROBAMNDO VALIDACIONES AL PRESIONAR LOGIN ---------------------------------
    def Validar_Login(self):
        global ssh_ip_url, ssh_user, var, var2
        if self.validar_IP_URL() and self.validar_USER():
            ssh_ip_url = self.IP_URL.text()
            ssh_user = self.USER.text()
            var = self.PASS.text()
            #var2 = self.check2()
            #ssh_pkey = self.PKEY.text()
            var1 = False
            var1 = self.ssh(ssh_ip_url,ssh_user,var)
            if var1 == False:
                QMessageBox.warning(self,"Error","Error de comunicación.",QMessageBox.Ok)
                self.clear()
            else:
                self.close()
        else:
            QMessageBox.warning(self,"Advertencia","Uno o varios de los campos son incorrectos.",QMessageBox.Ok)
#--------------------------------- GENERATE PKEY -------------------------------------------------------------
    #def Rsa_pkey(self):
    #    rsa =paramiko.RSAKey.generate(bits = 2048)
    #    rsa.write_private_key_file(rsa_file)
    #    QMessageBox.information(self,"Exito!","Su clave privada esta en la ruta por defecto " + rsa_file ,QMessageBox.Ok)


#---------------------------------- BOTON Exit ---------------------------------------------------------
    def salir(self):
        resultado = QMessageBox.question(self,"Salir..","¿Esta seguro que desea salir?",QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes:
            exit()
        else:
           pass

#------------------------------------- LIMPIAR VENTANDA --------------------------------------------------
    def clear(self):
        self.IP_URL.setText("")
        self.IP_URL.setStyleSheet("no border")
        self.IP_URL.setFocus()
        self.USER.setText("")
        self.USER.setStyleSheet("no border")
        self.PASS.setText("")
        #self.PKEY.setText("")
#------------------------- ESTADOS DE LOS  RADIO BUTTON ---------------------------------------------------

    #def check(self):
    #    if self.Pass_radioButton.isChecked():
    #        return self.PASS.text()

    #    if self.Pkey_radioButton.isChecked():
    #        return self.PKEY.text()


    #def check2(self):
    #    if self.Pass_radioButton.isChecked():
    #        return True
#
    #    if self.Pkey_radioButton.isChecked():
    #        return False

#------------------------------- LANZANDO APLICACION ------------------------------------------------------

def run(self):
    app = QApplication(sys.argv)
    dialogo = Dialog()
    dialogo.show()
    app.exec_()
    return ssh_ip_url, ssh_user, var, var2, True
