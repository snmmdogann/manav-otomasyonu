# -*- coding: utf-8 -*-
"""
Created on Thu May 30 11:28:43 2024

@author: pc
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 30 10:10:13 2024

@author: pc
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from widgets import Ui_MainWindow
from hakkinda_widgets import Hakkinda
from widgetsGiris import Ui_Giris
import sqlite3

#Program içindeki hakkında kısmını çalıştıracak kod

class Hakkinda_class(QtWidgets.QMainWindow,Hakkinda):
     def __init__(self):
         super(Hakkinda_class, self).__init__()
         self.setupUi(self)
         
#Giriş ekranına girmemizi sağlayacak olan kod

class Login(QtWidgets.QMainWindow,Ui_Giris):
    global keyf
    global kahya
    def __init__(self):
        super(Login,self).__init__()
        self.setupUi(self)
        self.btnlogin.clicked.connect(self.giris)#btn login tuşu giriş kısmına yönlendirecek kod
        
    def giris(self):
        _Lneusername = self.Lneusername.text()
        sifre = self.Lnepassword.text()
            
        if _Lneusername == "Sinem" and sifre =="1234":
            QtWidgets.QMessageBox.information(self,"Giriş","Giriş başarılı...")
            self.widgets = Ui_MainWindow()
            self.widgets.show()
            self.close()
        else:
                QtWidgets.QMessageBox().information(self,"Giriş","Kullanıcı adı veya şifre yanlış.")
                
#Ana program

class Ui_MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    global curs
    global conn
    
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.baglanti_olustur_meyve()
        self.baglanti_olustur_sebze()
        self.listele_meyve()
        self.listele_sebze()
        self.btnMeyveEkle.clicked.connect(self.MeyveEkle)
        self.btnSebzeEkle.clicked.connect(self.SebzeEkle)
        self.twmeyvelistesi.itemSelectionChanged.connect(self.doldur_meyve)
        self.twsebzelistesi.itemSelectionChanged.connect(self.doldur_sebze)
        self.btnGuncelle.clicked.connect(self.meyve_guncelle)
        self.btnSebzeGuncelle.clicked.connect(self.sebze_guncelle)
        self.btnMeyveSil.clicked.connect(self.meyve_sil)
        self.btnSebzesil.clicked.connect(self.sebze_sil)
        self.btnCikis.clicked.connect(self.cikis)
        self.btnMeyveAra.clicked.connect(self.meyve_ara)
        self.btnSebzeAra.clicked.connect(self.sebze_ara)
        self.menuYard_m.triggered.connect(self.hakkinda_pencereyi_ac)
        self.hakkinda_penceresi = Hakkinda_class()
        
# "Hakkında" penceresini gösteren kod
    def hakkinda_pencereyi_ac(self):
        self.hakkinda_penceresi.show()
#Bu fonksiyon, girilen adet ve fiyatın sadece sayılardan oluşup oluşmadığını kontrol eder. Eğer sayı değilse uyarı mesajı gösterir.
    def veri_giris_kontrol(self, adet, fiyat):
        if not adet.isdigit():
            QMessageBox.warning(self, "UYARI", "Adet yalnızca sayı içermelidir.")
            return False
        if not fiyat.isdigit():
            QMessageBox.warning(self, "UYARI", "Fiyat yalnızca sayı içermelidir.")
            return False
        return True
#Bu fonksiyon meyve eklerken kullanılır. Giriş kontrolü yapılır, veriler toplanır ve veritabanına eklenir. Başarı mesajı gösterilir veya hata oluşursa hata mesajı gösterilir.
    def MeyveEkle(self):
        _lneMeyveAdedi = self.lneMeyveAdedi.text()
        _lneMeyveFiyat = self.lneMeyveFiyat.text()

        if not self.veri_giris_kontrol(_lneMeyveAdedi, _lneMeyveFiyat):
            return

        _lwMeyveCinsi = self.lwMeyveCinsi.currentItem().text()
        _cmbMeyveMensei = self.cmbMeyveMensei.currentText()
        _spnMeyvesKilo = self.spnMeyvesKilo.value()

        try:
            self.meyve_cursor.execute("INSERT INTO meyve (MeyveCinsi, MeyveAdedi, Meyvekilo, MeyveMensei, MeyveFiyat) VALUES (?, ?, ?, ?, ?)", 
                                     (_lwMeyveCinsi,_lneMeyveAdedi,_spnMeyvesKilo,_cmbMeyveMensei,_lneMeyveFiyat))
            self.meyve_conn.commit()
            QMessageBox.information(self, "BİLGİ", "Kayıt başarıyla eklendi.")
            self.listele_meyve()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Hata", "Kayıt eklenirken hata: " + str(e))
            
            
#Bu fonksiyon sebze eklerken kullanılır. Giriş kontrolü yapılır, veriler toplanır ve veritabanına eklenir. Başarı mesajı gösterilir veya hata oluşursa hata mesajı gösterilir.
    def SebzeEkle(self):
        
        _lwSebzeCinsi = self.lwSebzeCinsi.currentItem().text()
        _spnSebzeKilo = self.spnSebzeKilo.value()
        
        _lneSebzeAdedi = self.lneSebzeAdedi.text()
        _cmbSebzeMensei = self.cmbSebzeMensei.currentText()
        _lneSebzeFiyat = self.lneSebzeFiyat.text()
        
        
        
        if not self.veri_giris_kontrol(_lneSebzeAdedi, _lneSebzeFiyat):
            return
        try:
            self.sebze_cursor.execute("INSERT INTO sebze (SebzeCinsi,SebzeAdedi,Sebzekilo,SebzeMensei,SebzeFiyat) VALUES (?, ?, ?, ?, ?)",
                                      (_lwSebzeCinsi,_lneSebzeAdedi,_spnSebzeKilo,_cmbSebzeMensei, _lneSebzeFiyat))
            self.sebze_conn.commit()
            QMessageBox.information(self, "BİLGİ", "Kayıt başarıyla eklendi.")
            self.listele_sebze()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Hata", "Kayıt eklenirken hata: " + str(e))
#Bu kod, bir SQLite veritabanı oluşturmayı ve meyve bilgilerini içeren bir tablo oluşturmayı amaçlar.  
    def baglanti_olustur_meyve(self):
        try:
            self.meyve_conn = sqlite3.connect("meyve_veritabani.db")
            self.meyve_cursor = self.meyve_conn.cursor()
            self.sorguCreTblmeyve = ("CREATE TABLE IF NOT EXISTS meyve ( \
                                         Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                                         MeyveCinsi TEXT NOT NULL, \
                                         MeyveAdedi TEXT NOT NULL, \
                                         Meyvekilo TEXT NOT NULL, \
                                         MeyveMensei TEXT NOT NULL, \
                                         MeyveFiyat TEXT NOT NULL)")
            self.meyve_cursor.execute(self.sorguCreTblmeyve)
            self.meyve_conn.commit()
        except sqlite3.Error as e:
            print("SQLite veritabanı hatası:", e)
#Bu kod, bir SQLite veritabanı oluşturmayı ve sebze bilgilerini içeren bir tablo oluşturmayı amaçlar. 
    def baglanti_olustur_sebze(self):
        try:
            self.sebze_conn = sqlite3.connect("sebze_veritabani.db")
            self.sebze_cursor = self.sebze_conn.cursor()
            self.sorguCreTblsebze = ("CREATE TABLE IF NOT EXISTS sebze ( \
                                         Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                                         SebzeCinsi TEXT NOT NULL, \
                                         SebzeAdedi TEXT NOT NULL, \
                                         Sebzekilo TEXT NOT NULL, \
                                         SebzeMensei TEXT NOT NULL, \
                                         SebzeFiyat TEXT NOT NULL)")
            self.sebze_cursor.execute(self.sorguCreTblsebze)
            self.sebze_conn.commit()
        except sqlite3.Error as e:
            print("SQLite veritabanı hatası:", e)
#Bu kod, bir SQLite veritabanından meyve verilerini çekip bir PyQt5 kullanıcı arayüzünde listelemeyi amaçlar.
    def listele_meyve(self):
        try:
            self.twmeyvelistesi.clear()
            self.twmeyvelistesi.setRowCount(0)
            self.twmeyvelistesi.setHorizontalHeaderLabels(('Sıra','Meyve Cinsi','Meyve Adedi','Meyve Kilo','Meyve Mensei','Meyve Fiyat'))
            self.twmeyvelistesi.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.meyve_cursor.execute("SELECT * FROM meyve")
            for satirIndeks, satirVeri in enumerate(self.meyve_cursor):
                self.twmeyvelistesi.insertRow(satirIndeks)
                for sutunIndeks, sutunVeri in enumerate(satirVeri):
                    self.twmeyvelistesi.setItem(satirIndeks, sutunIndeks, QtWidgets.QTableWidgetItem(str(sutunVeri)))
            self.lneMeyveAdedi.clear()
            self.lneMeyveFiyat.clear()
            self.cmbMeyveMensei.setCurrentIndex(-1)
            self.spnMeyvesKilo.setValue(0)
        except sqlite3.Error as e:
            print("SQLite hatası:", e)
#Bu kod, bir SQLite veritabanından sebze verilerini çekip bir PyQt5 kullanıcı arayüzünde listelemeyi amaçlar.
    def listele_sebze(self):
        try:
            self.twsebzelistesi.clear()
            self.twsebzelistesi.setRowCount(0)
            self.twsebzelistesi.setHorizontalHeaderLabels(('Sıra','Sebze Cinsi','Sebze Adedi','Sebze Kilosu','Sebze Mensei','Sebze Fiyatı'))
            self.twsebzelistesi.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.sebze_cursor.execute("SELECT * FROM sebze")
            for satirIndeks, satirVeri in enumerate(self.sebze_cursor):
                self.twsebzelistesi.insertRow(satirIndeks)
                for sutunIndeks, sutunVeri in enumerate(satirVeri):
                    self.twsebzelistesi.setItem(satirIndeks, sutunIndeks, QtWidgets.QTableWidgetItem(str(sutunVeri)))
            self.lneSebzeAdedi.clear()
            self.lneSebzeFiyat.clear()
            self.cmbSebzeMensei.setCurrentIndex(-1)
            self.spnSebzeKilo.setValue(0)
        except sqlite3.Error as e:
            print("SQLite hatası:", e)
#Bu fonksiyon, bir PyQt5 ListWidget (liste widgeti) üzerinde belirli bir metni seçmek için kullanılır.
    def set_lw_current_text(self, list_widget, text):
        items = list_widget.findItems(text, QtCore.Qt.MatchExactly)
        if items:
            item = items[0]
            row = list_widget.row(item)
            list_widget.setCurrentRow(row)
#Bu fonksiyon, bir PyQt5 kullanıcı arayüzünde meyve verilerini düzenlemek için kullanılır. 
    def doldur_meyve(self):
        secili = self.twmeyvelistesi.selectedItems()
        if len(secili) > 0:
            self.lneMeyveAdedi.setText(secili[2].text())
            self.lneMeyveFiyat.setText(secili[5].text())
            self.set_lw_current_text(self.lwMeyveCinsi, secili[1].text())
            self.cmbMeyveMensei.setCurrentText(secili[4].text())
            self.spnMeyvesKilo.setValue(int(secili[3].text()))
        else:
            self.lneMeyveAdedi.clear()
            self.lneMeyveFiyat.clear()
            self.lwMeyveCinsi.setCurrentRow(-1)
            self.cmbMeyveMensei.setCurrentIndex(-1)
            self.spnMeyvesKilo.setValue(0)
#Bu fonksiyon, bir PyQt5 kullanıcı arayüzünde sebze verilerini düzenlemek için kullanılır. 
    def doldur_sebze(self):
        secili = self.twsebzelistesi.selectedItems()
        if len(secili) > 0:
            self.lneSebzeAdedi.setText(secili[2].text())
            self.lneSebzeFiyat.setText(secili[5].text())
            self.set_lw_current_text(self.lwSebzeCinsi, secili[1].text())
            self.cmbSebzeMensei.setCurrentText(secili[4].text())
            self.spnSebzeKilo.setValue(int(secili[3].text()))
        else:
            self.lneSebzeAdedi.clear()
            self.lneSebzeFiyat.clear()
            self.lwSebzeCinsi.setCurrentRow(-1)
            self.cmbSebzeMensei.setCurrentIndex(-1)
            self.spnSebzeKilo.setValue(0)
#Bu kod, bir meyve öğesini güncellemek için kullanılır. 
    def meyve_guncelle(self):
        secili = self.twmeyvelistesi.selectedItems()
        if len(secili) > 0:
            try:
                Id = int(secili[0].text())
                MeyveAdedi = self.lneMeyveAdedi.text()
                MeyveFiyat = self.lneMeyveFiyat.text()
                MeyveCinsi = self.lwMeyveCinsi.currentItem().text()
                MeyveMensei = self.cmbMeyveMensei.currentText()
                Meyvekilo = self.spnMeyvesKilo.value()
                self.meyve_cursor.execute("UPDATE meyve SET MeyveAdedi = ?, MeyveFiyat = ?, MeyveCinsi = ?, MeyveMensei = ?, Meyvekilo = ? WHERE Id = ?",
                                          (MeyveAdedi, MeyveFiyat, MeyveCinsi, MeyveMensei, Meyvekilo, Id))
                self.meyve_conn.commit()
                QMessageBox.information(self, "Bilgi", "Meyve başarıyla güncellendi.")
                self.listele_meyve()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Hata", "Meyve güncellenirken hata: " + str(e))
#Bu kod, bir sebze öğesini güncellemek için kullanılır. 
    def sebze_guncelle(self):
        secili = self.twsebzelistesi.selectedItems()
        if len(secili) > 0:
            try:
                Id = int(secili[0].text())
                SebzeAdedi = self.lneSebzeAdedi.text()
                SebzeFiyat = self.lneSebzeFiyat.text()
                SebzeCinsi = self.lwSebzeCinsi.currentItem().text()
                SebzeMensei = self.cmbSebzeMensei.currentText()
                Sebzekilo = self.spnSebzeKilo.value()
                self.sebze_cursor.execute("UPDATE sebze SET SebzeAdedi = ?, SebzeFiyat = ?, SebzeCinsi = ?, SebzeMensei = ?, Sebzekilo = ? WHERE Id = ?",
                                          (SebzeAdedi, SebzeFiyat, SebzeCinsi, SebzeMensei, Sebzekilo, Id))
                self.sebze_conn.commit()
                QMessageBox.information(self, "Bilgi", "Sebze başarıyla güncellendi.")
                self.listele_sebze()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Hata", "Sebze güncellenirken hata: " + str(e))
#Bu fonksiyon, seçilen bir meyve öğesini veritabanından silmek için kullanılır. 
    def meyve_sil(self):
        secili = self.twmeyvelistesi.selectedItems()
        if len(secili) > 0:
            try:
                Id = int(secili[0].text())
                self.meyve_cursor.execute("DELETE FROM meyve WHERE Id = ?", (Id,))
                self.meyve_conn.commit()
                QMessageBox.information(self, "Bilgi", "Meyve başarıyla silindi.")
                self.listele_meyve()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Hata", "Meyve silinirken hata: " + str(e))
#Bu fonksiyon, seçilen bir sebze öğesini veritabanından silmek için kullanılır. 
    def sebze_sil(self):
        secili = self.twsebzelistesi.selectedItems()
        if len(secili) > 0:
            try:
                Id = int(secili[0].text())
                self.sebze_cursor.execute("DELETE FROM sebze WHERE Id = ?", (Id,))
                self.sebze_conn.commit()
                QMessageBox.information(self, "Bilgi", "Sebze başarıyla silindi.")
                self.listele_sebze()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Hata", "Sebze silinirken hata: " + str(e))
#Bu fonksiyon, kullanıcının meyve cinsine göre veritabanında arama yapmasını sağlar
    def meyve_ara(self):
        aranan_cinsi = self.lwMeyveCinsi.currentItem().text() if self.lwMeyveCinsi.currentItem() else ""


        filtre = []

        if aranan_cinsi:
            filtre.append(f"MeyveCinsi LIKE '%{aranan_cinsi}%'")
   
         
        filtre_sorgusu = " OR ".join(filtre)
        if filtre_sorgusu:
            sorgu = "SELECT * FROM meyve WHERE " + filtre_sorgusu
        
            self.meyve_cursor.execute(sorgu)
            sonuclar = self.meyve_cursor.fetchall()

            self.twmeyvelistesi.clearContents()
            self.twmeyvelistesi.setRowCount(0)

            for satirIndeks, satirVeri in enumerate(sonuclar):
                self.twmeyvelistesi.insertRow(satirIndeks)
                for sutunIndeks, sutunVeri in enumerate(satirVeri):
                    self.twmeyvelistesi.setItem(satirIndeks, sutunIndeks, QTableWidgetItem(str(sutunVeri)))

        else:
            QMessageBox.warning(None, "Uyarı", "Arama için en az bir kriter doldur.")
#Bu fonksiyon, kullanıcının sebze cinsine göre veritabanında arama yapmasını sağlar
    def sebze_ara(self):
        aranan_cinsi = self.lwSebzeCinsi.currentItem().text() if self.lwSebzeCinsi.currentItem() else ""


        filtre = []

        if aranan_cinsi:
            filtre.append(f"SebzeCinsi LIKE '%{aranan_cinsi}%'")
   
         
        filtre_sorgusu = " OR ".join(filtre)
        if filtre_sorgusu:
            sorgu = "SELECT * FROM sebze WHERE " + filtre_sorgusu
        
            self.sebze_cursor.execute(sorgu)
            sonuclar = self.sebze_cursor.fetchall()

            self.twsebzelistesi.clearContents()
            self.twsebzelistesi.setRowCount(0)

            for satirIndeks, satirVeri in enumerate(sonuclar):
                self.twsebzelistesi.insertRow(satirIndeks)
                for sutunIndeks, sutunVeri in enumerate(satirVeri):
                    self.twsebzelistesi.setItem(satirIndeks, sutunIndeks, QTableWidgetItem(str(sutunVeri)))

        else:
            QMessageBox.warning(None, "Uyarı", "Arama için en az bir kriter doldur.")
#Bu fonksiyon, kullanıcının programdan çıkış yapmasını sağlar.
    def cikis(self):
        cevap = QtWidgets.QMessageBox.question(
            self, "ÇIKIŞ", "Programdan çıkmak istediğinize emin misiniz?", 
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if cevap == QtWidgets.QMessageBox.Yes:
            self.close()
            
#Uygulama başlatma kodu  
  
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    lw = Login()
    lw.show()
    sys.exit(app.exec_())        
        
#Uygulama başlatma kodu            
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mw = Ui_MainWindow()
    mw.show()
    sys.exit(app.exec_())