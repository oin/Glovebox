cmake_minimum_required(VERSION 2.8)
project(ARToolKitPlus)

if(WIN32)
	add_definitions(-D_CRT_SECURE_NO_WARNINGS -DAR_LIBRARY)
else(WIN32)
    add_definitions(-Wall -g -O3)
endif(WIN32)

add_definitions(-arch i386 -m32)

set(AR_SOURCE_DIR ${PROJECT_SOURCE_DIR})
include_directories(${AR_SOURCE_DIR}/include)

# ARToolkitPlus core files (headers and sources)
file(GLOB_RECURSE HEADERS_AR ${AR_SOURCE_DIR}/include/ARToolKitPlus/*.h)
file(GLOB SOURCES_AR
	${AR_SOURCE_DIR}/src/*.cpp
	${AR_SOURCE_DIR}/src/core/*.cpp
	${AR_SOURCE_DIR}/src/extra/*.cpp
	${AR_SOURCE_DIR}/src/librpp/*.cpp
	)

add_library(ARToolKitPlus STATIC ${HEADERS_AR} ${SOURCES_AR})