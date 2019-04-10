cmake_minimum_required(VERSION 3.13)
project(001_json_process_compare)

set(CMAKE_CXX_STANDARD 14)

add_executable(001_json_process_compare
        caller-for-rustc-serialize/src/lib.rs
        caller-for-rustc-serialize/Cargo.toml
        caller_for_serde_json/src/lib.rs
        caller_for_serde_json/src/sample.rs
        caller_for_serde_json/src/use_macro.rs
        caller_for_serde_json/src/value_json.rs
        caller_for_serde_json/Cargo.toml
        src/main.rs
        Cargo.lock
        Cargo.toml
        config)
