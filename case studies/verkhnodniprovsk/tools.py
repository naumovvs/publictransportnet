from sklearn import linear_model
from scipy import stats
import numpy as np

def make_regression(X, Y, alpha=0.1, verbose=False):
    '''
    Performs the regression analysis:
    * calculates coefficients for multiple linear regression
    * estimates the coefficient of determination
    * provides confidence intervals for the given alpha
    Arguments:
    X - explanatory variables
    Y - an explained variable
    alpha - significance level
    Returns the fitted model, the determination coefficient, and confidence intervals
    '''
    rmodel = linear_model.LinearRegression()
    # estimate regression coefficients
    rmodel.fit(X, Y)
    if verbose:
        print(f'intercept={rmodel.intercept_}')
        print(f'coefs={rmodel.coef_}')
    # get the model predictions
    mY = rmodel.predict(X)
    # calculate residuals
    errors = mY - Y
    # calculate empirical average of the explained variable
    avgY = Y.mean()
    # estimate the coefficient of determination
    r2 = 1 - sum([e*e for e in errors]) / sum([(y - avgY)**2 for y in Y])
    if verbose: print(f'R2={r2}')
    # calculate the number of the degrees of freedom
    df = len(X) - len(rmodel.coef_) - 1
    s2 = sum([e*e for e in errors]) / df
    # get t-variable for the provided alpha and estimated df
    t_alpha = stats.t.ppf(1 - alpha / 2, df)
    if verbose: print(f't_alfa({alpha},{df})={t_alpha}')
    XTX = X.T.dot(X)
    invXTX = np.matrix(XTX).I
    # calculate confidence intervals
    bounds = {}
    for i in range(len(rmodel.coef_)):
        if invXTX[i, i] > 0:
            LB = rmodel.coef_[i] - t_alpha * np.sqrt(s2 * invXTX[i, i])
            UB = rmodel.coef_[i] + t_alpha * np.sqrt(s2 * invXTX[i, i])
            bounds[i] = (LB, UB)
            if verbose: print(f'coef{i + 1}\t{LB*UB > 0}\t{LB}\t{UB}')
    return rmodel, r2, bounds