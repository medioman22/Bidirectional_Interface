/****************************************************************************
** Meta object code from reading C++ file 'mainwindow.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../../IMU_read/mainwindow.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'mainwindow.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_MainWindow_t {
    QByteArrayData data[31];
    char stringdata0[565];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_MainWindow_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_MainWindow_t qt_meta_stringdata_MainWindow = {
    {
QT_MOC_LITERAL(0, 0, 10), // "MainWindow"
QT_MOC_LITERAL(1, 11, 12), // "closeLogFile"
QT_MOC_LITERAL(2, 24, 0), // ""
QT_MOC_LITERAL(3, 25, 9), // "resetIMUs"
QT_MOC_LITERAL(4, 35, 18), // "toggleRadioEnabled"
QT_MOC_LITERAL(5, 54, 15), // "setRadioChannel"
QT_MOC_LITERAL(6, 70, 7), // "channel"
QT_MOC_LITERAL(7, 78, 17), // "toggleMeasurement"
QT_MOC_LITERAL(8, 96, 15), // "toggleRecording"
QT_MOC_LITERAL(9, 112, 14), // "clearLogWindow"
QT_MOC_LITERAL(10, 127, 27), // "clearConnectedMtwDataLabels"
QT_MOC_LITERAL(11, 155, 20), // "requestBatteryLevels"
QT_MOC_LITERAL(12, 176, 28), // "handleWirelessMasterDetected"
QT_MOC_LITERAL(13, 205, 10), // "XsPortInfo"
QT_MOC_LITERAL(14, 216, 23), // "handleDockedMtwDetected"
QT_MOC_LITERAL(15, 240, 17), // "handleMtwUndocked"
QT_MOC_LITERAL(16, 258, 24), // "handleOpenPortSuccessful"
QT_MOC_LITERAL(17, 283, 20), // "handleOpenPortFailed"
QT_MOC_LITERAL(18, 304, 24), // "handleMeasurementStarted"
QT_MOC_LITERAL(19, 329, 10), // "XsDeviceId"
QT_MOC_LITERAL(20, 340, 24), // "handleMeasurementStopped"
QT_MOC_LITERAL(21, 365, 11), // "handleError"
QT_MOC_LITERAL(22, 377, 13), // "XsResultValue"
QT_MOC_LITERAL(23, 391, 30), // "handleWaitingForRecordingStart"
QT_MOC_LITERAL(24, 422, 22), // "handleRecordingStarted"
QT_MOC_LITERAL(25, 445, 20), // "handleProgressUpdate"
QT_MOC_LITERAL(26, 466, 17), // "handleMtwWireless"
QT_MOC_LITERAL(27, 484, 21), // "handleMtwDisconnected"
QT_MOC_LITERAL(28, 506, 19), // "handleDataAvailable"
QT_MOC_LITERAL(29, 526, 12), // "XsDataPacket"
QT_MOC_LITERAL(30, 539, 25) // "handleBatteryLevelChanged"

    },
    "MainWindow\0closeLogFile\0\0resetIMUs\0"
    "toggleRadioEnabled\0setRadioChannel\0"
    "channel\0toggleMeasurement\0toggleRecording\0"
    "clearLogWindow\0clearConnectedMtwDataLabels\0"
    "requestBatteryLevels\0handleWirelessMasterDetected\0"
    "XsPortInfo\0handleDockedMtwDetected\0"
    "handleMtwUndocked\0handleOpenPortSuccessful\0"
    "handleOpenPortFailed\0handleMeasurementStarted\0"
    "XsDeviceId\0handleMeasurementStopped\0"
    "handleError\0XsResultValue\0"
    "handleWaitingForRecordingStart\0"
    "handleRecordingStarted\0handleProgressUpdate\0"
    "handleMtwWireless\0handleMtwDisconnected\0"
    "handleDataAvailable\0XsDataPacket\0"
    "handleBatteryLevelChanged"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_MainWindow[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
      24,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       1,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    0,  134,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       3,    0,  135,    2, 0x08 /* Private */,
       4,    0,  136,    2, 0x08 /* Private */,
       5,    1,  137,    2, 0x08 /* Private */,
       7,    0,  140,    2, 0x08 /* Private */,
       8,    0,  141,    2, 0x08 /* Private */,
       9,    0,  142,    2, 0x08 /* Private */,
      10,    0,  143,    2, 0x08 /* Private */,
      11,    0,  144,    2, 0x08 /* Private */,
      12,    1,  145,    2, 0x08 /* Private */,
      14,    1,  148,    2, 0x08 /* Private */,
      15,    1,  151,    2, 0x08 /* Private */,
      16,    1,  154,    2, 0x08 /* Private */,
      17,    1,  157,    2, 0x08 /* Private */,
      18,    1,  160,    2, 0x08 /* Private */,
      20,    1,  163,    2, 0x08 /* Private */,
      21,    2,  166,    2, 0x08 /* Private */,
      23,    1,  171,    2, 0x08 /* Private */,
      24,    1,  174,    2, 0x08 /* Private */,
      25,    4,  177,    2, 0x08 /* Private */,
      26,    1,  186,    2, 0x08 /* Private */,
      27,    1,  189,    2, 0x08 /* Private */,
      28,    2,  192,    2, 0x08 /* Private */,
      30,    2,  197,    2, 0x08 /* Private */,

 // signals: parameters
    QMetaType::Void,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,    6,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 13,    2,
    QMetaType::Void, 0x80000000 | 13,    2,
    QMetaType::Void, 0x80000000 | 13,    2,
    QMetaType::Void, 0x80000000 | 13,    2,
    QMetaType::Void, 0x80000000 | 13,    2,
    QMetaType::Void, 0x80000000 | 19,    2,
    QMetaType::Void, 0x80000000 | 19,    2,
    QMetaType::Void, 0x80000000 | 19, 0x80000000 | 22,    2,    2,
    QMetaType::Void, 0x80000000 | 19,    2,
    QMetaType::Void, 0x80000000 | 19,    2,
    QMetaType::Void, 0x80000000 | 19, QMetaType::Int, QMetaType::Int, QMetaType::QString,    2,    2,    2,    2,
    QMetaType::Void, 0x80000000 | 19,    2,
    QMetaType::Void, 0x80000000 | 19,    2,
    QMetaType::Void, 0x80000000 | 19, 0x80000000 | 29,    2,    2,
    QMetaType::Void, 0x80000000 | 19, QMetaType::Int,    2,    2,

       0        // eod
};

void MainWindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<MainWindow *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->closeLogFile(); break;
        case 1: _t->resetIMUs(); break;
        case 2: _t->toggleRadioEnabled(); break;
        case 3: _t->setRadioChannel((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 4: _t->toggleMeasurement(); break;
        case 5: _t->toggleRecording(); break;
        case 6: _t->clearLogWindow(); break;
        case 7: _t->clearConnectedMtwDataLabels(); break;
        case 8: _t->requestBatteryLevels(); break;
        case 9: _t->handleWirelessMasterDetected((*reinterpret_cast< XsPortInfo(*)>(_a[1]))); break;
        case 10: _t->handleDockedMtwDetected((*reinterpret_cast< XsPortInfo(*)>(_a[1]))); break;
        case 11: _t->handleMtwUndocked((*reinterpret_cast< XsPortInfo(*)>(_a[1]))); break;
        case 12: _t->handleOpenPortSuccessful((*reinterpret_cast< const XsPortInfo(*)>(_a[1]))); break;
        case 13: _t->handleOpenPortFailed((*reinterpret_cast< const XsPortInfo(*)>(_a[1]))); break;
        case 14: _t->handleMeasurementStarted((*reinterpret_cast< XsDeviceId(*)>(_a[1]))); break;
        case 15: _t->handleMeasurementStopped((*reinterpret_cast< XsDeviceId(*)>(_a[1]))); break;
        case 16: _t->handleError((*reinterpret_cast< XsDeviceId(*)>(_a[1])),(*reinterpret_cast< XsResultValue(*)>(_a[2]))); break;
        case 17: _t->handleWaitingForRecordingStart((*reinterpret_cast< XsDeviceId(*)>(_a[1]))); break;
        case 18: _t->handleRecordingStarted((*reinterpret_cast< XsDeviceId(*)>(_a[1]))); break;
        case 19: _t->handleProgressUpdate((*reinterpret_cast< XsDeviceId(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2])),(*reinterpret_cast< int(*)>(_a[3])),(*reinterpret_cast< QString(*)>(_a[4]))); break;
        case 20: _t->handleMtwWireless((*reinterpret_cast< XsDeviceId(*)>(_a[1]))); break;
        case 21: _t->handleMtwDisconnected((*reinterpret_cast< XsDeviceId(*)>(_a[1]))); break;
        case 22: _t->handleDataAvailable((*reinterpret_cast< XsDeviceId(*)>(_a[1])),(*reinterpret_cast< XsDataPacket(*)>(_a[2]))); break;
        case 23: _t->handleBatteryLevelChanged((*reinterpret_cast< XsDeviceId(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2]))); break;
        default: ;
        }
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        switch (_id) {
        default: *reinterpret_cast<int*>(_a[0]) = -1; break;
        case 9:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< XsPortInfo >(); break;
            }
            break;
        case 10:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< XsPortInfo >(); break;
            }
            break;
        case 11:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< XsPortInfo >(); break;
            }
            break;
        case 12:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< XsPortInfo >(); break;
            }
            break;
        case 13:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< XsPortInfo >(); break;
            }
            break;
        case 14:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< XsDeviceId >(); break;
            }
            break;
        case 15:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< XsDeviceId >(); break;
            }
            break;
        case 16:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< XsDeviceId >(); break;
            case 1:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< XsResultValue >(); break;
            }
            break;
        case 17:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< XsDeviceId >(); break;
            }
            break;
        case 18:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< XsDeviceId >(); break;
            }
            break;
        case 19:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< XsDeviceId >(); break;
            }
            break;
        case 20:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< XsDeviceId >(); break;
            }
            break;
        case 21:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< XsDeviceId >(); break;
            }
            break;
        case 22:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 1:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< XsDataPacket >(); break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< XsDeviceId >(); break;
            }
            break;
        case 23:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< XsDeviceId >(); break;
            }
            break;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (MainWindow::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&MainWindow::closeLogFile)) {
                *result = 0;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject MainWindow::staticMetaObject = { {
    QMetaObject::SuperData::link<QMainWindow::staticMetaObject>(),
    qt_meta_stringdata_MainWindow.data,
    qt_meta_data_MainWindow,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *MainWindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *MainWindow::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_MainWindow.stringdata0))
        return static_cast<void*>(this);
    return QMainWindow::qt_metacast(_clname);
}

int MainWindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QMainWindow::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 24)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 24;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 24)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 24;
    }
    return _id;
}

// SIGNAL 0
void MainWindow::closeLogFile()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
