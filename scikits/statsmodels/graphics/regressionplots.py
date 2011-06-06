'''Partial Regression plot and residual plots to find misspecification


Author: josef-pktd
Created: 2011-01-23

update
2011-06-05 : start to convert example to usable functions

'''

from scikits.statsmodels.sandbox.regression.predstd import wls_prediction_std

def plot_fit(res, exog_idx, y_true=None):
    '''plot fit against one regressor

    check for which other models than OLS this also works, use model.name
    '''
    import matplotlib.pyplot as plt

    #maybe add option for wendog, wexog
    y = res.model.endog
    x1 = res.model.exog[:, exog_idx]

    #plt.figure()
    plt.plot(x1, y, 'bo')
    if not y_true is None:
        plt.plot(x1, y_true, 'b-')
        title = 'fitted versus regressor %d, blue: true,   black: OLS' % exog_idx
    else:
        title = 'fitted versus regressor %d, blue: observed, black: OLS' % exog_idx

    prstd, iv_l, iv_u = wls_prediction_std(res)
    plt.plot(x1, res.fittedvalues, 'k-') #'k-o')
    #plt.plot(x1, iv_u, 'r--')
    #plt.plot(x1, iv_l, 'r--')
    plt.fill_between(x1, iv_l, iv_u, alpha=0.1, color='k')
    plt.title(title)




def plot_regress_exog(res, exog_idx):
    '''plot regression results against one regressor

    '''

    import matplotlib.pyplot as plt

    #maybe add option for wendog, wexog
    #y = res.endog
    x1 = res.model.exog[:,exog_idx]


    fig2 = plt.figure()

    ax = fig2.add_subplot(2,2,1)
    #namestr = ' for %s' % self.name if self.name else ''
    plt.plot(x1, res.model.endog, 'o')
    ax.set_title('endog versus exog', fontsize='small')# + namestr)

    ax = fig2.add_subplot(2,2,2)
    #namestr = ' for %s' % self.name if self.name else ''
    ax.plot(x1, res.resid, 'o')
    ax.axhline(y=0)
    ax.set_title('residuals exog', fontsize='small')# + namestr)

    ax = fig2.add_subplot(2,2,3)
    #namestr = ' for %s' % self.name if self.name else ''
    plt.plot(x1, res.fittedvalues, 'o')
    ax.set_title('Fitted versus exog', fontsize='small')# + namestr)

    ax = fig2.add_subplot(2,2,4)
    #namestr = ' for %s' % self.name if self.name else ''
    plt.plot(x1, res.fittedvalues + res.resid, 'o')
    ax.set_title('Fitted plus residuals versus exog', fontsize='small')# + namestr)


def plot_partregress(endog, exog, exog_idx=None, grid=None):
    '''plot partial regression for a set of regressors

    see http://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/partregr.htm
    '''


    #maybe add option for using wendog, wexog instead
    y = res.model.endog

    #x1 = res.exog[exog_idx]
    if not grid is None:
        nrows, ncols = grid
    else:
        if len(exog_idx) > 2:
            nrows = int(np.ceil(len(exog_idx)/2.))
            ncols = 2
        else:
            nrows = len(exog_idx)
            ncols = 1


    k_vars = res.model.exog.shape[1]
    #this function doesn't make sense if k_vars=1

    fig5 = plt.figure()

    for i,idx in enumerate(exog_idx):
        others = range(k_vars)
        others.pop(idx)
        exog_others = exog[:, others]
        ax = fig5.add_subplot(nrows, ncols, i+1)
        #namestr = ' for %s' % self.name if self.name else ''
        res1a = sm.OLS(y, exog_others).fit()
        res1b = sm.OLS(exog[:, idx], exog_others).fit()
        plt.plot(res1b.resid, res1a.resid, 'o')
        res1c = sm.OLS(res1a.resid, res1b.resid).fit()
        plt.plot(res1b.resid, res1c.fittedvalues, '-', color='k')
        ax.set_title('Partial Regression plot %d' % idx)# + namestr)



def plot_ccpr(res, exog_idx=None):
    '''plto CCPR against 1 regressor

    see http://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/ccpr.htm

    '''

    x1 = res.model.exog[:,exog_idx]

    fig6 = plt.figure()
    ax = fig6.add_subplot(1,1,1)
    #namestr = ' for %s' % self.name if self.name else ''
    x1beta = x1*res.params[1]
##    x2beta = x2*res.params[2]
    ax.plot(x1, x1beta + res.resid, 'o')
    ax.plot(x1, x1beta, '-')
    ax.set_title('X_%d beta_%d plus residuals versus exog (CCPR)' % (
                                                exog_idx, exog_idx))
##    ax = fig6.add_subplot(2,1,2)
##    plt.plot(x2, x2beta + res.resid, 'o')
##    plt.plot(x2, x2beta, '-')



