cmake_minimum_required(VERSION 2.8)
project(ofMath)

set(OFMATH_SOURCE_DIR ${PROJECT_SOURCE_DIR})

# ofMath core files
file(GLOB SOURCES_OFMATH
	${OFMATH_SOURCE_DIR}/*.cpp
	)

add_library(ofMath STATIC ${SOURCES_OFMATH})