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
        # Set inputs to the character controller
        (0, -90, wecs.panda3d.character.UpdateCharacter),
        # Character controller
        (0, -110, wecs.panda3d.character.Walking),
        (0, -150, wecs.panda3d.character.Bumping),
        (0, -160, wecs.panda3d.character.Falling),
        (0, -200, wecs.panda3d.character.ExecuteMovement),
        # Camera
        (0, -210, wecs.panda3d.camera.ReorientObjectCentricCamera),
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
                    #file='models/scenes/lona.bam',
                    node=boterham_load_model('assets/bam/comp.bam'),
                    #node=boterham_load_model('assets/bam/gravitytest/cylinder.bam'),
                    #node=boterham_load_model('models/gravitytest/cylinder.bam'),
                ),
            },
        )
        
        aspects.player_character.add(
            base.ecs_world.create_entity(name="Playerbecca"),
            overrides={
                wecs.panda3d.spawnpoints.SpawnAt: dict(
                    name='spawn_0',
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
