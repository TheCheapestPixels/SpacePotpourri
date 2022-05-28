import wecs

from stageflow.wecs import WECSStage

# STARTPROJECT: Turn MainGameStage into your game.


class MainGameStage(WECSStage):
    system_specs = [
        # Set up newly added models/camera, tear down removed ones
        (0, -10, wecs.panda3d.prototype.ManageModels),
        (0, -20, wecs.panda3d.spawnpoints.Spawn),
        (0, -30, wecs.panda3d.camera.PrepareCameras),
        # Update clocks
        (0, -40, wecs.mechanics.clock.DetermineTimestep),
        ## Interface interactions
        ##(0, -50, wecs.panda3d.mouseover.MouseOverOnEntity),
        ##(0, -60, wecs.panda3d.mouseover.UpdateMouseOverUI),
        #AvatarUI,
        # Set inputs to the character controller
        #(0, -70, wecs.panda3d.ai.Think),
        #(0, -80, wecs.panda3d.ai.BehaviorInhibitsDirectCharacterControl),
        (0, -90, wecs.panda3d.character.UpdateCharacter),
        #(0, -91, wecs.panda3d.character.ReorientInputBasedOnCamera),
        # Character controller
        #(0, -100, wecs.panda3d.character.Floating),
        (0, -110, wecs.panda3d.character.Walking),
        #(0, -120, wecs.panda3d.character.Inertiing),
        #(0, -130, wecs.panda3d.character.Frictioning),
        #(0, -140, wecs.panda3d.character.WalkSpeedLimiting),
        (0, -150, wecs.panda3d.character.Bumping),
        (0, -160, wecs.panda3d.character.Falling),
        #(0, -170, wecs.panda3d.character.Jumping),
        #(0, -171, wecs.panda3d.character.DirectlyIndicateDirection),
        #(0, -172, wecs.panda3d.character.TurningBackToCamera),
        #(0, -173, wecs.panda3d.character.AutomaticallyTurnTowardsDirection),
        #(0, -180, wecs.panda3d.character.FaceMovement),
        #(0, -190, wecs.panda3d.character.TurningBackToCamera),
        (0, -200, wecs.panda3d.character.ExecuteMovement),
        # Camera
        (0, -210, wecs.panda3d.camera.ReorientObjectCentricCamera),
        (0, -220, wecs.panda3d.camera.CollideCamerasWithTerrain),
        # Debug keys (`escape` to close, etc.)
        (0, -1000, wecs.panda3d.debug.DebugTools),
    ]

    def setup(self, data):
        """
        Set up the game.

        data
            Data that was passed to this stage.
        """
        aspects.player_character.add(
            base.ecs_world.create_entity(name="Playerbecca"),
            overrides={
                **aspects.rebecca,
                **aspects.spawn_point_air,
            },
        )

    def teardown(self, data):
        """
        Tear down the game.

        data
            Data that was passed to :class:`Stage.exit`.

        :returns:
            Data to be passed on o the next stage
        """
        return data
