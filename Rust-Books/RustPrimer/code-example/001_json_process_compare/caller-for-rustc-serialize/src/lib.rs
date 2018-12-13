// This crate is a library
#![crate_type = "lib"]

// Error: The library is named "caller_std_json" can't compile
// #![crate_name = "caller_std_json"]

pub fn lib_test() {
    println!("Hi! I'm here!");
}