import wecs

from wecs.aspects import Aspect
from wecs.aspects import factory

from wecs.panda3d.constants import FALLING_MASK
from wecs.panda3d.constants import BUMPING_MASK


game_map = Aspect(
    [
        wecs.panda3d.prototype.Model,
        wecs.panda3d.prototype.Geometry,
        wecs.panda3d.prototype.CollidableGeometry,
        #wecs.panda3d.prototype.FlattenStrong,
        wecs.panda3d.spawnpoints.SpawnMap,
     ],
    overrides={
        wecs.panda3d.prototype.CollidableGeometry: dict(
            mask=FALLING_MASK|BUMPING_MASK,
        ),
    },
)


def rebecca_bumper():
    return {
        'bumper': dict(
            node_name='bumper',
            #shape=CollisionSphere,
            #center=Vec3(0.0, 0.0, 1.0),
            #radius=0.7,
            debug=True,
        ),
    }


def rebecca_lifter():
    return {
        'lifter': dict(
            node_name='lifter',
            #shape=CollisionSphere,
            #center=Vec3(0.0, 0.0, 0.5),
            #radius=0.5,
            debug=True,
        ),
    }


character = Aspect(
    [
        wecs.mechanics.clock.Clock,
        wecs.panda3d.prototype.Model,
        wecs.panda3d.prototype.Geometry,
        wecs.panda3d.spawnpoints.SpawnAt,
        wecs.panda3d.character.CharacterController,
        wecs.panda3d.character.WalkingMovement,
        wecs.panda3d.character.FallingMovement,
        wecs.panda3d.character.BumpingMovement,
    ],
    overrides={
        wecs.mechanics.clock.Clock: dict(
            clock=lambda: factory(wecs.mechanics.clock.panda3d_clock),
        ),
        wecs.panda3d.prototype.Geometry: dict(
            file='models/character/rebecca.bam',
        ),
        wecs.panda3d.character.WalkingMovement: dict(
            speed=30.0,
        ),
        wecs.panda3d.character.BumpingMovement: dict(
            node_name='bumper',
            tag_name='bumper',
            solids=factory(rebecca_bumper),
            debug=True,
        ),
        wecs.panda3d.character.FallingMovement: dict(
            node_name='lifter',
            tag_name='lifter',
            solids=factory(rebecca_lifter),
            #debug=True,
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
