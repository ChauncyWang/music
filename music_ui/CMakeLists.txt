cmake_minimum_required(VERSION 3.7)
project(music_ui)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

#查找Qt的库
find_package(Qt5Widgets)
find_package(Qt5Core)


set(SOURCE_FILES library.cpp library.h myitem.cpp myitem.h)
add_library(music_ui SHARED ${SOURCE_FILES})
target_link_libraries(music_ui Qt5::Widgets)
target_link_libraries(music_ui Qt5::Core)