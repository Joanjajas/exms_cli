#!/usr/bin/env sh

script_dir=$(dirname "$(readlink -f "$0")")
root_dir=$(dirname "$script_dir")
bin_dir="/usr/local/bin"
scraper_dir="/usr/local/scraper"

cd "$root_dir" || exit

# Build the binaries
cargo +nightly fmt
cargo build --release
cargo doc --no-deps

# Copy the binaries and scripts to their respective directories
sudo cp ./target/release/cli $bin_dir/cli
sudo cp ./target/release/parser $bin_dir/parser
sudo cp scripts/scraper.sh $bin_dir/scraper
sudo cp -r scraper /usr/local/

# Make scraper script executable
sudo chmod +x /usr/local/bin/scraper

# Get user credentials
printf "\nIntroduce your intranet username and password:\n"
printf "Dni: "
read -r username
printf "Password: "
stty -echo
read -r password
stty echo

# Replace the credentials inside the script
sudo sed -i '' "s/USERNAME = \".*\"/USERNAME = \"$username\"/" "$scraper_dir/scraper.py"
sudo sed -i '' "s/PASSWORD = \".*\"/PASSWORD = \"$password\"/" "$scraper_dir/scraper.py"
