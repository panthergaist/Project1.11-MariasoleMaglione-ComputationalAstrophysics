#!/bin/bash -x                                                                                                                                                                                                                  
#SBATCH --job-name=sevn                                                                                         
#SBATCH --partition=debug                                                                                        
#SBATCH --gres=gpu:0                                                                                              
                                                                                                                 
#SBATCH --nodes=1                                                                                                
#SBATCH --ntasks-per-node=20                                                                                      
#SBATCH --cpus-per-task=1                                                                                                                                                                                        
                                                                                                                 
#SBATCH --output=mpi-out                                                                                      
#SBATCH --error=mpi-err                                                                                       
                                                                                                                 
                                                                                                                                                                                                                                    
ulimit -s unlimited                                                                                              
ulimit -l 40000000                                                                                                
ulimit -v 40000000                                                                                                
                                                                                                                 

chmod u+x runproject_4Mbse_0.02.sh
srun ./runproject_4Mbse_0.02.s
