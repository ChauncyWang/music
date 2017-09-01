//
// Created by hy on 17-9-1.
//

#include <iostream>
#include <python3.5/Python.h>
#include <QtWidgets/QApplication>
#include <cpp/components/WButton.h>
#include <QtWidgets/QMainWindow>
#include <cpp/components/ProgressBar.h>

using namespace std;

int main(int argc, char **argv) {
    QApplication app(argc, argv);
    QMainWindow mainWindow;

    ProgressBar bar(&mainWindow);
    bar.setGeometry(0,0,800,40);

    mainWindow.show();
    return app.exec();
}