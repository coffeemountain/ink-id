#!/bin/bash

#SBATCH --gres=gpu:1
#SBATCH --job-name=lunateGridTraining
#SBATCH --output=lunateGridTraining_%A_%a.out
#SBATCH --array=0-9
# In the above line, replace 1 with the number of GPUs you wish to reserve (1
# or 2).

echo "My SLURM_ARRAY_TASK_ID: " $SLURM_ARRAY_TASK_ID

python ~/devel/ink-id/supervised/3DCNN/main.py #SLURM_ARRAY_TASK_ID
