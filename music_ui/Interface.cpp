//
// Created by hy on 17-9-1.
//

#include <python3.5/Python.h>
#include "Interface.h"
#include <iostream>

using namespace std;

Interface::Interface() {
    Py_Initialize();
    if (!Py_IsInitialized()) {
        cout << "python初始化失败!" << endl;
        exit(-1);
    }

    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('./python/')");

    PyObject *pModule = PyImport_ImportModule("FFF.testAAA");
    if (!pModule) {
        cout << "python模块加载失败!" << endl;
        exit(-1);
    }
    PyObject *pFunhello = PyObject_GetAttrString(pModule, "hello");
    if (!pFunhello) {
        cout << "python函数获取失败!" << endl;
        exit(-1);
    }
    PyObject *args = NULL;
    PyObject_CallObject(pFunhello, args);

    Py_Finalize();
}

Interface::~Interface() {
    cout << "释放 python 资源。" << endl;
    Py_Finalize();
}