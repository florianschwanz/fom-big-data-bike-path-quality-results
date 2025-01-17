import glob
import inspect
import os
from email.utils import formatdate

import matplotlib.pyplot as plt
import numpy as np
from label_encoder import LabelEncoder
from matplotlib.ticker import PercentFormatter
from tracking_decorator import TrackingDecorator


def create_array(dataframes, slice_width):
    """
    Converts an array of data frame into a 3D numpy array

    axis-0 = epoch
    axis-1 = features in a measurement
    axis-2 = measurements in an epoch
    """

    array = []

    for name, dataframe in dataframes.items():
        if dataframe.shape[0] == slice_width:
            array.append(dataframe.to_numpy())

    return np.dstack(array).transpose(2, 1, 0)


def get_label(index):
    return LabelEncoder().classes[int(index)]


#
# Main
#

class BikeActivitySurfaceTypePlotter:

    @TrackingDecorator.track_time
    def run(self, logger, dataframes, slice_width, results_path, file_name, title, description, xlabel,
            run_after_label_encoding=False, clean=False, quiet=False):
        if len(dataframes) == 0:
            logger.log_line("✗️ Not plotting " + file_name + " because there are no dataframes to plot", console=False, file=True)
        else:
            # Make results path
            os.makedirs(results_path, exist_ok=True)

            # Clean results path
            if clean:
                files = glob.glob(os.path.join(results_path, file_name + ".png"))
                for f in files:
                    os.remove(f)

            array = create_array(dataframes, slice_width)
            target_column = list(dataframes.values())[0].columns.get_loc("bike_activity_surface_type")

            # 1D array with
            # axis-0 = TARGET of an epoch
            data = array[:, target_column, 1]

            if run_after_label_encoding:
                data = list(map(get_label, data))

            plt.figure(2, figsize=(10,6))
            plt.clf()
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel("amount")
            plt.hist(data, rwidth=0.8)
            plt.savefig(
                fname=os.path.join(results_path, file_name + "_absolute.png"),
                format="png",
                metadata={
                    "Title": title,
                    "Author": "Florian Schwanz",
                    "Creation Time": formatdate(timeval=None, localtime=False, usegmt=True),
                    "Description": description
                }
            )
            plt.close()

            plt.figure(2, figsize=(10,6))
            plt.clf()
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel("percentage")
            plt.hist(data, rwidth=0.8, weights=np.ones(len(data)) / len(data), align="left")
            plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
            plt.savefig(
                fname=os.path.join(results_path, file_name + "_relative.png"),
                format="png",
                metadata={
                    "Title": title,
                    "Author": "Florian Schwanz",
                    "Creation Time": formatdate(timeval=None, localtime=False, usegmt=True),
                    "Description": description
                }
            )
            plt.close()

            if not quiet:
                logger.log_line("✓️ Plotting " + file_name, console=False, file=True)

            class_name = self.__class__.__name__
            function_name = inspect.currentframe().f_code.co_name

            if not quiet:
                logger.log_line(class_name + "." + function_name + " plotted surface types")


    @TrackingDecorator.track_time
    def run_bar(self, logger, data, results_path, file_name, title, description, xlabel, clean=False, quiet=False):
        # Make results path
        os.makedirs(results_path, exist_ok=True)

        # Clean results path
        if clean:
            files = glob.glob(os.path.join(results_path, file_name + ".png"))
            for f in files:
                os.remove(f)

        plt.figure(2, figsize=(10,6))
        plt.clf()
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel("amount")
        plt.bar(data.keys(), list(data.values()))
        plt.savefig(
            fname=os.path.join(results_path, file_name + "_absolute_bar.png"),
            format="png",
            metadata={
                "Title": title,
                "Author": "Florian Schwanz",
                "Creation Time": formatdate(timeval=None, localtime=False, usegmt=True),
                "Description": description
            }
        )
        plt.close()

        plt.figure(2, figsize=(10,6))
        plt.clf()
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel("percentage")
        plt.bar(data.keys(), list(map(lambda x: x / sum(list(data.values())), list(data.values()))))
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
        plt.savefig(
            fname=os.path.join(results_path, file_name + "_relative_bar.png"),
            format="png",
            metadata={
                "Title": title,
                "Author": "Florian Schwanz",
                "Creation Time": formatdate(timeval=None, localtime=False, usegmt=True),
                "Description": description
            }
        )
        plt.close()

        if not quiet:
            logger.log_line("✓️ Plotting " + file_name, console=False, file=True)

        class_name = self.__class__.__name__
        function_name = inspect.currentframe().f_code.co_name

        if not quiet:
            logger.log_line(class_name + "." + function_name + " plotted surface types")