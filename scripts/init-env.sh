export ENV_DIR="$1";
export PATH="$ENV_DIR/bin";

cd "$ENV_DIR" && sh;