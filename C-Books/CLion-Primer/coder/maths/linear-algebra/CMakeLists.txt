cmake_minimum_required(VERSION 3.13)

####################################################
# Use brew? or use vcpkg?
option(UD_USE_VCPKG "use vcpkg toolchain" OFF)
option(UD_USE_BREW "use brew toolchain" ON)

if(UD_USE_VCPKG)
    # https://vcpkg.readthedocs.io/en/latest/users/integration/
    #if(DEFINED ENV{VCPKG_ROOT} AND NOT DEFINED CMAKE_TOOLCHAIN_FILE)
    if(DEFINED ENV{VCPKG_ROOT})
        set(VCPKG_ROOT "$ENV{VCPKG_ROOT}")
        message(STATUS "VCPKG_ROOT=${VCPKG_ROOT}")
        set(CMAKE_TOOLCHAIN_FILE "${VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake" CACHE FILEPATH "")

        message(STATUS "VCPKG_TARGET_ARCHITECTURE=${VCPKG_TARGET_ARCHITECTURE}")
        message(STATUS "VCPKG_PLATFORM_TOOLSET=${VCPKG_PLATFORM_TOOLSET}")
    endif()
endif()

####################################################
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

message(STATUS "CMAKE_TOOLCHAIN_FILE=${CMAKE_TOOLCHAIN_FILE}")

# project
project(linear_algebra)

####################################################
if(UD_USE_BREW)
    message(STATUS "Using Homebrew ...")
    set(ARMADILLO_LIBRARY "$(brew --prefix armadillo)/lib")
    set(ARMADILLO_INCLUDE_DIR "$(brew --prefix armadillo)/include")

    set(EIGEN_LIBRARY "$(brew --prefix eigen)/lib")
    set(EIGEN_INCLUDE_DIR "$(brew --prefix eigen)/include")
else()
    message(STATUS "XXXX Not Using Homebrew ...")
endif()

if(UD_USE_VCPKG)
    message(STATUS "Using vcpkg ...")
    set(ARMADILLO_LIBRARY "${VCPKG_ROOT}/packages/armadillo_x64-osx/lib")
    set(ARMADILLO_INCLUDE_DIR "${VCPKG_ROOT}/packages/armadillo_x64-osx/include")

    include_directories(${VCPKG_ROOT}/installed/x64-osx/include)
else()
    message(STATUS "XXXX Not Using vcpkg ...")
endif()

####################################################
# Includes
include_directories(${ARMADILLO_INCLUDE_DIR})

# Get packages
find_package(Armadillo REQUIRED)

# Setting the source code directories
aux_source_directory(./src/ DIR_SRCS)

# Setting the executable
add_executable(${PROJECT_NAME} ${DIR_SRCS})

# Adding the link libraries
target_link_libraries(${PROJECT_NAME} ${ARMADILLO_LIBRARIES})