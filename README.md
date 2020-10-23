# pykgr

## A stupid simple nix rip-off for learning purposes

You will want to edit the pykgr.json file in the root of this repo to point to the
repos location.  Alternatively you can setup a .pykgr.json and pip install it (but
use any other dir as the one in this directory will overwrite certain configurations.)

Then just `python -m pykgr --init --build-toolchain -p packages.python`