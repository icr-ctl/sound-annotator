# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/goto.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(217, 115)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.filename = QtWidgets.QLineEdit(Dialog)
        self.filename.setObjectName("filename")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.filename)
        self.chooseButton = QtWidgets.QPushButton(Dialog)
        self.chooseButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.chooseButton.setObjectName("chooseButton")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.chooseButton)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "annotator"))
        self.label.setText(_translate("Dialog", "Filename:"))
        self.chooseButton.setText(_translate("Dialog", "Choose..."))
