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

    /// Set the maximum achievable grade in the exam
    #[arg(short, long, value_name = "GRADE")]
    pub max_grade: Option<f32>,

    /// Sort the students based on their grade in descending order
    #[arg(
        short,
        long,
        conflicts_with("alphabetic_sort"),
        requires("print_students")
    )]
    pub grade_sort: bool,

    /// Sort the students based on their name alphabetically
    #[arg(short, long, conflicts_with("grade_sort"), requires("print_students"))]
    pub alphabetic_sort: bool,

    /// Filter the students by name
    #[arg(short, long, value_name = "NAMES", num_args(1..))]
    pub name_filter: Option<Vec<String>>,

    /// Filter the students by another file containing exam results
    #[arg(short, long, value_name = "FILES", num_args(1..))]
    pub file_filter: Option<Vec<PathBuf>>,
}
