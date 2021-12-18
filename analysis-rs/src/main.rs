use pbr::ProgressBar;
use rayon::prelude::*;
use std::collections::HashMap;
use std::error::Error;
use std::fs::{canonicalize, read_dir, read_to_string};
use std::io::{stdin, stdout, Write};
use std::path::PathBuf;

const IGNORED_WORDS: &'static [&'static str] = &[
    "", "ab", "aber", "alle", "aller", "als", "am", "an", "auch", "auf", "aus", "bei", "beim",
    "bereits", "bis", "dabei", "das", "dass", "dem", "den", "der", "des", "die", "doch", "durch",
    "ein", "eine", "einem", "einen", "einer", "er", "es", "fast", "für", "gegen", "gibt", "haben",
    "hat", "ihm", "ihr", "im", "in", "ist", "laut", "mehr", "mit", "nach", "nicht", "noch", "nun",
    "nur", "sein", "seine", "seinen", "seiner", "sei", "seit", "sich", "sie", "sind", "so", "soll",
    "um", "und", "vom", "von", "vor", "war", "was", "wegen", "wer", "werden", "wie", "wieder",
    "will", "wird", "wo", "zu", "zum", "zur", "über",
];

fn main() -> Result<(), Box<dyn Error>> {
    let mut input = String::new();
    take_input(&mut input, "Enter path of directory to evaluate: ")?;
    let path = canonicalize(&PathBuf::from(input.trim()))?;
    println!();
    let articles = read_files(&path)?;
    println!("\n\nComputing statistics...\n");
    let articles: Vec<&str> = articles.par_iter().map(|s| remove_header(&s)).collect();
    let mut split_articles = vec![];
    articles
        .par_iter()
        .map(|a| article_to_words(a))
        .collect_into_vec(&mut split_articles);
    let word_maps = split_articles
        .par_iter()
        .map(|a| count_words(a))
        .collect::<Vec<HashMap<&str, usize>>>();
    let mut words = HashMap::new();
    for map in word_maps.iter() {
        merge_with_plus(&mut words, map);
    }
    let top = sort_by_value(&words);
    let top_amount = if top.len() < 10 { top.len() } else { 10 };
    let mut corr: HashMap<&str, HashMap<&str, usize>> = HashMap::new();
    split_articles
        .iter()
        .for_each(|a| correlated_words(&mut corr, a));

    println!("Top {top_amount} words:");
    for i in 1..(top_amount + 1) {
        let (amount, word) = top.get(top.len() - i).unwrap();
        println!("  {word} ({amount} times)");
    }
    take_input(&mut input, "\n> ")?;
    while input != ":quit\n" {
        let inp_word = input.trim();
        compute_output(&corr, &words, inp_word);
        take_input(&mut input, "\n> ")?;
    }
    println!("Good bye!");
    Ok(())
}

fn take_input(input: &mut String, prompt: &str) -> Result<usize, std::io::Error> {
    print!("{}", prompt);
    stdout().flush()?;
    input.clear();
    stdin().read_line(input)
}

fn compute_output(
    corr: &HashMap<&str, HashMap<&str, usize>>,
    words: &HashMap<&str, usize>,
    inp_word: &str,
) {
    match corr.get(inp_word) {
        Some(entry) => {
            let sorted = sort_by_value(&entry);
            let max = if sorted.len() < 10 { sorted.len() } else { 10 };
            println!(
                "The word '{}' was found {} times.",
                inp_word,
                words.get(inp_word).unwrap()
            );
            println!("Top {max} correlations:");
            for i in 1..(max + 1) {
                let (amount, word) = sorted.get(sorted.len() - i).unwrap();
                println!("  {inp_word} {word} ({amount} times)");
            }
        }
        None => println!("Nothing found"),
    };
}

fn read_files(path: &PathBuf) -> Result<Vec<String>, Box<dyn Error>> {
    let mut files = vec![];
    if path.is_dir() {
        let count = read_dir(path)?.count();
        let mut pb = ProgressBar::new(count as u64);
        pb.message("Reading files: ");
        for file in read_dir(path)? {
            let path = file?.path();
            if path.is_file() {
                files.push(read_to_string(&path)?);
                pb.inc();
            }
        }
        pb.finish();
    } else {
        println!("Reading article");
        files.push(read_to_string(path)?)
    }

    Ok(files)
}

fn remove_header<'a>(article: &'a str) -> &'a str {
    article
        .split_once("\n\n")
        .expect(&format!(
            "Couldn't split article at empty line: {:#?}",
            article
        ))
        .1
}

fn normalize_word(word: &str) -> String {
    word.chars()
        .filter(|c| c.is_alphabetic())
        .collect::<String>()
        .to_lowercase()
}

fn article_to_words(article: &str) -> Vec<String> {
    article
        .split_whitespace()
        .map(|s| normalize_word(s))
        .filter(|w| !IGNORED_WORDS.contains(&w.as_str()))
        .collect()
}

fn count_words(article: &Vec<String>) -> HashMap<&str, usize> {
    article
        .par_iter()
        .map(|s| (s.as_str(), article.par_iter().filter(|a| a == &s).count()))
        .collect()
}

fn merge_with_plus<'a>(d1: &mut HashMap<&'a str, usize>, d2: &HashMap<&'a str, usize>) {
    d2.iter().for_each(|(k, v)| *d1.entry(k).or_insert(0) += v);
}

fn sort_by_value<'a>(d: &'a HashMap<&'a str, usize>) -> Vec<(&'a usize, &'a str)> {
    let mut vec = Vec::from_par_iter(d.par_iter().map(|(k, v)| (v, *k)));
    vec.sort_by(|a, b| a.0.partial_cmp(b.0).unwrap());
    vec
}

fn correlated_words<'a>(d: &mut HashMap<&'a str, HashMap<&'a str, usize>>, words: &'a Vec<String>) {
    words.iter().for_each(|word| {
        words.iter().filter(|w| w != &word).for_each(|w| {
            *d.entry(word)
                .or_insert(HashMap::new())
                .entry(w)
                .or_insert(0) += 1
        })
    });
}
