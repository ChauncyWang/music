#ifndef MUSIC_UI_LIBRARY_H
#define MUSIC_UI_LIBRARY_H

void hello(int argc, char **argv);

extern "C" {
    void Hello() {
        hello(0,{});
    }
}
#endif