import argparse
import numpy as np


def get_args():
    parser = argparse.ArgumentParser(description="This is a test program")
    parser.add_argument("--nbeads", type=int, required=True, help="Number of beads per chain")
    parser.add_argument("--nchains", type=int, required=True, help="Number of chains")
    parser.add_argument("--nbigparticles", type=int, required=True, help="Number of big particles")
    parser.add_argument("--rho", type=float, required=True, help="Monomer density")
    parser.add_argument("--output", type=str, default="lmp.data", help="Output file name")

    return parser.parse_args()


def calculate_box_size(nbeads, nchains, rho):
    nparticles = nbeads * nchains
    volume = nparticles / rho
    box_size = volume ** (1/3)
    return box_size


def generate_random_walk(nbeads, nchains, box_size):
    chains = []
    for i in range(nchains):
        chain = []
        # 初期位置をランダムに決定
        current_position = np.random.rand(3) * box_size
        chain.append(current_position)
        for j in range(1, nbeads):
            # ランダムな方向にステップを移動
            step = np.random.normal(size=3)
            step /= np.linalg.norm(step)  # 正規化してステップの大きさを一定に
            step *= 0.97  # 歩幅を0.97に設定
            new_position = current_position + step
            chain.append(new_position)
            current_position = new_position

        # 最後に周期境界を適用し、nx, ny, nz を計算
        wrapped_chain = []
        for position in chain:
            nx = int(np.floor(position[0] / box_size))
            ny = int(np.floor(position[1] / box_size))
            nz = int(np.floor(position[2] / box_size))
            wrapped_position = np.mod(position, box_size)
            wrapped_chain.append((wrapped_position.tolist(), nx, ny, nz))
        chains.append(wrapped_chain)
    return chains


def generate_srd_particles(n_srd, box_size):
    srd_particles = np.random.rand(n_srd, 3) * box_size
    return srd_particles


def generate_big_particles(n_big, box_size):
    big_particles = np.random.rand(n_big, 3) * box_size
    return big_particles


def write_lammps_data(chains, srd_particles, big_particles, box_size, filename="lmp.data"):
    """
    atom_style bond sphere:
    atom_id atom_type x y z mol_id diameter density nx ny nz
    """
    nchains = len(chains)
    nbeads = len(chains[0])
    n_srd = len(srd_particles)
    n_big = len(big_particles)
    with open(filename, "w") as f:
        # ヘッダー情報の書き込み
        total_atoms = len(chains) * len(chains[0]) + n_srd + n_big
        f.write(f"LAMMPS data file generated by script\n\n")
        f.write(f"{total_atoms} atoms\n")
        f.write(f"{nchains*(nbeads - 1)} bonds\n\n")

        f.write(f"3 atom types\n")
        f.write(f"1 bond types\n\n")

        f.write(f"0.0 {box_size:.3f} xlo xhi\n")
        f.write(f"0.0 {box_size:.3f} ylo yhi\n")
        f.write(f"0.0 {box_size:.3f} zlo zhi\n\n")

        f.write("Masses\n\n")
        f.write("1 5.0\n")  # Mass for chain atoms
        f.write("2 1.0\n")  # Mass for SRD particles
        f.write("3 565.487\n\n")  # Mass for BIG particles

        f.write("Atoms\n\n")
        atom_id = 1
        for chain_id, chain in enumerate(chains, start=1):
            for bead in chain:
                position = bead[0]
                nx, ny, nz = bead[1], bead[2], bead[3]
                f.write(f"{atom_id} 1 {position[0]:.3f} {position[1]:.3f} {position[2]:.3f} {chain_id} 0.0 5.0 {nx} {ny} {nz}\n")
                atom_id += 1

        # SRD粒子の出力
        for srd_id, position in enumerate(srd_particles, start=atom_id):
            f.write(f"{srd_id} 2 {position[0]:.3f} {position[1]:.3f} {position[2]:.3f} 0 0.0 1.0 0 0 0\n")
            atom_id += 1

        # BIG粒子の出力
        for big_id, position in enumerate(big_particles, start=atom_id):
            f.write(f"{big_id} 3 {position[0]:.3f} {position[1]:.3f} {position[2]:.3f} 0 6.0 5.0 0 0 0\n")

        f.write("\nBonds\n\n")
        bond_id = 1
        for chain_id in range(1, nchains+1):
            for local_bead_id in range(1, nbeads):
                global_bead_id = (chain_id - 1) * nbeads + local_bead_id
                f.write(f"{bond_id} 1 {global_bead_id} {global_bead_id + 1}\n")
                bond_id += 1


def main():
    args = get_args()
    box_size = calculate_box_size(args.nbeads, args.nchains, args.rho)
    chains = generate_random_walk(args.nbeads, args.nchains, box_size)
    n_srd = args.nbeads * args.nchains * 50  # SRD粒子の数をビーズ数の50倍に設定
    srd_particles = generate_srd_particles(n_srd, box_size)
    big_particles = generate_big_particles(args.nbigparticles, box_size)
    write_lammps_data(chains, srd_particles, big_particles, box_size, args.output)


if __name__ == "__main__":
    main()
