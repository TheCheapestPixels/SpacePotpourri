#!/usr/bin/env python

import os

from wecs import boilerplate


def run_game():
    boilerplate.run_game(
        keybindings=True,       # panda3d-keybindings
        debug_keys=True,        # Esc/F9-12 via accept()
        simplepbr=False,        # calls simplepbr.init(simplepbr_kwargs)
        simplepbr_kwargs=None,  # default: {}
    )


if __name__ == '__main__':
    run_game()
