cmake_minimum_required(VERSION 3.13)

# https://vcpkg.readthedocs.io/en/latest/users/integration/
#if(DEFINED ENV{VCPKG_ROOT} AND NOT DEFINED CMAKE_TOOLCHAIN_FILE)
if(DEFINED ENV{VCPKG_ROOT})
    set(VCPKG_ROOT "$ENV{VCPKG_ROOT}")
    message(STATUS "VCPKG_ROOT=${VCPKG_ROOT}")
    set(CMAKE_TOOLCHAIN_FILE "${VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake" CACHE FILEPATH "")
endif()

set(CMAKE_CXX_STANDARD 17)
#set(CMAKE_CXX_STANDARD_REQUIRED OFF)
#set(CMAKE_CXX_EXTENSIONS OFF)

message(STATUS "CMAKE_TOOLCHAIN_FILE=${CMAKE_TOOLCHAIN_FILE}")
message(STATUS "VCPKG_TARGET_ARCHITECTURE=${VCPKG_TARGET_ARCHITECTURE}")
message(STATUS "VCPKG_PLATFORM_TOOLSET=${VCPKG_PLATFORM_TOOLSET}")

# project
project(linear_algebra)

# Use brew? or use vcpkg?
set(UD_USE_VCPKG false)
set(UD_USE_BREW true)

if(${UD_USE_BREW})
    set(ARMADILLO_LIBRARY "$(brew --prefix armadillo)/lib")
    set(ARMADILLO_INCLUDE_DIR "$(brew --prefix armadillo)/include")
endif()

if(${UD_USE_VCPKG})
    set(ARMADILLO_LIBRARY "${VCPKG_ROOT}/packages/armadillo_x64-osx/lib")
    set(ARMADILLO_INCLUDE_DIR "${VCPKG_ROOT}/packages/armadillo_x64-osx/include")

    include_directories(${VCPKG_ROOT}/installed/x64-osx/include)
endif()

# Includes
include_directories(${ARMADILLO_INCLUDE_DIR})

# Get packages
find_package(armadillo REQUIRED)

# Setting the source code directories
aux_source_directory(./src DIR_SRCS)

# Setting the executable
add_executable(${PROJECT_NAME} ${DIR_SRCS})

#NOTE: Use static link for armadillo, so don't use follow code.
target_link_libraries(${PROJECT_NAME} armadillo)