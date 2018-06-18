#!/bin/bash

# Number of GPUs per job. For now is set to one so that we can run
# multiple jobs at once, rather than one job with two GPUs.
#SBATCH --gres=gpu:1

#SBATCH --cpus-per-task=64
#SBATCH --job-name=slurm_train_and_predict
#SBATCH --output=slurm_train_and_predict_%A_%a.out

# Array to iterate over, as well as (%) number of jobs to run at once.
# The below has been commented out and this should instead be passed via
# command line when sbatch is run so that this file can remain unmofified
# for different values.
##SBATCH --array=0-4%2

# Run the train and predict process, passing all arguments to the script.
if [ -z "$SLURM_ARRAY_TASK_ID" ]; then
    time inkid-train-and-predict "$@"
else
    time inkid-train-and-predict "$@" -k $SLURM_ARRAY_TASK_ID
fi

# Backup ~/data/out to Team Google Drive.
time rclone copy -u -v /home/$USER/data/dri-experiments-drive/2018-ml-inkid/results/ dri-experiments-drive:2018-ml-inkid/results/
