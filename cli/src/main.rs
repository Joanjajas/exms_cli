mod cli;

use std::process;

use clap::Parser;
use cli::Options;
use colored::Colorize;
use exms::error::ParseError;
use exms::exam::Exam;

fn main() {
    // Load command line options
    let options = Options::parse();

    // Handle application error
    if let Err(err) = run(options) {
        eprintln!("{}: {} ", "[exms error]".red(), err);
        process::exit(1);
    };
}

fn run(options: Options) -> Result<(), ParseError> {
    let mut exam = Exam::from_file(&options.file)?;

    if let Some(max_grade) = options.max_grade {
        exam.set_max_grade(max_grade);
    }

    exam.summary();

    if options.histogram {
        exam.histogram();
    }

    if options.grade_sort {
        exam.sort_by_grade();
    }

    if options.alphabetic_sort {
        exam.sort_by_alphabetic_order();
    }

    if let Some(ref students) = options.name_filter {
        exam.filter_by_name(students);
    }

    if let Some(ref file_path) = options.file_filter {
        exam.filter_by_file(file_path)?;
    }

    // Print filtered statistics only if there is a filter applied
    if options.name_filter.is_some() || options.file_filter.is_some() {
        exam.set_name("Filter results");
        exam.summary();

        if options.histogram {
            exam.histogram();
        }
    }

    if options.print_students {
        exam.students();
    }

    Ok(())
}
