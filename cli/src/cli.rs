use clap::Parser;
use std::path::PathBuf;

#[derive(Parser)]
#[command(about, version)]
pub struct Options {
    /// File with the exam results
    pub file: PathBuf,

    /// Print students information in a table
    #[arg(short, long)]
    pub print_students: bool,

    /// Print the histogram of the grades
    #[arg(short = 'H', long)]
    pub histogram: bool,

    /// Sort the students based on their grade in descending order
    #[arg(short, long, conflicts_with("alphabetic_sort"), requires("print"))]
    pub grade_sort: bool,

    /// Sort the students based on their name alphabetically
    #[arg(short, long, conflicts_with("grade_sort"), requires("print"))]
    pub alphabetic_sort: bool,

    /// Filter the students by name
    #[arg(short, long, value_name = "STUDENTS", num_args(1..))]
    pub name_filter: Option<Vec<String>>,

    /// Filter the students by another file containing exam results
    #[arg(short, long, value_name = "FILE")]
    pub file_filter: Option<Vec<PathBuf>>,
}
