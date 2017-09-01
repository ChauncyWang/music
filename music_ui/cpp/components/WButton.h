//
// Created by hy on 17-9-1.
//

#ifndef MUSIC_UI_WBUTTON_H
#define MUSIC_UI_WBUTTON_H


#include <QtWidgets/QLabel>

class WButton: public QLabel {
Q_OBJECT

public:
    WButton(QWidget *parent=NULL);

public slots:

signals:
    void clicked();

protected:
    void mousePressEvent(QMouseEvent *ev);
};


#endif //MUSIC_UI_BUTTON_H
