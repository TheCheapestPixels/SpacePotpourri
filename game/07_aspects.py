from panda3d.core import Vec3

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
        wecs.panda3d.gravity.GravityMap,
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
        ),
    }


def rebecca_lifter():
    return {
        'lifter': dict(
            node_name='lifter',
        ),
    }


character = Aspect(
    [
        wecs.mechanics.clock.Clock,
        wecs.panda3d.prototype.Model,
        wecs.panda3d.prototype.Geometry,
        wecs.panda3d.spawnpoints.SpawnAt,
        wecs.panda3d.character.CharacterController,
        wecs.panda3d.character.InertialMovement,
        wecs.panda3d.character.WalkingMovement,
        wecs.panda3d.character.FallingMovement,
        wecs.panda3d.character.JumpingMovement,
        wecs.panda3d.character.BumpingMovement,
        wecs.panda3d.gravity.GravityMovement,
    ],
    overrides={
        wecs.mechanics.clock.Clock: dict(
            clock=lambda: factory(wecs.mechanics.clock.panda3d_clock),
        ),
        wecs.panda3d.prototype.Geometry: dict(
            file='models/character/rebecca.bam',
        ),
        wecs.panda3d.character.CharacterController: dict(
            gravity=Vec3(0, 0, -50),
        ),
        wecs.panda3d.character.WalkingMovement: dict(
            speed=30.0,
        ),
        wecs.panda3d.character.BumpingMovement: dict(
            node_name='bumper',
            tag_name='bumper',
            solids=factory(rebecca_bumper),
        ),
        wecs.panda3d.character.FallingMovement: dict(
            node_name='lifter',
            tag_name='lifter',
            solids=factory(rebecca_lifter),
        ),
        wecs.panda3d.character.JumpingMovement:dict(
            impulse=Vec3(0, 0, 20),
        ),
    },
)


third_person = Aspect(
    [
        wecs.panda3d.camera.Camera,
        wecs.panda3d.camera.ObjectCentricCameraMode,
        wecs.panda3d.character.AutomaticTurningMovement,
        wecs.panda3d.character.TurningBackToCameraMovement,
    ],
    overrides={
        wecs.panda3d.camera.ObjectCentricCameraMode: dict(
            turning_speed=180.0,
        ),
        wecs.panda3d.character.TurningBackToCameraMovement: dict(
            view_axis_alignment=0.4,
            threshold=0.2,
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
