#-------------------------------------------------
#
# Project created by QtCreator 2011-12-02T11:26:58
#
#-------------------------------------------------

QT += core gui widgets
QT += network

TARGET = awindamonitor
TEMPLATE = app

SOURCES +=  main.cpp \
		   mainwindow.cpp \
		   myxda.cpp \
		   connectedmtwdata.cpp \
    myudp.cpp

HEADERS  += mainwindow.h \
		   myxda.h \
		   connectedmtwdata.h \
    myudp.h

FORMS   += mainwindow.ui

win32-msvc* {
#	ARCH=Win32
        ARCH=x64
	contains(QMAKE_TARGET.arch, x86_64):ARCH=x64

#        XDP=32
        XDP=64
        contains(QMAKE_TARGET.arc, x86_64):XDP=64

        CONFIG(debug, debug|release) {
		CFG = Debug
        } else {
		CFG = Release
	}

	DESTDIR=../bin/$$TARGET/$$ARCH/$$CFG
        ARCH_DIR=../../$${ARCH}
	ARCH_DIR~=s,/,\\,g

#	LIB_PATH=$${ARCH_DIR}\\lib
        LIB_PATH=$${IN_PWD}\\x64\\lib
	INCLUDEPATH += \"$${ARCH_DIR}\\include\"
	LIBS += -L\"$${LIB_PATH}\"

	LIBS += xsensdeviceapi$${XDP}.lib \
			xstypes$${XDP}.lib

        FILES_TO_COPY=	$$LIB_PATH/Qt5Core.dll \
                        $$LIB_PATH/Qt5Gui.dll \
                        $$LIB_PATH/Qt5Widgets.dll \
                        $$LIB_PATH/platforms/qwindows.dll \
                        $$LIB_PATH/xsensdeviceapi$${XDP}.dll \
                        $$LIB_PATH/xstypes$${XDP}.dll
	FILES_TO_COPY ~= s,/,\\,g

	for(FILE,FILES_TO_COPY){
		QMAKE_PRE_LINK += copy /y /b \"$$FILE\" \"$$DESTDIR\" $$escape_expand(\\n\\t)
	}
}

unix {
	# On unix we cannot reliably detect cross-compilation
	# Just look at the host instead
	ARCH=32
	contains(QMAKE_HOST.arch, x86_64):ARCH=64
	!isEmpty(XSENS_INSTALL_PREFIX) {
		INCLUDEPATH += $$XSENS_INSTALL_PREFIX/include
		LIBS += -L$$XSENS_INSTALL_PREFIX/lib
		QMAKE_LFLAGS+=-Wl,-rpath=$$XSENS_INSTALL_PREFIX/lib
	}
	LIBS += -lxsensdeviceapi -lxstypes
}

INCLUDEPATH += x64\\include
#INCLUDEPATH += x64\include

RESOURCES += \
	awindamonitor.qrc

win32:RC_FILE = icon.rc

