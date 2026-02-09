import copy
import time
import pandas as pd
import matplotlib.pyplot as plt


class DataProcessor:
    def __init__(self, file_path, seed=100):

        df = pd.read_csv(file_path)
        df.fillna(0, inplace=True)
        random_sample = df.sample(n=1000, replace=False, random_state=seed)

        self.data_2d = random_sample.values.tolist()
        self.headers = random_sample.columns.tolist()

        self.print_data()

    def print_data(self):
        print("Headers:")
        print(self.headers, "\n")

        # print the first 10 rows
        print("=" * 10, "First 10 rows", "=" * 10)
        for row in self.data_2d[:10]:
            print(row)

        print("Last 10 rows")
        for row in self.data_2d[-10:]:
            print(row)

    def get_col_index(self, col_name):
        """
        :param col_name: The column name we are searching for
        :return: The index in which it exists in self.
        Note that this will return an error if the column name doesn't exist
        """
        return self.headers.index(col_name)

    def plot_bar_chart(self, data, x_col, y_col, title):
        """
        :param x_col: The column for the x axis
        :param y_col: The y-values we plot agains the x-asix
        :param title: The title of the graph
        :return:
        """
        x_idx = self.get_col_index(x_col)
        y_idx = self.get_col_index(y_col)

        # Extract data for plotting (first top_n rows)
        plot_data = data[:10]
        x_values = [str(row[x_idx]) for row in plot_data]
        y_values = [row[y_idx] for row in plot_data]

        plt.figure(figsize=(10, 6))
        plt.bar(x_values, y_values, color='skyblue')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(title)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_sorting_performance(self):
        sizes = [100, 300, 500, 800, 1000]  # more data points for fancier graph
        times_insertion = []
        times_merge = []
        times_quick = []

        # Use a numerical column for sorting performance test
        sort_col = 'cases'

        print("\nRunning Sorting Performance Test...")
        for size in sizes:
            subset = copy.deepcopy(self.data_2d[:size])

            # Insertion Sort Time
            start = time.time()
            self.insertion_sort(subset, sort_col)
            times_insertion.append(time.time() - start)

            # Merge Sort Time
            subset = copy.deepcopy(self.data_2d[:size])
            start = time.time()
            self.merge_sort(subset, sort_col)
            times_merge.append(time.time() - start)

            # Quick Sort Time
            subset = copy.deepcopy(self.data_2d[:size])
            start = time.time()
            self.quick_sort(subset, sort_col, 0, len(subset) - 1)
            times_quick.append(time.time() - start)

            print(
                f"Size {size}: Ins={round(times_insertion[-1], 4)}s "
                f"Mrg={round(times_merge[-1], 4)}s "
                f"Qck={round(times_quick[-1])}s ")

        plt.figure(figsize=(10, 6))
        plt.plot(sizes, times_insertion, label='Insertion Sort', marker='o')
        plt.plot(sizes, times_merge, label='Merge Sort', marker='o')
        plt.plot(sizes, times_quick, label='Quick Sort', marker='o')
        plt.xlabel('Input Size (Number of Rows)')
        plt.ylabel('Time (Seconds)')
        plt.title('Sorting Algorithm Performance Comparison')
        plt.legend()
        plt.grid(True)
        plt.show()

    def insertion_sort(self, data, column_name):
        """
        Insertion Sort Algorithm
        :param data: 2d list representing the data to be sorted
        :param column_name: The column name we want to sort by
        :return: The sorted data
        """
        col_index = self.get_col_index(column_name)
        # we start from the second element since we consider the first element as sorted
        for i in range(1, len(data)):
            key_row =data[i] # the row we want to insert into the sorted part
            key_value = key_row[col_index] # the value we want to sort by

            j = i - 1
            # we want to shift the elements in the sorted part to the right until we find the correct position for the key_row
            while j>=0 and data[j][col_index] > key_value:
                data[j+1] = data[j]
                j-=1

        # insert the key_row into the correct position
            data[j+1] = key_row
        return data


    def merge_sort(self, data, column_name):
        col_index = self.get_col_index(column_name)

        # divide in half by
        # base case
        if len(data) > 1:  # we want to return the data if we have just 1 element
            mid = len(data) // 2
            left = data[:mid]
            right = data[mid:]

            left = self.merge_sort(left, column_name)  # split it until 1 element remains
            right = self.merge_sort(right, column_name)

            i = j = k = 0
            # i for the keeping track of the left index
            # j for the keeping track of the right index
            # k for the keeping track merge array's current index

            # merge it back
            while i < len(left) and j < len(right):
                if left[i][col_index] < right[j][col_index]:  # we take the left one since it is smaller
                    data[k] = left[i]
                    i += 1
                else:  # take the right one since smaller than left
                    data[k] = right[j]
                    j += 1
                k += 1
            # only merges to the minimum of len(left) len(right)

            # merge the remaining parts
            while i < len(left):
                data[k] = left[i]
                i += 1
                k += 1

            while j < len(right):
                data[k] = right[j]
                j += 1
                k += 1

        return data

    def quick_sort(self, data, column_name, low, high):
        col_index = self.get_col_index(column_name)

        if low < high:
            # Partitioning index
            pi = self._partition(data, col_index, low, high)

            # Recursively sort elements before partition and after partition
            self.quick_sort(data, column_name, low, pi - 1)
            self.quick_sort(data, column_name, pi + 1, high)
        return data

    def _partition(self, data, col_index, low, high):
        pivot = data[high][col_index]
        i = low - 1
        for j in range(low, high):
            if data[j][col_index] <= pivot:
                i += 1
                data[i], data[j] = data[j], data[i]
        data[i + 1], data[high] = data[high], data[i + 1]
        return i + 1

    def str_check(self, v):
        if isinstance(v, str):
            return v.strip().lower()
        return v


    def compare(self, a, b):
        a = self.str_check(a)
        b = self.str_check(b)

        # numeric compare
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            if a == b:
                return 0
            return -1 if a < b else 1

        # string compare
        if isinstance(a, str) and isinstance(b, str):
            if a == b:
                return 0
            return -1 if a < b else 1

        return None


    def linear_search(self, data, column_name, value):
        index = self.get_col_index(column_name)

        for i, row in enumerate(data):
            if self.compare(row[index], value) == 0:
                return i

        return -1


    def binary_search(self, sorted_data, column_name, value):
        index = self.get_col_index(column_name)
        low, high = 0, len(sorted_data) - 1

        while low <= high:
            mid = (low + high) // 2
            cmp = self.compare(sorted_data[mid][index], value)

            if cmp is None:
                return -1
        
            if cmp == 0:
                return mid
            elif cmp < 0:
                low = mid + 1
            else:
                high = mid - 1

        return -1


    def perform_search(self):
            success = "Alameda"
            fail = "Meatball"
            
            print(f"\nLinear")
            # Success
            result = self.linear_search(self.data_2d, "area", success)
            print(f"Searching for '{success}': Result Index {result}")
            
            # Failure
            result = self.linear_search(self.data_2d, "area", fail)
            print(f"Searching for '{fail}': Result Index {result}")


            print(f"\nBinary")
            sorted_data = self.merge_sort(self.data_2d, "area")

            # Success
            result = self.binary_search(sorted_data, "area", success)
            print(f"Searching for '{success}': Result Index {result}")
            
            # Failure
            result = self.binary_search(sorted_data, "area", fail)
            print(f"Searching for '{fail}': Result Index {result}")


if __name__ == "__main__":
    data_processor = DataProcessor("covid19cases_test.csv")
    data_processor.plot_bar_chart(data_processor.data_2d,"area", "cases", "Top 10 Areas by Cases (Unsorted)")

    data_processor.plot_sorting_performance()
    data_processor.perform_search()



