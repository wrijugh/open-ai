import pandas as pd 
def showdata():
    print('showdata')
    df = pd.read_csv("books_new.csv")

    return df  


if __name__ == '__main__':
    showdata()