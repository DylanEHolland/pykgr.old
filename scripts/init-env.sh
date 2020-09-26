export ENV_DIR="$1";
export PATH="$ENV_DIR/bin";
export TERM="xterm-256color";

cd "$ENV_DIR" && bash;