export ENV_DIR="$1";
export PATH="$ENV_DIR/bin:/usr/bin:/bin";
export TERM="xterm-256color";

cd "$ENV_DIR" && HOME="$ENV_DIR" bash --norc;