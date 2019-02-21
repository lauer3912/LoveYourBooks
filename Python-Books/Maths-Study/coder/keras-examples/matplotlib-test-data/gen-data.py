# -*- coding: utf-8 -*-

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD

# Step 1: 选择模型
model = Sequential()

# Step 2: 构建网络层
model.add(Dense(output_dim=1, input_dim=1))
model.add(Activation('tanh'))
model.add(Dropout(0.5))

# Step 3: 编译
model.compile(loss='mse', optimizer=SGD(lr=0.01, momentum=0.9, nesterov=True))

# Step 4: 训练

# Step 4.1: 生成训练数据
import numpy as np
import matplotlib.pyplot as plt

X = np.linspace(-2, 6, 200)
np.random.shuffle(X)
Y = 0.5 * X + 2 + 0.15 * np.random.randn(200,)

# plot data
plt.scatter(X, Y)
plt.show()

X_train, Y_train = X[:160], Y[:160]
X_test, Y_test = X[160:], Y[160:]

# Step 4.2: 开始训练
model.fit(X_train, Y_train, epochs=100, batch_size=64)

print('Training -----------------')
for step in range(100):
    cost = model.train_on_batch(X_test, Y_test)
    if step % 20 == 0:
        print('train cost:', cost)


cost = model.evaluate(X_test, Y_test, batch_size=40)