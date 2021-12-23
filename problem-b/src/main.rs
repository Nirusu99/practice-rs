use std::{error::Error, io::stdin, ops::Sub};

#[derive(Debug, Copy, Clone, PartialEq, Eq, Ord, PartialOrd)]
struct Date {
    date: (u32, u32, u32),
}

impl From<&str> for Date {
    fn from(v: &str) -> Self {
        let v = v
            .split_whitespace()
            .map(|p| p.parse::<u32>().unwrap())
            .collect::<Vec<u32>>();
        Date {
            date: (v[2], v[1], v[0]),
        }
    }
}

impl Sub for Date {
    type Output = u32;

    fn sub(self, other: Self) -> Self::Output {
        if (self.date.1, self.date.2) < (other.date.1, other.date.2) {
            return self.date.0 - other.date.0 - 1;
        }
        self.date.0 - other.date.0
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut input = String::new();
    read_input(&mut input)?;

    let mut input: Vec<&str> = input.trim().split("\n\n").collect();
    let input = input
        .iter_mut()
        .map(|s| s.split("\n").collect::<Vec<&str>>())
        .map(|v| (Date::from(v[0]), Date::from(v[1])))
        .collect::<Vec<(Date, Date)>>();
    let mut i = 1;
    for person in input.iter() {
        let s = format!("Person #{}: ", i);
        i = i + 1;
        match person {
            (date1, date2) if date2 > date1 => println!("{}Ungueltiges Geburtsdatum", s),
            (date1, date2) if *date1 - *date2 > 130 => println!("{}Zu alt", s),
            (date1, date2) => println!("{}{}", s, *date1 - *date2),
        };
    }
    Ok(())
}

fn read_input(input: &mut String) -> Result<(), Box<dyn Error>> {
    stdin().read_line(input)?;
    let amount = input.trim().parse::<u32>()?;
    input.clear();
    for _ in 0..amount {
        for _ in 0..3 {
            stdin().read_line(input)?;
        }
    }
    Ok(())
}
