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
            let exam = create_exam(&args.exam_args)?;

            exam.summary();
            exam.histogram(args.step);
            print_students(exam, &args.filter_args, &args.sort_args)?;
        }

        Command::Statistics(args) => {
            let exam = create_exam(&args)?;
            exam.summary();
        }

        Command::Histogram(args) => {
            let exam = create_exam(&args.exam_args)?;
            exam.histogram(args.step)
        }

        Command::Students(args) => {
            let exam = create_exam(&args.exam_args)?;
            print_students(exam, &args.filter_args, &args.sort_args)?;
        }

        Command::Download => {
            std::process::Command::new("scraper").status()?;
        }
    }

    Ok(())
}

fn create_exam(args: &cli::ExamArgs) -> Result<Exam> {
    let mut exam = Exam::from_file(&args.file)?;

    if let Some(max_grade) = args.max_grade {
        exam.set_max_grade(max_grade);
    }

    Ok(exam)
}

fn print_students(
    mut exam: Exam,
    filter_args: &cli::FilterArgs,
    sort_args: &cli::SortArgs,
) -> Result<()> {
    if sort_args.sort_by_grade {
        exam.sort_by_grade();
    }

    if sort_args.sort_by_alphabetic_order {
        exam.sort_by_alphabetic_order();
    }

    if let Some(names) = &filter_args.name_filter {
        exam.filter_by_name(names);
    }

    if let Some(files) = &filter_args.file_filter {
        exam.filter_by_file(files)?;
    }

    exam.students();

    Ok(())
}
