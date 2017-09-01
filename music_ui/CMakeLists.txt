cmake_minimum_required(VERSION 3.7)
project(music_ui)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
set(EXECUTABLE_OUTPUT_PATH "../")

#查找Qt的库
find_package(Qt5Widgets)
find_package(Qt5Gui)
find_package(Qt5Core)
find_package(PythonLibs 3.5 REQUIRED)

set(SOURCE_FILES library.cpp library.h cpp/component.h cpp/component.cpp main.cpp Interface.cpp Interface.h cpp/components/WButton.cpp cpp/components/WButton.h cpp/components/ProgressBar.cpp cpp/components/ProgressBar.h)
add_executable(music_ui ${SOURCE_FILES})
target_link_libraries(music_ui Qt5::Widgets)
target_link_libraries(music_ui Qt5::Gui)
target_link_libraries(music_ui Qt5::Core)
target_link_libraries(music_ui python3.5m)