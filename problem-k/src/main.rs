use std::{collections::HashMap, error::Error, io::stdin};

fn main() -> Result<(), Box<dyn Error>> {
    let cas = read_input(String::new())?;
    let best = cas
        .iter()
        .map(|c| calc_best(c.0, &c.1))
        .collect::<Vec<u64>>();
    for i in 0..best.len() {
        println!("Case #{}: {}", i + 1, best[i]);
    }
    Ok(())
}

fn calc_best(mut h: u64, v: &Vec<(u64, u64, u64)>) -> u64 {
    let mut fun_ratios = calc_fun_ratio(v);
    fun_ratios
        .iter_mut()
        // TODO: this is propably going to explode
        .for_each(|(_, v)| v.sort_by(|a, b| b.partial_cmp(a).unwrap()));
    let mut val: u64 = 0;
    while h > 1 {
        let i = best_path(h, v, &fun_ratios);
        let b = v[i];
        val += b.2;
        h -= b.1 - b.0;
    }
    val
}

fn best_path(h: u64, v: &Vec<(u64, u64, u64)>, m: &HashMap<u64, Vec<(f64, usize)>>) -> usize {
    let poss = m.get(&h).expect("What the fuck?");
    let best = v[poss[0].1];
    if best.1 - best.0 == 1 {
        return poss[0].1;
    //} else if h > best.1 - best.0) {
    } else {
        let mut sh = h - 1;
        let mut val: u64 = 0;
        // TODO: I think this could be full recursive
        while sh > (h - (best.1 - best.0)) {
            let i = best_path(sh, v, m);
            let b = v[i];
            val += b.2;
            sh -= b.1 - b.0;
        }
        if val > best.2 {
            return best_path(sh - 1, v, m);
        } else {
            return poss[0].1;
        }
    }
}

fn calc_fun_ratio(v: &Vec<(u64, u64, u64)>) -> HashMap<u64, Vec<(f64, usize)>> {
    let mut map = HashMap::new();
    v.iter()
        .enumerate()
        .map(|en| (en.1 .2 as f64 / (en.1 .1 - en.1 .0) as f64, en.1 .1, en.0))
        .for_each(|tup| map.entry(tup.1).or_insert(Vec::new()).push((tup.0, tup.2)));
    map
}

fn read_input(mut input: String) -> Result<Vec<(u64, Vec<(u64, u64, u64)>)>, Box<dyn Error>> {
    stdin().read_line(&mut input)?;
    let amount = input.trim().parse::<u64>()?;
    input.clear();
    let mut casess = vec![];
    for _ in 0..amount {
        let mut inptr = String::new();
        stdin().read_line(&mut inptr)?;
        let amv = inptr
            .trim()
            .split_whitespace()
            .map(|s| s.parse::<u64>().unwrap())
            .collect::<Vec<u64>>();
        input.clear();
        for _ in 0..amv[1] {
            stdin().read_line(&mut input)?;
        }
        casess.push((
            amv[0],
            input
                .trim()
                .split("\n")
                .map(|s| {
                    s.split_whitespace()
                        .map(|s2| s2.parse::<u64>().unwrap())
                        .collect::<Vec<u64>>()
                })
                .map(|v| (v[0], v[1], v[2]))
                .collect(),
        ))
    }
    Ok(casess)
}
