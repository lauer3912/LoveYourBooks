cmake_minimum_required(VERSION 3.13)

# Add path for custom modules
# 添加自定义CMake的modules来处理扩展内容
set(CMAKE_MODULE_PATH
        ${CMAKE_MODULE_PATH}
        ${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules
        )

# 设置工程名称
project(two-sum)

# 设置使用的C++标准
set(CMAKE_CXX_STANDARD 14)

include(BrewHelper)
find_package(benchmark REQUIRED)

find_brew_prefix(GBENCHMARK_PREFIX google-benchmark)
message(${GBENCHMARK_PREFIX})

# 添加头文件及库的依赖环境
include_directories(
        #`$(brew --prefix google-benchmark)`/include
        #"/usr/local/opt/google-benchmark/include"
        "${GBENCHMARK_PREFIX}/include"
)

link_directories(
        "/usr/local/opt/google-benchmark/lib"
        #$(GBENCHMARK_DIR)/lib
)

# 由于libbenchmark.a google生成的一般使用静态库的方式，所以要采用link_libraries
# link_library 是用来链接静态库的
link_libraries(libbenchmark.a)



# 添加可执行文件
add_executable(two-sum
        main.cpp)


# 动态库链接方式，要使用 target_link_libraries， 而且 target_link_libraries 必须放到 add_executable 之后
#

