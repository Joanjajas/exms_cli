mod cli;

use std::process;

use anyhow::Result;
use clap::Parser;
use cli::{Cli, Command};
use colored::Colorize;
use exms::exam::Exam;

fn main() {
    // Load command line options
    let options = Cli::parse();

    // Handle application error
    if let Err(err) = run(options) {
        eprintln!("{}: {} ", "[exms error]".red(), err);
        process::exit(1);
    };
}

fn run(options: Cli) -> Result<()> {
    match options.command {
        Command::Summary(args) => {
            let mut exam = Exam::from_file(&args.file)?;

            if let Some(max_grade) = args.max_grade {
                exam.set_max_grade(max_grade);
            }

            exam.summary();
            exam.histogram(args.step);

            if args.sort_by_grade {
                exam.sort_by_grade();
            }

            if args.sort_by_alphabetic_order {
                exam.sort_by_alphabetic_order();
            }

            if let Some(names) = &args.name_filter {
                exam.filter_by_name(names);
            }

            if let Some(files) = &args.file_filter {
                exam.filter_by_file(files)?;
            }

            exam.students();
        }

        Command::Download(args) => {
            std::process::Command::new("python3")
                .arg("/usr/local/scraper/scraper.py")
                .arg(&args.path)
                .status()?;
        }
    }

    Ok(())
}
