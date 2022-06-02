Space Potpourri
===============

A cauldron in which we brew up game systems.


Dev Log
-------

This isn't strictly a changelog, but a few notes on how to develop a
game with the TheCheapestPixels stack. These notes are accompanied by a
set off files in `game/` (FIXME: Find better place), prefixed with
`<#phase>_´, e.g. `00_main_loop.py`. Most of these files are from the
`game/` directory as well, but `keybindings.config` stems from the root
directory. Please keep this in mind whe trying out a phase.


### `00`: Setting up basics

We set up a project not quite from scratch. Afterwards we can start it,
see a splash advertising Panda3D, and get dropped in the main game loop.

* Create repository
* Upload art to `assets/`; FIXME: Should be moved into the phase where
  it is used.
* Fiddle with `README.md`
* Copy files from `wecs_null_project`:
  ```plaintext
  cp ~/wecs_null_project/setup.py .
  cp ~/wecs_null_project/requirements.txt .
  cp ~/wecs_null_project/main.py .
  cp ~/wecs_null_project/keybindings.config .
  cp -r ~/wecs_null_project/game/ .
  ```

Current state: We have a running skeleton of a not-yet-a-game that we
can run and (FIXME: not yet) package. To this end, we're using these
packages:
* `panda3d-stageflow`: The game can now be started with
  `python main.py`, or `python main.py -s debug` to jump right into the
  `main_game_stage`. This is set up in `game/__init__.py`.
* `panda3d-keybindings`: The device listener is set up, and used below
  by the debug system.
* `wecs`: The main game loop is a stageflow WECS stage consisting only
  of the debug system and no entities. This is set up in
  `game/main_loop.py`. Specifically, the
  `wecs.panda3d.debug.DebugTools` system monitors whether any of
  the keys defined in `keybindings.config` in the `debug` context is
  pressed. These are:
  * `escape`: `quit`; This simply calls `sys.exit()`
  * `f9`: `console`; Toggles the console.
    FIXME: A console does currently not exist.
  * `f10`: `frame_rate_meter`; Toggles the frame rate meter on / off.
  * `f11`: `pdb`; Calls `pdb.set_trace()`, giving you a pdb session on
    the terminal that you started the game in.
  * `f12`: `pstats`; Calls out to the pstats process that you have
    hopefully started already.
  Each binding is a trigger, meaning that its functionality will be
  activated in the frame that the key was pressed down in.

TODO
* grep for STARTPROJECT and adapt
* Redo in a blank virtualenv, and deal with dependencies
* Package
* Set up docs and tests


### `01`: Let's see a rebecca.

In this phase we define aspects for characters and a third person
camera, then unite them make the `player_character` aspect. This lets
us create the player character model and look at it.

To do this, we need to modify two files:
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


### `02`: Rotating the camera

Since we have it set up already, we might as well add player control
over the camera, as it gives an opportunity for a deeper dive into
`panda3d-keybindings` and the `keybindings.config` to set it up.

First, in `aspects.py`, we add the `pc_mind` aspect containing the
`wecs.panda3d.input.Input` type, and the override value
`{'camera_movement', 'camera_zoom'}` for its `contexts` field. This
field indicates which input contexts are currently active for the entity
with an `Input` component on it, and will likely see a lot of context-
driven change thoughout a playthrough.

Then we add this aspect to the `player_character` aspect, so it will get
added to our player entity.

Lastly we need to define the keybindings. In `keybindings.config`, we
add the contexts `camera_movement` and `camera_zoom`. The former
contains an axis2d input named `rotation`, which in the case of a camera
in `ObjectCentricCameraMode` will (to nobody's surprise) rotate it
around the centered object.

FIXME: Maybe repeat the whole definition of bindings and their order
here; Right now I have better things to type out.

FIXME: Why do we need two contexts for camera controls?

Now we can rotate around the player character using a gamepad or the
`ijkl` keys, and also see that gamepad input takes priority over
keyboard input. As the camera is rather slow, we now add a higher
`turning_speed` value to the `ObjectCentricCameraMode` as an override in
the `third_person` aspect.


### `03`: And now a level around us, please.

So, what is a level? A bunch of geometry created (likely in Blender)
after some technical specifications (FIXME: which need to be defined and
documented here), put into the right kind of entity. That kind has
`Model´ and `Geometry` component types, plus
`wecs.panda3d.spawnpoints.SpawnMap` which allows the spawning system to
easily relocate models to spawn points on the level. Correspondingly, we
add the `wecs.panda3d.spawnpoints.SpawnAt` to what a character is.

In `main_loop.py`, we add the `wecs.panda3d.spawnpoints.Spawn` system,
create a new entity using the `game_map` aspect, and add the name of the
spawn point to use on the existing character.

We can now see the level geometry around the character, and that it is
indeed put on the spawn point.


### TODO

Everything else
