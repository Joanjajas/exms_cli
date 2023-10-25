#!/bin/env sh

cargo +nightly fmt
cargo build --release
cargo doc --no-deps
sudo cp ./target/release/cli /usr/local/bin/exms
sudo cp ./target/release/parser /usr/local/bin/parser
