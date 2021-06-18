import pyximport; pyximport.install()

from torch import multiprocessing as mp

from alphazero.Coach import Coach, get_args
from alphazero.NNetWrapper import NNetWrapper as nn
from alphazero.connect4.Connect4Game import Connect4Game as Game
from alphazero.utils import dotdict

args = get_args(dotdict({
    'run_name': 'connect4',
    'workers': mp.cpu_count(),
    'startIter': 1,
    'numIters': 1000,
    'numWarmupIters': 1,
    'process_batch_size': 2048,
    'train_batch_size': 128,
    # should preferably be a multiple of process_batch_size and workers
    'gamesPerIteration': 2048*mp.cpu_count(),
    'symmetricSamples': True,
    'numMCTSSims': 50,
    'numFastSims': 5,
    'probFastSim': 0.75,
    'tempThreshold': 20,
    'temp': 1,
    'compareWithBaseline': True,
    'arenaCompareBaseline': 32,
    'arenaCompare': 256,
    'arena_batch_size': 64,
    'arenaTemp': 0.1,
    'arenaMCTS': True,
    'baselineCompareFreq': 1,
    'compareWithPast': True,
    'pastCompareFreq': 1,
    'expertValueWeight': dotdict({
        'start': 0,
        'end': 0,
        'iterations': 35
    }),
    'cpuct': 4,
    'load_model': True,
    }),
    model_gating=False,
    
    lr=0.01,
    num_channels=64,
    depth=8,
    value_head_channels=8,
    policy_head_channels=8,
    value_dense_layers=[256, 128],
    policy_dense_layers=[256]
)

if __name__ == "__main__":
    nnet = nn(Game, args)
    c = Coach(Game, nnet, args)
    c.learn()
