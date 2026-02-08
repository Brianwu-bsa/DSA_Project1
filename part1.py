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
        print("=" * 10, "First 10 rows", "="*10)
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




if __name__ == "__main__":
    data_processor = DataProcessor("covid19cases_test.csv")
    data_processor.plot_bar_chart(data_processor.data_2d,"area", "cases", "Top 10 Areas by Cases (Unsorted)")

