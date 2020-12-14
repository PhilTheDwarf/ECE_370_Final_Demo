# Need to update these to use correct file path!
./final.sh # Load the environment
./reset_robo.sh # Load the robot
python ./dd_robo_vel.py & # Control the robot
python ./vel_controller.py