#!/usr/bin/env sh

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
ROOT_DIR=$(dirname "$SCRIPT_DIR")
BIN_DIR="/usr/local/bin"
SCRAPER_DIR="/usr/local/scraper"

cd "$ROOT_DIR" || exit

# Build the binaries
cargo +nightly fmt
cargo build --release
cargo doc --no-deps

# Copy the binaries and scripts to their respective directories
sudo cp ./target/release/cli $BIN_DIR/exms
sudo cp ./target/release/parser $BIN_DIR/parser
sudo cp scripts/scraper.sh $BIN_DIR/scraper
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
sudo sed -i '' "s/USERNAME = \".*\"/USERNAME = \"$username\"/" "$SCRAPER_DIR/scraper.py"
sudo sed -i '' "s/PASSWORD = \".*\"/PASSWORD = \"$password\"/" "$SCRAPER_DIR/scraper.py"
