#include "library.h"

#include <QtWidgets/QApplication>
#include <iostream>

void hello(int argc, char **argv) {
    QApplication app(argc, argv);
    app.exec();
}
void callback(int *a(int, int)) {
    std::cout << a(1,2);
}