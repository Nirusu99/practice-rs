use std::io::{stdin, stdout, Write};

use std::{error::Error, result::Result};

fn main() -> Result<(), Box<dyn Error>> {
    let mut buffer = String::new();
    stdin().read_line(&mut buffer)?;
    buffer = buffer
        .chars()
        .map(|c| match c {
            'r' => String::from("w"),
            'l' => String::from("w"),
            'o' => String::from("ow"),
            's' => String::from("sh"),
            'p' => String::from("pw"),
            _ => String::from(c),
        })
        .collect::<String>();
    stdout().write_all(buffer.as_bytes())?;
    Ok(())
}