if __name__ == '__main__':
    import numpy as np
    import scikits.statsmodels.api as sm
    import matplotlib.pyplot as plt

    from scikits.statsmodels.sandbox.regression.predstd import wls_prediction_std

    #example from tut.ols with changes
    #fix a seed for these examples
    np.random.seed(9876789)

    # OLS non-linear curve but linear in parameters
    # ---------------------------------------------

    nsample = 100
    sig = 0.5
    x1 = np.linspace(0, 20, nsample)
    x2 = 5 + 3* np.random.randn(nsample)
    X = np.c_[x1, x2, np.sin(0.5*x1), (x2-5)**2, np.ones(nsample)]
    beta = [0.5, 0.5, 1, -0.04, 5.]
    y_true = np.dot(X, beta)
    y = y_true + sig * np.random.normal(size=nsample)

    #estimate only linear function, misspecified because of non-linear terms
    exog0 = sm.add_constant(np.c_[x1, x2], prepend=False)

#    plt.figure()
#    plt.plot(x1, y, 'o', x1, y_true, 'b-')

    res = sm.OLS(y, exog0).fit()
    #print res.params
    #print res.bse


    plot_old = 0 #True
    if plot_old:

        #current bug predict requires call to model.results
        #print res.model.predict
        prstd, iv_l, iv_u = wls_prediction_std(res)
        plt.plot(x1, res.fittedvalues, 'r-o')
        plt.plot(x1, iv_u, 'r--')
        plt.plot(x1, iv_l, 'r--')
        plt.title('blue: true,   red: OLS')

        plt.figure()
        plt.plot(res.resid, 'o')
        plt.title('Residuals')

        fig2 = plt.figure()
        ax = fig2.add_subplot(2,1,1)
        #namestr = ' for %s' % self.name if self.name else ''
        plt.plot(x1, res.resid, 'o')
        ax.set_title('residuals versus exog')# + namestr)
        ax = fig2.add_subplot(2,1,2)
        plt.plot(x2, res.resid, 'o')

        fig3 = plt.figure()
        ax = fig3.add_subplot(2,1,1)
        #namestr = ' for %s' % self.name if self.name else ''
        plt.plot(x1, res.fittedvalues, 'o')
        ax.set_title('Fitted values versus exog')# + namestr)
        ax = fig3.add_subplot(2,1,2)
        plt.plot(x2, res.fittedvalues, 'o')

        fig4 = plt.figure()
        ax = fig4.add_subplot(2,1,1)
        #namestr = ' for %s' % self.name if self.name else ''
        plt.plot(x1, res.fittedvalues + res.resid, 'o')
        ax.set_title('Fitted values plus residuals versus exog')# + namestr)
        ax = fig4.add_subplot(2,1,2)
        plt.plot(x2, res.fittedvalues + res.resid, 'o')

        # see http://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/partregr.htm
        fig5 = plt.figure()
        ax = fig5.add_subplot(2,1,1)
        #namestr = ' for %s' % self.name if self.name else ''
        res1a = sm.OLS(y, exog0[:,[0,2]]).fit()
        res1b = sm.OLS(x1, exog0[:,[0,2]]).fit()
        plt.plot(res1b.resid, res1a.resid, 'o')
        res1c = sm.OLS(res1a.resid, res1b.resid).fit()
        plt.plot(res1b.resid, res1c.fittedvalues, '-')
        ax.set_title('Partial Regression plot')# + namestr)
        ax = fig5.add_subplot(2,1,2)
        #plt.plot(x2, res.fittedvalues + res.resid, 'o')
        res2a = sm.OLS(y, exog0[:,[0,1]]).fit()
        res2b = sm.OLS(x2, exog0[:,[0,1]]).fit()
        plt.plot(res2b.resid, res2a.resid, 'o')
        res2c = sm.OLS(res2a.resid, res2b.resid).fit()
        plt.plot(res2b.resid, res2c.fittedvalues, '-')

        # see http://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/ccpr.htm
        fig6 = plt.figure()
        ax = fig6.add_subplot(2,1,1)
        #namestr = ' for %s' % self.name if self.name else ''
        x1beta = x1*res.params[1]
        x2beta = x2*res.params[2]
        plt.plot(x1, x1beta + res.resid, 'o')
        plt.plot(x1, x1beta, '-')
        ax.set_title('X_i beta_i plus residuals versus exog (CCPR)')# + namestr)
        ax = fig6.add_subplot(2,1,2)
        plt.plot(x2, x2beta + res.resid, 'o')
        plt.plot(x2, x2beta, '-')


        #print res.summary()

    plot_fit(res, 0, y_true=None)
    plot_partregress(y, exog0, exog_idx=[0,1])
    plot_regress_exog(res, exog_idx=[0])
    plot_ccpr(res, exog_idx=0)
    plot_ccpr(res, exog_idx=1)

    plt.show()
