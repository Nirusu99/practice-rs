use std::cmp::Ordering;
use std::collections::BinaryHeap;
use std::error::Error;
use std::io::stdin;

#[derive(Debug, Eq, PartialEq, PartialOrd, Ord)]
struct Edge {
    node: usize,
    cost: i64,
}

#[derive(Debug, Copy, Clone, Eq, PartialEq)]
struct State {
    cost: i64,
    position: usize,
}
impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other
            .cost
            .cmp(&self.cost)
            .then_with(|| self.position.cmp(&other.position))
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let cv = read_input(String::new())?;
    for (i, c) in cv.iter().enumerate() {
        println!(
            "Case #{}: {}",
            i + 1,
            -dijkstra_algorithm(&c, 0, c.len() - 1).unwrap()
        );
    }
    Ok(())
}

/// (dijkstra)[https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm]
fn dijkstra_algorithm(m: &Vec<Vec<Edge>>, s: usize, e: usize) -> Option<i64> {
    let mut d = vec![i64::MAX; m.len()];
    let mut b_heap = BinaryHeap::new();

    d[s] = 0;
    b_heap.push(State {
        cost: 0,
        position: s,
    });

    while let Some(State {
        cost: c,
        position: p,
    }) = b_heap.pop()
    {
        if p == e {
            return Some(c);
        }

        if c > d[p as usize] {
            continue;
        }

        for edge in &m[p as usize] {
            let next = State {
                cost: c + edge.cost,
                position: edge.node,
            };

            if next.cost < d[next.position as usize] {
                b_heap.push(next);
                d[next.position] = next.cost;
            }
        }
    }
    None
}

fn read_input(mut input: String) -> Result<Vec<Vec<Vec<Edge>>>, Box<dyn Error>> {
    stdin().read_line(&mut input)?;
    let amount = input.trim().parse::<i64>()?;
    input.clear();
    let mut casess = vec![];
    for _ in 0..amount {
        let mut inptr = String::new();
        stdin().read_line(&mut inptr)?;
        let amv = inptr
            .trim()
            .split_whitespace()
            .map(|s| s.trim().parse::<i64>().unwrap())
            .collect::<Vec<i64>>();
        input.clear();
        let mut v = vec![];
        for _ in 0..amv[0] {
            v.push(vec![]);
        }
        for _ in 0..amv[1] {
            stdin().read_line(&mut input)?;
        }
        input
            .trim()
            .split("\n")
            .map(|line| {
                line.trim()
                    .split_whitespace()
                    .map(|str_num| str_num.trim().parse::<i64>().unwrap())
                    .collect::<Vec<i64>>()
            })
            .for_each(|num_v| {
                v[(num_v[0] - 1) as usize].push(Edge {
                    node: (num_v[1] - 1) as usize,
                    cost: -num_v[2],
                })
            });
        casess.push(v);
    }
    Ok(casess)
}
