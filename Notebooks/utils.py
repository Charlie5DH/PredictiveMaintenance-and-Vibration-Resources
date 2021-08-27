import os
import numpy as np
import pandas as pd
from scipy.special import entr
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler

# Fnctions to extract features from vibration data
# to use copy the code below and uncomment
# set_1_df = merge_data(dataset_path_1st,1)
# set_1_df.head()


def calculate_rms(df):
    result = []
    for col in df:
        r = np.sqrt((df[col]**2).sum() / len(df[col]))
        result.append(r)
    return result

# extract peak-to-peak features


def calculate_p2p(df):
    return np.array(df.max().abs() + df.min().abs())

# extract shannon entropy (cut signals to 500 bins)


def calculate_entropy(df):
    entropy = []
    for col in df:
        entropy.append(scipy.stats.entropy(
            pd.cut(df[col], 500).value_counts()))
    return np.array(entropy)


def time_features(dataset_path, id_set=None):
    time_features = ['mean', 'std', 'skew',
                     'kurtosis', 'entropy', 'rms', 'max', 'p2p']
    cols1 = ['B1_a', 'B1_b', 'B2_a', 'B2_b', 'B3_a', 'B3_b', 'B4_a', 'B4_b']
    cols2 = ['B1', 'B2', 'B3', 'B4']

    # initialize
    if id_set == 1:
        columns = [c+'_'+tf for c in cols1 for tf in time_features]
        data = pd.DataFrame(columns=columns)
    else:
        columns = [c+'_'+tf for c in cols2 for tf in time_features]
        data = pd.DataFrame(columns=columns)

    for filename in os.listdir(dataset_path):
        # read dataset
        raw_data = pd.read_csv(os.path.join(dataset_path, filename), sep='\t')

        # time features
        mean_abs = np.array(raw_data.abs().mean())
        std = np.array(raw_data.std())
        skew = np.array(raw_data.skew())
        kurtosis = np.array(raw_data.kurtosis())
        entropy = calculate_entropy(raw_data)
        rms = np.array(calculate_rms(raw_data))
        max_abs = np.array(raw_data.abs().max())
        p2p = calculate_p2p(raw_data)

        if id_set == 1:
            mean_abs = pd.DataFrame(mean_abs.reshape(
                1, 8), columns=[c+'_mean' for c in cols1])
            std = pd.DataFrame(std.reshape(1, 8), columns=[
                               c+'_std' for c in cols1])
            skew = pd.DataFrame(skew.reshape(1, 8), columns=[
                                c+'_skew' for c in cols1])
            kurtosis = pd.DataFrame(kurtosis.reshape(1, 8), columns=[
                                    c+'_kurtosis' for c in cols1])
            entropy = pd.DataFrame(entropy.reshape(1, 8), columns=[
                                   c+'_entropy' for c in cols1])
            rms = pd.DataFrame(rms.reshape(1, 8), columns=[
                               c+'_rms' for c in cols1])
            max_abs = pd.DataFrame(max_abs.reshape(
                1, 8), columns=[c+'_max' for c in cols1])
            p2p = pd.DataFrame(p2p.reshape(1, 8), columns=[
                               c+'_p2p' for c in cols1])
        else:
            mean_abs = pd.DataFrame(mean_abs.reshape(
                1, 4), columns=[c+'_mean' for c in cols2])
            std = pd.DataFrame(std.reshape(1, 4), columns=[
                               c+'_std' for c in cols2])
            skew = pd.DataFrame(skew.reshape(1, 4), columns=[
                                c+'_skew' for c in cols2])
            kurtosis = pd.DataFrame(kurtosis.reshape(1, 4), columns=[
                                    c+'_kurtosis' for c in cols2])
            entropy = pd.DataFrame(entropy.reshape(1, 4), columns=[
                                   c+'_entropy' for c in cols2])
            rms = pd.DataFrame(rms.reshape(1, 4), columns=[
                               c+'_rms' for c in cols2])
            max_abs = pd.DataFrame(max_abs.reshape(
                1, 4), columns=[c+'_max' for c in cols2])
            p2p = pd.DataFrame(p2p.reshape(1, 4), columns=[
                               c+'_p2p' for c in cols2])

        mean_abs.index = [filename]
        std.index = [filename]
        skew.index = [filename]
        kurtosis.index = [filename]
        entropy.index = [filename]
        rms.index = [filename]
        max_abs.index = [filename]
        p2p.index = [filename]

        # concat
        merge = pd.concat([mean_abs, std, skew, kurtosis,
                          entropy, rms, max_abs, p2p], axis=1)
        data = data.append(merge)

    if id_set == 1:
        cols = [c+'_'+tf for c in cols1 for tf in time_features]
        data = data[cols]
    else:
        cols = [c+'_'+tf for c in cols2 for tf in time_features]
        data = data[cols]

    data.index = pd.to_datetime(data.index, format='%Y.%m.%d.%H.%M.%S')
    data = data.sort_index()
    return data
