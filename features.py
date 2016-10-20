'''
features.py
feature extraction for ink/no-ink vectors
'''

__author__ = "Jack Bandy"
__email__ = "jgba225@g.uky.edu"

import numpy as np
from sklearn import preprocessing


def extract_for_vol(volume, surf_pts, CUT_IN, CUT_BACK, NEIGH_RADIUS, THRESH):
    USE_SINGLE = True
    USE_NEIGH = True

    output_dims = (volume.shape[0], volume.shape[1])

    features = []

    features_filename = "feat_cache/features-in{}-back{}-neigh{}".format(
            CUT_IN, CUT_BACK, NEIGH_RADIUS)
    try:
        features = np.load(features_filename+".npy")
        print("loaded features from file")
        return features
    except Exception:
        pass

    # single-vector features calculate
    depth_vals = np.zeros(output_dims,dtype=np.float64)
    avg_vals = np.zeros(output_dims,dtype=np.float64)
    sum_vals = np.zeros(output_dims,dtype=np.float64)
    min_vals = np.zeros(output_dims,dtype=np.float64)
    max_vals = np.zeros(output_dims,dtype=np.float64)
    std_vals = np.zeros(output_dims,dtype=np.float64)
    for i in range(volume.shape[0]):
        for j in range(volume.shape[1]):
            srf = surf_pts[i,j] - CUT_BACK
            if srf < 0: srf = 0
            cut = srf + CUT_IN
            #print("srf = {}, cut = {}".format(srf,cut))
            tmp_vect = volume[i,j][srf:cut]
            #print(tmp_vect)

            depth = np.count_nonzero(np.where(tmp_vect > THRESH, tmp_vect, 0))
            depth_vals[i,j] = depth

            avg_vals[i,j] = np.mean(tmp_vect)
            sum_vals[i,j] = np.sum(tmp_vect)
            min_vals[i,j] = np.min(tmp_vect)
            max_vals[i,j] = np.max(tmp_vect)
            std_vals[i,j] = np.std(tmp_vect)

    if USE_SINGLE:
        features.append(preprocessing.normalize(np.nan_to_num(sum_vals)))
        features.append(preprocessing.normalize(depth_vals))
        features.append(preprocessing.normalize(avg_vals))
        features.append(preprocessing.normalize(np.nan_to_num(min_vals)))
        features.append(preprocessing.normalize(np.nan_to_num(max_vals)))
        features.append(preprocessing.normalize(np.nan_to_num(std_vals)))

    print("single-vector features: {}".format(len(features)))


    # neighborhood features
    NR = NEIGH_RADIUS
    mean_neigh = np.zeros(output_dims, dtype=np.float64)
    sum_neigh = np.zeros(output_dims, dtype=np.float64)
    surf_stdev_neigh = np.zeros(output_dims, dtype=np.float64)
    depth_neigh = np.zeros(output_dims, dtype=np.float64)

    if USE_NEIGH:
        for i in range(NR, volume.shape[0]-NR):
            for j in range(NR, volume.shape[1]-NR):
                srf = surf_pts[i,j] - CUT_BACK
                if srf < 0: srf = 0
                cut = srf + CUT_IN
                neigh_vects = volume[i-NR:i+NR+1, j-NR:j+NR+1, srf:cut]
                mean_neigh[i,j] = np.mean(neigh_vects.flatten()).astype(np.float64)
                sum_neigh[i,j] = np.sum(neigh_vects.flatten()).astype(np.float64)
                surf_stdev_neigh[i,j] = np.std(neigh_vects.flatten()).astype(np.float64)
                depth_neigh[i,j] = np.count_nonzero(
                        np.where(neigh_vects < THRESH, neigh_vects, 0).flatten())
        features.append(preprocessing.normalize(np.nan_to_num(mean_neigh)))
        features.append(preprocessing.normalize(np.nan_to_num(sum_neigh)))
        features.append(preprocessing.normalize(np.nan_to_num(surf_stdev_neigh)))
        features.append(preprocessing.normalize(np.nan_to_num(depth_neigh)))


    features = np.array(features)
    print("total features: {}".format(len(features)))
    features = np.swapaxes(features,1,2)
    features = np.swapaxes(features,0,2)

    np.save(features_filename, features)
    return features
