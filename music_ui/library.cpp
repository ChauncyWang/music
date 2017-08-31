#include "library.h"

#include <iostream>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtCore/QTime>
#include <QtWidgets/QGraphicsView>
#include <QtWidgets/QSlider>
#include "myitem.h"

void hello(int argc, char **argv) {
    QApplication app(argc, argv);
    QWidget qWidget;
    QSlider slider(&qWidget);
    slider.setOrientation(Qt::Horizontal);
    qWidget.setStyleSheet("QSlider::add-page:Horizontal{\
        background-color: rgb(87, 97, 106);\
        height:4px;\
     }\
     QSlider::sub-page:Horizontal \
    {\
        background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(231,80,229, 255), stop:1 rgba(7,208,255, 255));\
        height:4px;\
     }\
    QSlider::groove:Horizontal \
    {\
        background:transparent;\
        height:6px;\
    }\
    QSlider::handle:Horizontal \
    {\
        height: 30px;\
        width:8px;\
        background-color:red;\
        margin: -8 0px; \
    }\
    ");
    qWidget.show();
    app.exec();
}