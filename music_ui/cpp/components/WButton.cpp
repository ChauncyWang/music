//
// Created by hy on 17-9-1.
//

#include "WButton.h"

WButton::WButton(QWidget *parent):QLabel(parent) {

}

void WButton::mousePressEvent(QMouseEvent *ev) {
    emit clicked();
}