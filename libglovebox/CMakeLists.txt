cmake_minimum_required(VERSION 2.8)
set(TARGET_GLOVEBOX glovebox)
set(LIBRARIES "")

# ==============
# = BUILD TYPE =
# ==============
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "DEBUG")
  #set(CMAKE_BUILD_TYPE "RELEASE")
  #set(CMAKE_BUILD_TYPE "RELWITHDEBINFO")
  #set(CMAKE_BUILD_TYPE "MINSIZEREL")
endif()

# ====================
# = MODULE INCLUSION =
# ====================
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake-modules")


# ====================
# = STATIC LIBRARIES =
# ====================

# Static library: libpd
subdirs("libpd")
include_directories("libpd/pure-data/src" "libpd/libpd_wrapper")
list(APPEND LIBRARIES pd dl m pthread)

# Static library: libARToolKitPlus (2.2.1)
subdirs("libARToolKitPlus")
include_directories("libARToolKitPlus/include")
list(APPEND LIBRARIES ARToolKitPlus)

# Static library: libofMath
subdirs("libofMath")
include_directories("libofMath")
list(APPEND LIBRARIES ofMath)

# =======================
# = GENERAL DEFINITIONS =
# =======================

# ================
# = SOURCE FILES =
# ================
set(SOURCES "src/glovebox.cpp" "src/audio_engine.cpp" "src/pd_engine.cpp" "src/system_audio.cpp" "src/pd_patch.cpp" "src/webcam_tracker.cpp" "src/gl_texture.cpp")
set_source_files_properties(${SOURCES} PROPERTIES COMPILE_FLAGS "-Wall")

# =======================================
# = PLATFORM-SPECIFIC OPTIONS AND FILES =
# =======================================
if(APPLE)
	# We must compile in 32bit since we need Quicktime legacy functionality
	set(CMAKE_OSX_ARCHITECTURES i386)
	set(CMAKE_CXX_FLAGS "-m32")
	# If you're on Lion, don't forget to change this variable !
	# set(CMAKE_OSX_SYSROOT /Developer/SDKs/MacOSX10.6.sdk)
	# We need to link against some nasty frameworks
	include_directories("/Developer/Headers/FlatCarbon")
	find_library(QUICKTIME_LIBRARY QuickTime)
	find_library(CARBON_LIBRARY Carbon)
	find_library(APP_SERVICES_LIBRARY ApplicationServices)
	find_library(CORE_SERVICES_LIBRARY CoreServices)
	mark_as_advanced(QUICKTIME_LIBRARY APP_SERVICES_LIBRARY CORE_SERVICES_LIBRARY CARBON_LIBRARY)
	list(APPEND LIBRARIES "${QUICKTIME_LIBRARY}" "${APP_SERVICES_LIBRARY}" "${CORE_SERVICES_LIBRARY}" "${CARBON_LIBRARY}")
	
	# There are sources that are OS X specific
	set(OSX_SOURCES "src/mac/qt_cameraman.cpp" "src/mac/qt_sequence_grabber.cpp")
	list(APPEND SOURCES ${OSX_SOURCES})
	# Don't show these deprecation warnings
	set_source_files_properties(${OSX_SOURCES} PROPERTIES COMPILE_FLAGS "-Wno-deprecated-declarations")
endif()

if(UNIX AND NOT APPLE)
	
endif()

if(WIN32)
	
endif()

# ===========================================
# = SHARED LIBRARIES AND OTHER REQUIREMENTS =
# ===========================================
# Requirement: Boost
find_package(Boost REQUIRED COMPONENTS python system filesystem)
include_directories(${Boost_INCLUDE_DIRS})
link_directories(${Boost_LIBRARY_DIRS})
list(APPEND LIBRARIES ${Boost_PYTHON_LIBRARY} ${Boost_FILESYSTEM_LIBRARY} ${Boost_SYSTEM_LIBRARY})
set(Boost_USE_STATIC_LIBS off)
# set(Boost_USE_MULTITHREADED on)
set(Boost_USE_STATIC_RUNTIME off)

# Requirement: Python
find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})
list(APPEND LIBRARIES ${PYTHON_LIBRARIES})

# Requirement: Portaudio
find_package(Portaudio REQUIRED)
include_directories(${PORTAUDIO_INCLUDE_DIRS})
list(APPEND LIBRARIES ${PORTAUDIO_LIBRARIES})

# Requirement: OpenGL
find_package(OpenGL REQUIRED)
include_directories(${OPENGL_INCLUDE_DIRS})
list(APPEND LIBRARIES ${OPENGL_LIBRARIES})

# ===================
# = TARGET SETTINGS =
# ===================
add_library(${TARGET_GLOVEBOX} SHARED ${SOURCES})
target_link_libraries(${TARGET_GLOVEBOX} ${LIBRARIES})

# ================
# = FINE TUNINGS =
# ================
if(APPLE)
	# For Python, the module has to be a .so
	set_target_properties(${TARGET_GLOVEBOX} PROPERTIES SUFFIX ".so")
endif()