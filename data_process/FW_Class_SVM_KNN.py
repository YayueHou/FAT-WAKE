import numpy
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection  import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import LeaveOneOut


# feature_data : numpy with shape (datanum,24)
# KSS_annotation : numpy with shape (datanum,1)
# leave_oneout: bool to define whether to leave one out (take attention: leave one out will be very costly!!!)
# return is average accuracy of 10 fold cross verification repeat for twice
def FW_classby_SVM(feature_data,KSS_annotation,leave_oneout=0): 
    x=feature_data
    y=KSS_annotation
    average_acc = 0.0
    acc_std = 0.0
    acc = []
    if(leave_oneout):
        loo =  LeaveOneOut()
        loo.get_n_splits(x)
        index = 0
        for i,(train_index, test_index) in enumerate(loo.split(x)):
            train_X= x[train_index]
            train_y =y[train_index]
            test_X, test_y = x[test_index], y[test_index]
            regr = make_pipeline(StandardScaler(), SVC())
            regr.fit(train_X, train_y)
            y_pred = regr.predict(test_X)
            acc.append(accuracy_score(test_y, y_pred))
        acc=numpy.array(acc)
        print("SVM leave one out average_acc:", numpy.mean(acc), "std_acc:", numpy.std(acc))
    else:
        kf = RepeatedKFold(n_splits=10, n_repeats=2)
        for i,(train_index, test_index) in enumerate(kf.split(x)):
            train_X= x[train_index]
            train_y =y[train_index]
            test_X, test_y = x[test_index], y[test_index]
            regr = make_pipeline(StandardScaler(), SVC())
            regr.fit(train_X, train_y)
            y_pred = regr.predict(test_X)
            acc.append(accuracy_score(test_y, y_pred)) 
        acc=numpy.array(acc)
        print("SVM average_acc:", numpy.mean(acc), "std_acc:", numpy.std(acc))
    average_acc=numpy.mean(acc)
    acc_std=numpy.std(acc)
    return average_acc , acc_std



# feature_data : numpy with shape (datanum,24)
# KSS_annotation : numpy with shape (datanum,1)
# return is average accuracy of 10 fold cross verification repeat for twice
def FW_classby_KNN(feature_data,KSS_annotation): 
    x=feature_data
    y=KSS_annotation
    print(x.shape)
    k_range = range(1,100)
    k_error = []
    average_acc = 0.0
    acc_std = 0.0
    for k in k_range:
        knn = KNeighborsClassifier(n_neighbors=k)
        scores = cross_val_score(knn, x, y, cv=10, scoring='accuracy')
        k_error.append(1 - scores.mean())
    k_min=k_error.index(min(k_error))+1
    knn = KNeighborsClassifier(n_neighbors=k_min)
    scores = cross_val_score(knn, x, y, cv=10, scoring='accuracy')
    average_acc=scores.mean()
    acc_std=scores.std()
    print("KNN acc:",scores.mean(),"acc_std",scores.std())
    return average_acc, acc_std

