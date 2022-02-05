from improv_noise import inputUser, func
from improv_gaps import inputUser2
from improv_outliers import inputUser3
from metric_accuracy import accuracy
from metric_precision import precision
from metric_consistency import consistency
from metric_completeness import gaps
from heatmap import heatmap

def main():
    choice = input("Welcome! Please choose one of the following options that you'd like to explore \n 1) Accuracy metrics \n 2) Precision metrics \n 3) Consistency metrics \n 4) Completeness metrics \n 5) Noise improvement techniques \n 6) Gap improvement techniques \n 7) Outlier improvement techniques \n 8) Heap map \n 9) Exit \n")
    if choice == "1":
        accuracy()
        main()
    elif choice == "2":
        precision()
        main()
    elif choice == "3":
        consistency()
        main()
    elif choice == "4":
        gaps()
        main()
    elif choice == "5":
        inputUser()
        main()
    elif choice == "6":
        inputUser2()
        main()
    elif choice == "7":
        inputUser3()
        main()
    elif choice == "8":
        heatmap()
        main()
    else:
        exit()
if __name__ == '__main__':
    main()
