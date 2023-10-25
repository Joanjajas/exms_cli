use indexmap::IndexMap;
use std::error::Error;
use std::path::{Path, PathBuf};
use std::{env, process};
use std::{fs, fs::File};
use std::{io, io::Write};

fn main() {
    if let Err(e) = run() {
        eprintln!("error: {}", e);
        process::exit(1)
    }
}

fn run() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        return Err("File path required".into());
    }

    let mut file_path = PathBuf::from(&args[1]);

    if file_path.extension().is_some() {
        return Err("File path must not have an extension".into());
    }

    let students = parse_file(&file_path)?;
    let toml_str = toml::to_string(&students)?;

    fs::remove_file(&file_path)?;

    file_path.set_extension("toml");
    let mut file = File::create(&file_path)?;

    file.write_all(b"[students]\n")?;
    file.write_all(toml_str.as_bytes())?;

    Ok(())
}

fn parse_file<P: AsRef<Path>>(path: P) -> Result<IndexMap<String, f32>, io::Error> {
    // Read file content into a String
    let file_content = fs::read_to_string(path)?;

    // Create an empty vector to store the parsed students
    let mut students = IndexMap::new();

    for line in file_content.lines() {
        // Replace all tab characters with spaces
        let line = line.replace('\t', " ");
        let line = line.trim();

        // Split the line into two parts, separating the name from the grade
        let mut r_line_split = line.rsplitn(2, ' ');

        // Get the grade string from the end of the line
        let Some(grade_str) = r_line_split.next() else {
            continue;
        };

        // Parse the grade string into a f32
        let Ok(grade) = grade_str.replace(',', ".").parse() else {
            continue;
        };

        // Collect the rest of the line as a String
        let name: String = r_line_split.collect();

        // Create new Student instance with the parsed name and grade
        students.insert(name, grade);
    }

    Ok(students)
}
