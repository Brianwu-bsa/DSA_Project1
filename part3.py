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

    def insertion_sort(self, colum_name):
        index_to_sort_by = self.get_col_index(colum_name)
        data = self.data_2d.copy()

        return []

    #
    #
    # def merge_sort(self):

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
            sorted_data = self.quick_sort(self.data_2d, "area") 

            # Success
            result = self.binary_search(sorted_data, "area", success)
            print(f"Searching for '{success}': Result Index {result}")
            
            # Failure
            result = self.binary_search(sorted_data, "area", fail)
            print(f"Searching for '{fail}': Result Index {result}")


if __name__ == "__main__":
    data_processor = DataProcessor("covid19cases_test.csv")
    # data_processor.plot_bar_chart(data_processor.data_2d, "area", "cases", "Top 10 Areas by Cases (Unsorted)")
