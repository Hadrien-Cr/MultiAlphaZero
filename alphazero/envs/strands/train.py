import pyximport; pyximport.install()

from torch import multiprocessing as mp

from alphazero.Coach import Coach, get_args
from alphazero.NNetWrapper import NNetWrapper as nn
from alphazero.envs.strands.strands import Game
from alphazero.GenericPlayers import RawMCTSPlayer
from alphazero.utils import dotdict

args = get_args(dotdict({
    'run_name': 'strands_fpu',
    'self_play_search_strategy': 'BB-MCTS',
    'baseline_search_strategy': 'BB-MCTS',
    'workers': mp.cpu_count(),
    'startIter': 1,
    'numIters': 1000,
    'numWarmupIters': 1,
    'process_batch_size': 64,
    'train_batch_size': 1024,
    # should preferably be a multiple of process_batch_size and workers
    'gamesPerIteration': 10_000,
    'symmetricSamples': True,
    'skipSelfPlayIters': None,
    'selfPlayModelIter': None,
    'numMCTSSims': 500,
    'numFastSims': 1000,
    'probFastSim': 0.,
    'compareWithBaseline': True,
    'arenaCompareBaseline': 128,
    'arenaCompare': 128,
    'arena_batch_size': 128,
    'arenaTemp': 1,
    'arenaMCTS': True,
    'baselineCompareFreq': 1,
    'compareWithPast': True,
    'pastCompareFreq': 1,
    'cpuct': 4,
    'fpu_reduction': 0.4,
    'load_model': True,
}),
    model_gating=True,
    max_gating_iters=None,
    max_moves=42,

    lr=0.01,
    num_channels=128,
    depth=8,
    value_head_channels=32,
    policy_head_channels=32,
    value_dense_layers=[1024, 256],
    policy_dense_layers=[1024]
)
args.scheduler_args.milestones = [75, 150]


if __name__ == "__main__":
    nnet = nn(Game, args)
    c = Coach(Game, nnet, args)
    c.learn()
