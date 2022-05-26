Space Potpourri
===============

A cauldron in which we brew up game systems.


Dev Log
-------

This isn't strictly a changelog, but a few notes on how to develop a
game with the TheCheapestPixels stack.


###Setting up basics

* Created repository
* Uploaded art to `assets/`
* Fiddled with `README.md`
* Copied files from `wecs_null_project`:
  ```plaintext
  cp ~/wecs_null_project/setup.py .
  cp ~/wecs_null_project/requirements.txt .
  cp ~/wecs_null_project/main.py .
  cp ~/wecs_null_project/keybindings.config .
  cp -r ~/wecs_null_project/game/ .
  ```
* Current state
  * `stageflow`: The game can now be started with `python main.py`, or
    `python main.py -s debug` to jump right into the `main_game_stage`.
    This is set up in `game/__init__.py`.
  * `wecs`: The main game loop is a stageflow WECS stage consisting only
    of the debug system and no entities. This is set up in
    `game/main_loop.py`.
* TODO
  * Redo in a blank virtualenv, and deal with dependencies.
  * Package
  * Set up docs and tests


###From blank slate to walking around in the station

* TODO
  * Everything
