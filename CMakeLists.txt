cmake_minimum_required(VERSION 3.18)
project(termux-gui-pm)



add_custom_command(
    OUTPUT termux-gui-pm
    COMMAND python3 -m zipapp -o ${CMAKE_CURRENT_BINARY_DIR}/termux-gui-pm -p "/usr/bin/env python3" -c ${CMAKE_CURRENT_SOURCE_DIR}/src/
    DEPENDS
        src/res/icon.png
        src/__main__.py
        src/activity.py
        src/apt.py
        src/install_layout.py
        src/install_progress_layout.py
        src/mainlayout.py
        src/pm.py
        src/pms.py
        src/proot_distro.py
        src/uninstall_layout.py
        src/uninstall_progress_layout.py
        src/update_layout.py
        src/upgrade_layout.py
    VERBATIM
)

add_custom_target(pm ALL DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/termux-gui-pm)

install(PROGRAMS ${CMAKE_CURRENT_BINARY_DIR}/termux-gui-pm TYPE BIN)

