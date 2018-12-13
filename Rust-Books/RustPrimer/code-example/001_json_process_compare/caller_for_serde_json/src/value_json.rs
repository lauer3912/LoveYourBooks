extern crate serde_json;

use serde_json::{Value, Error};

fn untyped_example() -> Result<(), Error> {
 // Some JSON input data as a &str. Maybe this comes from the user.
 let data = r#"{
                 "name": "John Doe",
                 "age": 43,
                 "phones": [
                   "+44 1234567",
                   "+44 2345678"
                 ]
               }"#;

 // Parse the string of data into serde_json::Value.
 let v: Value = serde_json::from_str(data)?;

 // Access parts of the data by indexing with square brackets.
 println!("Please call {} at the number {}", v["name"], v["phones"][0]);

 Ok(())
}

pub fn main() {
     untyped_example().unwrap();
}