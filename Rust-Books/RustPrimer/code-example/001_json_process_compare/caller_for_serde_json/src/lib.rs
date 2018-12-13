// Copyright 2018
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/licenses/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option. This file may not be copied, modified, or distributed
// except according to those terms.


//! # Use Serde JSON to read json struct data
//! Example for JSON
//! Rust language Version 1.31 (2018)
//! The Serde JSON You can visit their official website: [serde.rs](https://serde.rs)
//!
extern crate serde;
#[macro_use] extern crate serde_derive;
#[macro_use] extern crate serde_json;


//
pub mod sample;
pub mod value_json;

// Announce:
#[cfg(feature = "raw_value")]
pub mod use_macro;
