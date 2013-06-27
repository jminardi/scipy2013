import numpy as np
from traits.api import HasStrictTraits, Int, Instance, Any
from chaco.api import Plot, ArrayPlotData


class IOController(HasStrictTraits):

    ### Current Sensor Values  ################################################

    acc_x = Int(plot_data=True)
    acc_y = Int(plot_data=True)
    acc_z = Int(plot_data=True)

    ### Plots  ################################################################

    acc_x_plot = Instance(Plot)
    acc_y_plot = Instance(Plot)
    acc_z_plot = Instance(Plot)
    plot_data = Instance(ArrayPlotData)

    ### Private Traits  #######################################################

    _logo_ax = Any()

    ### Trait Defaults  #######################################################

    def _acc_x_plot_default(self):
        plot = Plot(self.plot_data)
        plot.plot(('acc_x',))
        plot.padding = (0, 0, 0, 0)
        return plot

    def _acc_y_plot_default(self):
        plot = Plot(self.plot_data)
        plot.plot(('acc_y',))
        plot.padding = (0, 0, 0, 0)
        return plot

    def _acc_z_plot_default(self):
        plot = Plot(self.plot_data)
        plot.plot(('acc_z',))
        plot.padding = (0, 0, 0, 0)
        return plot

    def _plot_data_default(self):
        plot_data = ArrayPlotData()
        plot_data.set_data('acc_x', np.zeros(50))
        plot_data.set_data('acc_y', np.zeros(50))
        plot_data.set_data('acc_z', np.zeros(50))
        return plot_data

    def push_to_plot_data(self):
        for name, value in self.get(plot_data=True).iteritems():
            # XXX This is causing NSConcreteMapTable to leak
            ary = self.plot_data[name]
            if ary is not None:
                ary = np.append(ary, value)
                ary = ary[-50:]
                self.plot_data.set_data(name, ary)
