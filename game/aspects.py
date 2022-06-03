import wecs

from wecs.aspects import Aspect
from wecs.aspects import factory


game_map = Aspect(
    [
        wecs.panda3d.prototype.Model,
        wecs.panda3d.prototype.Geometry,
        wecs.panda3d.spawnpoints.SpawnMap,
     ],
)


character = Aspect(
    [
        wecs.mechanics.clock.Clock,
        wecs.panda3d.prototype.Model,
        wecs.panda3d.prototype.Geometry,
        wecs.panda3d.spawnpoints.SpawnAt,
        wecs.panda3d.character.CharacterController,
        wecs.panda3d.character.WalkingMovement,
    ],
    overrides={
        wecs.mechanics.clock.Clock: dict(
            clock=lambda: factory(wecs.mechanics.clock.panda3d_clock),
        ),
        wecs.panda3d.prototype.Geometry: dict(
            file='models/character/rebecca.bam',
        ),
        wecs.panda3d.character.WalkingMovement: dict(
            speed=500.0,
        ),
    },
)


third_person = Aspect(
    [
        wecs.panda3d.camera.Camera,
        wecs.panda3d.camera.ObjectCentricCameraMode,
    ],
    overrides={
        wecs.panda3d.camera.ObjectCentricCameraMode: dict(
            turning_speed=180.0,
        ),
    },
)


pc_mind = Aspect(
    [
        wecs.panda3d.input.Input,
    ],
    overrides={
        wecs.panda3d.input.Input: dict(
            contexts={
                'camera_movement',
                'camera_zoom',
                'character_movement',
            },
        ),
    },
)


player_character = Aspect(
    [
        character,
        third_person,
        pc_mind,
    ],
)
