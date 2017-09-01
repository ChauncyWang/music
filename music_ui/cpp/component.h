//
// Created by hy on 17-9-1.
//

#ifndef MUSIC_UI_COMPONENT_H
#define MUSIC_UI_COMPONENT_H

#include <QtWidgets/QWidget>
#include <QtWidgets/QLabel>

class BtnLabel: public QLabel {
public:
    BtnLabel(QWidget parent);

public slots:

signals:
    void clicked();
};
#endif //MUSIC_UI_COMPONENT_H
