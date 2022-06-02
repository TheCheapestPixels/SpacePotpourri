Space Potpourri
===============

A cauldron in which we brew up game systems.


Dev Log
-------

This isn't strictly a changelog, but a few notes on how to develop a
game with the TheCheapestPixels stack.


### Setting up basics

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
  * grep for STARTPROJECT and adapt
  * Redo in a blank virtualenv, and deal with dependencies
  * Package
  * Set up docs and tests


### From blank slate to walking around in the station

The directory `game/` contains copies of several files after phases of
development, prefixed with `<#phase>_`, e.g. `00_main_loop.py`.

* `00`: Blank slate. `00_main_loop.py` sets up the debug keys by adding
  the `wecs.panda3d.debug.DebugTools` system, monitoring whether any of
  the keys defined in `00_keybindings.config` is pressed. These are:
  * `escape`: `quit`; This simply calls `sys.exit()`
  * `f9`: `console`; Toggles the console.
    FIXME: A console does currently not exist.
  * `f10`: `frame_rate_meter`; Toggles the frame rate meter on / off.
  * `f11`: `pdb`; Calls `pdb.set_trace()`, giving you a pdb session on
    the terminal that you started the game in.
  * `f12`: `pstats`; Calls out to the pstats process that you have
    hopefully started already.
* `01`: Let's see a rebecca.
  In this phase we define aspects for characters and a third person
  camera, then unite them make the `player_character` aspect. This lets
  us create the player character model and look at it.
  * `aspects.py`: An `Aspect` is a kind of class for entities, with a
    strict inheritance mechanism that will hopefully prove to prevent
    common error sources and make code maintainance easier by
    encouraging clear idioms from the start.

    Specifically, an aspect can be thought of as a list of component
    types. An aspect can be added to an entity, meaning that fresh new
    components of these types are added to that entity. Aspects also
    maintain override values, which are simply the values to be used
    when creating the components.

    Aspects can also be created from other aspects by simply adding them
    to its "component types" list. As this can happen recursively, you
    have a tree of "inheritance" that creates an aspect's list of
    component types. The inheritance mechanism prevents you from
    creating a situation where any component type is added several
    times, as that can lead to surprisingly hard to debug hierarchies,
    and ambiguity in which override value of several options to use.
    
    Now as for the aspects that we do define here, and the component
    types they contain:
    * `character`:
      * `wecs.panda3d.prototype.Model`: Acts as a in of anchor node in a
        scene, to which further nodes can be attached as the situation
        necessitates.
      * `wecs.panda3d.prototype.Geometry`: Adds a geometry, in this case
        `models/character/rebecca.bam` from the assetcoop package.
      * `wecs.mechanics.clock.Clock`: Quite a lot of systems need to
        know about the flow of time, usually to calculate speeds and
	distances. Ironically in this case it'll first be used by the
	camera (see below), suggesting that the clock should be broken
	out into a more basic aspect.
    * `third_person`:
      * `wecs.panda3d.camera.Camera`: The camera itself.
      * `wecs.panda3d.camera.ObjectCentricCameraMode`: The camera will
        be moved around by the `ReorientObjectCentricCamera` system so
	as to keep the `Model` (and thus presumably its `Geometry`)
	focused.
    * `player_character`: Unifies `character` and `third_person`
  * `main_loop.py`:
    * `import assetcoop`: rebecca is a model from the
      `panda3d-assetcoop` package. Importing it as a module adds the
      directory with the art assets to Panda3D's list of lookup paths.
    * System list
      * `wecs.panda3d.prototype.ManageModels`: This system does a whole
        lot of things, depending on which component types from
	`prototype` are used. In our case, the `Model`'s node gets
	attached to the scene, and the `Geometry` attached to that node.
      * `wecs.panda3d.camera.PrepareCameras`: Attaches the camera to the
        model.
      * `wecs.mechanics.clock.DetermineTimestep`: Updates the `Clock`
        components.
      * `wecs.panda3d.camera.ReorientObjectCentricCamera`: Rotates the
        camera. As we have no input yet, this does nothing except for
	setting the camera to its initial position.
    * `setup`: We create an entity and add the `player_character` aspect
      to it.
* TODO
  * Everything else
