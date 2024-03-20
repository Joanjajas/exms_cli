use clap::{Args, Parser, Subcommand};
use std::path::PathBuf;

#[derive(Parser)]
pub struct Cli {
    #[clap(subcommand)]
    pub command: Command,
}

#[derive(Subcommand)]
pub enum Command {
    /// Prints the summary of the exam (Statistics, Histogram, Students)
    Summary(SummaryArgs),

    /// Prints the statistics of the exam
    Statistics(ExamArgs),

    /// Prints the histogram of the grades
    Histogram(HistogramArgs),

    /// Prints the exam students
    Students(StudentsArgs),

    /// Downloads the exam results
    Download(DownloadArgs),
}

#[derive(Args)]
pub struct SummaryArgs {
    // Exam args
    #[command(flatten)]
    pub exam_args: ExamArgs,

    // Filter args
    #[command(flatten)]
    pub filter_args: FilterArgs,

    // Sort args
    #[command(flatten)]
    pub sort_args: SortArgs,

    /// Step of the histogram
    #[arg(short, long, value_name = "STEP")]
    pub step: Option<f64>,
}

#[derive(Args)]
pub struct StatisticsArgs {
    // Exam args
    #[command(flatten)]
    pub exam_args: ExamArgs,
}

#[derive(Args)]
pub struct StudentsArgs {
    // Exam args
    #[command(flatten)]
    pub exam_args: ExamArgs,

    // Filter args
    #[command(flatten)]
    pub filter_args: FilterArgs,

    // Sort args
    #[command(flatten)]
    pub sort_args: SortArgs,
}

#[derive(Args)]
pub struct HistogramArgs {
    // Exam args
    #[command(flatten)]
    pub exam_args: ExamArgs,

    /// Step of the histogram
    #[arg(short, long, value_name = "STEP")]
    pub step: Option<f64>,
}

#[derive(Args)]
pub struct ExamArgs {
    /// File with the exam results
    pub file: PathBuf,

    /// Maximum achievable grade in the exam
    #[clap(short, long, value_name = "GRADE")]
    pub max_grade: Option<f32>,
}

#[derive(Args)]
pub struct FilterArgs {
    /// Filter the students by name
    #[arg(short, long, value_name = "NAMES", num_args(1..))]
    pub name_filter: Option<Vec<String>>,

    /// Filter the students by another file containing exam results
    #[arg(short, long, value_name = "FILES", num_args(1..))]
    pub file_filter: Option<Vec<PathBuf>>,
}

#[derive(Args)]
pub struct SortArgs {
    /// Sort the students based on their grade in descending order
    #[arg(short = 'g', long)]
    pub sort_by_grade: bool,

    /// Sort the students based on their name alphabetically
    #[arg(short = 'a', long)]
    pub sort_by_alphabetic_order: bool,
}

#[derive(Args, Debug)]
pub struct DownloadArgs {
    /// Path to download the exam results
    pub path: PathBuf,
}
