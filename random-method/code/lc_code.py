import numpy as np
import matplotlib.pyplot as plt

from scipy import spatial

def mtx_similar3(arr1:np.ndarray, arr2:np.ndarray) ->float:
    '''
    :param arr1:矩阵1
    :param arr2:矩阵2
    :return:相似度（0~1之间）
    '''
    if arr1.shape != arr2.shape:
        minx = min(arr1.shape[0],arr2.shape[0])
        miny = min(arr1.shape[1],arr2.shape[1])
        differ = arr1[:minx,:miny] - arr2[:minx,:miny]
    else:
        differ = arr1 - arr2
    dist = np.linalg.norm(differ, ord='fro')
    len1 = np.linalg.norm(arr1)
    len2 = np.linalg.norm(arr2)     # 普通模长
    denom = (len1 + len2) / 2
    similar = 1 - (dist / denom)
    return similar


def EuclideanDistances(A, B):
    BT = B.transpose()
    # vecProd = A * BT
    vecProd = np.dot(A, BT)
    # print(vecProd)
    SqA = A ** 2
    # print(SqA)
    sumSqA = np.matrix(np.sum(SqA, axis=1))
    sumSqAEx = np.tile(sumSqA.transpose(), (1, vecProd.shape[1]))
    # print(sumSqAEx)

    SqB = B ** 2
    sumSqB = np.sum(SqB, axis=1)
    sumSqBEx = np.tile(sumSqB, (vecProd.shape[0], 1))
    SqED = sumSqBEx + sumSqAEx - 2 * vecProd
    SqED[SqED < 0] = 0.0
    ED = np.sqrt(SqED)
    return ED

def normalization(data):
    _range = np.max(data) - np.min(data)
    print(np.max(data))
    print(np.min(data))
    return (data - np.min(data)) / _range


matrix_1=np.random.random((50,100)).transpose()
matrix_2=np.random.random((50,100)).transpose()



similar_1=mtx_similar3(matrix_1,matrix_2)
similar_2=EuclideanDistances(matrix_1,matrix_2)
print(similar_1)
print(similar_2)
print((spatial.distance.cdist(matrix_1,matrix_2)).shape)
print(spatial.distance.cdist(matrix_1,matrix_2))
print(normalization(similar_2))

np.savetxt('sample.csv', matrix_2, delimiter=",")


plt.imshow(normalization(similar_2), vmin=0, vmax=1)
plt.colorbar()
plt.show()