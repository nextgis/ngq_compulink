# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ReconstructLine
 QGIS tool to reconstruct linear features from points

The main idea of the processing is to constrict Hamiltonian path.

To do it we use 1-d Self Organising Map. It allows:
  order data points
  connect nearest points

                              -------------------
        begin                : 2015-03-23
        git sha              : $Format:%H$
        copyright            : (C) 2015 by NextGIS

        email                : info@nextgis.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import numpy as np
from tuner import Tuner

EPSILON = 0.00001    # A small number

class SOM1d():
    '''1-d self organizing map for 2-dimmential inputs
    '''
    def __init__(self, data):
        assert len(data.shape) == 2

        self.z = np.array([complex(p[0], p[1]) for p in data])

        self.x_avg = np.average(data[:, 0], axis=0)
        self.y_avg = np.average(data[:, 1], axis=0)

        self.x_std = np.std(data[:, 0], axis=0)
        self.y_std = np.std(data[:, 1], axis=0)

        ratio = 4.0/3.0     # (Number of SOM unit) / (Number of points)
        self.w = np.zeros(data.shape[0]*ratio, dtype=np.complex)


    @property
    def size(self):
        return self.w.shape[0]

    def _normalize(self):
        self.z.real = (self.z.real - self.x_avg)/self.x_std
        self.z.imag = (self.z.imag - self.y_avg)/self.y_std


    def _denormalyze(self):
        self.z.real = self.x_std*self.z.real + self.x_avg
        self.z.imag = self.y_std*self.z.imag + self.y_avg

        self.w.real = self.x_std*self.w.real + self.x_avg
        self.w.imag = self.y_std*self.w.imag + self.y_avg

    def _distances(self, point):
        '''Return array of Euclidean distances between self.w and point
        '''
        diff = self.w - point
        return abs(diff)

    def _BMU_idx(self, point):
        '''Return index of best matching unit pf the point
        '''
        dists = self._distances(point)
        return np.argmin(dists)

    def _gaussian(self, c, sigma):
        """ Returns a Gaussian centered in c """
        d = 2*np.pi * sigma**2

        dists = range(self.size)-c
        ax = np.exp(-np.power(dists, 2)/d)

        return ax

    def _update(self, sigma):
        data = np.random.permutation(self.z)
        for point in data:
            bmu = self._BMU_idx(point)

            delta = (point - self.w[bmu])
            bubble = self._gaussian(bmu, sigma)
            delta = delta * bubble

            self.w += delta

    def _train(self,rlen, lrate=0.99, sigma_init=5.0):
        sigma = sigma_init
        for t in range(rlen):
            sigma = sigma * lrate
            if sigma < EPSILON:
                break
            self._update(sigma)

    def connect(self):
        # train SOM
        self._normalize()
        self._train(self.size*100, lrate=0.99, sigma_init=self.size)
        self._train(self.size*250, lrate=0.99, sigma_init=2)
        self._denormalyze()

        ordered = {}
        for point_id in range(len(self.z)):
            bmu = self._BMU_idx(self.z[point_id])
            try:
                ordered[bmu].append(point_id)
            except KeyError:
                ordered[bmu] = [point_id]

        order = []
        for i in range(self.size):
            try:
                pnts = ordered[i]
                if len(pnts) != 1:
                    for point_id in pnts:
                        order.append(point_id)
                else:
                    order.append(pnts[0])
            except KeyError:
                # It's Ok, if self.size > len(self.z)
                pass

        # Some shapes of points (eg., angles) are difficult for SOM.
        # Use a little of postprocessing for tuning
        tuner = Tuner(self.z)
        order = tuner.reorder(order)

        result = np.take(self.z, order)
        result = np.array([[z.real, z.imag] for z in result])

        return result


if __name__ == "__main__":
    data = np.array([
        [-0.1, 0],
        [0, 1.1],
        [0, 2.03],
        [0, 3.2],
        [0, 4.1],
        [0, 5.2],
        [0, 6.02],
        [1, 5.1],
        [1, 4.03],
        [3, 1.5],
        [2, 2.01],
        [1, 2],
        [1, 3]
    ])

    data1 = np.array([
        [34.773262991,52.656898974],
        [34.77316903,52.656709962],
        [34.772321032,52.656871984],
        [34.771443028,52.657045992],
        [34.770453963,52.657227963],
        [34.76949499,52.657386968],
        [34.768617991,52.657537004],
        [34.767743004,52.657693997],
        [34.766845973,52.65785099],
        [34.765947014,52.65802701],
        [34.765082002,52.658178974],
        [34.764174996,52.65833999],
        [34.763295986,52.658496983],
        [34.762430973,52.658654982],
        [34.761546012,52.658806024],
        [34.760566,52.658975003],
        [34.759678021,52.659143982],
        [34.75881502,52.659289995],
        [34.757920001,52.659457969],
        [34.757035039,52.659610016],
        [34.756114036,52.659775978],
        [34.755199989,52.659943029],
        [34.75427404,52.66009097],
        [34.753378015,52.660273025],
        [34.75253203,52.660425995],
        [34.751642961,52.660590028],
        [34.750703014,52.660750961],
        [34.74987899,52.660898985],
        [34.748970978,52.661063019],
        [34.748048969,52.661219006],
        [34.747141041,52.661388991],
        [34.746245015,52.661553025],
        [34.745294005,52.661717981],
        [34.744335031,52.661794005],
        [34.743413022,52.661860976],
        [34.742446002,52.661921997],
        [34.741450986,52.662007995],
        [34.740509028,52.662063986],
        [34.73963798,52.662112014],
        [34.738820996,52.662183009],
        [34.772797041,52.657160992],
        [34.771933034,52.657704977],
        [34.770236034,52.658766964],
        [34.769355012,52.659326037],
        [34.76850098,52.659875974],
        [34.767625993,52.660431024],
        [34.766791994,52.660960006],
        [34.765842995,52.661571968],
        [34.764949987,52.662127018],
        [34.764039963,52.662702017],
        [34.763292968,52.663179031],
        [34.762440026,52.663719999],
        [34.761606026,52.664241018],
        [34.760725005,52.664806964],
        [34.75988497,52.665335024],
        [34.75904502,52.66585202],
        [34.758163998,52.666408997],
        [34.757231008,52.667002017],
        [34.756441014,52.667503003],
        [34.755566027,52.668050006],
        [34.754646029,52.668644032],
        [34.753865004,52.669138983],
        [34.771071039,52.658235971]
    ])

    data2 = np.array([
        [34.746993016,52.706206022],
        [34.747126959,52.706670966],
        [34.747186974,52.707015965],
        [34.747258974,52.70734001],
        [34.747356037,52.707667993],
        [34.747418985,52.706163023],
        [34.747858029,52.706148019],
        [34.747888036,52.706127986],
        [34.748256002,52.706080042],
        [34.74869404,52.70605104],
        [34.748547021,52.704327973],
    ])

    som = SOM1d(data1)
    result = som.connect()

    #~ import matplotlib.pyplot as plt
    #~ plt.plot(som.z.real, som.z.imag, 'o',
            #~ # som.w.real, som.w.imag, 'r-o',
            #~ result[:, 0], result[:, 1], '-g')
    #~ plt.show()
