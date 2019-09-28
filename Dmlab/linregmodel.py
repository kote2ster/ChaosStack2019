from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np


class LinRegModel():
    coeffs = []
    def __init__(self, houses, degree=1):
        self.x = [[float(house['property'].split(' m2')[0]), float(house['balcony']), float(house['room'].split(' m2')[0]), float(house['small room'])] for house in houses]
        self.x = np.array(self.x).reshape((-1, 4))
        self.x = PolynomialFeatures(degree=degree, include_bias=False).fit_transform(self.x)

        self.y = [float(house['price'].split(' m')[0]) for house in houses]
        
        self.model = LinearRegression().fit(self.x, self.y)
        self.coeffs = self.model.coef_
        self.intercept = self.model.intercept_
    
    def predict(self, house):
        return self.model.predict(np.array([house['property'], house['balcony'], house['room'], house['small_room']]).reshape(-1, 4))
