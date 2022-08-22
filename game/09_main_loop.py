import wecs

from stageflow.wecs import WECSStage

import assetcoop

from boterham.loader import boterham_load_model

from game import aspects


class MainGameStage(WECSStage):
    system_specs = [
        # Set up newly added models/camera, tear down removed ones
        (0, -10, wecs.panda3d.prototype.ManageModels),
        (0, -20, wecs.panda3d.spawnpoints.Spawn),
        (0, -30, wecs.panda3d.camera.PrepareCameras),
        # Update clocks
        (0, -40, wecs.mechanics.clock.DetermineTimestep),
        # Interaction
        (0, -60, wecs.panda3d.interaction.Interacting),
        # Set inputs to the character controller
        (0, -90, wecs.panda3d.character.UpdateCharacter),
        # Character controller
        (0, -110, wecs.panda3d.character.Walking),
        (0, -120, wecs.panda3d.character.Inertiing),
        (0, -150, wecs.panda3d.character.Bumping),
        (0, -160, wecs.panda3d.character.Falling),
        (0, -170, wecs.panda3d.character.Jumping),
        (0, -172, wecs.panda3d.character.TurningBackToCamera),
        (0, -173, wecs.panda3d.character.AutomaticallyTurnTowardsDirection),
        (0, -200, wecs.panda3d.character.ExecuteMovement),
        # Determine and apply character's local gravity
        # Camera
        (0, -210, wecs.panda3d.camera.ReorientObjectCentricCamera),
        (0, -220, wecs.panda3d.camera.ZoomObjectCentricCamera),
        # Debug keys (`escape` to close, etc.)
        (0, -1000, wecs.panda3d.debug.DebugTools),
    ]

    def setup(self, data):
        """
        Sets up the game.

        data
            Data that was passed to this stage; Ignored.
        """
        aspects.game_map.add(
            base.ecs_world.create_entity(name="Level geometry"),
            overrides={
                wecs.panda3d.prototype.Geometry: dict(
                    node=boterham_load_model('models/gravitytest/interact_plane.bam'),
                ),
                wecs.panda3d.gravity.GravityMap: dict(
                    node_names=['gravity'],
                ),
            },
        )
        
        aspects.player_character.add(
            base.ecs_world.create_entity(name="Playerbecca"),
            overrides={
                wecs.panda3d.spawnpoints.SpawnAt: dict(
                    name='spawn_a',
                ),
                wecs.panda3d.gravity.GravityMovement: dict(
                    node_names=['gravity'],
                ),
            },
        )
        aspects.character.add(
            base.ecs_world.create_entity(name="NPBecca"),
            overrides={
                wecs.panda3d.spawnpoints.SpawnAt: dict(
                    name='spawn_b',
                ),
                wecs.panda3d.gravity.GravityMovement: dict(
                    node_names=['gravity'],
                ),
            },
        )

    def teardown(self, data):
        """
        Should tear down the game, but does nothing yet.

        data
            Data that was passed to :class:`Stage.exit`.

        :returns:
            Data to be passed on to the next stage; In this case, 
            whatever was passed to this method.
        """
        return data
