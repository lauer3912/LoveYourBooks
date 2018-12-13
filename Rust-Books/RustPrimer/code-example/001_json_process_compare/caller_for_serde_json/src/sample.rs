
#[derive(Serialize, Deserialize, Debug)]
struct Point {
    x: i32,
    y: i32,
}


pub fn run_example() {
    let point = Point {
        x: 1,
        y: 50,
    };

    // Convert the point to a JSON string.
    let serialized = serde_json::to_string(&point).unwrap();

    // Prints serialized = {"x":1,"y": 50}
    println!("serialized = {}", serialized);

    // Convert the JSON string back to a Point.
    let deserialized: Point = serde_json::from_str(&serialized).unwrap();

    // Prints deserialized = Point { x: 1, y: 50}
    println!("deserialized = {:?}", deserialized);
}