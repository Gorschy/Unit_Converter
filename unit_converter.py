import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QTabWidget
from PyQt5.QtCore import Qt
from math import pow

class ConverterTab(QWidget):
    def __init__(self, units, conversion_funcs):
        super().__init__()
        self.units = units
        self.conversion_funcs = conversion_funcs
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        self.input_unit = QComboBox()
        self.input_unit.addItems(self.units)
        self.input_value = QLineEdit()
        self.output_unit = QComboBox()
        self.output_unit.addItems(self.units)
        self.output_value = QLineEdit()

        layout.addWidget(self.input_unit)
        layout.addWidget(self.input_value)
        layout.addWidget(self.output_unit)
        layout.addWidget(self.output_value)

        self.setLayout(layout)

        # Connect signals and slots
        self.input_value.textChanged.connect(self.perform_conversion)
        self.input_unit.currentIndexChanged.connect(self.perform_conversion)
        self.output_unit.currentIndexChanged.connect(self.perform_conversion)

    def perform_conversion(self):
        try:
            input_value = float(self.input_value.text())
            input_unit = self.input_unit.currentText()
            output_unit = self.output_unit.currentText()

            # Convert to base unit
            input_to_base = self.conversion_funcs[(input_unit, 'Base')]
            base_value = input_to_base(input_value)

            # Convert from base unit
            base_to_output = self.conversion_funcs[('Base', output_unit)]
            output_value = base_to_output(base_value)

            self.output_value.setText(str(output_value))
        except ValueError:
            # If the input value can't be converted to float, clear the output value
            self.output_value.clear()


class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

        # Define units and conversion functions for each type

        # Length tab
        length_units = ['Millimeter', 'Centimeter', 'Meter', 'Kilometer', 'Mile', 'Yard', 'Foot', 'Inch']
        length_conversions = {
            ('Millimeter', 'Base'): lambda x: x / 1000,
            ('Base', 'Millimeter'): lambda x: x * 1000,
            ('Centimeter', 'Base'): lambda x: x / 100,
            ('Base', 'Centimeter'): lambda x: x * 100,
            ('Meter', 'Base'): lambda x: x,
            ('Base', 'Meter'): lambda x: x,
            ('Kilometer', 'Base'): lambda x: x * 1000,
            ('Base', 'Kilometer'): lambda x: x / 1000,
            ('Mile', 'Base'): lambda x: x * 1609.34,
            ('Base', 'Mile'): lambda x: x / 1609.34,
            ('Yard', 'Base'): lambda x: x * 0.9144,
            ('Base', 'Yard'): lambda x: x / 0.9144,
            ('Foot', 'Base'): lambda x: x * 0.3048,
            ('Base', 'Foot'): lambda x: x / 0.3048,
            ('Inch', 'Base'): lambda x: x * 0.0254,
            ('Base', 'Inch'): lambda x: x / 0.0254,
        }
        length_tab = ConverterTab(length_units, length_conversions)
        self.tab_widget.addTab(length_tab, 'Length')

        # Temperature tab
        temperature_units = ['Celsius', 'Kelvin', 'Fahrenheit']
        temperature_conversions = {
            ('Celsius', 'Base'): lambda x: x + 273.15,
            ('Base', 'Celsius'): lambda x: x - 273.15,
            ('Kelvin', 'Base'): lambda x: x,
            ('Base', 'Kelvin'): lambda x: x,
            ('Fahrenheit', 'Base'): lambda x: (x + 459.67) * 5/9,
            ('Base', 'Fahrenheit'): lambda x: x * 9/5 - 459.67,
        }
        temperature_tab = ConverterTab(temperature_units, temperature_conversions)
        self.tab_widget.addTab(temperature_tab, 'Temperature')

        # Area tab
        area_units = ['Square Kilometer', 'Square Mile', 'Hectare', 'Acre']
        area_conversions = {
            ('Square Kilometer', 'Base'): lambda x: x * pow(10, 6),
            ('Base', 'Square Kilometer'): lambda x: x / pow(10, 6),
            ('Square Mile', 'Base'): lambda x: x * 2.59 * pow(10, 6),
            ('Base', 'Square Mile'): lambda x: x / (2.59 * pow(10, 6)),
            ('Hectare', 'Base'): lambda x: x * 10000,
            ('Base', 'Hectare'): lambda x: x / 10000,
            ('Acre', 'Base'): lambda x: x * 4046.86,
            ('Base', 'Acre'): lambda x: x / 4046.86,
        }
        area_tab = ConverterTab(area_units, area_conversions)
        self.tab_widget.addTab(area_tab, 'Area')

        # Weight tab
        weight_units = ['Gram', 'Kilogram', 'Pound', 'Ounce']
        weight_conversions = {
            ('Gram', 'Base'): lambda x: x,
            ('Base', 'Gram'): lambda x: x,
            ('Kilogram', 'Base'): lambda x: x * 1000,
            ('Base', 'Kilogram'): lambda x: x / 1000,
            ('Pound', 'Base'): lambda x: x * 453.592,
            ('Base', 'Pound'): lambda x: x / 453.592,
            ('Ounce', 'Base'): lambda x: x * 28.3495,
            ('Base', 'Ounce'): lambda x: x / 28.3495,
        }
        weight_tab = ConverterTab(weight_units, weight_conversions)
        self.tab_widget.addTab(weight_tab, 'Weight')

        # Time tab
        time_units = ['Second', 'Minute', 'Hour', 'Day', 'Week', 'Month', 'Year']
        time_conversions = {
            ('Second', 'Base'): lambda x: x,
            ('Base', 'Second'): lambda x: x,
            ('Minute', 'Base'): lambda x: x * 60,
            ('Base', 'Minute'): lambda x: x / 60,
            ('Hour', 'Base'): lambda x: x * 3600,
            ('Base', 'Hour'): lambda x: x / 3600,
            ('Day', 'Base'): lambda x: x * 86400,
            ('Base', 'Day'): lambda x: x / 86400,
            ('Week', 'Base'): lambda x: x * 604800,
            ('Base', 'Week'): lambda x: x / 604800,
            ('Month', 'Base'): lambda x: x * 2629746, # using average length of a month in seconds
            ('Base', 'Month'): lambda x: x / 2629746,
            ('Year', 'Base'): lambda x: x * 31556952, # using average length of a year in seconds
            ('Base', 'Year'): lambda x: x / 31556952,
        }
        time_tab = ConverterTab(time_units, time_conversions)
        self.tab_widget.addTab(time_tab, 'Time')

def main():
    app = QApplication(sys.argv)

    window = ConverterApp()
    window.setWindowTitle('Unit Converter')
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
