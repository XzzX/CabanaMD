#! python3

src_dir = 'CabanaMD'
build_dir = 'build'
bin_dir = 'bin'

with open('compile.sh', 'w') as fcompile, open('run.sh', 'w') as frun:
    frun.write(f'#!/bin/bash -l\n')
    frun.write('\n')
    frun.write(f'#SBATCH --nodes=1\n')
    frun.write(f'#SBATCH --ntasks-per-node=1\n')
    frun.write(f'#SBATCH --time=00:30:00\n')
    frun.write('\n')
    frun.write(f'#SBATCH -o out.%j\n')
    frun.write(f'#SBATCH -e err.%j\n')
    frun.write('\n')
    frun.write('export OMP_NUM_THREADS=1\n')
    frun.write('export OMP_PROC_BIND=spread\n')
    frun.write('export OMP_PLACES=threads\n')
    frun.write('\n')


    for layout in [1, 2, 6]:
        for vector_length in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]:
            fcompile.write(f'cmake -S {src_dir} -B {build_dir} -DCabanaMD_LAYOUT={layout} -DCabanaMD_VECTORLENGTH={vector_length}\n')
            fcompile.write(f'cmake --build {build_dir} --target cbnMD -j 8\n')
            fcompile.write(f'cp {build_dir}/bin/cbnMD {bin_dir}/cbnMD_{layout}_{vector_length}\n')
            fcompile.write(f'rm -rf {build_dir}\n')
            fcompile.write(f'\n')

            frun.write(f'srun ./cbnMD_{layout}_{vector_length} -il in.lj --device-type SERIAL\n')
