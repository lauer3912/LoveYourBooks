// Copyright 2018 
//
// Licensed under the Apache License, Version 2.0


//! # JSON Process Compare
//! Example for JSON

extern crate caller_for_serde_json;

// Note: The old name of the crate is "caller-for-rustc-serialize"
// Auto converted to "caller_for_rustc_serialize" by rust compiler.
extern crate caller_for_rustc_serialize as caller_std_json;

fn main() {
    println!("Hello, world!");

    caller_for_serde_json::sample::run_example();
    caller_for_serde_json::value_json::main();
    caller_for_serde_json::use_macro::main();

    caller_std_json::lib_test();
}
