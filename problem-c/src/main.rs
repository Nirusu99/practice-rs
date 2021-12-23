use std::{error::Error, io::stdin};

#[derive(Debug)]
enum Field {
    Mine,
    NotMine,
}

impl ToString for Field {
    fn to_string(&self) -> String {
        match self {
            Field::Mine => "*".to_string(),
            Field::NotMine => ".".to_string(),
        }
    }
}

impl Field {
    fn to_field(&self, value: u32) -> String {
        match self {
            Field::Mine => "*".to_string(),
            Field::NotMine => value.to_string(),
        }
    }

    fn is_mine(&self) -> bool {
        match self {
            Field::Mine => true,
            _ => false,
        }
    }
}

impl From<char> for Field {
    fn from(s: char) -> Self {
        match s {
            '*' => Field::Mine,
            _ => Field::NotMine,
        }
    }
}

#[derive(Debug)]
struct MineField {
    board: Vec<Vec<Field>>,
}

impl ToString for MineField {
    fn to_string(&self) -> String {
        let mut out = String::new();
        for x in 0..self.board.len() {
            for y in 0..self.board[x].len() {
                out.push_str(&self.board[x][y].to_field(self.calc_value(x, y)));
            }
            out.push('\n');
        }

        out
    }
}

impl MineField {
    fn calc_value(&self, x: usize, y: usize) -> u32 {
        let mut value = 0;
        let offsets: [(i32, i32); 4] = [(-1, 0), (1, 0), (0, -1), (0, 1)];
        for (dx, dy) in offsets {
            if x as i32 + dx >= 0 && y as i32 + dy >= 0 {
                value += self
                    .board
                    .get((x as i32 + dx) as usize)
                    .map(|v| v.get((y as i32 + dy) as usize).unwrap_or(&Field::NotMine))
                    .map_or(0, |f| f.is_mine() as u32);
            }
        }
        let offsets: [(i32, i32); 4] = [(-1, 1), (1, -1), (-1, -1), (1, 1)];
        for (dx, dy) in offsets {
            if x as i32 + dx >= 0 && y as i32 + dy >= 0 {
                value += self
                    .board
                    .get((x as i32 + dx) as usize)
                    .map(|v| v.get((y as i32 + dy) as usize).unwrap_or(&Field::NotMine))
                    .map_or(0, |f| f.is_mine() as u32);
            }
        }

        value
    }
}

impl From<&str> for MineField {
    fn from(s: &str) -> Self {
        Self {
            board: s
                .trim()
                .split("\n")
                .map(|s| s.chars())
                .map(|vc| vc.map(|c| Field::from(c)).collect::<Vec<Field>>())
                .collect::<Vec<Vec<Field>>>(),
        }
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut input = String::new();
    read_input(&mut input)?;
    input
        .trim()
        .split("---")
        .map(|s| MineField::from(s))
        .for_each(|b| println!("{}", b.to_string()));
    Ok(())
}

fn read_input(input: &mut String) -> Result<(), Box<dyn Error>> {
    stdin().read_line(input)?;
    let amount = input.trim().parse::<u32>()?;
    input.clear();
    for i in 0..amount {
        let mut inptr = String::new();
        stdin().read_line(&mut inptr)?;
        let amount2 = inptr
            .trim()
            .split_whitespace()
            .map(|s| s.parse::<i32>().unwrap())
            .collect::<Vec<i32>>()[0];
        if i > 0 {
            input.push_str("---");
        }
        for _ in 0..amount2 {
            stdin().read_line(input)?;
        }
    }
    Ok(())
}
