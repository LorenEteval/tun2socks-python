cmake_minimum_required(VERSION 3.15)
project(tun2socks C CXX)

set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(
    TUN2SOCKS_GO_BUILD_DIR
    "${CMAKE_SOURCE_DIR}/gobuild"
    CACHE PATH
    "Directory containing the Go c-archive and generated header"
)

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(${PROJECT_NAME} src/tun2socks.cpp)

if (WIN32)
    if (MINGW)
        target_compile_options(${PROJECT_NAME} PRIVATE "-Wa,-mbig-obj")
        target_link_options(
            ${PROJECT_NAME} PRIVATE
            "-static-libgcc" "-static-libstdc++"
            "-Wl,-Bstatic,--whole-archive"
            "-lwinpthread"
            "-Wl,--no-whole-archive"
        )
    endif ()

    target_link_libraries(
        ${PROJECT_NAME} PRIVATE
        ${TUN2SOCKS_GO_BUILD_DIR}/tun2socks.lib
    )
else ()
    target_link_libraries(
        ${PROJECT_NAME} PRIVATE
        ${TUN2SOCKS_GO_BUILD_DIR}/tun2socks.a
        "-lresolv"
    )

    if (APPLE)
        target_link_libraries(
            ${PROJECT_NAME} PRIVATE
            "-framework CoreFoundation"
            "-framework Security"
        )
    endif ()
endif ()

target_include_directories(${PROJECT_NAME} PRIVATE ${TUN2SOCKS_GO_BUILD_DIR})
