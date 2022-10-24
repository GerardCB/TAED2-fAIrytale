import pandas as pd

# Test for decreasing loss after each epoch

epoch_loss = pd.read_csv("epoch_loss.csv").iloc[1:,:]
n_models = (len(epoch_loss.columns) - 1)//3
eps = 0.05

def test_decreasing_epoch_loss():
	for model in range(n_models):
		for epoch in epoch_loss.iloc[:,0]:
			epoch -= 1
			if epoch != 0:
				prevloss = epoch_loss.iloc[epoch - 1, model*n_models + 1]
				loss = epoch_loss.iloc[epoch, model*n_models + 1]

				assert prevloss*(1 + eps) > loss