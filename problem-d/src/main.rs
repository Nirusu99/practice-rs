use std::{collections::HashSet, error::Error, io::stdin};

fn main() -> Result<(), Box<dyn Error>> {
    let mut input = String::new();
    read_input(&mut input)?;

    input
        .trim()
        .split("\n")
        .map(|s| s.split_whitespace().collect::<Vec<&str>>())
        .for_each(|arr| {
            let mut steps = 0;
            let mut word = arr[0].chars().collect::<HashSet<char>>();
            arr[1].chars().for_each(|c| {
                steps += 1;
                if word.remove(&c) && word.is_empty() {
                    println!("{}", steps);
                }
            });
        });
    Ok(())
}

fn read_input(input: &mut String) -> Result<(), Box<dyn Error>> {
    stdin().read_line(input)?;
    let amount = input.trim().parse::<u32>()?;
    input.clear();
    for _ in 0..amount {
        stdin().read_line(input)?;
    }
    Ok(())
}
