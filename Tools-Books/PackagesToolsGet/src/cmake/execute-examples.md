# 可执行文件的配置 CMakeLists.txt

明确要构建的是一个可执行文件，需要通过`add_executable`来指定。

## 构建方式

```bash
# 定位到C++工程目录
cd ~/linear-algebra

# 先删除生成的cmake-build-*. 这里包括cmake-build-debug 和 cmake-build-release
rm -fr ./cmake-build-*

# 先生成makefile
# -S 用来指定CMakeLists.txt的位置; -B 说明构建输出, 相对于输出来说:
# 以下两种做法都可以得到：
# 做法1：进入~/linear-algebra/cmake-build-debug 目录，然后再执行
mkdir cmake-build-debug && cd cmake-build-debug
cmake -DCMAKE_BUILD_TYPE=Debug -G "CodeBlocks - Unix Makefiles" -S ../ -B ../cmake-build-debug

# 做法2：进入~/linear-algebra目录
cd ~/linear-algebra
cmake -DCMAKE_BUILD_TYPE=Debug -G "CodeBlocks - Unix Makefiles" -S ./ -B ./cmake-build-debug

# 再执行构建命令
cmake --build ./cmake-build-debug --target linear_algebra -- -j 2

# 如果构建没有问题，尝试测试执行情况
./cmake-build-debug/linear_algebra

# 以上内容完毕
```

## 最优例子

```c
cmake_minimum_required(VERSION 3.13)

####################################################
# Use brew? or use vcpkg?
set(UD_USE_VCPKG false)
set(UD_USE_BREW true)

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
```

## 例子 1

```c
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

# Setting the executable
add_executable(${PROJECT_NAME} main.cpp)

# Adding the link libraries
target_link_libraries(${PROJECT_NAME} armadillo)

```

## 例子 2

```c
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

# Adding the link libraries
target_link_libraries(${PROJECT_NAME} armadillo)
```

例子 3：

```c
cmake_minimum_required(VERSION 3.13)

####################################################
# Use brew? or use vcpkg?
set(UD_USE_VCPKG false)
set(UD_USE_BREW true)

if(UD_USE_VCPKG)
    # https://vcpkg.readthedocs.io/en/latest/users/integration/
    #if(DEFINED ENV{VCPKG_ROOT} AND NOT DEFINED CMAKE_TOOLCHAIN_FILE)
    if(DEFINED ENV{VCPKG_ROOT})
        set(VCPKG_ROOT "$ENV{VCPKG_ROOT}")
        message(STATUS "VCPKG_ROOT=${VCPKG_ROOT}")
        set(CMAKE_TOOLCHAIN_FILE "${VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake" CACHE FILEPATH "")
    endif()
endif()

####################################################
set(CMAKE_CXX_STANDARD 17)
#set(CMAKE_CXX_STANDARD_REQUIRED OFF)
#set(CMAKE_CXX_EXTENSIONS OFF)

message(STATUS "CMAKE_TOOLCHAIN_FILE=${CMAKE_TOOLCHAIN_FILE}")
message(STATUS "VCPKG_TARGET_ARCHITECTURE=${VCPKG_TARGET_ARCHITECTURE}")
message(STATUS "VCPKG_PLATFORM_TOOLSET=${VCPKG_PLATFORM_TOOLSET}")

# project
project(linear_algebra)

# setting the target output path
set(executable_output_path ${PROJECT_SOURCE_DIR}/build/bin)
set(library_output_path ${PROJECT_SOURCE_DIR}/build/lib)

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
# include_directories(${ARMADILLO_INCLUDE_DIR})

# Get packages
find_package(armadillo REQUIRED)
#find_package(eigen REQUIRED)

# Setting the source code directories
aux_source_directory(./src/ DIR_SRCS)

# Setting the executable
#add_executable(${PROJECT_NAME} ${DIR_SRCS})
add_executable(${PROJECT_NAME} ./src/main.cpp ./src/ArmadilloHelper.cpp ./src/EigenHelper.cpp)

# Adding the link libraries
target_link_libraries(${PROJECT_NAME} armadillo)
```
