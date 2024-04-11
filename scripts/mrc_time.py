import os
import sys
import itertools
from collections import defaultdict
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

params = {
    "axes.labelsize": 24,
    "axes.titlesize": 24,
    "xtick.labelsize": 24,
    "ytick.labelsize": 24,
    "lines.linewidth": 2,
    "legend.fontsize": 24,
    "legend.handlelength": 2,
    "legend.borderaxespad": 0.2,
}
plt.rcParams.update(params)

from multiprocessing import Process
from concurrent.futures import ProcessPoolExecutor
import subprocess

BIN_PATH = "/home/lpy/libCacheSim/_build/cachesim"
MARKERS = itertools.cycle(Line2D.markers.keys())

# REGEX = "[INFO]  04-26-2023 10:34:39    sim.c:51   (tid=139697109580096): sieve.oracleGeneral.bin ARC 167.00 hour: 39761839 requests, miss ratio 0.3008, interval miss ratio 0.3913"
REGEX = r"(\d+\.\d+) hour: (\d+) requests, miss ratio (\d+\.\d+), interval miss ratio (\d+\.\d+)"


def run_cachesim(datapath, algo, cache_size, trace_format, extra_args, miss_ratio_type="accumulated", report_interval="3600"):

    ts_list, mrc_list = [], []

    p = subprocess.run([
        BIN_PATH,
        datapath,
        trace_format,
        algo,
        cache_size,
        "--report-interval=" + report_interval,
        "-t",
        extra_args,
    ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    o = p.stdout.decode("utf-8")
    print(p.stderr.decode("utf-8"))

    for line in o.split("\n"):
        if "[INFO]" in line[:16]:
            m = re.search(REGEX, line)
            if m:
                ts_list.append(int(float((m.group(1)))))
                if miss_ratio_type == "accumulated":
                    mrc_list.append(float(m.group(3)))
                elif miss_ratio_type == "interval":
                    mrc_list.append(float(m.group(4)))
                else:
                    raise Exception("Unknown miss ratio type {}".format(miss_ratio_type))
            continue
        if line.startswith("result"):
            print(line)

    return ts_list, mrc_list

def plot_mrc_time(mrc_dict, name="mrc", color=None):

    linestyles = itertools.cycle(["-", "--", "-.", ":"])
    # linestyles = itertools.cycle(["--", "-", "--", "-.", ":"])
    colors = itertools.cycle(["navy", "darkorange", "tab:green", "cornflowerblue", ])

    plt.figure(figsize=(10, 6))
    
    for algo, (ts, mrc) in mrc_dict.items():
        ts = np.array(ts) / ts[-1]
        mrc = np.array(mrc)
        plt.plot(ts, mrc, linewidth=4, color=next(colors), linestyle=next(linestyles), label=algo)

    
    plt.xlabel("Logical Time")
    plt.ylabel("Miss Ratio")
    # plt.ylim(0.48,0.8)
    # plt.ylim(0.12,0.32)
    plt.legend(ncol=2, loc="upper left", frameon=False)
    plt.grid(axis="y", linestyle='--')
    plt.savefig('{}.png'.format(name), dpi=300, bbox_inches='tight')
    


def run():
    import glob

    algos = "lru,slru,arc,lirs,lhd,tinylfu,qdlpv1"
    cache_sizes = "0"
    for i in range(1, 100, 2):
        cache_sizes += str(i / 100.0) + ","
    cache_sizes = cache_sizes[:-1]
    print(cache_sizes)

    for tracepath in glob.glob("/disk/data/*.zst"):
        dataname = tracepath.split("/")[-1].split(".")[0]
        mrc_dict = run_cachesim(tracepath, algos, cache_sizes)
        plot_mrc_time(mrc_dict, dataname)


if __name__ == "__main__":
    # if len(sys.argv) != 4:
    #     # print("Usage: python3 {} <datapath> <algos> <cache_sizes>".format(sys.argv[0]))
    #     # exit(1)
    #     # tracepath = "/disk/data/w96.oracleGeneral.bin.zst"
    #     # tracepath = "/mntData2/oracleReuse/msr/web_2.IQI.bin.oracleGeneral.zst"
    #     # tracepath = "/mntData2/oracleReuse/msr/src1_0.IQI.bin.oracleGeneral.zst"
    #     tracepath = "/mntData2/oracleReuse/msr/src1_1.IQI.bin.oracleGeneral.zst"
    #     algos = "lru,slru,arc,lirs,tinylfu,qdlpv1"
    #     cache_sizes = "0"
    # else:
    #     tracepath = sys.argv[1]
    #     algos = sys.argv[2]
    #     cache_sizes = sys.argv[3]

    # if cache_sizes == "0":
    #     cache_sizes = ""
    #     for i in range(1, 100, 2):
    #         cache_sizes += str(i / 100.0) + ","
    #     cache_sizes = cache_sizes[:-1]

    # run()

    mrc_dict = {}
    tracepath = sys.argv[1]
    trace_format = sys.argv[2]
    algos = sys.argv[3].split(",")
    size = sys.argv[4]
    dataname = tracepath.split("/")[-1].split(".")[0]
    report_interval = sys.argv[5].split("=")[-1]
    extra_args = sys.argv[7]

    miss_ratio_type = "accumulated"

    for algo in algos:
        mrc_dict[algo] = run_cachesim(tracepath, algo, size, trace_format, extra_args, miss_ratio_type, report_interval)

    plot_mrc_time(mrc_dict, "{}_{}".format(dataname, size))
