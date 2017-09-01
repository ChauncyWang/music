//
// Created by hy on 17-9-1.
//

#ifndef MUSIC_UI_PROCESSBAR_H
#define MUSIC_UI_PROCESSBAR_H


#include <QtWidgets/QFrame>

class ProcessBar : public QFrame {
Q_OBJECT
public:
    ProcessBar(QWidget *parent = NULL);

public slots:

signals:

    /**
     * 进度改变的槽
     * @param rate 改变的进度
     */
    void rateChanged(float rate);

private:
    float rate = 0;         ///< 进度
    bool clicked = false;   ///< 是否点击了
    int in_radius = 3;      ///< 内圆半径
    int out_radius = 10;    ///< 外圆半径
};


#endif //MUSIC_UI_PROCESSBAR_H
