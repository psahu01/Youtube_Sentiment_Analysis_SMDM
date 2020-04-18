import pandas as p
import numpy as np
from matplotlib import pyplot

dataframe = p.read_json("comments/" + "Dude Perfect" + "_stats.json")
dataframe.info()
dataframe.shape

# X = dataframe.drop(['kind','etag','id','title','likedislikeratio'],axis=1)
X = p.DataFrame(dataframe, columns=["positive", "negative", "viewCount", "commentCount"])
#

X.head()

# Y = dataframe['likedislikeratio']
Y = p.DataFrame(dataframe, columns=["likedislikeratio"])

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

from sklearn.preprocessing import StandardScaler

sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)

sc_y = StandardScaler()
y_train = sc_y.fit_transform(y_train)
# y_test = sc_y.fit_transform(y_test)

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

Rfc = RandomForestRegressor(random_state=2)

fitResultR = Rfc.fit(X_train, y_train)
predictedValues = fitResultR.predict(X_test)
print("MAE:", mean_absolute_error(y_test, predictedValues))
print("MSE:", mean_squared_error(y_test, predictedValues))
print("RMSE:", np.sqrt(mean_squared_error(y_test, predictedValues)))
print("R2:", r2_score(y_test, predictedValues))

from sklearn.linear_model import LinearRegression

LinR = LinearRegression()

fitResult = LinR.fit(X_train, y_train)
y_pred = fitResult.predict(X_test)
print("MAE:", mean_absolute_error(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R2:", r2_score(y_test, y_pred))

from sklearn.ensemble import AdaBoostRegressor

Boost_Lin = AdaBoostRegressor(base_estimator=LinR, random_state=2)

fitResultBl = Boost_Lin.fit(X_train, y_train)
predictedValues = fitResultBl.predict(X_test)
print("MAE:", mean_absolute_error(y_test, predictedValues))
print("MSE:", mean_squared_error(y_test, predictedValues))
print("RMSE:", np.sqrt(mean_squared_error(y_test, predictedValues)))
print("R2:", r2_score(y_test, predictedValues))

from sklearn.neural_network import MLPRegressor

mlp = MLPRegressor(random_state=0, activation="relu", hidden_layer_sizes=16)

mlp.fit(X_train, y_train)

predictedValues = mlp.predict(X_test)
print("MAE:", mean_absolute_error(y_test, predictedValues))
print("MSE:", mean_squared_error(y_test, predictedValues))
print("RMSE:", np.sqrt(mean_squared_error(y_test, predictedValues)))
print("R2:", r2_score(y_test, predictedValues))

from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline

# load dataset
# define base model
def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(15, input_dim=4, kernel_initializer="normal", activation="relu"))
    model.add(Dense(1, kernel_initializer="normal"))
    # Compile model
    model.compile(loss="mean_squared_error", optimizer="adam", metrics=["accuracy"])
    return model


# evaluate model
estimators = []
estimators.append(("standardize", StandardScaler()))
estimators.append(("mlp", KerasRegressor(build_fn=baseline_model, epochs=50, batch_size=5, verbose=0)))
pipeline = Pipeline(estimators)
kfold = KFold(n_splits=10)
results = cross_val_score(pipeline, X, Y, cv=kfold)
print("Standardized: %.2f (%.2f) MSE" % (results.mean(), results.std()))
print("RMSE: %2.f" % (results.std() ** (1 / 2)))

print()
