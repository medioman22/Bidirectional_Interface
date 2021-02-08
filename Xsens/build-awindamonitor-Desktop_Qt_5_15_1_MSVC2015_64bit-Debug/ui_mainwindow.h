/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.15.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QProgressBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QTextBrowser>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QGroupBox *connectedMtwListGroupBox;
    QListWidget *connectedMtwList;
    QCheckBox *pitchToSelectCheckBox;
    QGroupBox *mtwPropertiesGroupBox;
    QLabel *batteryLevelCaptionLabel;
    QLabel *effUpdateRateCaptionLabel;
    QLabel *rssiCaptionLabel;
    QLabel *rssiLabel;
    QLabel *batteryLevelLabel;
    QLabel *effUpdateRateLabel;
    QLabel *rollLabel;
    QLabel *rollCaptionLabel;
    QLabel *yawCaptionLabel;
    QLabel *pitchLabel;
    QLabel *pitchCaptionLabel;
    QLabel *yawLabel;
    QGroupBox *stationPropertiesGroupBox;
    QLabel *updateRateCaptionLabel;
    QComboBox *allowedUpdateRatesComboBox;
    QLabel *channelCaptionLabel;
    QComboBox *channelComboBox;
    QLabel *stationIdCaptionLabel;
    QLabel *stationIdLabel;
    QPushButton *enableButton;
    QPushButton *startMeasurementButton;
    QPushButton *recordingButton;
    QLineEdit *logFilenameEdit;
    QLabel *logFilenameCaptionLabel;
    QProgressBar *flushingProgressBar;
    QLabel *flushingCaptionLabel;
    QPushButton *resetIMUs;
    QGroupBox *loggingGroupBox;
    QTextBrowser *logWindow;
    QPushButton *clearLogPushButton;
    QGroupBox *stateMachineImageGroupBox;
    QLabel *stateDiagramLabel;
    QGroupBox *dockedMtwListGroupBox;
    QListWidget *dockedMtwList;
    QLabel *logoLabel;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(824, 348);
        QSizePolicy sizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(MainWindow->sizePolicy().hasHeightForWidth());
        MainWindow->setSizePolicy(sizePolicy);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        connectedMtwListGroupBox = new QGroupBox(centralWidget);
        connectedMtwListGroupBox->setObjectName(QString::fromUtf8("connectedMtwListGroupBox"));
        connectedMtwListGroupBox->setGeometry(QRect(170, 170, 151, 171));
        connectedMtwList = new QListWidget(connectedMtwListGroupBox);
        connectedMtwList->setObjectName(QString::fromUtf8("connectedMtwList"));
        connectedMtwList->setGeometry(QRect(10, 20, 131, 111));
        connectedMtwList->setSortingEnabled(true);
        pitchToSelectCheckBox = new QCheckBox(connectedMtwListGroupBox);
        pitchToSelectCheckBox->setObjectName(QString::fromUtf8("pitchToSelectCheckBox"));
        pitchToSelectCheckBox->setGeometry(QRect(10, 140, 101, 20));
        mtwPropertiesGroupBox = new QGroupBox(centralWidget);
        mtwPropertiesGroupBox->setObjectName(QString::fromUtf8("mtwPropertiesGroupBox"));
        mtwPropertiesGroupBox->setGeometry(QRect(330, 170, 161, 171));
        batteryLevelCaptionLabel = new QLabel(mtwPropertiesGroupBox);
        batteryLevelCaptionLabel->setObjectName(QString::fromUtf8("batteryLevelCaptionLabel"));
        batteryLevelCaptionLabel->setGeometry(QRect(20, 30, 71, 16));
        batteryLevelCaptionLabel->setScaledContents(true);
        effUpdateRateCaptionLabel = new QLabel(mtwPropertiesGroupBox);
        effUpdateRateCaptionLabel->setObjectName(QString::fromUtf8("effUpdateRateCaptionLabel"));
        effUpdateRateCaptionLabel->setGeometry(QRect(20, 78, 91, 16));
        rssiCaptionLabel = new QLabel(mtwPropertiesGroupBox);
        rssiCaptionLabel->setObjectName(QString::fromUtf8("rssiCaptionLabel"));
        rssiCaptionLabel->setEnabled(true);
        rssiCaptionLabel->setGeometry(QRect(20, 54, 46, 16));
        rssiLabel = new QLabel(mtwPropertiesGroupBox);
        rssiLabel->setObjectName(QString::fromUtf8("rssiLabel"));
        rssiLabel->setGeometry(QRect(100, 54, 50, 13));
        rssiLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        batteryLevelLabel = new QLabel(mtwPropertiesGroupBox);
        batteryLevelLabel->setObjectName(QString::fromUtf8("batteryLevelLabel"));
        batteryLevelLabel->setGeometry(QRect(100, 30, 50, 16));
        batteryLevelLabel->setLayoutDirection(Qt::LeftToRight);
        batteryLevelLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        effUpdateRateLabel = new QLabel(mtwPropertiesGroupBox);
        effUpdateRateLabel->setObjectName(QString::fromUtf8("effUpdateRateLabel"));
        effUpdateRateLabel->setGeometry(QRect(100, 78, 50, 16));
        effUpdateRateLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        rollLabel = new QLabel(mtwPropertiesGroupBox);
        rollLabel->setObjectName(QString::fromUtf8("rollLabel"));
        rollLabel->setGeometry(QRect(79, 102, 71, 20));
        rollLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        rollCaptionLabel = new QLabel(mtwPropertiesGroupBox);
        rollCaptionLabel->setObjectName(QString::fromUtf8("rollCaptionLabel"));
        rollCaptionLabel->setGeometry(QRect(20, 102, 46, 16));
        yawCaptionLabel = new QLabel(mtwPropertiesGroupBox);
        yawCaptionLabel->setObjectName(QString::fromUtf8("yawCaptionLabel"));
        yawCaptionLabel->setGeometry(QRect(20, 150, 46, 16));
        pitchLabel = new QLabel(mtwPropertiesGroupBox);
        pitchLabel->setObjectName(QString::fromUtf8("pitchLabel"));
        pitchLabel->setGeometry(QRect(79, 126, 71, 20));
        pitchLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        pitchCaptionLabel = new QLabel(mtwPropertiesGroupBox);
        pitchCaptionLabel->setObjectName(QString::fromUtf8("pitchCaptionLabel"));
        pitchCaptionLabel->setGeometry(QRect(20, 126, 46, 16));
        yawLabel = new QLabel(mtwPropertiesGroupBox);
        yawLabel->setObjectName(QString::fromUtf8("yawLabel"));
        yawLabel->setGeometry(QRect(79, 150, 71, 20));
        yawLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        stationPropertiesGroupBox = new QGroupBox(centralWidget);
        stationPropertiesGroupBox->setObjectName(QString::fromUtf8("stationPropertiesGroupBox"));
        stationPropertiesGroupBox->setGeometry(QRect(10, 10, 151, 331));
        updateRateCaptionLabel = new QLabel(stationPropertiesGroupBox);
        updateRateCaptionLabel->setObjectName(QString::fromUtf8("updateRateCaptionLabel"));
        updateRateCaptionLabel->setEnabled(false);
        updateRateCaptionLabel->setGeometry(QRect(10, 120, 61, 20));
        allowedUpdateRatesComboBox = new QComboBox(stationPropertiesGroupBox);
        allowedUpdateRatesComboBox->setObjectName(QString::fromUtf8("allowedUpdateRatesComboBox"));
        allowedUpdateRatesComboBox->setEnabled(false);
        allowedUpdateRatesComboBox->setGeometry(QRect(80, 120, 61, 22));
        channelCaptionLabel = new QLabel(stationPropertiesGroupBox);
        channelCaptionLabel->setObjectName(QString::fromUtf8("channelCaptionLabel"));
        channelCaptionLabel->setEnabled(false);
        channelCaptionLabel->setGeometry(QRect(10, 50, 46, 13));
        channelComboBox = new QComboBox(stationPropertiesGroupBox);
        channelComboBox->addItem(QString());
        channelComboBox->addItem(QString());
        channelComboBox->addItem(QString());
        channelComboBox->addItem(QString());
        channelComboBox->addItem(QString());
        channelComboBox->addItem(QString());
        channelComboBox->addItem(QString());
        channelComboBox->addItem(QString());
        channelComboBox->addItem(QString());
        channelComboBox->addItem(QString());
        channelComboBox->addItem(QString());
        channelComboBox->addItem(QString());
        channelComboBox->addItem(QString());
        channelComboBox->addItem(QString());
        channelComboBox->addItem(QString());
        channelComboBox->setObjectName(QString::fromUtf8("channelComboBox"));
        channelComboBox->setEnabled(false);
        channelComboBox->setGeometry(QRect(90, 41, 51, 31));
        stationIdCaptionLabel = new QLabel(stationPropertiesGroupBox);
        stationIdCaptionLabel->setObjectName(QString::fromUtf8("stationIdCaptionLabel"));
        stationIdCaptionLabel->setGeometry(QRect(10, 20, 46, 13));
        stationIdLabel = new QLabel(stationPropertiesGroupBox);
        stationIdLabel->setObjectName(QString::fromUtf8("stationIdLabel"));
        stationIdLabel->setGeometry(QRect(30, 20, 61, 16));
        stationIdLabel->setScaledContents(false);
        enableButton = new QPushButton(stationPropertiesGroupBox);
        enableButton->setObjectName(QString::fromUtf8("enableButton"));
        enableButton->setEnabled(false);
        enableButton->setGeometry(QRect(10, 80, 131, 31));
        startMeasurementButton = new QPushButton(stationPropertiesGroupBox);
        startMeasurementButton->setObjectName(QString::fromUtf8("startMeasurementButton"));
        startMeasurementButton->setEnabled(false);
        startMeasurementButton->setGeometry(QRect(10, 150, 131, 31));
        recordingButton = new QPushButton(stationPropertiesGroupBox);
        recordingButton->setObjectName(QString::fromUtf8("recordingButton"));
        recordingButton->setEnabled(false);
        recordingButton->setGeometry(QRect(10, 220, 131, 31));
        logFilenameEdit = new QLineEdit(stationPropertiesGroupBox);
        logFilenameEdit->setObjectName(QString::fromUtf8("logFilenameEdit"));
        logFilenameEdit->setEnabled(false);
        logFilenameEdit->setGeometry(QRect(60, 190, 81, 21));
        logFilenameCaptionLabel = new QLabel(stationPropertiesGroupBox);
        logFilenameCaptionLabel->setObjectName(QString::fromUtf8("logFilenameCaptionLabel"));
        logFilenameCaptionLabel->setEnabled(false);
        logFilenameCaptionLabel->setGeometry(QRect(10, 190, 46, 21));
        flushingProgressBar = new QProgressBar(stationPropertiesGroupBox);
        flushingProgressBar->setObjectName(QString::fromUtf8("flushingProgressBar"));
        flushingProgressBar->setEnabled(false);
        flushingProgressBar->setGeometry(QRect(60, 260, 81, 23));
        flushingProgressBar->setValue(0);
        flushingProgressBar->setTextVisible(false);
        flushingProgressBar->setInvertedAppearance(true);
        flushingCaptionLabel = new QLabel(stationPropertiesGroupBox);
        flushingCaptionLabel->setObjectName(QString::fromUtf8("flushingCaptionLabel"));
        flushingCaptionLabel->setEnabled(false);
        flushingCaptionLabel->setGeometry(QRect(10, 260, 46, 20));
        resetIMUs = new QPushButton(stationPropertiesGroupBox);
        resetIMUs->setObjectName(QString::fromUtf8("resetIMUs"));
        resetIMUs->setEnabled(false);
        resetIMUs->setGeometry(QRect(50, 290, 93, 28));
        loggingGroupBox = new QGroupBox(centralWidget);
        loggingGroupBox->setObjectName(QString::fromUtf8("loggingGroupBox"));
        loggingGroupBox->setGeometry(QRect(330, 10, 341, 141));
        logWindow = new QTextBrowser(loggingGroupBox);
        logWindow->setObjectName(QString::fromUtf8("logWindow"));
        logWindow->setGeometry(QRect(10, 20, 321, 101));
        clearLogPushButton = new QPushButton(loggingGroupBox);
        clearLogPushButton->setObjectName(QString::fromUtf8("clearLogPushButton"));
        clearLogPushButton->setGeometry(QRect(10, 125, 321, 10));
        stateMachineImageGroupBox = new QGroupBox(centralWidget);
        stateMachineImageGroupBox->setObjectName(QString::fromUtf8("stateMachineImageGroupBox"));
        stateMachineImageGroupBox->setGeometry(QRect(500, 170, 311, 171));
        stateDiagramLabel = new QLabel(stateMachineImageGroupBox);
        stateDiagramLabel->setObjectName(QString::fromUtf8("stateDiagramLabel"));
        stateDiagramLabel->setGeometry(QRect(10, 20, 291, 141));
        dockedMtwListGroupBox = new QGroupBox(centralWidget);
        dockedMtwListGroupBox->setObjectName(QString::fromUtf8("dockedMtwListGroupBox"));
        dockedMtwListGroupBox->setGeometry(QRect(170, 10, 151, 141));
        dockedMtwList = new QListWidget(dockedMtwListGroupBox);
        dockedMtwList->setObjectName(QString::fromUtf8("dockedMtwList"));
        dockedMtwList->setGeometry(QRect(10, 20, 131, 111));
        dockedMtwList->setSortingEnabled(true);
        logoLabel = new QLabel(centralWidget);
        logoLabel->setObjectName(QString::fromUtf8("logoLabel"));
        logoLabel->setGeometry(QRect(690, 20, 121, 131));
        MainWindow->setCentralWidget(centralWidget);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "Awinda monitor", nullptr));
        connectedMtwListGroupBox->setTitle(QCoreApplication::translate("MainWindow", "Connected MTw list (0):", nullptr));
        pitchToSelectCheckBox->setText(QCoreApplication::translate("MainWindow", "Pitch to select", nullptr));
        mtwPropertiesGroupBox->setTitle(QCoreApplication::translate("MainWindow", "Selected MTw properties:", nullptr));
        batteryLevelCaptionLabel->setText(QCoreApplication::translate("MainWindow", "Battery level:", nullptr));
        effUpdateRateCaptionLabel->setText(QCoreApplication::translate("MainWindow", "Eff. update rate:", nullptr));
        rssiCaptionLabel->setText(QCoreApplication::translate("MainWindow", "RSSI:", nullptr));
        rssiLabel->setText(QCoreApplication::translate("MainWindow", "-", nullptr));
        batteryLevelLabel->setText(QCoreApplication::translate("MainWindow", "-", nullptr));
        effUpdateRateLabel->setText(QCoreApplication::translate("MainWindow", "-", nullptr));
        rollLabel->setText(QCoreApplication::translate("MainWindow", "-", nullptr));
        rollCaptionLabel->setText(QCoreApplication::translate("MainWindow", "Roll:", nullptr));
        yawCaptionLabel->setText(QCoreApplication::translate("MainWindow", "Yaw:", nullptr));
        pitchLabel->setText(QCoreApplication::translate("MainWindow", "-", nullptr));
        pitchCaptionLabel->setText(QCoreApplication::translate("MainWindow", "Pitch:", nullptr));
        yawLabel->setText(QCoreApplication::translate("MainWindow", "-", nullptr));
        stationPropertiesGroupBox->setTitle(QCoreApplication::translate("MainWindow", "Wireless master properties:", nullptr));
        updateRateCaptionLabel->setText(QCoreApplication::translate("MainWindow", "Update rate:", nullptr));
        channelCaptionLabel->setText(QCoreApplication::translate("MainWindow", "Channel:", nullptr));
        channelComboBox->setItemText(0, QCoreApplication::translate("MainWindow", "11", nullptr));
        channelComboBox->setItemText(1, QCoreApplication::translate("MainWindow", "12", nullptr));
        channelComboBox->setItemText(2, QCoreApplication::translate("MainWindow", "13", nullptr));
        channelComboBox->setItemText(3, QCoreApplication::translate("MainWindow", "14", nullptr));
        channelComboBox->setItemText(4, QCoreApplication::translate("MainWindow", "15", nullptr));
        channelComboBox->setItemText(5, QCoreApplication::translate("MainWindow", "16", nullptr));
        channelComboBox->setItemText(6, QCoreApplication::translate("MainWindow", "17", nullptr));
        channelComboBox->setItemText(7, QCoreApplication::translate("MainWindow", "18", nullptr));
        channelComboBox->setItemText(8, QCoreApplication::translate("MainWindow", "19", nullptr));
        channelComboBox->setItemText(9, QCoreApplication::translate("MainWindow", "20", nullptr));
        channelComboBox->setItemText(10, QCoreApplication::translate("MainWindow", "21", nullptr));
        channelComboBox->setItemText(11, QCoreApplication::translate("MainWindow", "22", nullptr));
        channelComboBox->setItemText(12, QCoreApplication::translate("MainWindow", "23", nullptr));
        channelComboBox->setItemText(13, QCoreApplication::translate("MainWindow", "24", nullptr));
        channelComboBox->setItemText(14, QCoreApplication::translate("MainWindow", "25", nullptr));

        stationIdCaptionLabel->setText(QCoreApplication::translate("MainWindow", "ID:", nullptr));
        stationIdLabel->setText(QCoreApplication::translate("MainWindow", "-", nullptr));
        enableButton->setText(QCoreApplication::translate("MainWindow", "Enable", nullptr));
        startMeasurementButton->setText(QCoreApplication::translate("MainWindow", "Start Measurement", nullptr));
        recordingButton->setText(QCoreApplication::translate("MainWindow", "Start recording", nullptr));
        logFilenameEdit->setText(QCoreApplication::translate("MainWindow", "logfile.mtb", nullptr));
        logFilenameCaptionLabel->setText(QCoreApplication::translate("MainWindow", "Filename:", nullptr));
        flushingCaptionLabel->setText(QCoreApplication::translate("MainWindow", "Flushing:", nullptr));
        resetIMUs->setText(QCoreApplication::translate("MainWindow", "Reset IMUs", nullptr));
        loggingGroupBox->setTitle(QCoreApplication::translate("MainWindow", "What's going on:", nullptr));
        clearLogPushButton->setText(QString());
        stateMachineImageGroupBox->setTitle(QCoreApplication::translate("MainWindow", "State diagram:", nullptr));
        stateDiagramLabel->setText(QCoreApplication::translate("MainWindow", "<State diagram>", nullptr));
        dockedMtwListGroupBox->setTitle(QCoreApplication::translate("MainWindow", "Docked MTw list (0):", nullptr));
        logoLabel->setText(QCoreApplication::translate("MainWindow", "<Logo label>", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
