//
// Created by hy on 17-9-1.
//

#include <iostream>
#include <python3.5/Python.h>
#include <QtWidgets/QApplication>
#include <cpp/components/WButton.h>

using namespace std;

int main(int argc, char **argv) {
    QApplication app(argc, argv);

    WButton btn;
    btn.show();

    return app.exec();
}