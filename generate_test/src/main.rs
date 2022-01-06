use std::io::prelude::*;
use std::{error::Error, fs::File};

use pbr::ProgressBar;
use rand::Rng;

fn main() -> Result<(), Box<dyn Error>> {
    let mut mock_str = String::new();

    let mut rng = rand::thread_rng();
    let mut file = File::create("sample")?;

    let mut pb = ProgressBar::new(1000 as u64);
    pb.message("Creating fields ");
    mock_str.push_str("1000");
    for _ in 0..1000 {
        mock_str.push_str("\n200 200");
        for _ in 0..200 {
            mock_str.push('\n');
            for _ in 0..200 {
                if rng.gen() {
                    mock_str.push('*');
                } else {
                    mock_str.push('.');
                }
            }
        }
        pb.inc();
    }
    pb.finish();
    file.write_all(mock_str.as_bytes())?;
    Ok(())
}
